# VPS Deployment Guide for KANSOTEX Flask Application

This guide provides step-by-step instructions for deploying the KANSOTEX Flask application on a VPS (Virtual Private Server).

## Table of Contents
- [Server Requirements](#server-requirements)
- [Environment Variables](#environment-variables)
- [Installation Steps](#installation-steps)
- [Deployment Scripts](#deployment-scripts)
- [Systemd Service Configuration](#systemd-service-configuration)
- [Nginx Configuration](#nginx-configuration)
- [SSL Certificate Setup](#ssl-certificate-setup)
- [Database Setup](#database-setup)
- [Maintenance](#maintenance)

---

## Server Requirements

### Minimum Server Specifications
- **OS**: Ubuntu 20.04 LTS or later / Debian 11 or later
- **RAM**: 2GB minimum (4GB recommended)
- **CPU**: 2 cores minimum
- **Storage**: 20GB minimum
- **Python**: 3.10 or later

### Required Software
- Python 3.10+
- PostgreSQL 14+
- Nginx
- Git
- Supervisor or Systemd (for process management)

---

## Environment Variables

Create a `.env` file in your project root with the following variables:

```bash
# Application Settings
FLASK_APP=wsgi.py
FLASK_ENV=production
SESSION_SECRET=your-secret-key-here-generate-a-strong-random-string

# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/kansotex_db

# Admin Panel
ADMIN_PASSWORD=your-secure-admin-password-here

# SMTP Email Configuration (Optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-email-app-password
SMTP_SENDER_EMAIL=noreply@kansotex.ma

# Application URLs
REPLIT_DOMAINS=your-domain.com,www.your-domain.com
```

### How to Generate Secure Keys

```bash
# Generate SESSION_SECRET
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate ADMIN_PASSWORD
python3 -c "import secrets; print(secrets.token_urlsafe(16))"
```

---

## Installation Steps

### 1. Update System and Install Dependencies

```bash
# Update package lists
sudo apt update && sudo apt upgrade -y

# Install system dependencies
sudo apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib nginx git
```

### 2. Create Application User

```bash
# Create dedicated user for the application
sudo adduser --system --group --home /opt/kansotex kansotex
```

### 3. Clone Repository

```bash
# Switch to application user
sudo su - kansotex

# Clone your repository
cd /opt/kansotex
git clone https://github.com/yourusername/kansotex.git app
cd app
```

### 4. Set Up Python Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### 5. Configure Environment Variables

```bash
# Create .env file
nano .env

# Add all environment variables from the section above
# Save and exit (Ctrl+O, Enter, Ctrl+X)

# Secure the .env file
chmod 600 .env
```

---

## Deployment Scripts

### Deployment Script (`deploy.sh`)

Create a deployment script for easy updates:

```bash
#!/bin/bash

# deploy.sh - KANSOTEX Deployment Script

set -e  # Exit on error

APP_DIR="/opt/kansotex/app"
USER="kansotex"

echo "Starting deployment..."

# Navigate to app directory
cd $APP_DIR

# Pull latest changes
echo "Pulling latest code..."
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Database migrations (if needed)
# python manage.py db upgrade

# Restart the application
echo "Restarting application..."
sudo systemctl restart kansotex

echo "Deployment completed successfully!"
```

Make it executable:

```bash
chmod +x deploy.sh
```

### Backup Script (`backup.sh`)

```bash
#!/bin/bash

# backup.sh - Database and Files Backup Script

BACKUP_DIR="/opt/kansotex/backups"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="kansotex_db"
DB_USER="kansotex"

mkdir -p $BACKUP_DIR

# Backup database
echo "Backing up database..."
pg_dump -U $DB_USER $DB_NAME | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Backup uploaded files
echo "Backing up uploaded files..."
tar -czf $BACKUP_DIR/uploads_$DATE.tar.gz /opt/kansotex/app/static/uploads

# Keep only last 7 days of backups
find $BACKUP_DIR -name "*.gz" -mtime +7 -delete

echo "Backup completed: $BACKUP_DIR"
```

---

## Systemd Service Configuration

Create a systemd service file to manage the application:

### Create Service File

```bash
sudo nano /etc/systemd/system/kansotex.service
```

### Service Configuration

```ini
[Unit]
Description=KANSOTEX Flask Application
After=network.target postgresql.service

[Service]
Type=simple
User=kansotex
Group=kansotex
WorkingDirectory=/opt/kansotex/app
Environment="PATH=/opt/kansotex/app/venv/bin"
EnvironmentFile=/opt/kansotex/app/.env

ExecStart=/opt/kansotex/app/venv/bin/gunicorn \
    --workers 4 \
    --bind 127.0.0.1:8000 \
    --timeout 120 \
    --access-logfile /var/log/kansotex/access.log \
    --error-logfile /var/log/kansotex/error.log \
    --log-level info \
    wsgi:app

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Create Log Directory

```bash
sudo mkdir -p /var/log/kansotex
sudo chown kansotex:kansotex /var/log/kansotex
```

### Enable and Start Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable kansotex

# Start the service
sudo systemctl start kansotex

# Check status
sudo systemctl status kansotex
```

### Service Management Commands

```bash
# Start service
sudo systemctl start kansotex

# Stop service
sudo systemctl stop kansotex

# Restart service
sudo systemctl restart kansotex

# View logs
sudo journalctl -u kansotex -f

# View last 100 lines
sudo journalctl -u kansotex -n 100
```

---

## Nginx Configuration

### Install Nginx

```bash
sudo apt install nginx -y
```

### Create Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/kansotex
```

### Nginx Config File

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;
    
    # SSL Configuration (will be added by Certbot)
    # ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    # ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    
    # Max upload size
    client_max_body_size 20M;
    
    # Logs
    access_log /var/log/nginx/kansotex_access.log;
    error_log /var/log/nginx/kansotex_error.log;
    
    # Static files
    location /static {
        alias /opt/kansotex/app/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # Proxy to Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

### Enable Site

```bash
# Create symbolic link
sudo ln -s /etc/nginx/sites-available/kansotex /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

---

## SSL Certificate Setup

### Install Certbot

```bash
sudo apt install certbot python3-certbot-nginx -y
```

### Obtain SSL Certificate

```bash
# Get certificate and auto-configure Nginx
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Follow the prompts:
# - Enter email address
# - Agree to terms
# - Choose whether to redirect HTTP to HTTPS (recommended: yes)
```

### Auto-Renewal

Certbot automatically adds a renewal cron job. Verify it:

```bash
# Test renewal
sudo certbot renew --dry-run

# Check renewal timer
sudo systemctl status certbot.timer
```

---

## Database Setup

### 1. Install PostgreSQL

```bash
sudo apt install postgresql postgresql-contrib -y
```

### 2. Create Database and User

```bash
# Switch to postgres user
sudo -u postgres psql

# Inside psql:
CREATE DATABASE kansotex_db;
CREATE USER kansotex WITH PASSWORD 'your-secure-password';
GRANT ALL PRIVILEGES ON DATABASE kansotex_db TO kansotex;
\q
```

### 3. Configure PostgreSQL Access

```bash
# Edit pg_hba.conf
sudo nano /etc/postgresql/14/main/pg_hba.conf

# Add this line:
# local   kansotex_db     kansotex                                md5

# Restart PostgreSQL
sudo systemctl restart postgresql
```

### 4. Initialize Database

```bash
# Switch to application user
sudo su - kansotex
cd /opt/kansotex/app
source venv/bin/activate

# Run the application once to initialize database
python main.py
# Press Ctrl+C after database is initialized
```

---

## Maintenance

### View Application Logs

```bash
# Real-time logs
sudo journalctl -u kansotex -f

# Last 100 lines
sudo journalctl -u kansotex -n 100

# Today's logs
sudo journalctl -u kansotex --since today

# Gunicorn access logs
sudo tail -f /var/log/kansotex/access.log

# Gunicorn error logs
sudo tail -f /var/log/kansotex/error.log
```

### Monitor System Resources

```bash
# CPU and memory usage
htop

# Disk usage
df -h

# Check service status
sudo systemctl status kansotex nginx postgresql
```

### Database Maintenance

```bash
# Backup database
sudo -u kansotex pg_dump kansotex_db > /tmp/backup.sql

# Restore database
sudo -u kansotex psql kansotex_db < /tmp/backup.sql

# Vacuum database (optimize)
sudo -u postgres psql -d kansotex_db -c "VACUUM ANALYZE;"
```

### Update Application

```bash
# Switch to app user
sudo su - kansotex
cd /opt/kansotex/app

# Run deployment script
./deploy.sh
```

---

## Troubleshooting

### Application Won't Start

```bash
# Check service status
sudo systemctl status kansotex

# View detailed logs
sudo journalctl -u kansotex -n 50

# Check if port 8000 is in use
sudo netstat -tulpn | grep 8000

# Check environment variables
sudo cat /opt/kansotex/app/.env
```

### Database Connection Issues

```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Test database connection
sudo -u kansotex psql -d kansotex_db -c "SELECT 1;"

# Check database logs
sudo tail -f /var/log/postgresql/postgresql-14-main.log
```

### Nginx Issues

```bash
# Test Nginx configuration
sudo nginx -t

# Check Nginx status
sudo systemctl status nginx

# View Nginx error log
sudo tail -f /var/log/nginx/error.log
```

### Permission Issues

```bash
# Fix ownership
sudo chown -R kansotex:kansotex /opt/kansotex/app

# Fix .env permissions
sudo chmod 600 /opt/kansotex/app/.env

# Fix static files permissions
sudo chmod -R 755 /opt/kansotex/app/static
```

---

## Security Best Practices

1. **Use strong passwords** for all services (database, admin panel, etc.)
2. **Keep system updated**: `sudo apt update && sudo apt upgrade -y`
3. **Enable firewall**:
   ```bash
   sudo ufw allow 22/tcp
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw enable
   ```
4. **Restrict database access** to localhost only
5. **Regular backups**: Schedule the backup script with cron
6. **Monitor logs** regularly for suspicious activity
7. **Use SSL/TLS** for all connections
8. **Disable SSH password authentication** (use keys only)

---

## Performance Optimization

### Gunicorn Workers

Calculate optimal number of workers:
```
workers = (2 × CPU_cores) + 1
```

For a 4-core server:
```
workers = (2 × 4) + 1 = 9
```

Update in systemd service file accordingly.

### Database Connection Pooling

Add to your Flask configuration:
```python
SQLALCHEMY_POOL_SIZE = 10
SQLALCHEMY_MAX_OVERFLOW = 20
SQLALCHEMY_POOL_RECYCLE = 3600
```

### Nginx Caching

Add to Nginx location block for static files:
```nginx
location /static {
    alias /opt/kansotex/app/static;
    expires 1y;
    add_header Cache-Control "public, immutable";
    gzip on;
    gzip_types text/css application/javascript image/svg+xml;
}
```

---

## Support

For issues or questions:
- Check application logs: `sudo journalctl -u kansotex -f`
- Review this documentation
- Contact system administrator

---

**Last Updated**: November 2025  
**Version**: 1.0
