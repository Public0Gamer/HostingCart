import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import threading
import sqlite3
import os
from models import get_db, log_activity

def get_smtp_settings():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT key, value FROM server_settings WHERE key LIKE 'smtp_%' OR key IN ('brand_name', 'support_email')")
    settings = dict(cursor.fetchall())
    conn.close()
    return {
        "host": settings.get("smtp_host", "").strip(),
        "port": int(settings.get("smtp_port", 587) or 587),
        "user": settings.get("smtp_user", "").strip(),
        "password": settings.get("smtp_password", "").strip(),
        "from_email": settings.get("smtp_from_email", settings.get("smtp_user", "")).strip(),
        "brand_name": settings.get("brand_name", "HostingCart"),
        "support_email": settings.get("support_email", "voltaramedia@gmail.com")
    }

def send_test_email(to_email):
    """Sends a verification email to test SMTP settings"""
    cfg = get_smtp_settings()
    if not cfg["host"] or not cfg["user"] or not cfg["password"]:
        return {
            "success": False,
            "message": "SMTP Host, Username, aur Password enter karein."
        }
    
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"✔ {cfg['brand_name']} SMTP Test Successful"
        msg["From"] = f"{cfg['brand_name']} <{cfg['from_email']}>"
        msg["To"] = to_email

        html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background: #f8fafc; border-radius: 16px;">
            <div style="background: white; padding: 30px; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
                <h2 style="color: #4f46e5; margin-top: 0;">{cfg['brand_name']} SMTP Active</h2>
                <p style="color: #334155; font-size: 14px;">Aapka automated email notification system 100% verified aur operational hai.</p>
                <div style="background: #ecfdf5; border: 1px solid #a7f3d0; border-radius: 8px; padding: 12px; margin: 20px 0; color: #065f46; font-size: 13px;">
                    <strong>Status:</strong> Connected to {cfg['host']}:{cfg['port']} as {cfg['user']}.
                </div>
                <p style="color: #64748b; font-size: 12px; margin-bottom: 0;">Sent via HostingCart High-Security Automated Mailer.</p>
            </div>
        </div>
        """
        msg.attach(MIMEText(html, "html"))

        if cfg["port"] == 465:
            server = smtplib.SMTP_SSL(cfg["host"], cfg["port"], timeout=12)
        else:
            server = smtplib.SMTP(cfg["host"], cfg["port"], timeout=12)
            server.starttls()

        server.login(cfg["user"], cfg["password"])
        server.sendmail(cfg["from_email"], [to_email], msg.as_string())
        server.quit()
        return {"success": True, "message": f"Test email sent successfully to {to_email}!"}
    except Exception as e:
        return {"success": False, "message": f"SMTP Connection Failed: {str(e)}"}

def _dispatch_order_email_worker(order_id, base_url):
    """Internal thread worker to send order fulfillment email"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT o.*, u.name as customer_name, u.email as customer_email,
               h.username as h_user, h.password_hash as h_pass, h.server_ip as h_ip,
               p.name as plan_name
        FROM orders o
        JOIN users u ON o.user_id = u.id
        LEFT JOIN hosting_accounts h ON o.id = h.order_id
        LEFT JOIN plans p ON o.plan_id = p.id
        WHERE o.id = ?
        """, (order_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return

        cfg = get_smtp_settings()
        customer_email = row["customer_email"]
        customer_name = row["customer_name"]
        order_number = row["order_number"]
        domain_name = row["domain_name"]
        total_amount = row["total_amount"]
        plan_name = row["plan_name"] or "Custom Cloud Hosting"
        server_ip = row["h_ip"] or "152.58.156.166"
        cpanel_user = row["h_user"] or "client"
        cpanel_pass = "Same as your client login password"

        invoice_url = f"{base_url}/invoice/{order_id}"
        login_url = f"{base_url}/login"
        hpanel_url = f"{base_url}/hpanel"

        log_activity('EMAIL_DISPATCH', f"Preparing order welcome email for #{order_number} to {customer_email}")

        if not cfg["host"] or not cfg["user"] or not cfg["password"]:
            log_activity('EMAIL_NOTICE', f"SMTP not configured in Admin Settings. Email link generated: {invoice_url}")
            return

        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"🎉 Order Confirmed! Your {cfg['brand_name']} Services & Login Details (#{order_number})"
        msg["From"] = f"{cfg['brand_name']} <{cfg['from_email']}>"
        msg["To"] = customer_email

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f1f5f9; margin: 0; padding: 20px; }}
                .card {{ max-width: 620px; margin: 0 auto; background: #ffffff; border-radius: 20px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.06); }}
                .header {{ background: linear-gradient(135deg, #4f46e5 0%, #3730a3 100%); padding: 36px 30px; text-align: center; color: white; }}
                .header h1 {{ margin: 0; font-size: 26px; font-weight: 800; letter-spacing: -0.5px; }}
                .header p {{ margin: 6px 0 0 0; font-size: 14px; opacity: 0.9; }}
                .content {{ padding: 32px 30px; color: #1e293b; line-height: 1.6; font-size: 14px; }}
                .badge {{ display: inline-block; background: #dcfce7; color: #166534; padding: 4px 12px; border-radius: 9999px; font-weight: 700; font-size: 12px; }}
                .info-box {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 14px; padding: 20px; margin: 20px 0; }}
                .info-row {{ display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #e2e8f0; font-size: 13px; }}
                .info-row:last-child {{ border-bottom: none; }}
                .btn {{ display: block; text-align: center; background: #4f46e5; color: #ffffff !important; padding: 14px 24px; border-radius: 12px; text-decoration: none; font-weight: 700; font-size: 14px; margin: 24px 0 12px 0; }}
                .btn-secondary {{ display: block; text-align: center; background: #f1f5f9; color: #334155 !important; padding: 12px 24px; border-radius: 12px; text-decoration: none; font-weight: 700; font-size: 13px; }}
                .footer {{ background: #f8fafc; border-top: 1px solid #e2e8f0; padding: 24px 30px; text-align: center; font-size: 12px; color: #64748b; }}
            </style>
        </head>
        <body>
            <div class="card">
                <div class="header">
                    <h1>{cfg['brand_name']}</h1>
                    <p>Order #{order_number} Confirmed &amp; Provisioned</p>
                </div>
                <div class="content">
                    <p>Namaste <strong>{customer_name}</strong>,</p>
                    <p>Aapka order successfully confirm aur cloud servers par live provision ho chuka hai! Aapke services ki complete details neeche di gayi hain:</p>
                    
                    <div class="info-box">
                        <div class="info-row">
                            <span style="color: #64748b;">Plan:</span>
                            <strong>{plan_name}</strong>
                        </div>
                        <div class="info-row">
                            <span style="color: #64748b;">Primary Domain:</span>
                            <strong style="color: #4f46e5;">{domain_name}</strong>
                        </div>
                        <div class="info-row">
                            <span style="color: #64748b;">Total Paid:</span>
                            <strong style="color: #16a34a;">₹{total_amount} (Paid)</strong>
                        </div>
                        <div class="info-row">
                            <span style="color: #64748b;">Server Node IP:</span>
                            <strong style="font-family: monospace;">{server_ip}</strong>
                        </div>
                        <div class="info-row">
                            <span style="color: #64748b;">Nameserver 1:</span>
                            <span style="font-family: monospace;">ns1.hostingcart.in</span>
                        </div>
                        <div class="info-row">
                            <span style="color: #64748b;">Nameserver 2:</span>
                            <span style="font-family: monospace;">ns2.hostingcart.in</span>
                        </div>
                        <div class="info-row">
                            <span style="color: #64748b;">Control Panel User:</span>
                            <strong style="font-family: monospace;">{cpanel_user}</strong>
                        </div>
                    </div>

                    <a href="{invoice_url}" class="btn">📥 View &amp; Print Official Invoice</a>
                    <a href="{login_url}" class="btn-secondary">🚀 Login to hPanel Control Panel</a>

                    <div style="margin-top: 24px; padding: 14px; background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 12px; font-size: 12px; color: #166534;">
                        <strong>✔ Real ICANN Domain Registration Active:</strong> Aapka domain registrar network me active hai. Agar aapne new domain register kiya hai toh DNS propagation globally shuru ho chuki hai.
                    </div>
                </div>
                <div class="footer">
                    <p style="margin: 0;">For support, contact: <strong>{cfg['support_email']}</strong></p>
                    <p style="margin: 4px 0 0 0;">&copy; 2026 {cfg['brand_name']} Infrastructure Services. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        msg.attach(MIMEText(html, "html"))

        if cfg["port"] == 465:
            server = smtplib.SMTP_SSL(cfg["host"], cfg["port"], timeout=15)
        else:
            server = smtplib.SMTP(cfg["host"], cfg["port"], timeout=15)
            server.starttls()

        server.login(cfg["user"], cfg["password"])
        server.sendmail(cfg["from_email"], [customer_email], msg.as_string())
        server.quit()

        log_activity('EMAIL_SUCCESS', f"Welcome email with invoice link delivered to {customer_email} (#{order_number})")
    except Exception as e:
        log_activity('EMAIL_FAILED', f"Failed to send welcome email for Order #{order_id}: {str(e)}")

def send_order_welcome_email(order_id, base_url="https://hostingcart.onrender.com"):
    """
    Spawns background daemon thread so customer checkout experiences zero latency.
    """
    t = threading.Thread(target=_dispatch_order_email_worker, args=(order_id, base_url), daemon=True)
    t.start()
