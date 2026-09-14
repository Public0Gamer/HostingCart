"""
Database models and helpers for ApexHost Platform.
Uses SQLite for zero-configuration, reliable out-of-the-box performance.
"""
import sqlite3
import os
import json
import secrets
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = os.path.join(os.path.dirname(__file__), 'apexhost.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # 1. Users table (Clients and Admins)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'client', -- 'client' or 'admin'
        phone TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # 2. Hosting Plans table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS plans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        slug TEXT UNIQUE NOT NULL,
        tagline TEXT,
        price_monthly INTEGER NOT NULL,
        price_yearly INTEGER NOT NULL,
        price_48m INTEGER NOT NULL,
        discount_percent INTEGER DEFAULT 0,
        storage_gb INTEGER NOT NULL,
        bandwidth_gb INTEGER NOT NULL,
        websites_limit INTEGER NOT NULL,
        free_domain INTEGER DEFAULT 0,
        free_ssl INTEGER DEFAULT 1,
        daily_backups INTEGER DEFAULT 0,
        litespeed INTEGER DEFAULT 1,
        featured INTEGER DEFAULT 0
    )
    ''')

    # 3. Coupons table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS coupons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE NOT NULL,
        discount_type TEXT DEFAULT 'percent', -- 'percent' or 'fixed'
        discount_value REAL NOT NULL,
        discount_percent INTEGER DEFAULT 0,
        active INTEGER DEFAULT 1,
        is_featured INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # 4. Orders / Invoices table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_number TEXT UNIQUE NOT NULL,
        user_id INTEGER NOT NULL,
        plan_id INTEGER NOT NULL,
        domain_name TEXT NOT NULL,
        domain_type TEXT NOT NULL, -- 'new' or 'existing'
        billing_cycle TEXT NOT NULL, -- 'monthly', 'yearly', '48m'
        subtotal REAL NOT NULL,
        discount_amount REAL DEFAULT 0,
        regulatory_fee REAL DEFAULT 0,
        tax_amount REAL DEFAULT 0,
        total_amount REAL NOT NULL,
        wholesale_cost REAL DEFAULT 0,
        profit_amount REAL DEFAULT 0,
        payment_method TEXT DEFAULT 'UPI_QR', -- 'UPI_QR', 'RAZORPAY', 'TEST'
        payment_status TEXT DEFAULT 'pending', -- 'pending', 'paid', 'failed'
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        paid_at TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(plan_id) REFERENCES plans(id)
    )
    ''')

    # 5. Hosting Accounts table (Provisioned services)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS hosting_accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        order_id INTEGER NOT NULL,
        plan_id INTEGER NOT NULL,
        domain_name TEXT NOT NULL,
        server_ip TEXT DEFAULT '152.58.156.166',
        nameserver1 TEXT DEFAULT 'ns1.hostingcart.in',
        nameserver2 TEXT DEFAULT 'ns2.hostingcart.in',
        cpanel_username TEXT UNIQUE NOT NULL,
        cpanel_password TEXT NOT NULL,
        status TEXT DEFAULT 'active', -- 'active', 'suspended', 'terminated'
        ssl_active INTEGER DEFAULT 1,
        wordpress_installed INTEGER DEFAULT 0,
        wordpress_version TEXT DEFAULT '6.6.1',
        disk_used_mb INTEGER DEFAULT 120,
        disk_total_mb INTEGER NOT NULL,
        bandwidth_used_gb REAL DEFAULT 1.2,
        bandwidth_total_gb INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expires_at TIMESTAMP NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(order_id) REFERENCES orders(id),
        FOREIGN KEY(plan_id) REFERENCES plans(id)
    )
    ''')

    # 6. DNS Records table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dns_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_id INTEGER NOT NULL,
        record_type TEXT NOT NULL, -- 'A', 'CNAME', 'MX', 'TXT'
        name TEXT NOT NULL,
        value TEXT NOT NULL,
        ttl INTEGER DEFAULT 14400,
        FOREIGN KEY(account_id) REFERENCES hosting_accounts(id)
    )
    ''')

    # 7. Backups table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS backups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_id INTEGER NOT NULL,
        filename TEXT NOT NULL,
        size_mb REAL NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(account_id) REFERENCES hosting_accounts(id)
    )
    ''')

    # 8. Support Tickets table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_number TEXT UNIQUE NOT NULL,
        user_id INTEGER NOT NULL,
        subject TEXT NOT NULL,
        category TEXT DEFAULT 'Technical', -- 'Technical', 'Billing', 'Domain'
        priority TEXT DEFAULT 'Medium', -- 'Low', 'Medium', 'High'
        status TEXT DEFAULT 'Open', -- 'Open', 'In Progress', 'Answered', 'Closed'
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    ''')

    # 9. Support Ticket Replies
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ticket_replies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id INTEGER NOT NULL,
        sender_id INTEGER NOT NULL,
        sender_role TEXT NOT NULL, -- 'client' or 'admin'
        message TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(ticket_id) REFERENCES tickets(id)
    )
    ''')

    # 10. System & Server Settings
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS server_settings (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
    )
    ''')

    # 11. Customer Reviews table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT,
        role_or_city TEXT NOT NULL,
        rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
        comment TEXT NOT NULL,
        is_verified INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # 12. Activity & Audit Logs (Real-time tracking of events)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS activity_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type TEXT NOT NULL,
        description TEXT NOT NULL,
        user_info TEXT,
        ip_address TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # 13. Real-Time Visitor Traffic Analytics
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS visitor_traffic (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip_address TEXT NOT NULL,
        path TEXT NOT NULL,
        method TEXT DEFAULT 'GET',
        device_type TEXT DEFAULT 'Desktop',
        user_agent TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # 14. Customer Files (Cloud Web File Manager)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customer_files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_id INTEGER,
        domain_name TEXT NOT NULL,
        filename TEXT NOT NULL,
        file_path TEXT NOT NULL,
        content TEXT,
        size_bytes INTEGER DEFAULT 0,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(account_id) REFERENCES hosting_accounts(id)
    )
    ''')

    # 15. Customer WordPress Sites
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS wp_sites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        domain_name TEXT UNIQUE NOT NULL,
        site_title TEXT NOT NULL,
        tagline TEXT,
        template_type TEXT DEFAULT 'business',
        phone TEXT DEFAULT '+91 9555838550',
        email TEXT DEFAULT 'contact@hostingcart.in',
        address TEXT DEFAULT 'Kanpur, India',
        primary_color TEXT DEFAULT '#4f46e5',
        hero_headline TEXT,
        hero_subheadline TEXT,
        about_text TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # 16. Customer WordPress Posts
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS wp_posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        domain_name TEXT NOT NULL,
        title TEXT NOT NULL,
        slug TEXT NOT NULL,
        content TEXT NOT NULL,
        category TEXT DEFAULT 'General',
        author TEXT DEFAULT 'Admin',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()

    # Seed initial data if plans table is empty
    cursor.execute('SELECT COUNT(*) FROM plans')
    if cursor.fetchone()[0] == 0:
        seed_starter_data(cursor)
        conn.commit()

    conn.close()

def seed_starter_data(cursor):
    # Seed default hosting plans
    plans = [
        (
            'Single Starter', 'single', 'Perfect for personal portfolios, resumes, and simple blogs.',
            199, 1188, 3312, 72,
            10, 100, 1, 0, 1, 0, 1, 0
        ),
        (
            'Plus Growth', 'premium', 'Best value for growing creators, startups & small businesses. Includes Free Domain.',
            349, 2148, 6672, 72,
            25, 500, 3, 1, 1, 0, 1, 0
        ),
        (
            'Business Pro', 'unlimited', 'All-inclusive cloud package for e-commerce, high traffic & agencies. Free Domain + Daily Backups.',
            599, 3348, 10992, 71,
            50, 1500, 9999, 1, 1, 1, 1, 1
        ),
        (
            'Enterprise Cloud', 'cloud-startup', 'Dedicated isolated vCPU & NVMe power for mission-critical portals & stores.',
            999, 7188, 21552, 70,
            100, 5000, 9999, 1, 1, 1, 1, 0
        )
    ]
    cursor.executemany('''
    INSERT INTO plans (
        name, slug, tagline,
        price_monthly, price_yearly, price_48m, discount_percent,
        storage_gb, bandwidth_gb, websites_limit, free_domain, free_ssl, daily_backups, litespeed, featured
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', plans)

    # Seed demo coupons
    coupons = [
        ('LAUNCH50', 50),
        ('SAVE20', 20),
        ('HOSTINGERKILLER', 30)
    ]
    cursor.executemany('INSERT INTO coupons (code, discount_percent) VALUES (?, ?)', coupons)

    # Seed Official Master Admin user: voltaramedia@gmail.com / voltara@123
    admin_pw = generate_password_hash('voltara@123')
    cursor.execute('''
    INSERT OR IGNORE INTO users (name, email, password_hash, role, phone)
    VALUES (?, ?, ?, ?, ?)
    ''', ('HostingCart Admin', 'voltaramedia@gmail.com', admin_pw, 'admin', '+91 9555838550'))

    # Seed settings
    default_settings = [
        ('adapter_type', 'mock'), # 'mock', 'hestiacp', 'cyberpanel'
        ('hestia_host', 'https://your-oracle-vps:8083'),
        ('hestia_user', 'admin'),
        ('hestia_password', 'secret_api_key'),
        ('cyberpanel_host', 'https://your-oracle-vps:8090'),
        ('cyberpanel_admin_user', 'admin'),
        ('cyberpanel_admin_password', 'secret_api_key'),
        ('brand_name', 'HostingCart'),
        ('company_city', 'Kanpur Nagar, Uttar Pradesh'),
        ('support_email', 'voltaramedia@gmail.com'),
        ('whatsapp_number', '+91 9555838550'),
        ('default_nameserver1', 'ns1.hostingcart.in'),
        ('default_nameserver2', 'ns2.hostingcart.in'),
        ('server_public_ip', '152.58.156.166'),
        ('razorpay_key_id', 'rzp_test_HostingCart'),
        ('razorpay_key_secret', 'test_secret_hw_key'),
        ('upi_id', 'pawan8550@naviaxis')
    ]
    cursor.executemany('INSERT OR IGNORE INTO server_settings (key, value) VALUES (?, ?)', default_settings)

def log_activity(event_type, description, user_info=None, ip_address=None):
    """Safely log any platform event into activity_logs table for real-time tracking."""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO activity_logs (event_type, description, user_info, ip_address)
        VALUES (?, ?, ?, ?)
        ''', (event_type, description, user_info or '', ip_address or '127.0.0.1'))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Failed to log activity: {e}")

def seed_customer_default_files(cursor, account_id, domain_name):
    """Seed initial public_html files (index.html, style.css, app.js, robots.txt) for a hosting account."""
    clean_dom = domain_name.strip().lower()
    cursor.execute("SELECT COUNT(*) FROM customer_files WHERE LOWER(domain_name) = ?", (clean_dom,))
    if cursor.fetchone()[0] > 0:
        return

    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to {clean_dom}</title>
    <link rel="stylesheet" href="/site/{clean_dom}/style.css">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Plus Jakarta Sans', sans-serif; background: #0b0f19; color: #f8fafc; min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; }}
        .card {{ background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 24px; padding: 48px; max-width: 680px; width: 100%; text-align: center; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5); }}
        .badge {{ display: inline-block; padding: 6px 16px; border-radius: 9999px; background: rgba(16, 185, 129, 0.15); color: #34d399; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 24px; border: 1px solid rgba(16, 185, 129, 0.3); }}
        h1 {{ font-size: 32px; font-weight: 800; line-height: 1.2; margin-bottom: 16px; background: linear-gradient(135deg, #fff 0%, #94a3b8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        p {{ color: #94a3b8; font-size: 15px; line-height: 1.6; margin-bottom: 32px; }}
        .btn-group {{ display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; }}
        .btn {{ padding: 12px 24px; border-radius: 12px; font-size: 13px; font-weight: 700; text-decoration: none; transition: all 0.2s; }}
        .btn-primary {{ background: #4f46e5; color: white; }}
        .btn-primary:hover {{ background: #4338ca; transform: translateY(-1px); }}
        .btn-secondary {{ background: #1e293b; color: #cbd5e1; border: 1px solid rgba(255, 255, 255, 0.1); }}
        .btn-secondary:hover {{ background: #334155; }}
        .footer-text {{ margin-top: 32px; font-size: 12px; color: #64748b; }}
    </style>
</head>
<body>
    <div class="card">
        <span class="badge">&#9679; Website Live &amp; Operational</span>
        <h1>Welcome to {clean_dom}</h1>
        <p>Your cloud hosting account is active on HostingCart. You can now replace this page by uploading your files via the hPanel File Manager or building your site with WordPress.</p>
        <div class="btn-group">
            <a href="/hpanel" class="btn btn-primary">Open hPanel File Manager</a>
            <a href="/site/{clean_dom}/wp-admin" class="btn btn-secondary">Open WordPress Studio</a>
        </div>
        <p class="footer-text">Powered by HostingCart LiteSpeed Cloud Infrastructure</p>
    </div>
    <script src="/site/{clean_dom}/app.js"></script>
</body>
</html>"""

    style_css = f"""/* Custom Stylesheet for {clean_dom} */
body {{
    -webkit-font-smoothing: antialiased;
}}
"""

    app_js = f"""// Custom JavaScript for {clean_dom}
console.log('HostingCart Website Node: Loaded successfully for {clean_dom}');
"""

    robots_txt = """User-agent: *
Allow: /
"""

    files = [
        (account_id, clean_dom, 'index.html', 'public_html/index.html', index_html, len(index_html.encode('utf-8'))),
        (account_id, clean_dom, 'style.css', 'public_html/style.css', style_css, len(style_css.encode('utf-8'))),
        (account_id, clean_dom, 'app.js', 'public_html/app.js', app_js, len(app_js.encode('utf-8'))),
        (account_id, clean_dom, 'robots.txt', 'public_html/robots.txt', robots_txt, len(robots_txt.encode('utf-8'))),
    ]

    cursor.executemany('''
    INSERT INTO customer_files (account_id, domain_name, filename, file_path, content, size_bytes)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', files)

if __name__ == '__main__':
    init_db()
    print("HostingCart Database successfully initialized and seeded.")
