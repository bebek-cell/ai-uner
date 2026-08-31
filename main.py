import os
import sys
from dotenv import load_dotenv

# Tambahkan path backend ke sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Ini penting: import dari backend
from backend.ai.talent_analyzer import TalentAnalyzer

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY tidak ditemukan di file .env")

# CV Text
cv_text = """
Nama: Andi Pradana Wijayanto
Email: andi.pradana@email.com
Telepon: 0812-3456-7890

PENDIDIKAN:
Sarjana Teknik Informatika
Universitas Brawijaya, Malang
2018 - 2022
IPK: 3.75/4.00

PENGALAMAN KERJA:
Staff Administrasi
PT Maju Jaya Sentosa, Surabaya
2022 - 2023
- Mengelola database pelanggan menggunakan Microsoft Excel
- Membuat laporan penjualan mingguan
- Mengkoordinasikan jadwal meeting tim

Asisten Administrasi (Magang)
Dinas Pendidikan Kota Malang
2021 - 2022
- Mengarsipkan dokumen penting
- Membantu pengelolaan surat masuk dan keluar

KETERAMPILAN:
- Microsoft Excel (Mahir)
- Microsoft Word (Mahir)
- Google Workspace
- Administrasi Perkantoran
- Manajemen Database

LOKASI:
Malang, Indonesia

POSISI YANG DICARI:
- Staff Administrasi
- Admin Kantor
- Data Entry Specialist

PREFERENSI KERJA:
- Full-time
- On-site atau Hybrid
- Gaji: Rp 3.500.000 - Rp 5.000.000
"""

try:
    # Inisialisasi analyzer
    analyzer = TalentAnalyzer(api_key)
    
    # Analisis CV
    print("⏳ Menganalisis CV dengan AI...")
    profile = analyzer.analyze(cv_text)
    
    print("\n========== TALENT PROFILE ==========")
    print(f"Nama: {profile.get('name', 'Tidak tersedia')}")
    
    education = profile.get("education", {})
    print("\nPendidikan:")
    print(f"  Level: {education.get('level', 'Tidak tersedia')}")
    print(f"  Institusi: {education.get('institution', 'Tidak tersedia')}")
    print(f"  Jurusan: {education.get('major', 'Tidak tersedia')}")
    
    print(f"\nLokasi: {profile.get('location', 'Tidak tersedia')}")
    
    skills = profile.get("skills", [])
    print("\nSkills:")
    if skills:
        for skill in skills:
            print(f"  - {skill}")
    else:
        print("  (Tidak ada skill yang terdeteksi)")
    
    experiences = profile.get("experience", [])
    print("\nExperience:")
    if experiences:
        for exp in experiences:
            print(f"  Position: {exp.get('position', 'Tidak tersedia')}")
            print(f"  Company: {exp.get('company', 'Tidak tersedia')}")
            print(f"  Duration: {exp.get('duration_months', 0)} bulan")
            responsibilities = exp.get("responsibilities", [])
            print("  Responsibilities:")
            for resp in responsibilities:
                print(f"    - {resp}")
    else:
        print("  (Tidak ada pengalaman yang terdeteksi)")
    
    desired_positions = profile.get("desired_positions", [])
    print("\nDesired Positions:")
    if desired_positions:
        for pos in desired_positions:
            print(f"  - {pos}")
    else:
        print("  (Tidak ada posisi yang diinginkan)")
    
    work_prefs = profile.get("work_preferences", {})
    print("\nWork Preferences:")
    print(f"  Employment Type: {work_prefs.get('employment_type', 'Tidak tersedia')}")
    print(f"  Preferred Location: {work_prefs.get('preferred_location', 'Tidak tersedia')}")
    print(f"  Salary Expectation: {work_prefs.get('salary_expectation', 'Tidak tersedia')}")
    
    print("\n====================================")
    print("✅ Analisis selesai!")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()