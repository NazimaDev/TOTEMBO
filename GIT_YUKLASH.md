# Git va GitHubga yuklash

## NazimaDev hisobi bilan push qilish (bu loyiha)

Bu repo **NazimaDev** hisobiga ulanadi. Push qilganda **NazimaDev** login va uning **Personal Access Token** (parol o‘rnida) so‘raladi — **miraziz-Developer** emas.

```bash
cd /Users/mirazizerkinaliyev_dev/Desktop/Totembo-1
git add .
git commit -m "O'zgarishlar"
git push origin main
```
Parol so‘ralsa: NazimaDev ning GitHub tokenini kiriting.

---

## 1. GitHubda yangi repo yaratish

1. https://github.com ga kiring.
2. **New repository** (yoki **+** → New repository).
3. Repository name: masalan `totembo-shop`.
4. **Public** tanlang.
5. **Create repository** bosing (README, .gitignore qo‘shmasangiz ham bo‘ladi).

---

## 2. Loyihani GitHubga ulash va push qilish

Terminalda (Totembo-1 papkasida):

```bash
cd /Users/mirazizerkinaliyev_dev/Desktop/Totembo-1

# GitHubdagi repo manzilini o‘zingiznikiga almashtiring:
git remote add origin https://github.com/SIZNING_USERNAME/totembo-shop.git

# Asosiy branch nomi (agar GitHubda main bo‘lsa):
git branch -M main

# Yuklash:
git push -u origin main
```

**HTTPS** ishlatayotgan bo‘lsangiz, GitHub **username** va **password** (yoki Personal Access Token) so‘raydi.

---

## 3. Keyingi o‘zgarishlarni yuklash

Har safar kod o‘zgargach:

```bash
cd /Users/mirazizerkinaliyev_dev/Desktop/Totembo-1

git add .
git status
git commit -m "O'zgarishlar haqida qisqacha"
git push
```

---

## 4. SSH ishlatish (ixtiyari)

Agar SSH kalit qo‘ygan bo‘lsangiz:

```bash
git remote add origin git@github.com:SIZNING_USERNAME/totembo-shop.git
git push -u origin main
```

---

## Eslatma

- `.env` fayli Git ga **yuklanmaydi** (.gitignore da).
- Serverda loyihani clone qilgach, `shop/.env` ni qo‘lda yaratib, `shop/.env.example` dagi o‘zgaruvchilarni to‘ldiring.
