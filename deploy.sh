#!/bin/bash
# Quick Deploy Script for Stock Tracker
# Run on server: bash deploy.sh your-domain.com

DOMAIN=$1

if [ -z "$DOMAIN" ]; then
    echo "❌ Usage: bash deploy.sh your-domain.com"
    exit 1
fi

echo "🚀 Deploying Stock Tracker to $DOMAIN..."
echo ""

# Update system
echo "📦 Updating system..."
sudo apt update && sudo apt upgrade -y

# Install dependencies
echo "📦 Installing Python & Git..."
sudo apt install -y python3.11 python3.11-venv python3-pip git

# Install Caddy
echo "📦 Installing Caddy..."
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install -y caddy

# Clone repo
echo "📥 Cloning repository..."
cd /opt
sudo git clone https://github.com/MichalSy/stock-tracker.git
cd stock-tracker

# Setup Python
echo "🐍 Setting up Python environment..."
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create systemd service
echo "⚙️ Creating systemd service..."
sudo tee /etc/systemd/system/stock-tracker.service > /dev/null <<EOL
[Unit]
Description=Stock Tracker Streamlit App
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/stock-tracker
Environment="PATH=/opt/stock-tracker/venv/bin"
ExecStart=/opt/stock-tracker/venv/bin/streamlit run app.py --server.port 8501 --server.address 0.0.0.0
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOL

# Start service
sudo systemctl daemon-reload
sudo systemctl enable stock-tracker
sudo systemctl start stock-tracker

# Configure Caddy
echo "🌐 Configuring Caddy..."
sudo tee /etc/caddy/Caddyfile > /dev/null <<EOL
$DOMAIN {
    reverse_proxy localhost:8501 {
        header_up Host {host}
        header_up X-Real-IP {remote_host}
        header_up X-Forwarded-For {remote_host}
        header_up X-Forwarded-Proto {scheme}
    }
}
EOL

# Restart Caddy
sudo systemctl restart caddy

echo ""
echo "✅ Deployment complete!"
echo "🌐 Access at: https://$DOMAIN"
echo ""
echo "📋 Commands:"
echo "  Check logs:     sudo journalctl -u stock-tracker -f"
echo "  Restart app:    sudo systemctl restart stock-tracker"
echo "  Check status:   sudo systemctl status stock-tracker"
