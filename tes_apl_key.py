import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ API Key tidak ditemukan di .env")
    exit()

print(f"✅ API Key ditemukan: {api_key[:10]}...")

try:
    client = genai.Client(api_key=api_key)
    
    # Ganti model ke gemini-3.6-flash
    response = client.models.generate_content(
        model="gemini-3.6-flash",  # <-- Model terbaru
        contents="Halo, sebutkan 3 keahlian utama Frontend Developer"
    )
    print("✅ API Key valid! Response:")
    print(response.text)
except Exception as e:
    print(f"❌ Error: {e}")