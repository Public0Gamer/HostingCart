import os
import sys

def update_app_py():
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Helper function fulfill_paid_order
    fulfill_func = '''def fulfill_paid_order(order_id):
    """
    Handles domain registration and server provisioning when an order is marked paid:
    1. If domain_type != 'existing', registers domain via wholesale registrar API.
    2. If domain_type == 'existing', wholesale_cost is set to 0.0 and no registrar API call is made.
    3. Auto-provisions hosting account, creates DNS records, creates welcome backup, and installs WordPress.
    """
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT o.*, u.name as customer_name, u.email as customer_email, u.phone as customer_phone
    FROM orders o JOIN users u ON o.user_id = u.id WHERE o.id = ?
    """, (order_id,))
    ord_info = cursor.fetchone()
    if ord_info:
        if ord_info['domain_type'] != 'existing':
            customer_payload = {
                'name': ord_info['customer_name'],
                'email': ord_info['customer_email'],
                'phone': ord_info['customer_phone']
            }
            reg_res = DomainRegistrarClient.register_domain(ord_info['domain_name'], customer_payload)
            actual_wholesale = reg_res.get('wholesale_cost', ord_info['wholesale_cost'] or 649.0)
            net_profit = round(ord_info['total_amount'] - actual_wholesale, 2)
            cursor.execute("UPDATE orders SET wholesale_cost = ?, profit_amount = ? WHERE id = ?", (actual_wholesale, net_profit, order_id))
            conn.commit()
        else:
            cursor.execute("UPDATE orders SET wholesale_cost = 0.0, profit_amount = total_amount WHERE id = ?", (order_id,))
            conn.commit()
    conn.close()

    success, msg = auto_provision_order(order_id)
    conn_wp = get_db()
    c_wp = conn_wp.cursor()
    c_wp.execute("UPDATE hosting_accounts SET wordpress_installed = 1 WHERE order_id = ?", (order_id,))
    conn_wp.commit()
    conn_wp.close()
    return success, msg

'''

    # Place fulfill_paid_order before verify_utr
    target_utr = "@app.route('/api/order/verify-utr', methods=['POST'])"
    if "def fulfill_paid_order" not in content:
        if target_utr in content:
            content = content.replace(target_utr, fulfill_func + target_utr)
            print("Added fulfill_paid_order helper")
        else:
            print("ERROR: Could not find target_utr")
            return False

    # 2. Update create_order pricing and order insert
    old_create_target = """    base_bill = max(0.0, subtotal - discount_amount)
    # Regulatory & Cloud Infrastructure Surcharge: 12%
    regulatory_fee = round(base_bill * 0.12, 2)
    taxable_amount = base_bill + regulatory_fee
    tax_amount = round(taxable_amount * 0.18, 2)
    total_amount = round(taxable_amount + tax_amount, 2)

    # Wholesale registrar domain registry cost & net profit
    wholesale_cost = DomainRegistrarClient.get_wholesale_cost(domain_name)
    profit_amount = round(max(0.0, total_amount - wholesale_cost), 2)

    order_number = f"HW-{datetime.now().strftime('%Y%m%d')}-{''.join(random.choices(string.digits, k=4))}"

    cursor.execute('''
    INSERT INTO orders (
        order_number, user_id, plan_id, domain_name, domain_type,
        billing_cycle, subtotal, discount_amount, regulatory_fee,
        tax_amount, total_amount, wholesale_cost, profit_amount,
        payment_method, payment_status
    ) VALUES (?, ?, ?, ?, 'new', ?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending')
    ''', (
        order_number, user_id, plan_id, domain_name, billing_cycle,
        subtotal, discount_amount, regulatory_fee, tax_amount,
        total_amount, wholesale_cost, profit_amount, payment_method
    ))"""

    new_create_target = """    # Hostinger Free Domain Protection Rule:
    # 1. Single Starter plan NEVER has free domain (plan['free_domain'] == 0)
    # 2. Plus Growth, Business Pro, Enterprise Cloud only get free domain if billing_cycle in ['yearly', '48m']
    # 3. 1-Month plan NEVER gets free domain under any circumstances!
    is_domain_free = (int(plan['free_domain']) == 1 and billing_cycle in ['yearly', '48m'])
    domain_action = data.get('domain_action', 'register')

    domain_fee = 0.0
    domain_type = 'new'
    if domain_action == 'existing':
        domain_type = 'existing'
        domain_fee = 0.0
        wholesale_cost = 0.0
    else:
        domain_type = 'new'
        if is_domain_free:
            domain_fee = 0.0
            wholesale_cost = DomainRegistrarClient.get_wholesale_cost(domain_name) if domain_name else 0.0
        else:
            # Paid domain registration on 1-month or Single Starter plans
            domain_fee = 399.0 if (domain_name.endswith('.in') or domain_name.endswith('.co.in')) else 799.0
            wholesale_cost = DomainRegistrarClient.get_wholesale_cost(domain_name) if domain_name else 0.0

    base_bill = max(0.0, subtotal - discount_amount) + domain_fee
    # Regulatory & Cloud Infrastructure Surcharge: 12%
    regulatory_fee = round(base_bill * 0.12, 2)
    taxable_amount = base_bill + regulatory_fee
    tax_amount = round(taxable_amount * 0.18, 2)
    total_amount = round(taxable_amount + tax_amount, 2)
    profit_amount = round(max(0.0, total_amount - wholesale_cost), 2)

    order_number = f"HW-{datetime.now().strftime('%Y%m%d')}-{''.join(random.choices(string.digits, k=4))}"

    cursor.execute('''
    INSERT INTO orders (
        order_number, user_id, plan_id, domain_name, domain_type,
        billing_cycle, subtotal, discount_amount, regulatory_fee,
        tax_amount, total_amount, wholesale_cost, profit_amount,
        payment_method, payment_status
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending')
    ''', (
        order_number, user_id, plan_id, domain_name, domain_type, billing_cycle,
        subtotal, discount_amount, regulatory_fee, tax_amount,
        total_amount, wholesale_cost, profit_amount, payment_method
    ))"""

    if old_create_target in content:
        content = content.replace(old_create_target, new_create_target)
        print("Updated create_order pricing and domain protection")
    else:
        print("ERROR: old_create_target not found")
        return False

    # Also update create_order return json to include domain_fee and is_domain_free
    old_return = """"subtotal": round(subtotal, 2),
        "discount_amount": round(discount_amount, 2),"""
    new_return = """"subtotal": round(subtotal, 2),
        "domain_fee": round(domain_fee, 2),
        "is_domain_free": is_domain_free,
        "discount_amount": round(discount_amount, 2),"""
    if old_return in content:
        content = content.replace(old_return, new_return)
        print("Updated create_order return JSON")

    # 3. Simplify verify_utr with fulfill_paid_order
    old_utr_block = """    # Auto Wholesale Domain Registration
    cursor.execute('''
    SELECT o.*, u.name as customer_name, u.email as customer_email, u.phone as customer_phone
    FROM orders o JOIN users u ON o.user_id = u.id WHERE o.id = ?
    ''', (order_id,))
    ord_info = cursor.fetchone()
    if ord_info:
        customer_payload = {'name': ord_info['customer_name'], 'email': ord_info['customer_email'], 'phone': ord_info['customer_phone']}
        reg_res = DomainRegistrarClient.register_domain(ord_info['domain_name'], customer_payload)
        actual_wholesale = reg_res.get('wholesale_cost', ord_info['wholesale_cost'] or 649.0)
        net_profit = round(ord_info['total_amount'] - actual_wholesale, 2)
        cursor.execute("UPDATE orders SET wholesale_cost = ?, profit_amount = ? WHERE id = ?", (actual_wholesale, net_profit, order_id))
        conn.commit()
    conn.close()

    success, msg = auto_provision_order(order_id)
    # Enable WordPress by default
    conn_wp = get_db()
    c_wp = conn_wp.cursor()
    c_wp.execute("UPDATE hosting_accounts SET wordpress_installed = 1 WHERE order_id = ?", (order_id,))
    conn_wp.commit()
    conn_wp.close()
    log_activity('PAYMENT', f"Payment confirmed (UTR: {utr_number or 'Auto-Scan'}) for #{ord_row['order_number']} ({ord_row['domain_name']})", user_info=f"User #{ord_row['user_id']}")"""

    new_utr_block = """    conn.close()
    success, msg = fulfill_paid_order(order_id)
    log_activity('PAYMENT', f"Payment confirmed (UTR: {utr_number or 'Auto-Scan'}) for #{ord_row['order_number']} ({ord_row['domain_name']})", user_info=f"User #{ord_row['user_id']}")"""

    if old_utr_block in content:
        content = content.replace(old_utr_block, new_utr_block)
        print("Updated verify_utr to use fulfill_paid_order")

    # 4. Simplify razorpay verify
    old_rzp_block = """    # Auto Wholesale Domain Registration
    cursor.execute(\"\"\"
    SELECT o.*, u.name as customer_name, u.email as customer_email, u.phone as customer_phone
    FROM orders o JOIN users u ON o.user_id = u.id WHERE o.id = ?
    \"\"\", (order_id,))
    ord_info = cursor.fetchone()
    if ord_info:
        customer_payload = {'name': ord_info['customer_name'], 'email': ord_info['customer_email'], 'phone': ord_info['customer_phone']}
        reg_res = DomainRegistrarClient.register_domain(ord_info['domain_name'], customer_payload)
        actual_wholesale = reg_res.get('wholesale_cost', ord_info['wholesale_cost'] or 649.0)
        net_profit = round(ord_info['total_amount'] - actual_wholesale, 2)
        cursor.execute("UPDATE orders SET wholesale_cost = ?, profit_amount = ? WHERE id = ?", (actual_wholesale, net_profit, order_id))
        conn.commit()
    conn.close()

    success, msg = auto_provision_order(order_id)
    conn_wp = get_db()
    c_wp = conn_wp.cursor()
    c_wp.execute("UPDATE hosting_accounts SET wordpress_installed = 1 WHERE order_id = ?", (order_id,))
    conn_wp.commit()
    conn_wp.close()"""

    new_rzp_block = """    conn.close()
    success, msg = fulfill_paid_order(order_id)"""

    if old_rzp_block in content:
        content = content.replace(old_rzp_block, new_rzp_block)
        print("Updated razorpay verify to use fulfill_paid_order")

    # 5. Simplify cashfree verify
    old_cf_block = """    cursor.execute(\"\"\"
    SELECT o.*, u.name as customer_name, u.email as customer_email, u.phone as customer_phone
    FROM orders o JOIN users u ON o.user_id = u.id WHERE o.id = ?
    \"\"\", (order_id,))
    ord_info = cursor.fetchone()
    if ord_info:
        customer_payload = {'name': ord_info['customer_name'], 'email': ord_info['customer_email'], 'phone': ord_info['customer_phone']}
        reg_res = DomainRegistrarClient.register_domain(ord_info['domain_name'], customer_payload)
        actual_wholesale = reg_res.get('wholesale_cost', ord_info['wholesale_cost'] or 649.0)
        net_profit = round(ord_info['total_amount'] - actual_wholesale, 2)
        cursor.execute("UPDATE orders SET wholesale_cost = ?, profit_amount = ? WHERE id = ?", (actual_wholesale, net_profit, order_id))
        conn.commit()
    conn.close()

    success, msg = auto_provision_order(order_id)
    conn_wp = get_db()
    c_wp = conn_wp.cursor()
    c_wp.execute("UPDATE hosting_accounts SET wordpress_installed = 1 WHERE order_id = ?", (order_id,))
    conn_wp.commit()
    conn_wp.close()"""

    new_cf_block = """    conn.close()
    success, msg = fulfill_paid_order(order_id)"""

    if old_cf_block in content:
        content = content.replace(old_cf_block, new_cf_block)
        print("Updated cashfree verify to use fulfill_paid_order")

    # 6. Simplify process_payment (/api/order/pay)
    old_pay_block = """    # Auto Wholesale Domain Registration
    cursor.execute('''
    SELECT o.*, u.name as customer_name, u.email as customer_email, u.phone as customer_phone
    FROM orders o JOIN users u ON o.user_id = u.id WHERE o.id = ?
    ''', (order_id,))
    ord_info = cursor.fetchone()
    if ord_info:
        customer_payload = {'name': ord_info['customer_name'], 'email': ord_info['customer_email'], 'phone': ord_info['customer_phone']}
        reg_res = DomainRegistrarClient.register_domain(ord_info['domain_name'], customer_payload)
        actual_wholesale = reg_res.get('wholesale_cost', ord_info['wholesale_cost'] or 649.0)
        net_profit = round(ord_info['total_amount'] - actual_wholesale, 2)
        cursor.execute("UPDATE orders SET wholesale_cost = ?, profit_amount = ? WHERE id = ?", (actual_wholesale, net_profit, order_id))
        conn.commit()
    conn.close()

    # Trigger Automated Server Provisioning
    success, msg = auto_provision_order(order_id)
    # Enable WordPress by default
    conn_wp = get_db()
    c_wp = conn_wp.cursor()
    c_wp.execute("UPDATE hosting_accounts SET wordpress_installed = 1 WHERE order_id = ?", (order_id,))
    conn_wp.commit()
    conn_wp.close()"""

    new_pay_block = """    conn.close()
    # Trigger Automated Fulfillment & Domain Handling
    success, msg = fulfill_paid_order(order_id)"""

    if old_pay_block in content:
        content = content.replace(old_pay_block, new_pay_block)
        print("Updated process_payment to use fulfill_paid_order")

    # 7. Simplify admin verify
    old_admin_block = """    if not acc:
        # Auto Wholesale Domain Registration
        conn_r = get_db()
        c_r = conn_r.cursor()
        c_r.execute('''
        SELECT o.*, u.name as customer_name, u.email as customer_email, u.phone as customer_phone
        FROM orders o JOIN users u ON o.user_id = u.id WHERE o.id = ?
        ''', (order_id,))
        ord_info = c_r.fetchone()
        if ord_info:
            customer_payload = {'name': ord_info['customer_name'], 'email': ord_info['customer_email'], 'phone': ord_info['customer_phone']}
            reg_res = DomainRegistrarClient.register_domain(ord_info['domain_name'], customer_payload)
            actual_wholesale = reg_res.get('wholesale_cost', ord_info['wholesale_cost'] or 649.0)
            net_profit = round(ord_info['total_amount'] - actual_wholesale, 2)
            c_r.execute("UPDATE orders SET wholesale_cost = ?, profit_amount = ? WHERE id = ?", (actual_wholesale, net_profit, order_id))
            conn_r.commit()
        conn_r.close()

        success, prov_msg = auto_provision_order(order_id)
        conn_wp = get_db()
        c_wp = conn_wp.cursor()
        c_wp.execute("UPDATE hosting_accounts SET wordpress_installed = 1 WHERE order_id = ?", (order_id,))
        conn_wp.commit()
        conn_wp.close()
        msg = f"Order #{order['order_number']} verified as PAID! Hosting space & domain for '{order['domain_name']}' automatically provisioned."
    else:"""

    new_admin_block = """    if not acc:
        success, prov_msg = fulfill_paid_order(order_id)
        msg = f"Order #{order['order_number']} verified as PAID! Hosting space & domain for '{order['domain_name']}' automatically provisioned."
    else:"""

    if old_admin_block in content:
        content = content.replace(old_admin_block, new_admin_block)
        print("Updated admin verify to use fulfill_paid_order")

    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("app.py updated successfully!")
    return True

if __name__ == '__main__':
    update_app_py()
