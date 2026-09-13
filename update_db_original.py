import sqlite3

print("1. Updating plans table with 100% Original HostingChahiye Brand Names...")
conn = sqlite3.connect("apexhost.db")
cursor = conn.cursor()

plans_original = [
    (1, 'Single Starter', 'single', 'Perfect for personal portfolios, resumes, and simple blogs.', 49, 588, 2352, 84, 10, 100, 1, 0, 1, 0, 1, 0),
    (2, 'Plus Growth', 'premium', 'Best value for growing creators, startups & small businesses. Includes Free Domain.', 119, 1428, 5712, 78, 20, 500, 3, 1, 1, 0, 1, 0),
    (3, 'Business Pro', 'unlimited', 'All-inclusive cloud package for e-commerce, high traffic & agencies. Free Domain + Daily Backups.', 199, 2388, 9552, 68, 50, 1500, 9999, 1, 1, 1, 1, 1),
    (4, 'Enterprise Cloud', 'cloud-startup', 'Dedicated isolated vCPU & NVMe power for mission-critical portals & stores.', 479, 5748, 22992, 68, 100, 5000, 9999, 1, 1, 1, 1, 0)
]

for p in plans_original:
    cursor.execute("""
    UPDATE plans SET
        name = ?, slug = ?, tagline = ?, price_monthly = ?, price_yearly = ?, price_48m = ?,
        discount_percent = ?, storage_gb = ?, bandwidth_gb = ?, websites_limit = ?,
        free_domain = ?, free_ssl = ?, daily_backups = ?, litespeed = ?, featured = ?
    WHERE id = ?
    """, (p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11], p[12], p[13], p[14], p[15], p[0]))

# Ensure HOSTINGCHAHIYE promo code exists
cursor.execute("INSERT OR IGNORE INTO coupons (code, discount_type, discount_value, active) VALUES ('HOSTINGCHAHIYE', 'percent', 10, 1)")
cursor.execute("INSERT OR IGNORE INTO coupons (code, discount_type, discount_value, active) VALUES ('LAUNCH50', 'percent', 50, 1)")

conn.commit()
conn.close()
print("[OK] Database updated with original HostingChahiye plans and coupons.")
