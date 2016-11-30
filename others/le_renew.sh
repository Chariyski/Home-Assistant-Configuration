#!/usr/bin/env bash
# Check if cert is about to expire (3 days)
if openssl x509 -checkend 259200 -noout -in /etc/letsencrypt/live/*/fullchain.pem
then
echo "Good for now"
else
# Launching certbot from installed location with HTTPS challenge on port 8123 (port your HA usually running on)
# Stopping HA service first and running after update
sudo /home/pi/certbot/certbot-auto renew --quiet --no-self-upgrade --standalone --preferred-challenges tls-sni-01 --tls-sni-01-port 8123 --pre-hook "systemctl stop home-assistant@rootservice" --post-hook "systemctl start home-assistant@root.service"
fi
