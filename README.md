# Eurofiora e-commerce

Demo storefront and portals for Eurofiora, Milan.

| Portal | Address | For |
|---|---|---|
| Shop | https://shop.eurofiora.it | Customers buying flowers |
| App | https://app.eurofiora.it | Vendors (distributors) |
| Admin | https://admin.eurofiora.it | Vendor accounts, catalogue, tracking, metrics |

One FastAPI service on port 8030 serves all three; the hostname decides the portal. Own PostgreSQL database `eurofiora_shop`, separate from FreshFlow.

Design rules: see `design.md`. Read it before touching any template or CSS.

## Deploy on the server

```bash
cd ~/src/e-commerce && git pull
bash deploy/install.sh
```

First time only:

```bash
mkdir -p ~/src && git clone https://github.com/ahmed-touseef/e-commerce.git ~/src/e-commerce
```

The installer backs up nginx and the app, keeps the existing `.env`, restarts the `eurofiora-shop` service and prints PASS or FAIL for each portal.
