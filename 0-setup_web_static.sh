#!/usr/bin/env bash
# Install Nginx if not installed
sudo apt-get -y update
sudo apt-get -y install nginx

# Create necessary directories if they don't exist
sudo mkdir -p /data/web_static/releases/test/ /data/web_static/shared/

# Create a fake HTML file for testing
echo "Hello, this is a test index page." | sudo tee /data/web_static/releases/test/index.html

# Create symbolic link if it doesn't exist, delete and recreate otherwise
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of /data/ to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to serve content from /data/web_static/current/ to hbnb_static
sudo bash -c 'cat <<EOF | sudo tee /etc/nginx/sites-available/default
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    root /var/www/html;
    index index.html index.htm index.nginx-debian.html;

    server_name _;

    location /hbnb_static/ {
        alias /data/web_static/current/;
    }

    location /redirect_me {
        return 301 https://bentechnews.blogspot.com;
    }
}
EOF'

# Restart Nginx
sudo service nginx restart

