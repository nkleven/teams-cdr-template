#!/bin/bash
# Project Eden - Worker VM Initialization Script
# Runs on first boot via cloud-init

set -e

echo "=== Project Eden Worker Initialization ===" | tee /var/log/eden-init.log

# Update system
echo "Updating system packages..." | tee -a /var/log/eden-init.log
apt-get update && apt-get upgrade -y

# Install essential packages
echo "Installing essential packages..." | tee -a /var/log/eden-init.log
apt-get install -y \
    curl \
    wget \
    git \
    unzip \
    jq \
    htop \
    nginx \
    docker.io \
    docker-compose \
    nodejs \
    npm \
    python3 \
    python3-pip \
    azure-cli

# Enable and start Docker
echo "Configuring Docker..." | tee -a /var/log/eden-init.log
systemctl enable docker
systemctl start docker
usermod -aG docker edenadmin

# Install Node.js LTS
echo "Installing Node.js LTS..." | tee -a /var/log/eden-init.log
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt-get install -y nodejs

# Create Eden directories
echo "Creating Eden directories..." | tee -a /var/log/eden-init.log
mkdir -p /opt/eden/{app,logs,config,data}
chown -R edenadmin:edenadmin /opt/eden

# Configure health check endpoint
echo "Configuring health check endpoint..." | tee -a /var/log/eden-init.log
cat > /etc/nginx/sites-available/health << 'EOF'
server {
    listen 8080;
    server_name _;
    
    location /health {
        access_log off;
        add_header Content-Type text/plain;
        return 200 'healthy';
    }
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_cache_bypass $http_upgrade;
    }
}
EOF

ln -sf /etc/nginx/sites-available/health /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
systemctl restart nginx

# Create systemd service for Eden worker
echo "Creating Eden worker service..." | tee -a /var/log/eden-init.log
cat > /etc/systemd/system/eden-worker.service << 'EOF'
[Unit]
Description=Eden Worker Service
After=network.target docker.service
Requires=docker.service

[Service]
Type=simple
User=edenadmin
WorkingDirectory=/opt/eden/app
Environment=NODE_ENV=production
Environment=PORT=3000
ExecStart=/usr/bin/node server.js
Restart=always
RestartSec=10
StandardOutput=append:/opt/eden/logs/worker.log
StandardError=append:/opt/eden/logs/worker-error.log

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload

# Install Azure Monitor agent for observability
echo "Installing Azure Monitor agent..." | tee -a /var/log/eden-init.log
wget -O azcmagent.deb "https://aka.ms/azcmagent-linux-amd64"
dpkg -i azcmagent.deb || apt-get install -f -y
rm azcmagent.deb

# Configure firewall
echo "Configuring firewall..." | tee -a /var/log/eden-init.log
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 8080/tcp
ufw allow 3000/tcp
ufw --force enable

# Set up log rotation
echo "Configuring log rotation..." | tee -a /var/log/eden-init.log
cat > /etc/logrotate.d/eden << 'EOF'
/opt/eden/logs/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 edenadmin edenadmin
    sharedscripts
}
EOF

# Create placeholder app
echo "Creating placeholder app..." | tee -a /var/log/eden-init.log
cat > /opt/eden/app/server.js << 'EOF'
const http = require('http');
const os = require('os');

const PORT = process.env.PORT || 3000;
const HOSTNAME = os.hostname();

const server = http.createServer((req, res) => {
    const response = {
        status: 'healthy',
        hostname: HOSTNAME,
        timestamp: new Date().toISOString(),
        path: req.url
    };
    
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(response, null, 2));
});

server.listen(PORT, () => {
    console.log(`Eden Worker running on port ${PORT} (${HOSTNAME})`);
});
EOF

chown -R edenadmin:edenadmin /opt/eden
systemctl enable eden-worker
systemctl start eden-worker

echo "=== Eden Worker Initialization Complete ===" | tee -a /var/log/eden-init.log
echo "Completed at: $(date)" | tee -a /var/log/eden-init.log
