import os
from dotenv import load_dotenv
from backend.ai.job_analyzer import JobAnalyzer

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY tidak ditemukan di file .env")

job_text = """
LOWONGAN PEKERJAAN

Posisi: Admin Toko / Staff Administrasi
Nama Perusahaan: Toko Makmur Jaya
Industri: Retail / Perdagangan
Lokasi: Mojokerto, Jawa Timur

DESKRIPSI PEKERJAAN:
Kami adalah toko retail yang bergerak di bidang penjualan perlengkapan rumah tangga dan 
kebutuhan sehari-hari. Saat ini kami membuka lowongan untuk posisi Admin Toko yang akan 
membantu operasional administrasi harian toko.

TANGGUNG JAWAB:
1. Menginput dan mengelola data penjualan harian ke dalam sistem
2. Membuat laporan penjualan mingguan dan bulanan
3. Mengelola dokumen-dokumen administrasi toko
4. Membantu pelayanan pelanggan di kasir
5. Melakukan stock opname barang secara berkala
6. Membantu koordinasi dengan supplier

PERSYARATAN:
1. Minimal lulusan SMA/SMK (semua jurusan)
2. Menguasai Microsoft Excel dan Microsoft Word (minimal dasar)
3. Memiliki pengalaman administrasi minimal 1 tahun (fresh graduate dipersilakan)
4. Mampu berkomunikasi dengan baik dan ramah
5. Teliti, jujur, dan bertanggung jawab
6. Bersedia bekerja on-site
7. Diutamakan berdomisili di Mojokerto atau sekitarnya

BENEFIT:
- Gaji pokok: Rp 2.500.000 - Rp 3.500.000
- Tunjangan makan
- Tunjangan transportasi
- BPJS Kesehatan & Ketenagakerjaan

JAM KERJA:
Senin - Sabtu, 08.00 - 16.00 WIB
Istirahat: 12.00 - 13.00 WIB

TIPE PEKERJAAN:
Full-time, On-site
"""

try:
    analyzer = JobAnalyzer(api_key)
    job_profile = analyzer.analyze(job_text)
    
    print("\n========== JOB PROFILE ==========")
    print(f"Job Title: {job_profile.get('job_title', 'Tidak tersedia')}")
    print(f"Employer: {job_profile.get('employer', 'Tidak tersedia')}")
    print(f"Location: {job_profile.get('location', 'Tidak tersedia')}")
    print(f"Employment Type: {job_profile.get('employment_type', 'Tidak tersedia')}")
    
    salary = job_profile.get("salary_range", {})
    print("\nSalary:")
    print(f"  Minimum: Rp {salary.get('min', 'Tidak tersedia')}")
    print(f"  Maximum: Rp {salary.get('max', 'Tidak tersedia')}")
    print(f"  Currency: {salary.get('currency', 'Tidak tersedia')}")
    
    requirements = job_profile.get("requirements", {})
    print("\nRequirements:")
    print(f"  Education: {requirements.get('education_level', 'Tidak tersedia')}")
    print(f"  Experience: {requirements.get('experience_months', 0)} bulan")
    
    skills = requirements.get("skills", [])
    print("  Skills:")
    for skill in skills:
        print(f"   - {skill}")
    
    responsibilities = job_profile.get("responsibilities", [])
    print("\nResponsibilities:")
    for resp in responsibilities:
        print(f"  - {resp}")
    
    work_prefs = job_profile.get("work_preferences", {})
    print("\nWork Preferences:")
    print(f"  Location Type: {work_prefs.get('work_location_type', 'Tidak tersedia')}")
    print(f"  Working Hours: {work_prefs.get('working_hours', 'Tidak tersedia')}")
    
    print("\n================================")

except Exception as e:
    print(f"Error: {e}")