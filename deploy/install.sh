#!/usr/bin/env bash
# Eurofiora Shop installer: deploys this repo to ~/eurofiora-shop (shop, app, admin portals).
# Run as your normal user (NOT with sudo):  bash deploy/install.sh
set -euo pipefail

SRC="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$HOME/eurofiora-shop"
PORT=8030
DB_NAME=eurofiora_shop
DB_USER=eurofiora_shop
SERVICE=eurofiora-shop
HOSTS=(shop.eurofiora.it app.eurofiora.it admin.eurofiora.it)
CERT_DIR=/etc/letsencrypt/live/shop.eurofiora.it
STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP="$HOME/backups/eurofiora-shop-$STAMP"

say()  { printf '\n==> %s\n' "$*"; }
fail() { printf '\nFAILED: %s\n' "$*" >&2; exit 1; }

[ "$EUID" -ne 0 ] || fail "run as your normal user: bash deploy/install.sh (no sudo)"

say "Asking for sudo once"
sudo -v

say "Prechecks"
for f in "$CERT_DIR/fullchain.pem" "$CERT_DIR/privkey.pem" \
         /etc/letsencrypt/options-ssl-nginx.conf /etc/letsencrypt/ssl-dhparams.pem; do
  sudo test -f "$f" || fail "missing $f"
done
if ! systemctl is-active --quiet "$SERVICE"; then
  if ss -tln | grep "127.0.0.1:$PORT " >/dev/null; then
    fail "port $PORT is already used by another program"
  fi
fi
echo "ok"

say "Backing up to $BACKUP"
mkdir -p "$BACKUP/nginx"
for h in "${HOSTS[@]}"; do
  if sudo test -f "/etc/nginx/sites-available/$h"; then
    sudo cp "/etc/nginx/sites-available/$h" "$BACKUP/nginx/$h"
  fi
done
if [ -d "$DEST/app" ]; then
  cp -a "$DEST/app" "$BACKUP/app"
fi
echo "ok"

say "Copying application to $DEST"
mkdir -p "$DEST"
rm -rf "$DEST/app"
cp -a "$SRC/app" "$DEST/app"
cp "$SRC/requirements.txt" "$DEST/requirements.txt"
echo "ok"

say "Database password (.env)"
if [ -f "$DEST/.env" ]; then
  DB_PASS="$(grep '^DB_PASSWORD=' "$DEST/.env" | cut -d= -f2)"
  [ -n "$DB_PASS" ] || fail "$DEST/.env exists but has no DB_PASSWORD line"
  echo "kept existing .env"
else
  DB_PASS="$(openssl rand -hex 24)"
  umask 077
  cat > "$DEST/.env" <<ENV
DB_PASSWORD=$DB_PASS
DATABASE_URL=postgresql+psycopg://$DB_USER:$DB_PASS@localhost:5432/$DB_NAME
ENV
  umask 022
  echo "created new .env"
fi
chmod 600 "$DEST/.env"

say "PostgreSQL role and database ($DB_NAME, separate from FreshFlow)"
pg() { (cd /tmp && sudo -u postgres psql -v ON_ERROR_STOP=1 -tAc "$1"); }
if [ "$(pg "SELECT 1 FROM pg_roles WHERE rolname='$DB_USER'")" = "1" ]; then
  pg "ALTER ROLE $DB_USER WITH LOGIN PASSWORD '$DB_PASS'" >/dev/null
  echo "role exists, password synced"
else
  pg "CREATE ROLE $DB_USER WITH LOGIN PASSWORD '$DB_PASS'" >/dev/null
  echo "role created"
fi
if [ "$(pg "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'")" = "1" ]; then
  echo "database exists"
else
  (cd /tmp && sudo -u postgres createdb -O "$DB_USER" "$DB_NAME")
  echo "database created"
fi

say "Python virtualenv and packages"
if [ ! -x "$DEST/.venv/bin/python" ]; then
  if ! python3 -m venv "$DEST/.venv" 2>/dev/null; then
    rm -rf "$DEST/.venv"
    sudo apt-get update -qq
    sudo apt-get install -y -qq python3-venv
    python3 -m venv "$DEST/.venv"
  fi
fi
"$DEST/.venv/bin/pip" install -q --upgrade pip
"$DEST/.venv/bin/pip" install -q -r "$DEST/requirements.txt"
echo "ok"

say "systemd service $SERVICE (port $PORT)"
sudo tee "/etc/systemd/system/$SERVICE.service" >/dev/null <<UNIT
[Unit]
Description=Eurofiora Shop (shop, app, admin portals)
After=network.target postgresql.service

[Service]
User=$USER
Group=$(id -gn)
WorkingDirectory=$DEST
ExecStart=$DEST/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port $PORT --proxy-headers --forwarded-allow-ips 127.0.0.1
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
UNIT
sudo systemctl daemon-reload
sudo systemctl enable --quiet "$SERVICE"
sudo systemctl restart "$SERVICE"

ok=0
for i in $(seq 1 20); do
  code="$(curl -s -o /dev/null -w '%{http_code}' -H 'Host: shop.eurofiora.it' "http://127.0.0.1:$PORT/healthz" || true)"
  if [ "$code" = "200" ]; then ok=1; break; fi
  sleep 1
done
if [ "$ok" != "1" ]; then
  sudo journalctl -u "$SERVICE" -n 40 --no-pager
  fail "service did not answer on port $PORT (log above); nginx was NOT changed"
fi
echo "service is up"

say "nginx: pointing the three subdomains at the service"
for h in "${HOSTS[@]}"; do
  sed "s/__HOST__/$h/g" "$SRC/deploy/portal.nginx.tpl" | sudo tee "/etc/nginx/sites-available/$h" >/dev/null
  sudo ln -sf "/etc/nginx/sites-available/$h" "/etc/nginx/sites-enabled/$h"
done
if ! sudo nginx -t 2>/tmp/eurofiora-nginx-test.log; then
  cat /tmp/eurofiora-nginx-test.log
  for h in "${HOSTS[@]}"; do
    if [ -f "$BACKUP/nginx/$h" ]; then
      sudo cp "$BACKUP/nginx/$h" "/etc/nginx/sites-available/$h"
    fi
  done
  fail "nginx config test failed, previous files restored, nginx not reloaded"
fi
sudo systemctl reload nginx
echo "ok"

say "Verification"
bad=0
for h in "${HOSTS[@]}"; do
  portal="${h%%.*}"
  body="$(curl -s "https://$h/healthz" || true)"
  code="$(curl -s -o /dev/null -w '%{http_code}' "https://$h/" || true)"
  if [[ "$body" == *"\"portal\":\"$portal\""* ]] && [ "$code" = "200" ]; then
    echo "PASS  https://$h  (page 200, portal $portal, database ok)"
  else
    echo "FAIL  https://$h  page=$code healthz=$body"; bad=1
  fi
done
code="$(curl -s -o /dev/null -w '%{http_code}' https://www.eurofiora.it/ || true)"
if [ "$code" = "200" ]; then echo "PASS  https://www.eurofiora.it  (FreshFlow untouched)"; else echo "FAIL  https://www.eurofiora.it  $code"; bad=1; fi

[ "$bad" = "0" ] || fail "see FAIL lines above"
printf '\nDeploy complete. Backup: %s\n' "$BACKUP"
