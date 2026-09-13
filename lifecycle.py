"""
Subscription Expiry, Renewal Automation & Lifecycle Manager for ApexHost.
Handles:
- Expiration checks
- Automatic service suspension after 3-day grace period
- Auto-unsuspension on renewal
- Invoice generation helper
"""
from datetime import datetime, timedelta
from models import get_db
from provisioning import get_server_adapter

def run_lifecycle_checks():
    """
    Simulates or executes daily cron check for hosting services.
    Flags impending expiries and auto-suspends overdue accounts.
    """
    conn = get_db()
    cursor = conn.cursor()
    now = datetime.now()
    grace_period_cutoff = (now - timedelta(days=3)).strftime('%Y-%m-%d %H:%M:%S')

    # 1. Accounts that need suspension (expired > 3 days ago and still active)
    cursor.execute('''
    SELECT id, domain_name, cpanel_username 
    FROM hosting_accounts 
    WHERE expires_at < ? AND status = 'active'
    ''', (grace_period_cutoff,))
    overdue_accounts = cursor.fetchall()

    adapter = get_server_adapter()
    suspended_count = 0
    for acc in overdue_accounts:
        # Call server adapter to suspend
        adapter.suspend_account(acc['cpanel_username'])
        cursor.execute("UPDATE hosting_accounts SET status = 'suspended' WHERE id = ?", (acc['id'],))
        suspended_count += 1

    # 2. Count accounts expiring in next 7 days for alerts
    seven_days = (now + timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
    SELECT COUNT(*) FROM hosting_accounts 
    WHERE expires_at BETWEEN ? AND ? AND status = 'active'
    ''', (now.strftime('%Y-%m-%d %H:%M:%S'), seven_days))
    expiring_soon = cursor.fetchone()[0]

    conn.commit()
    conn.close()

    return {
        "suspended_count": suspended_count,
        "expiring_soon_count": expiring_soon,
        "checked_at": now.strftime('%Y-%m-%d %H:%M:%S')
    }

def reactivate_account(account_id, additional_days=365):
    """
    Called when a renewal payment is completed.
    Extends expiration date and unsuspends service on server.
    """
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM hosting_accounts WHERE id = ?", (account_id,))
    acc = cursor.fetchone()
    if not acc:
        conn.close()
        return False, "Account not found"

    # Compute new expiry
    current_expiry = datetime.strptime(acc['expires_at'], '%Y-%m-%d %H:%M:%S')
    base_time = max(datetime.now(), current_expiry)
    new_expiry = base_time + timedelta(days=additional_days)

    adapter = get_server_adapter()
    adapter.unsuspend_account(acc['cpanel_username'])

    cursor.execute('''
    UPDATE hosting_accounts 
    SET status = 'active', expires_at = ? 
    WHERE id = ?
    ''', (new_expiry.strftime('%Y-%m-%d %H:%M:%S'), account_id))

    conn.commit()
    conn.close()
    return True, f"Service renewed until {new_expiry.strftime('%d %b %Y')}"
