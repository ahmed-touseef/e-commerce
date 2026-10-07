server {
    server_name __HOST__;
    client_max_body_size 20m;

    location / {
        proxy_pass http://127.0.0.1:8030;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    listen 443 ssl;
    listen [::]:443 ssl;
    ssl_certificate /etc/letsencrypt/live/shop.eurofiora.it/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/shop.eurofiora.it/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
}

server {
    listen 80;
    listen [::]:80;
    server_name __HOST__;
    return 301 https://$host$request_uri;
}
