# ₹0 Budget Production Deployment Guide: Launching Your Hosting Company

This guide explains step-by-step how to take **Hosting Wallah** from your local machine to live production servers **without spending a single rupee on infrastructure**.

---

## Architecture: The ₹0 Startup Blueprint

```
[ Your Customers ]
        │ (Browser)
        ▼
[ Cloudflare Free CDN & DDoS Shield ]
        │
        ▼
[ Oracle Cloud "Always Free" Server ] ── (4 OCPU, 24 GB RAM, 200 GB SSD)
  ├── 1. Hosting Wallah Web Engine (Python/Flask + SQLite)
  └── 2. HestiaCP / CyberPanel (Automated Hosting Engine & LiteSpeed/Nginx)
```

---

## Step 1: Claim Your Lifetime Free Server (Oracle Cloud Always Free)

Oracle offers the world's most generous free cloud tier for developers and entrepreneurs:
* **Specs:** 4 OCPU ARM Ampere A1 Cores, 24 GB RAM, 200 GB Storage, 10 TB Monthly Bandwidth.
* **Cost:** ₹0 Forever.
* **Capacity:** Capable of running 50 to 100 client WordPress websites smoothly.

### Instructions:
1. Visit [oracle.com/cloud/free](https://www.oracle.com/cloud/free/) and click **Start for free**.
2. Select your Home Region as **India (Mumbai or Hyderabad)** for ultra-low latency.
3. Verify your identity with a debit/credit card (around ₹70-₹100 is temporarily held and refunded immediately).
4. Go to **Compute > Instances > Create Instance**:
   * **Image:** Ubuntu 22.04 LTS (ARM64).
   * **Shape:** `VM.Standard.A1.Flex` (Change to 4 OCPU, 24 GB RAM).
   * **Boot Volume:** 200 GB.
   * **SSH Keys:** Download your private `.key` file.
5. In **Networking > Virtual Cloud Networks > Security Lists**, open ports:
   * `80`, `443` (Web HTTP/HTTPS)
   * `8083` (HestiaCP Admin Panel)
   * `21`, `22` (FTP and SSH)
   * `53` (DNS Zone)

---

## Step 2: Install HestiaCP Control Panel (1 Command)

SSH into your Oracle Ubuntu server:
```bash
ssh -i your-key.key ubuntu@<YOUR_SERVER_PUBLIC_IP>
```

Run the automated installer script:
```bash
# 1. Download HestiaCP installer
wget https://raw.githubusercontent.com/hestiacp/hestiacp/release/install/hst-install.sh

# 2. Run optimized installation (low-resource footprint)
sudo bash hst-install.sh --port 8083 --apache yes --phpfpm yes --multiphp yes --named yes --mysql yes --clamav no --spamassassin no --force
```
*(Disabling ClamAV and SpamAssassin saves over 2GB of RAM, leaving more memory for client websites).*

Once finished, note your HestiaCP admin URL and password:
* **URL:** `https://<YOUR_SERVER_IP>:8083`
* **Username:** `admin`
* **Password:** *(Shown on terminal)*

---

## Step 3: Setup White-Label Nameservers on Cloudflare (Free)

To look 100% professional like Hostinger, clients should point to your own branded nameservers:
* `ns1.yourdomain.com` ➔ `<YOUR_SERVER_IP>`
* `ns2.yourdomain.com` ➔ `<YOUR_SERVER_IP>`

1. Add your primary domain to a free [Cloudflare](https://dash.cloudflare.com/) account.
2. In Cloudflare DNS, add two `A` records:
   * Name: `ns1`, IPv4: `<YOUR_SERVER_IP>`, Proxy: DNS only (Grey Cloud).
   * Name: `ns2`, IPv4: `<YOUR_SERVER_IP>`, Proxy: DNS only (Grey Cloud).
3. At your domain registrar (e.g. Namecheap / Dynadot), create "Glue Records" / "Personal Nameservers" pointing `ns1` and `ns2` to your server IP.

---

## Step 4: Deploy & Connect Hosting Wallah

On your Oracle server, clone or upload this Hosting Wallah directory:

```bash
# Install Python and pip
sudo apt update && sudo apt install -y python3-pip python3-venv git

# Clone or transfer Hosting Wallah files
cd /var/www/
git clone <your-repo> hostingwallah
cd hostingwallah

# Install requirements
pip3 install -r requirements.txt

# Run Hosting Wallah in background with systemd
sudo cp hostingwallah.service /etc/systemd/system/
sudo systemctl enable --now hostingwallah
```

### Connect to HestiaCP API:
1. Log into your Hosting Wallah admin panel at `http://<YOUR_SERVER_IP>:5000/login` with `voltaramedia@gmail.com` / `voltara@123`.
2. Go to **Admin WHM > Server Adapter & Payment Configuration**.
3. Set:
   * **Active Adapter:** `HestiaCP REST API`
   * **Panel Host:** `https://127.0.0.1:8083`
   * **API Password:** Your HestiaCP admin password.
   * **UPI ID:** `pawan8550@naviaxis`
4. Click **Save Settings**.

Now, every time a customer pays via UPI QR or card on your storefront, Hosting Wallah will **automatically trigger HestiaCP to provision their website, generate DNS zones, and activate free SSL**!

---

## Step 5: Growth Strategy — Acquiring Your First 10 Clients

1. **Local Businesses (High Conversion):**
   * Visit 10 local shops, clinics, or services in your town.
   * Offer: *"We'll build your online presence with website + 1 year free hosting for just ₹2,500."*
   * 4 clients = ₹10,000 profit with ₹0 hosting expense.
2. **Student & Freelancer Discount:**
   * Offer students your ₹49/month Starter plan. Hostinger costs ₹2,500+ upfront for a year, so students will gladly choose your ₹49/mo flexible plan.
3. **Freelance Web Designers:**
   * Partner with web designers and give them 30% recurring commissions for hosting their client sites with you.
