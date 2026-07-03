#!/bin/bash
# scripts/server_setup.sh
# Run ONCE on a fresh Ubuntu 22.04 VPS (Oracle Cloud, EC2, etc.)
set -e

echo "Installing Docker..."
curl -fsSL https://get.docker.com | sh
usermod -aG docker $USER

echo "Installing Docker Compose plugin..."
apt-get install -y docker-compose-plugin

echo "Creating project directory..."
mkdir -p /home/$USER/ecommerce_project/nginx

echo ""
echo " Server ready. Next steps:"
echo ""
echo "  1. Copy .env.prod to /home/$USER/ecommerce_project/.env.prod"
echo "  2. Push to main branch — GitHub Actions handles the rest"
echo ""
echo "Or deploy manually:"
echo "  cd /home/$USER/ecommerce_project"
echo "  docker compose -f docker-compose.prod.yml up -d"