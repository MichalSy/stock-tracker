# 🚀 Deployment Guide (Without Docker)

Deploy Stock Tracker on your own server with custom domain.

---

## 📋 Prerequisites

- Linux Server (Ubuntu/Debian recommended)
- Python 3.11+
- Domain pointing to server IP
- SSH access

---

## 1️⃣ Server Setup

```bash
# SSH into server
ssh user@your-server.com

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip -y

# Install Nginx (Reverse Proxy)
sudo apt install nginx -y
```

---

## 2️⃣ App Setup

```bash
# Clone repo
cd /opt
sudo git clone https://github.com/MichalSy/stock-tracker.git
cd stock-tracker

# Create virtual env
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Test run
streamlit run app.py --server.port 8501
# → Should work! Stop with Ctrl+C
```

---

## 3️⃣ Systemd Service (Auto-start)

```bash
# Create service file
sudo nano /etc/systemd/system/stock-tracker.service
```

**Paste this:**
```ini
[Unit]
Description=Stock Tracker Streamlit App
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/stock-tracker
Environment="PATH=/opt/stock-tracker/venv/bin"
ExecStart=/opt/stock-tracker/venv/bin/streamlit run app.py --server.port 8501 --server.address 0.0.0.0
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
# Enable & start service
sudo systemctl daemon-reload
sudo systemctl enable stock-tracker
sudo systemctl start stock-tracker

# Check status
sudo systemctl status stock-tracker
```

---

## 4️⃣ Nginx Reverse Proxy (HTTPS)

```bash
# Create Nginx config
sudo nano /etc/nginx/sites-available/stock-tracker
```

**Paste this:**
```nginx
server {
    listen 80;
    server_name your-domain.com;  # ← CHANGE THIS

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Streamlit WebSocket support
        proxy_read_timeout 86400;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/stock-tracker /etc/nginx/sites-enabled/

# Test config
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

---

## 5️⃣ SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal test
sudo certbot renew --dry-run
```

---

## 6️⃣ Firewall (Optional but Recommended)

```bash
# Allow HTTP/HTTPS
sudo ufw allow 'Nginx Full'

# Enable firewall
sudo ufw enable
```

---

## ✅ Done!

**Access your app:**
- `https://your-domain.com`
- Mobile-friendly! 📱

---

## 🔧 Management Commands

```bash
# Check logs
sudo journalctl -u stock-tracker -f

# Restart app
sudo systemctl restart stock-tracker

# Update app
cd /opt/stock-tracker
sudo git pull
sudo systemctl restart stock-tracker

# Stop app
sudo systemctl stop stock-tracker
```

---

## 🔒 Security Tips

1. **Change SSH port** (from 22 to random)
2. **Disable root login**
3. **Use SSH keys** (not passwords)
4. **Enable UFW firewall**
5. **Keep system updated** (`apt update && apt upgrade`)

---

## 🐛 Troubleshooting

### App not starting?
```bash
# Check logs
sudo journalctl -u stock-tracker -n 50

# Manual test
cd /opt/stock-tracker
source venv/bin/activate
streamlit run app.py
```

### 502 Bad Gateway?
```bash
# Check if app is running
sudo systemctl status stock-tracker

# Check Nginx config
sudo nginx -t
```

### Permission issues?
```bash
# Fix permissions
sudo chown -R www-data:www-data /opt/stock-tracker
```

---

## 📊 Monitoring (Optional)

```bash
# Install htop
sudo apt install htop

# Monitor resources
htop
```

---

**Next Steps:**
- Set up alerts (Phase 3)
- Add authentication if needed (Streamlit has built-in password protection)
- Configure auto-refresh in the app
