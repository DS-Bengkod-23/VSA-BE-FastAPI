import google.generativeai as genai
from config import API_KEY, GENERATION_CONFIG, DEFAULT_TEXT

genai.configure(api_key=API_KEY)

def generate_text_response(input_text: str) -> str:
    keywords = ["reservasi", "pinjam", "peminjaman", "pinjam ruangan", "meminjam", "pinjam ruangan", "peminjaman ruangan", "reservasi ruangan"]

    if any(keyword in input_text.lower() for keyword in keywords):
        return "Jika anda ingin memesan atau melakukan reservasi silahkan mengunjungi link berikut: https://bengkelkoding.com", "https://bengkelkoding.com"        


    model = genai.GenerativeModel("gemini-1.5-flash")
    chat = model.start_chat(
        history=[
            {"role": "user", "parts": [DEFAULT_TEXT]},
            {"role": "user", "parts": [input_text]},
        ]
    )
    response = chat.send_message(input_text, generation_config=GENERATION_CONFIG)
    return response.text, None
