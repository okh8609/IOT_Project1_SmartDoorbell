sed 's/server_name _;/server_name khaos.tw;/g' -i /etc/nginx/sites-available/default

/etc/init.d/nginx start

curl  https://get.acme.sh | sh

~/.acme.sh/acme.sh --issue -d khaos.tw  --nginx

~/.acme.sh/acme.sh --install-cert -d khaos.tw \
    --key-file /etc/letsencrypt/nginx/key.pem \
    --fullchain-file /etc/letsencrypt/nginx/cert.pem

cp /data/nginx_conf/default /etc/nginx/sites-available/default

/etc/init.d/nginx restart
