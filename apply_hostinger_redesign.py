import sqlite3
import os
import re

print("Starting Hostinger Redesign & Pricing Synchronization...")

db_path = r"C:\Users\at781\.gemini\antigravity\scratch\apexhost-platform\apexhost.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. Update Plans Table
# Check if plans exist, update them with new Hostinger-style cheaper pricing
cursor.execute("SELECT COUNT(*) FROM plans")
count = cursor.fetchone()[0]

plans_data = [
    (1, 'Single', 'single', 'Get your first website online. Best for beginners or simple projects.', 49, 588, 2352, 84, 10, 100, 1, 0, 1, 0, 1, 0),
    (2, 'Premium Web Hosting', 'premium', 'Run websites smoothly. Great for creators and small brands.', 119, 1428, 5712, 78, 20, 500, 3, 1, 1, 0, 1, 0),
    (3, 'Unlimited', 'unlimited', 'Unlimited websites and mailboxes, plus AI tools and priority support for maximum flexibility.', 199, 2388, 9552, 68, 50, 1500, 9999, 1, 1, 1, 1, 1),
    (4, 'Cloud Startup', 'cloud-startup', 'Dedicated power for agencies or high-traffic projects.', 479, 5748, 22992, 68, 100, 5000, 9999, 1, 1, 1, 1, 0)
]

for p in plans_data:
    cursor.execute("""
    INSERT INTO plans (id, name, slug, tagline, price_monthly, price_yearly, price_48m, discount_percent, storage_gb, bandwidth_gb, websites_limit, free_domain, free_ssl, daily_backups, litespeed, featured)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(id) DO UPDATE SET
        name=excluded.name,
        slug=excluded.slug,
        tagline=excluded.tagline,
        price_monthly=excluded.price_monthly,
        price_yearly=excluded.price_yearly,
        price_48m=excluded.price_48m,
        discount_percent=excluded.discount_percent,
        storage_gb=excluded.storage_gb,
        bandwidth_gb=excluded.bandwidth_gb,
        websites_limit=excluded.websites_limit,
        free_domain=excluded.free_domain,
        free_ssl=excluded.free_ssl,
        daily_backups=excluded.daily_backups,
        litespeed=excluded.litespeed,
        featured=excluded.featured
    """, p)

# Also ensure CYBERNEWS and HOSTINGPRO coupon codes exist in coupons table
cursor.execute("INSERT OR IGNORE INTO coupons (code, discount_type, discount_value, active) VALUES ('CYBERNEWS', 'percent', 10, 1)")
cursor.execute("INSERT OR IGNORE INTO coupons (code, discount_type, discount_value, active) VALUES ('HOSTINGPRO', 'percent', 10, 1)")

conn.commit()
conn.close()
print("[OK] SQLite plans updated with Hostinger 4-tier cheaper pricing.")
