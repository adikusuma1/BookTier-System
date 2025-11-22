from pydantic import BaseModel
from typing import List, Optional

# Input dari Frontend
class BookRequest(BaseModel):
    title: str

# --- FORMULIR HASIL AI ---
# Ini format jawaban yang akan diisi oleh Gemini
class AIAnalysis(BaseModel):
    jenjang: str           # Contoh: "Jenjang B1"
    confidence_score: int  # Contoh: 85
    alasan: str            # Penjelasan teknis (Visual/Teks)
    saran: str             # Saran Scaffolding
    badge_color: str       # Warna Badge (MERAH, UNGU, dll)

# Output Akhir ke Frontend
class BookResult(BaseModel):
    title: str
    authors: List[str]
    page_count: Optional[int]
    categories: List[str]
    screenshots: List[str]
    analysis: Optional[AIAnalysis] = None # Bisa kosong jika AI gagal