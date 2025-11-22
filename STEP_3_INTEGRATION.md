## Instruksi Integrasi API
Di `app/page.tsx`:
Buat fungsi `handleSearch`:
1. Set state `isLoading = true`.
2. Panggil `axios.post('http://localhost:8000/analyze', {title: query})`.
3. Tangkap response data.
4. Tampilkan data ke Result Card.
5. Handle error: Jika API gagal, tampilkan Alert Shadcn "Gagal menganalisis buku".