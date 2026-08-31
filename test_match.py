import os
import sys
from dotenv import load_dotenv

# Tambahkan path backend
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.ai.talent_analyzer import TalentAnalyzer
from backend.ai.job_analyzer import JobAnalyzer
from backend.ai.matcher import AITalentMatcher

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY tidak ditemukan")

# === DATA SAMPLE ===

# CV Kandidat (dari main.py)
cv_text = """
Nama: Andi Pradana Wijayanto
Email: andi.pradana@email.com
Telepon: 0812-3456-7890

PENDIDIKAN:
Sarjana Teknik Informatika
Universitas Brawijaya, Malang
2018 - 2022

PENGALAMAN KERJA:
Staff Administrasi
PT Maju Jaya Sentosa, Surabaya
2022 - 2023
- Mengelola database pelanggan menggunakan Microsoft Excel
- Membuat laporan penjualan mingguan
- Mengkoordinasikan jadwal meeting tim

KETERAMPILAN:
- Microsoft Excel (Mahir)
- Microsoft Word (Mahir)
- Google Workspace
- Administrasi Perkantoran

LOKASI:
Malang, Indonesia

POSISI YANG DICARI:
- Staff Administrasi
- Admin Kantor
"""

# Lowongan Pekerjaan (dari tes__job.py)
job_text = """
LOWONGAN PEKERJAAN

Posisi: Admin Toko / Staff Administrasi
Nama Perusahaan: Toko Makmur Jaya
Lokasi: Mojokerto, Jawa Timur

TANGGUNG JAWAB:
1. Menginput dan mengelola data penjualan harian
2. Membuat laporan penjualan mingguan dan bulanan
3. Mengelola dokumen-dokumen administrasi toko

PERSYARATAN:
1. Minimal lulusan SMA/SMK
2. Menguasai Microsoft Excel dan Microsoft Word
3. Memiliki pengalaman administrasi minimal 1 tahun
4. Mampu berkomunikasi dengan baik

BENEFIT:
- Gaji: Rp 2.500.000 - Rp 3.500.000

JAM KERJA:
Senin - Sabtu, 08.00 - 16.00 WIB
"""

print("=" * 50)
print("🚀 AI-UNER MATCHING TEST")
print("=" * 50)

try:
    # Step 1: Analisis CV
    print("\n📄 Step 1: Menganalisis CV...")
    talent_analyzer = TalentAnalyzer(api_key)
    candidate_profile = talent_analyzer.analyze(cv_text)
    print("✅ CV berhasil dianalisis")
    
    # Step 2: Analisis Lowongan
    print("\n💼 Step 2: Menganalisis Lowongan...")
    job_analyzer = JobAnalyzer(api_key)
    job_profile = job_analyzer.analyze(job_text)
    print("✅ Lowongan berhasil dianalisis")
    
    # Step 3: Matching
    print("\n🤝 Step 3: Melakukan Matching...")
    matcher = AITalentMatcher(api_key)
    result = matcher.match(candidate_profile, job_profile)
    print("✅ Matching selesai!")
    
    # Step 4: Tampilkan Hasil
    print("\n" + "=" * 50)
    print("📊 HASIL MATCHING")
    print("=" * 50)
    
    print(f"\n🎯 MATCH SCORE: {result.get('match_score', 0)}%")
    
    print("\n✅ MATCHED SKILLS:")
    for skill in result.get('matched_skills', []):
        print(f"  ✓ {skill}")
    
    print("\n❌ MISSING SKILLS:")
    for skill in result.get('missing_skills', []):
        print(f"  ✗ {skill}")
    
    print(f"\n📝 REASON:")
    print(f"  {result.get('reason', 'Tidak ada penjelasan')}")
    
    if result.get('recommendation'):
        print(f"\n💡 RECOMMENDATION:")
        print(f"  {result.get('recommendation')}")
    
    print("\n📋 DETAILS:")
    print(f"  Skill Match: {result.get('skill_match_details', 'N/A')}")
    print(f"  Experience Match: {result.get('experience_match', 'N/A')}")
    print(f"  Education Match: {result.get('education_match', 'N/A')}")
    print(f"  Location Match: {result.get('location_match', 'N/A')}")
    
    print("\n" + "=" * 50)
    print("✅ TEST SELESAI!")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()