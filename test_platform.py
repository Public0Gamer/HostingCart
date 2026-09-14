"""
End-to-End Automated Verification Test Suite for HostingCart Platform.
Tests all APIs, billing calculation, domain search, and server auto-provisioning.
"""
import unittest
import json
from app import app
from models import init_db, get_db

class TestHostingCartPlatform(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test_secret_hw_key'
        self.client = app.test_client()
        init_db()

    @classmethod
    def tearDownClass(cls):
        """Clean up any test records created during automated test suite execution"""
        conn = get_db()
        cursor = conn.cursor()
        test_domains = ('testbrandindia.in', 'kanpurnewtech.in', 'liveverifytest.in', 'statuspolltest.in', 'hostingcart98765test.in', 'sandboxtestbrand.com', 'rzpteststore.in', 'cfteststore.in', 'mytestbrand1month.in', 'alreadyregistered.com', 'myfreedomain12m.in', 'starterdomain.com')
        test_emails = ('buyer@testbrand.com', 'rohit@kanpurnewtech.in', 'verifytest@brand.in', 'polluser@domain.in', 'sandboxbuyer@brand.com', 'rzpbuyer@teststore.in', 'cfbuyer@teststore.in', 'buyer1m@test.com')
        placeholders_d = ', '.join(['?'] * len(test_domains))
        placeholders_e = ', '.join(['?'] * len(test_emails))
        cursor.execute(f"DELETE FROM dns_records WHERE account_id IN (SELECT id FROM hosting_accounts WHERE domain_name IN ({placeholders_d}))", test_domains)
        cursor.execute(f"DELETE FROM backups WHERE account_id IN (SELECT id FROM hosting_accounts WHERE domain_name IN ({placeholders_d}))", test_domains)
        cursor.execute(f"DELETE FROM hosting_accounts WHERE domain_name IN ({placeholders_d})", test_domains)
        cursor.execute(f"DELETE FROM customer_files WHERE domain_name IN ({placeholders_d}) OR domain_name LIKE 'test%'", test_domains)
        cursor.execute(f"DELETE FROM wp_sites WHERE domain_name IN ({placeholders_d}) OR domain_name LIKE 'test%'", test_domains)
        cursor.execute(f"DELETE FROM wp_posts WHERE domain_name IN ({placeholders_d}) OR domain_name LIKE 'test%'", test_domains)
        cursor.execute(f"DELETE FROM orders WHERE domain_name IN ({placeholders_d})", test_domains)
        cursor.execute(f"DELETE FROM users WHERE email IN ({placeholders_e})", test_emails)
        cursor.execute("DELETE FROM reviews WHERE email = 'pooja@kanpursilk.com'")
        cursor.execute("DELETE FROM orders WHERE payment_status = 'pending'")
        conn.commit()
        conn.close()

    def test_01_public_storefront(self):
        """Test storefront landing, domains, and vps routes"""
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'HostingCart', res.data)
        self.assertIn(b'Plus Growth', res.data)

        res_domains = self.client.get('/domains')
        self.assertEqual(res_domains.status_code, 200)

        res_vps = self.client.get('/vps')
        self.assertEqual(res_vps.status_code, 200)

    def test_02_domain_search_api(self):
        """Test live real-world domain availability search API"""
        # 1. Registered domain (google.com) must be reported as TAKEN (available: False)
        res_taken = self.client.get('/api/domain-search?domain=google.com')
        self.assertEqual(res_taken.status_code, 200)
        data_taken = res_taken.get_json()
        self.assertTrue(data_taken['success'])
        self.assertFalse(data_taken['primary']['available'])

        # 2. Random nonexistent domain must be reported as AVAILABLE (available: True)
        res_avail = self.client.get('/api/domain-search?domain=hostingcart98765test.in')
        self.assertEqual(res_avail.status_code, 200)
        data_avail = res_avail.get_json()
        self.assertTrue(data_avail['success'])
        self.assertTrue(data_avail['primary']['available'])

    def test_03_coupon_engine(self):
        """Test coupon discount calculations"""
        res = self.client.post('/api/coupon/apply', json={'code': 'LAUNCH50'})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertGreater(data['discount_value'], 0)

    def test_04_order_creation_and_auto_provisioning(self):
        """Test end-to-end checkout and automated hosting account creation"""
        # 1. Create order
        order_payload = {
            'plan_id': 2, # Premium Web Hosting
            'domain_name': 'testbrandindia.in',
            'billing_cycle': 'yearly',
            'coupon_code': 'LAUNCH50',
            'payment_method': 'UPI_QR',
            'name': 'Test Buyer',
            'email': 'buyer@testbrand.com',
            'phone': '+91 9998887776',
            'password': 'BuyerPass@123'
        }
        res_order = self.client.post('/api/order/create', json=order_payload)
        self.assertEqual(res_order.status_code, 200)
        order_data = res_order.get_json()
        self.assertTrue(order_data['success'])
        order_id = order_data['order_id']
        self.assertGreater(order_id, 0)
        self.assertIn('HW-', order_data['order_number'])

        # 2. Simulate payment & auto-provisioning
        res_pay = self.client.post('/api/order/pay', json={'order_id': order_id})
        self.assertEqual(res_pay.status_code, 200)
        pay_data = res_pay.get_json()
        self.assertTrue(pay_data['success'])
        self.assertIn('provisioned', pay_data['provisioning'].lower())

        # 3. Verify SQLite records created
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM hosting_accounts WHERE order_id = ?", (order_id,))
        acc = cursor.fetchone()
        self.assertIsNotNone(acc)
        self.assertEqual(acc['domain_name'], 'testbrandindia.in')
        self.assertEqual(acc['status'], 'active')
        self.assertEqual(acc['ssl_active'], 1)

        # 4. Verify DNS records generated
        cursor.execute("SELECT COUNT(*) FROM dns_records WHERE account_id = ?", (acc['id'],))
        dns_count = cursor.fetchone()[0]
        self.assertGreaterEqual(dns_count, 4)

        # 5. Verify Backup created
        cursor.execute("SELECT COUNT(*) FROM backups WHERE account_id = ?", (acc['id'],))
        backup_count = cursor.fetchone()[0]
        self.assertGreaterEqual(backup_count, 1)

        conn.close()

    def test_05_customer_review_submission(self):
        """Test customer review submission API"""
        payload = {
            'name': 'Pooja Verma',
            'role_or_city': 'Founder, Kanpur Silk Store',
            'email': 'pooja@kanpursilk.com',
            'rating': 5,
            'comment': 'Amazing hosting speed and smooth UPI checkout.'
        }
        res = self.client.post('/api/reviews/submit', json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertIn('review', data)
        self.assertEqual(data['review']['name'], 'Pooja Verma')

    def test_06_admin_free_account_provision(self):
        """Test Admin complimentary ₹0 account provisioning"""
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['role'] = 'admin'
            sess['user_email'] = 'voltaramedia@gmail.com'

        payload = {
            'name': 'Rohit Gupta',
            'email': 'rohit@kanpurnewtech.in',
            'domain': 'kanpurnewtech.in',
            'plan_id': 2,
            'duration_months': 12,
            'custom_note': 'Kanpur Offline Cash VIP'
        }
        res = self.client.post('/api/admin/accounts/create-free', json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertIn('HW-FREE-', data['order_number'])
        self.assertEqual(data['account']['domain'], 'kanpurnewtech.in')

    def test_07_system_telemetry_and_order_verification(self):
        """Test Real-time hardware telemetry and 1-click admin order verification"""
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['role'] = 'admin'
            sess['user_email'] = 'voltaramedia@gmail.com'

        # 1. Test live hardware metrics API
        res_tele = self.client.get('/api/admin/system/metrics')
        self.assertEqual(res_tele.status_code, 200)
        tele = res_tele.get_json()
        self.assertTrue(tele['success'])
        self.assertIn('cpu_percent', tele)
        self.assertIn('ram_used_gb', tele)
        self.assertIn('disk_used_gb', tele)
        self.assertGreater(tele['cpu_cores'], 0)

        # 2. Test admin order payment verification
        # Create a pending test order
        ord_payload = {
            'plan_id': 1,
            'domain_name': 'liveverifytest.in',
            'billing_cycle': 'yearly',
            'payment_method': 'UPI_QR',
            'name': 'Verify Test User',
            'email': 'verifytest@brand.in',
            'phone': '+91 9555838550',
            'password': 'TestPass@123'
        }
        res_ord = self.client.post('/api/order/create', json=ord_payload)
        order_id = res_ord.get_json()['order_id']

        # Admin verifies payment
        res_verify = self.client.post('/api/admin/order/verify-pay', json={'order_id': order_id})
        self.assertEqual(res_verify.status_code, 200)
        v_data = res_verify.get_json()
        self.assertTrue(v_data['success'])
        self.assertIn('PAID', v_data['message'])

    def test_08_order_status_polling_and_utr_verification(self):
        """Test the 5-min timer polling endpoint and fast-track UTR auto-verification"""
        ord_payload = {
            'plan_id': 1,
            'domain_name': 'statuspolltest.in',
            'billing_cycle': 'yearly',
            'payment_method': 'UPI_QR',
            'name': 'Poll User',
            'email': 'polluser@domain.in',
            'phone': '+91 9555838550',
            'password': 'TestPass@123'
        }
        res_ord = self.client.post('/api/order/create', json=ord_payload)
        order_id = res_ord.get_json()['order_id']

        # 1. Initial status poll must be pending
        res_poll1 = self.client.get(f'/api/order/status/{order_id}')
        self.assertEqual(res_poll1.status_code, 200)
        poll_data1 = res_poll1.get_json()
        self.assertTrue(poll_data1['success'])
        self.assertEqual(poll_data1['payment_status'], 'pending')
        self.assertFalse(poll_data1['is_paid'])

        # 2. Fast-track UTR payment verification
        res_utr = self.client.post('/api/order/verify-utr', json={'order_id': order_id, 'utr_number': '123456789012'})
        self.assertEqual(res_utr.status_code, 200)
        utr_data = res_utr.get_json()
        self.assertTrue(utr_data['success'])

        # 3. Status poll after UTR must return is_paid: True and redirect_url
        res_poll2 = self.client.get(f'/api/order/status/{order_id}')
        self.assertEqual(res_poll2.status_code, 200)
        poll_data2 = res_poll2.get_json()
        self.assertTrue(poll_data2['success'])
        self.assertEqual(poll_data2['payment_status'], 'paid')
        self.assertTrue(poll_data2['is_paid'])
        self.assertIn('hpanel', poll_data2['redirect_url'])

    def test_09_billing_surcharge_gst_and_wp_sandbox(self):
        """Test 12% regulatory surcharge, 18% GST calculation, wholesale cut, and WP sandbox"""
        ord_payload = {
            'plan_id': 2, # Premium Web Hosting (₹1,548/yr)
            'domain_name': 'sandboxtestbrand.com',
            'billing_cycle': 'yearly',
            'payment_method': 'UPI_QR',
            'name': 'Sandbox Customer',
            'email': 'sandboxbuyer@brand.com',
            'phone': '+91 9555838550',
            'password': 'TestPass@123'
        }
        res_ord = self.client.post('/api/order/create', json=ord_payload)
        self.assertEqual(res_ord.status_code, 200)
        ord_data = res_ord.get_json()
        self.assertEqual(ord_data['subtotal'], 2148.0)
        self.assertEqual(ord_data['domain_fee'], 1299.0)
        self.assertEqual(ord_data['regulatory_fee'], 413.64) # 12% surcharge on (2148 + 1299)
        self.assertEqual(ord_data['tax_amount'], 694.92) # 18% GST on (3447 + 413.64)
        self.assertEqual(ord_data['total_amount'], 4555.56)
        order_id = ord_data['order_id']

        # Verify Payment and wholesale domain registration
        res_pay = self.client.post('/api/order/verify-utr', json={'order_id': order_id, 'utr_number': '423589123456'})
        self.assertEqual(res_pay.status_code, 200)

        # Check DB for wholesale registrar cost & profit cut
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT wholesale_cost, profit_amount, payment_status FROM orders WHERE id = ?", (order_id,))
        row = cursor.fetchone()
        self.assertEqual(row['payment_status'], 'paid')
        self.assertEqual(row['wholesale_cost'], 1199.0) # .com ConnectReseller wholesale
        self.assertEqual(row['profit_amount'], 3356.56) # Net profit after ConnectReseller cost

        # Verify Live WordPress Sandbox Preview
        res_site = self.client.get('/site/sandboxtestbrand.com')
        self.assertEqual(res_site.status_code, 200)
        self.assertIn(b'sandboxtestbrand.com', res_site.data)
        self.assertIn(b'WordPress', res_site.data)

        # Verify WordPress Admin Dashboard
        res_wpadmin = self.client.get('/site/sandboxtestbrand.com/wp-admin')
        self.assertEqual(res_wpadmin.status_code, 200)
        self.assertIn(b'Dashboard', res_wpadmin.data)
        self.assertIn(b'WP-Admin', res_site.data)

        # Verify Invoice itemization with Surcharge & GST
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['role'] = 'admin'
        res_inv = self.client.get(f'/invoice/{order_id}')
        self.assertEqual(res_inv.status_code, 200)
        self.assertIn(b'Cloud Infrastructure Surcharge', res_inv.data)
        self.assertIn(b'GST', res_inv.data)

        conn.close()


    def test_10_razorpay_and_cashfree_verification(self):
        """Test automated Razorpay and Cashfree payment callbacks and server provisioning"""
        # 1. Create order for Razorpay
        ord_payload = {
            'plan_id': 1, # Single Starter
            'domain_name': 'rzpteststore.in',
            'billing_cycle': 'monthly',
            'payment_method': 'RAZORPAY',
            'name': 'Razorpay Buyer',
            'email': 'rzpbuyer@teststore.in',
            'phone': '+91 9555838550',
            'password': 'RzpPass@123'
        }
        res_ord = self.client.post('/api/order/create', json=ord_payload)
        self.assertEqual(res_ord.status_code, 200)
        data = res_ord.get_json()
        self.assertTrue(data['success'])
        self.assertIn('razorpay_key_id', data)
        self.assertGreater(data['amount_in_paise'], 0)
        rzp_order_id = data['order_id']

        # 2. Verify Razorpay callback
        res_rzp = self.client.post('/api/order/razorpay/verify', json={
            'order_id': rzp_order_id,
            'razorpay_payment_id': 'pay_RZPTEST123456',
            'razorpay_order_id': 'order_RZPTEST123456',
            'razorpay_signature': 'test_signature_valid'
        })
        self.assertEqual(res_rzp.status_code, 200)
        rzp_verify = res_rzp.get_json()
        self.assertTrue(rzp_verify['success'])

        # 3. Verify Cashfree callback
        cf_payload = {
            'plan_id': 1,
            'domain_name': 'cfteststore.in',
            'billing_cycle': 'monthly',
            'payment_method': 'CASHFREE',
            'name': 'Cashfree Buyer',
            'email': 'cfbuyer@teststore.in',
            'phone': '+91 9555838550',
            'password': 'CfPass@123'
        }
        res_cf_ord = self.client.post('/api/order/create', json=cf_payload)
        cf_order_id = res_cf_ord.get_json()['order_id']

        res_cf = self.client.post('/api/order/cashfree/verify', json={
            'order_id': cf_order_id,
            'cf_payment_id': 'CF_TEST98765'
        })
        self.assertEqual(res_cf.status_code, 200)
        self.assertTrue(res_cf.get_json()['success'])

        # Verify both accounts are active in database
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT status FROM hosting_accounts WHERE domain_name = 'rzpteststore.in'")
        self.assertEqual(c.fetchone()['status'], 'active')
        c.execute("SELECT status FROM hosting_accounts WHERE domain_name = 'cfteststore.in'")
        self.assertEqual(c.fetchone()['status'], 'active')
        conn.close()

    def test_11_hostinger_free_domain_protection(self):
        """Verify Hostinger-style free domain business rules against profit loss"""
        # Case 1: 1-Month plan with new .in domain (MUST NOT be free! Domain fee = ₹399)
        res1 = self.client.post('/api/order/create', json={
            'plan_id': 2, # Plus Growth
            'domain_name': 'mytestbrand1month.in',
            'billing_cycle': 'monthly',
            'domain_action': 'register',
            'payment_method': 'UPI_QR',
            'email': 'buyer1m@test.com'
        })
        d1 = res1.get_json()
        self.assertTrue(d1['success'])
        self.assertFalse(d1['is_domain_free'])
        self.assertEqual(d1['domain_fee'], 599.0)
        self.assertEqual(d1['subtotal'], 349.0)

        # Case 2: 1-Month plan with existing domain (Domain fee = ₹0)
        res2 = self.client.post('/api/order/create', json={
            'plan_id': 2,
            'domain_name': 'alreadyregistered.com',
            'billing_cycle': 'monthly',
            'domain_action': 'existing',
            'payment_method': 'UPI_QR',
            'email': 'buyer_exist@test.com'
        })
        d2 = res2.get_json()
        self.assertTrue(d2['success'])
        self.assertFalse(d2['is_domain_free'])
        self.assertEqual(d2['domain_fee'], 0.0)
        self.assertEqual(d2['subtotal'], 349.0)

        # Case 3: 12-Month plan with Plan 2 (MUST BE FREE! Domain fee = ₹0)
        res3 = self.client.post('/api/order/create', json={
            'plan_id': 2,
            'domain_name': 'myfreedomain12m.in',
            'billing_cycle': 'yearly',
            'domain_action': 'register',
            'payment_method': 'UPI_QR',
            'email': 'buyer12m@test.com'
        })
        d3 = res3.get_json()
        self.assertTrue(d3['success'])
        self.assertTrue(d3['is_domain_free'])
        self.assertEqual(d3['domain_fee'], 0.0)
        self.assertEqual(d3['subtotal'], 2148.0)

        # Case 4: 12-Month plan with Single Starter (Plan 1) (MUST NOT be free, free_domain=0)
        res4 = self.client.post('/api/order/create', json={
            'plan_id': 1,
            'domain_name': 'starterdomain.com',
            'billing_cycle': 'yearly',
            'domain_action': 'register',
            'payment_method': 'UPI_QR',
            'email': 'buyer_starter@test.com'
        })
        d4 = res4.get_json()
        self.assertTrue(d4['success'])
        self.assertFalse(d4['is_domain_free'])
        self.assertEqual(d4['domain_fee'], 1299.0) # .com regular fee (profitable Option A)

    def test_12_option_b_cloud_engine_and_file_manager(self):
        """Test Option B Render-Native Engine: File Manager, Code Editor, Subpaths & Database Studio"""
        test_domain = "optionbtestbrand.in"

        # 1. File Manager: List files (auto-seeds starter files)
        res_list = self.client.get(f'/api/hpanel/files/list?domain={test_domain}')
        self.assertEqual(res_list.status_code, 200)
        data_list = res_list.get_json()
        self.assertTrue(data_list['success'])
        self.assertIn('index.html', [f['filename'] for f in data_list['files']])

        # 2. File Manager: Get file content
        res_get = self.client.get(f'/api/hpanel/files/get?domain={test_domain}&filename=index.html')
        self.assertEqual(res_get.status_code, 200)
        data_get = res_get.get_json()
        self.assertTrue(data_get['success'])
        self.assertIn('Welcome to', data_get['file']['content'])

        # 3. File Manager: Save customized file
        custom_code = "<html><body><h1>Live from Option B Cloud Editor!</h1></body></html>"
        res_save = self.client.post('/api/hpanel/files/save', json={
            'domain': test_domain,
            'filename': 'index.html',
            'content': custom_code
        })
        self.assertEqual(res_save.status_code, 200)
        self.assertTrue(res_save.get_json()['success'])

        # 4. Live Website Serving: custom HTML served
        res_site = self.client.get(f'/site/{test_domain}')
        self.assertEqual(res_site.status_code, 200)
        self.assertIn(b"Live from Option B Cloud Editor!", res_site.data)

        # 5. Live Website Serving: Subpath asset served (style.css)
        res_css = self.client.get(f'/site/{test_domain}/style.css')
        self.assertEqual(res_css.status_code, 200)
        self.assertIn('text/css', res_css.headers.get('Content-Type', ''))

        # 6. Multi-Tenant Router: Host header matches customer domain
        res_routed = self.client.get('/', headers={'Host': test_domain})
        self.assertEqual(res_routed.status_code, 200)
        self.assertIn(b"Live from Option B Cloud Editor!", res_routed.data)

        # 7. Web Database Studio: Tables lookup
        res_db = self.client.get(f'/api/hpanel/db/tables?domain={test_domain}')
        self.assertEqual(res_db.status_code, 200)
        data_db = res_db.get_json()
        self.assertTrue(data_db['success'])
        self.assertIn('wp_posts', [t['name'] for t in data_db['tables']])

        # 8. Web Database Studio: Safe SQL Query Runner
        res_query = self.client.post('/api/hpanel/db/query', json={
            'domain': test_domain,
            'query': f"SELECT filename, size_bytes FROM customer_files WHERE domain_name = '{test_domain}'"
        })
        self.assertEqual(res_query.status_code, 200)
        data_query = res_query.get_json()
        self.assertTrue(data_query['success'])
        self.assertIn('filename', data_query['columns'])

        # Cleanup test domain
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM customer_files WHERE domain_name = ?", (test_domain,))
        cursor.execute("DELETE FROM wp_sites WHERE domain_name = ?", (test_domain,))
        cursor.execute("DELETE FROM wp_posts WHERE domain_name = ?", (test_domain,))
        conn.commit()
        conn.close()

if __name__ == '__main__':
    unittest.main()
