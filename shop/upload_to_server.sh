#!/bin/bash
# Lokal: shop papkasida ishga tushiring. Parol so'ralsa server parolini kiriting.
# Masalan: cd /Users/mirazizerkinaliyev_dev/Desktop/Totembo-1/shop && ./upload_to_server.sh

set -e
SERVER="${1:-root@103.6.168.149}"
REMOTE_DIR="/root/TOTEMBO/shop"
SHOP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SHOP_DIR"

echo "=== 1. db.sqlite3 yuborilmoqda... ==="
scp -o StrictHostKeyChecking=no db.sqlite3 "$SERVER:$REMOTE_DIR/db.sqlite3.new"

echo "=== 2. media papka yuborilmoqda... ==="
scp -o StrictHostKeyChecking=no -r media "$SERVER:$REMOTE_DIR/" || true

echo ""
echo "=== Yuklash tugadi. Endi SERVERda quyidagi buyruqlarni bajaring (SSH orqali): ==="
echo ""
echo "  cd $REMOTE_DIR"
echo "  mkdir -p backups"
echo "  cp db.sqlite3 backups/db.sqlite3.old-\$(date +%Y-%m-%d)"
echo "  mv db.sqlite3.new db.sqlite3"
echo "  chmod 644 db.sqlite3"
echo "  sudo systemctl restart totembo"
echo ""
echo "Agar gunicorn qo'lda ishlatayotgan bo'lsangiz: Ctrl+C, keyin"
echo "  gunicorn --bind 0.0.0.0:8000 shop.wsgi:application"
echo ""
