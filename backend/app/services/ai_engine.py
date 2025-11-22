import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from app.models import AIAnalysis

# Load Environment Variables
load_dotenv()

async def analyze_book_with_ai(metadata: dict, screenshot_base64: str) -> AIAnalysis:
    # 1. Setup Model Gemini (GUNAKAN VERSI 2.0 FLASH YANG ADA DI LIST ANDA)
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY tidak ditemukan di .env")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash", # <--- KITA UPDATE KE VERSI INI
        temperature=0.0, 
        max_retries=2,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    # 2. SYSTEM PROMPT (Aturan PDF Kemendikbud SK 030/P/2022)
    system_prompt = """
    PERAN: Anda adalah Auditor Ahli Perjenjangan Buku Kemendikbud (SK 030/P/2022).
    TUGAS: Analisis metadata buku dan screenshot halaman untuk menentukan 'Jenjang Pembaca'.

    PEDOMAN KLASIFIKASI (STRICT RULES):
    
    1. JENJANG A (Pembaca Dini) -> Simbol: MERAH
       - Target: PAUD (0-7 thn).
       - Fisik: 8-24 halaman.
       - Teks: Sedikit sekali (Maksimal 5 kata/kalimat). Kalimat tunggal.
       - Visual: Gambar SANGAT DOMINAN (memenuhi halaman). Tanpa balon kata.
       
    2. JENJANG B (Pembaca Awal) -> Simbol: UNGU
       - Target: SD Kelas 1-3 (6-10 thn).
       - B1: 16-32 hal, Maks 7 kata/kalimat. Gambar dominan.
       - B2: 24-48 hal, Maks 9 kata/kalimat. 
       - B3: 32-48 hal, Maks 12 kata/kalimat. Mulai ada paragraf pendek.
       - Visual: Gambar masih dominan, tapi teks mulai bertambah.
       
    3. JENJANG C (Pembaca Semenjana) -> Simbol: BIRU
       - Target: SD Kelas 4-6 (10-12 thn).
       - Teks: Sudah berupa paragraf narasi/deskripsi penuh.
       - Visual: Proporsi gambar seimbang atau lebih kecil dari teks.
       - Fitur: Boleh menggunakan balon kata (Komik).
       
    4. JENJANG D (Pembaca Madya) -> Simbol: HIJAU
       - Target: SMP (13-15 thn).
       - Teks: Kompleks, kalimat majemuk bertingkat.

    5. JENJANG E (Pembaca Mahir) -> Simbol: KUNING
       - Target: SMA+ (16+ thn).
       - Teks: Sangat kompleks, analitis, kritis.
       - Kosakata: Banyak istilah teknis/asing/akademik.
       - Struktur: Paragraf Deduktif/Induktif variatif.

    FORMAT OUTPUT (WAJIB JSON):
    Kembalikan HANYA JSON valid dengan format ini:
    {
        "jenjang": "Jenjang X",
        "confidence_score": 0-100,
        "alasan": "Jelaskan alasan berdasarkan bukti visual (proporsi gambar) dan bukti teks (jumlah kata/halaman).",
        "saran": "Saran pendampingan (Perlu Perancah / Mandiri).",
        "badge_color": "WARNA (MERAH/UNGU/BIRU/HIJAU/KUNING)"
    }
    """

    # 3. Menyusun Pesan untuk AI
    metadata_info = f"""
    Data Buku:
    - Judul: {metadata['title']}
    - Jumlah Halaman: {metadata.get('page_count', 'Tidak diketahui')}
    - Kategori: {metadata.get('categories', [])}
    """

    # Logic: Jika screenshot kosong (gagal scrap), kirim teks saja. Jika ada, kirim gambar.
    content_message = [
        {"type": "text", "text": system_prompt},
        {"type": "text", "text": metadata_info}
    ]

    if screenshot_base64:
        content_message.append({
            "type": "image_url", 
            "image_url": {"url": f"data:image/png;base64,{screenshot_base64}"}
        })
    else:
        content_message.append({"type": "text", "text": "[PERINGATAN: Screenshot tidak tersedia. Analisis hanya berdasarkan Metadata.]"})

    message = HumanMessage(content=content_message)

    # 4. Eksekusi AI
    try:
        # print("🤖 AI: Sedang menganalisis...") 
        response = await llm.ainvoke([message])
        
        clean_content = response.content.replace("```json", "").replace("```", "").strip()
        result_json = json.loads(clean_content)
        
        return AIAnalysis(**result_json)
        
    except Exception as e:
        print(f"❌ Error AI: {e}")
        return AIAnalysis(
            jenjang="Tidak Teridentifikasi",
            confidence_score=0,
            alasan=f"Gagal analisis AI: {str(e)}",
            saran="-",
            badge_color="ABU"
        )