#!/bin/bash
# SQLite bazasini backup qilish (shop papkasida ishga tushiring: ./backup_db.sh)
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
BACKUP_DIR="$SCRIPT_DIR/backups"
mkdir -p "$BACKUP_DIR"
NAME="db.sqlite3.$(date +%Y-%m-%d_%H-%M-%S)"
cp -a db.sqlite3 "$BACKUP_DIR/$NAME"
echo "Backup saqlandi: $BACKUP_DIR/$NAME"
