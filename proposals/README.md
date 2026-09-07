# عروض الأسعار (Proposals)

**المرجع الأساسي للعروض هو Google Drive:** مجلد `Offers/<اسم العميل>` (مثال: `Offers/ashraffarag` لحدائق اللوتس — المالك شركة أشرف فرج). هذا المجلد في الريبو نسخة للمصدر والتعديل فقط.

كل عرض في مجلد باسم العميل والتاريخ، ويحتوي `index.html` (المصدر) و PDF بنفس رقم العرض.

## النشر على offers.vadecom.net
- الأصل (origin): سيرفر Hetzner `root@178.156.203.42` — nginx site `/etc/nginx/sites-available/offers.vadecom.net`، الملفات في `/var/www/offers/<slug>/index.html`. الجذر `/` يرد 404 والفهرسة مغلقة و`X-Robots-Tag: noindex`.
- DNS: `offers` على Cloudflare (zone vadecom.net) يجب أن يشير إلى 178.156.203.42. الشهادة: `certbot --nginx -d offers.vadecom.net`.
- الرفع: `scp index.html root@178.156.203.42:/var/www/offers/<slug>/index.html`

## توليد PDF من الصفحة (من WSL عبر Chrome على ويندوز)
```bash
cp index.html /mnt/c/Windows/Temp/aspace-pdf/offer.html
"/mnt/c/Program Files/Google/Chrome/Application/chrome.exe" --headless=new --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="C:\Windows\Temp\aspace-pdf\offer.pdf" --virtual-time-budget=10000 "file:///C:/Windows/Temp/aspace-pdf/offer.html"
```
الصفحة تحتوي CSS للطباعة (غلاف A4 + فواصل صفحات) فالـ PDF يخرج جاهزاً.

| العرض | العميل | الرابط | الحالة |
|-------|--------|--------|--------|
| VC-2026-0907-01 | حدائق اللوتس — Lotus Gardens | https://offers.vadecom.net/lotus-gardens-9f3c/ | بانتظار سجل DNS + شهادة |
