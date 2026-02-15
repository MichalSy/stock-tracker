# 🚀 Deployment Guide (Caddy)

Deploy Stock Tracker on your own server with Caddy (automatic HTTPS!).

---

## 📋 Prerequisites

- Linux Server (Ubuntu/Debian recommended)
- Python 3.11+
- Domain pointing to server IP (DNS A record)
- SSH access

---

## 1️⃣ Server Setup

```bash
# SSH into server
ssh user@your-server.com

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip git -y

# Install Caddy (Automatic HTTPS!)
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install caddy
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

## 4️⃣ Caddy Reverse Proxy (Automatic HTTPS!)

**Create Caddy config:**
```bash
sudo nano /etc/caddy/Caddyfile
```

**Replace entire file with:**
```
your-domain.com {
    reverse_proxy localhost:8501 {
        header_up Host {host}
        header_up X-Real-IP {remote_host}
        header_up X-Forwarded-For {remote_host}
        header_up X-Forwarded-Proto {scheme}
    }
}
```

**Replace `your-domain.com` with your actual domain!**

```bash
# Test config
sudo caddy validate --config /etc/caddy/Caddyfile

# Restart Caddy
sudo systemctl restart caddy

# Check status
sudo systemctl status caddy
```

**That's it!** Caddy automatically:
- ✅ Gets SSL certificate (Let's Encrypt)
- ✅ Renews certificates
- ✅ Redirects HTTP → HTTPS
- ✅ Handles WebSocket (Streamlit needs it)

---

## 5️⃣ DNS Setup (Before accessing!)

**Important:** Make sure DNS is configured BEFORE starting Caddy!

```
Type: A
Name: @ (or subdomain like "stocks")
Value: YOUR_SERVER_IP
TTL: 3600
```

Example for `stocks.yourdomain.com`:
- A record: stocks → YOUR_SERVER_IP

Caddy will automatically get SSL once DNS resolves!

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

### Caddy errors?
```bash
# Check Caddy logs
sudo journalctl -u caddy -f

# Validate config
sudo caddy validate --config /etc/caddy/Caddyfile

# Check if DNS resolves
dig your-domain.com
```

### SSL not working?
```bash
# Check DNS first! (must point to server IP)
dig your-domain.com

# Caddy logs
sudo journalctl -u caddy -n 100

# Manual certificate request (debug)
sudo caddy trust
```

### 502 Bad Gateway?
```bash
# Check if Streamlit is running
sudo systemctl status stock-tracker

# Check port 8501
curl http://localhost:8501
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
