# 📂 TAHAPAN 1: BACKEND & DATA ENGINE

Target Gol: Memiliki API Server yang berjalan di localhost, bisa menerima judul buku, mencari metadata dari Google Books, dan mengambil bukti visual (screenshot) halaman buku tersebut secara otomatis.

🛠️ Tools & Stack yang Digunakan:
- Python 3.10+: Bahasa pemrograman utama.
- FastAPI: Framework server (API) yang sangat cepat dan modern.
- Uvicorn: Server ASGI untuk menjalankan FastAPI.
- Playwright: Library otomasi browser (pengganti Selenium) yang lebih tangguh untuk website modern (React/Angular) seperti Google Books.
- Requests: Library sederhana untuk memanggil API Google Books.
- Base64: Format encoding gambar agar bisa dikirim lewat JSON tanpa menyimpan file fisik.

## 📝 LANGKAH 1: Struktur Folder & Environment
Kita mulai dengan membuat "rumah" yang bersih untuk kode kita.

Instruksi Teknis:

- [x] Buat folder root proyek: book-classifier.
- [ ] Masuk ke dalamnya dan buat folder backend.
- [x] Di dalam backend, kita butuh struktur modular agar rapi.

Struktur File yang Akan Kita Buat:

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Pintu masuk server API
│   ├── models.py            # Schema data (Validasi input/output)
│   └── services/            # Logika bisnis
│       ├── __init__.py
│       ├── google_books.py  # Script pencari metadata
│       └── scraper.py       # Script pengambil screenshot
├── .env                     # File rahasia (API Key)
├── .gitignore               # Daftar file yang diabaikan git
└── requirements.txt         # Daftar library
```

🚀 Action (Terminal):

```bash
# Buat folder
mkdir backend
cd backend

# Setup Virtual Environment (Wajib untuk Python)
python -m venv venv

# Aktifkan Venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

## 📝 LANGKAH 2: Instalasi Dependensi (Library)
Kita perlu menginstal alat-alat tukang yang disebutkan di atas.

- [x] Buat file requirements.txt di dalam folder backend dengan isi sebagai berikut:

```
fastapi==0.109.0
uvicorn==0.27.0
requests==2.31.0
playwright==1.41.0
python-dotenv==1.0.1
pydantic==2.6.0
```

🚀 Action (Terminal): Jalankan perintah ini untuk menginstal semua alat sekaligus:

```bash
pip install -r requirements.txt
```

⚠️ Langkah Kritis (Jangan Lewatkan): Playwright membutuhkan browser khusus agar bisa berjalan tanpa kepala (headless).

```bash
playwright install chromium
```

Tanpa perintah di atas, scraper Anda akan error.

## 📝 LANGKAH 3: Service 1 - Google Books Metadata
Sekarang kita buat script untuk mengambil data teks (Judul, Halaman, Kategori).

Lokasi File: app/services/google_books.py

Logika Program:

- [ ] Menerima input string query (Judul Buku).
- [ ] Mengirim request ke API publik https://www.googleapis.com/books/v1/volumes.
- [ ] Mengambil hasil paling atas (indeks 0).
- [ ] Mengekstrak data penting: title, authors, pageCount, categories, dan previewLink.
- [ ] Mengembalikan data bersih dalam bentuk Dictionary.

Prompt untuk AI Coding (Vibe Coding):

"Buatkan fungsi Python di app/services/google_books.py bernama search_book_metadata(query: str). Gunakan library requests. Lakukan GET request ke https://www.googleapis.com/books/v1/volumes?q={query}. Ambil item pertama dari hasil pencarian. Return dictionary berisi: title, authors (list), page_count (int), categories (list), preview_link (str), dan thumbnail (url). Handle error jika buku tidak ditemukan (return None)."

## 📝 LANGKAH 4: Service 2 - Playwright Scraper (Visual Engine)
Ini bagian paling rumit tapi keren. Kita akan menyuruh robot membuka browser diam-diam.

Lokasi File: app/services/scraper.py

Logika Program:

- [ ] Menerima preview_link dari Google Books.
- [ ] Membuka browser Chromium secara headless (tidak muncul di layar).
- [ ] Pergi ke link tersebut.
- [ ] Tunggu loading: Google Books menggunakan canvas/JavaScript, jadi kita harus menunggu elemen #viewport atau .pageImage muncul.
- [ ] Sampling: Kita tidak butuh cover saja. Kita butuh isi.
- [ ] Scroll sedikit ke bawah.
- [ ] Ambil screenshot layar saat ini.
- [ ] Encoding: Ubah gambar screenshot menjadi format Base64 string (agar bisa dikirim lewat API JSON tanpa save file jpg).

Prompt untuk AI Coding (Vibe Coding):

"Buatkan fungsi Async Python di app/services/scraper.py bernama capture_book_preview(url: str). Gunakan async_playwright. Flow:

Launch browser chromium (headless=True).

Buat context dan page baru.

Goto url dengan wait_until='networkidle'.

Tunggu selector canvas atau gambar buku muncul (timeout 10 detik).

Ambil screenshot halaman tersebut.

Encode hasil screenshot ke base64 string utf-8.

Tutup browser.

Return list berisi string base64 tersebut. Tambahkan try-except block. Jika gagal/timeout, return list kosong."

## 📝 LANGKAH 5: Schema Data (Pydantic Models)
Agar data yang keluar masuk API rapi dan valid.

Lokasi File: app/models.py

- [ ] Buatkan Pydantic Models di app/models.py:

BookRequest: Menerima title (str).

BookData: Output berisi title, authors, page_count, categories, screenshots (list of str).

## 📝 LANGKAH 6: Menyatukan di API Server (Main App)
Menghubungkan semua komponen di atas menjadi satu pintu gerbang API.

Lokasi File: app/main.py

Logika Program:

- [ ] Inisialisasi FastAPI.
- [ ] Setup CORS Middleware (Sangat penting agar Frontend Next.js nanti bisa mengakses API ini tanpa diblokir browser).
- [ ] Buat endpoint POST /api/search.
- [ ] Di dalam endpoint:

  - Panggil search_book_metadata.
  - Jika buku ada, panggil capture_book_preview menggunakan URL preview dari metadata.
  - Gabungkan hasilnya dan return JSON.

Prompt untuk AI Coding:

"Buatkan file app/main.py. Setup FastAPI app dengan CORS middleware (allow origins *). Import fungsi dari services.google_books dan services.scraper. Buat endpoint POST /api/search yang menerima BookRequest. Flow endpoint:

Cari metadata buku. Jika None, raise HTTPException 404.

Jalankan scraper capture_book_preview dengan preview_link dari metadata.

Return JSON gabungan metadata dan screenshots. Gunakan async def untuk endpoint."

## 📝 LANGKAH 7: Uji Coba (Debugging)
Sebelum lanjut ke AI atau Frontend, kita harus pastikan "mesin" ini jalan.

Cara Menjalankan Server: Di terminal backend/:

```bash
uvicorn app.main:app --reload
```

(Flag --reload artinya server akan restart otomatis kalau kita ubah kode).

Cara Testing (Tanpa Frontend):

- [ ] Buka browser ke alamat: http://127.0.0.1:8000/docs
- [ ] Ini adalah Swagger UI, fitur bawaan FastAPI untuk test API.
- [ ] Cari endpoint POST /api/search.
- [ ] Klik Try it out.
- [ ] Isi Request Body:

```json
{
  "title": "Laskar Pelangi"
}
```

- [ ] Klik Execute.

Indikator Sukses (Checklist):

- [ ] Server merespons code 200 OK.
- [ ] Response Body berisi JSON dengan data:

  - title: "Laskar Pelangi"
  - page_count: Sekian ratus halaman.
  - screenshots: String panjang acak (ini adalah base64 gambar).

- [ ] Terminal backend tidak menunjukkan error merah.

💡 Tips Debugging untuk Tahap Ini
- Playwright Timeout: Jika internet lambat, scraper mungkin gagal loading Google Books dalam 10 detik. Anda bisa naikkan timeout di script scraper menjadi 30000ms (30 detik).
- Google Books API Rate Limit: Jika terlalu sering request, Google mungkin memblokir sementara. Untuk tahap development, ini jarang terjadi, tapi jika terjadi, tunggu beberapa menit.
- No Preview Available: Coba cari buku yang pasti ada previewnya dulu (misal: buku-buku populer luar negeri atau buku klasik) untuk memastikan kode scraper jalan.

Jika Tahap 1 ini sudah centang hijau semua, berarti Anda sudah punya "Mata" (Scraper) dan "Tangan" (API) untuk sistem Anda. Kita siap lanjut memasang "Otak" (AI) di Tahap 2.