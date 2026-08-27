
import os
from dotenv import load_dotenv

from ai.job_analyzer import JobAnalyzer


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY tidak ditemukan."
    )


job_text = """
LOWONGAN PEKERJAAN

Posisi: Admin Toko

Nama usaha: Toko Makmur Jaya

Lokasi: Indonesia

Kami mencari Admin Toko untuk membantu operasional
administrasi harian.

Persyaratan:
- Minimal lulusan SMA/SMK
- Mampu menggunakan Microsoft Excel dan Microsoft Word
- Memiliki pengalaman administrasi minimal 1 tahun
- Mampu berkomunikasi dengan baik

Tanggung jawab:
- Menginput data penjualan
- Membuat laporan sederhana
- Mengelola dokumen
- Membantu pelayanan pelanggan

Jam kerja:
Senin-Sabtu, 08.00-16.00

Gaji:
Rp2.500.000 - Rp3.500.000 per bulan

Lokasi kerja:
On-site di Mojokerto
"""


analyzer = JobAnalyzer(api_key)

job_profile = analyzer.analyze(job_text)


print("\n========== JOB PROFILE ==========")

print("Job Title:", job_profile["job_title"])
print("Employer:", job_profile["employer"])
print("Location:", job_profile["location"])
print("Employment Type:", job_profile["employment_type"])

print("\nSalary:")
print("  Minimum:", job_profile["salary_range"]["min"])
print("  Maximum:", job_profile["salary_range"]["max"])
print("  Currency:", job_profile["salary_range"]["currency"])

print("\nRequirements:")

print(
    "  Education:",
    job_profile["requirements"]["education_level"]
)

print(
    "  Experience:",
    job_profile["requirements"]["experience_months"],
    "bulan"
)

print("  Skills:")

for skill in job_profile["requirements"]["skills"]:
    print("   -", skill)


print("\nResponsibilities:")

for responsibility in job_profile["responsibilities"]:
    print("  -", responsibility)


print("\nWork Preferences:")

print(
    "  Location Type:",
    job_profile["work_preferences"]["work_location_type"]
)

print(
    "  Working Hours:",
    job_profile["work_preferences"]["working_hours"]
)

print("\n================================")