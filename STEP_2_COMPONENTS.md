## Instruksi Coding UI
Buat halaman utama `app/page.tsx` dengan desain minimalis modern.

Fitur UI:
1. **Search Bar Besar:** Di tengah layar.
2. **Loading State:** Tampilkan Skeleton Loader saat backend memproses (karena Playwright butuh 5-10 detik).
3. **Result Card:**
   - Tampilkan Judul & Penulis.
   - Tampilkan BADGE JENJANG dengan kode warna spesifik Kemendikbud:
     - A: Merah (#FF0000)
     - B: Ungu (#800080)
     - C: Biru (#0000FF)
     - D: Hijau (#008000)
     - E: Kuning (#FFD700)
   - Tampilkan "Reasoning" dari AI di dalam card.