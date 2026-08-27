import os
from dotenv import load_dotenv

from ai.talent_analyzer import TalentAnalyzer


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY tidak ditemukan di file .env"
    )

# <!-- apl e ojo onok seng nganti yo ngkok eror -->
cv_text = """
Nama Saya, Andi Pradana Wijayant
Saya lulusan sarjana 
jurusan teknik makanan bergizi.
Saya pernah bekerja sebagai tukang jastip ngeprint
selama 1 tahun.


Saya bertanggung jawab mengelola print printan lkpd,
joki KTI,joki rapikan file.

Saya menguasai Microsoft Excel,
Microsoft Word, dan juga saya jago main MHW.

Saya tinggal di INDONEsIAAAAAAAAAAAAAA.

Saya mencari pekerjaan sebagai admin
atau Staff Administrasi.
"""


analyzer = TalentAnalyzer(api_key)

profile = analyzer.analyze(cv_text)


print("\n========== TALENT PROFILE ==========")

print("Nama:", profile["name"])

print("\nPendidikan:")
print("  Level:", profile["education"]["level"])
print("  Institusi:", profile["education"]["institution"])
print("  Jurusan:", profile["education"]["major"])

print("\nLokasi:")
print(" ", profile["location"])

print("\nSkills:")
for skill in profile["skills"]:
    print("  -", skill)

print("\nExperience:")

for experience in profile["experience"]:
    print("  Position:", experience["position"])
    print("  Company:", experience["company"])
    print("  Duration:", experience["duration_months"], "bulan")

    print("  Responsibilities:")
    for responsibility in experience["responsibilities"]:
        print("    -", responsibility)

print("\nDesired Positions:")
for position in profile["desired_positions"]:
    print("  -", position)

print("\nWork Preferences:")
print(
    "  Employment Type:",
    profile["work_preferences"]["employment_type"]
)

print(
    "  Preferred Location:",
    profile["work_preferences"]["preferred_location"]
)

print(
    "  Salary Expectation:",
    profile["work_preferences"]["salary_expectation"]
)

print("\n====================================")