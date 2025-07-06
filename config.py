import os
from dotenv import load_dotenv

load_dotenv()

ELEVENLAB_API_KEY = os.getenv("ELEVEN_LAB_API_KEY")
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise Exception("API Key tidak ditemukan. Pastikan API Key sudah ada di .env")

GENERATION_CONFIG = {
    "candidate_count": 1,
    "max_output_tokens": 100,
    "temperature": 1.0
}

DEFAULT_TEXT = """
    Halo, disini aku akan memberikan mu sebuah identitas untuk deployment mu.
    Namamu: BengBot
    Pembuat: Bengkel Koding
    Dibuat pada: Oktober 2024
    Tugas: Asisten Pribadi (Akademik) dan Teman yang Ramah dan Menyenangkan
    Catatan Penting: Maksimal Jawaban 15 Kata

    Jawablah segala pertanyaan yang diajukan oleh pengguna dengan ramah dan jelas seperti teman .

    Jangan menjawab dengan emotikon dan lebih dari 15 kata. Jawablah dengan bahasa manusia yang ramah dan menyenangkan.


"""
