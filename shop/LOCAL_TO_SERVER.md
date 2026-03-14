# Lokal loyihadagi ma'lumotlarni serverga yuklash

Lokal kompyuteringizdagi **db.sqlite3** va **media/** ni serverga yuborib, serverdagi loyihani shu ma'lumotlar bilan yangilash.

---

## 1. Lokal kompyuterdan (Mac/Linux)

Terminalda **Totembo-1/shop** papkasida yoki uning ustida ishlang.

### Bazani serverga yuborish (scp)

```bash
cd /Users/mirazizerkinaliyev_dev/Desktop/Totembo-1/shop

# db.sqlite3 ni serverga yuborish
scp db.sqlite3 root@103.6.168.149:/root/TOTEMBO/shop/db.sqlite3.new
```

Parol so‘ralsa server parolini kiriting. Keyin serverda (2-qadam) yangi faylni asl bazaga almashtiramiz.

### Media fayllarni ham yuborish (rasmlar, yuklangan fayllar)

Agar **shop/media/** papkangizda fayllar bo‘lsa:

```bash
scp -r media root@103.6.168.149:/root/TOTEMBO/shop/
```

---

## 2. Serverda

SSH orqali serverga kiring, keyin:

```bash
cd /root/TOTEMBO/shop

# Eski bazani backup qilish
cp db.sqlite3 backups/db.sqlite3.before-restore-$(date +%Y-%m-%d) 2>/dev/null || (mkdir -p backups && cp db.sqlite3 backups/db.sqlite3.before-restore-$(date +%Y-%m-%d))

# Yangi bazani o‘rniga qo‘yish
mv db.sqlite3.new db.sqlite3

# Ruxsatlar (Django/gunicorn foydalanuvchisi uchun)
chmod 644 db.sqlite3

# Gunicorn/Django ni qayta ishga tushirish
sudo systemctl restart totembo
# yoki agar qo‘lda ishlatayotgan bo‘lsangiz: pkill -f gunicorn, keyin gunicorn ... qayta ishga tushiring
```

Shundan keyin saytda lokal loyihadagi mahsulotlar, kategoriyalar va admin ma’lumotlari ko‘rinadi.

---

## 3. Bir buyruqda (lokalda — baza + media)

```bash
cd /Users/mirazizerkinaliyev_dev/Desktop/Totembo-1/shop
scp db.sqlite3 root@103.6.168.149:/root/TOTEMBO/shop/db.sqlite3.new
scp -r media root@103.6.168.149:/root/TOTEMBO/shop/ 2>/dev/null || true
```

Keyin serverda yuqoridagi 2-qadamdagi buyruqlarni bajaring.

---

## Eslatma

- **103.6.168.149** o‘rniga o‘z server IP yoki hostnomingizni yozing.
- **root** o‘rniga serverdagi foydalanuvchi nomini yozing (masalan `ubuntu`).
- SSH kalit ishlatsangiz: `scp -i /yo'l/kalit.pem db.sqlite3 user@server:/root/TOTEMBO/shop/db.sqlite3.new`
