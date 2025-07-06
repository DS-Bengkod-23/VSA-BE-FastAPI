import requests
import datetime
from config import ELEVENLAB_API_KEY

def generate_speech(text):
    CHUNK_SIZE = 1024
    url = "https://api.elevenlabs.io/v1/text-to-speech/8EkOjt4xTPGMclNlh1pk"  # Ganti <voice-id> dengan ID yang sesuai

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLAB_API_KEY  
    }

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.8,
            "similarity_boost": 0.5,
            "style" : 0.4
        }
    }

    response = requests.post(url, json=data, headers=headers)

    # Mendapatkan timestamp untuk membuat nama file unik
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f'output_{timestamp}.mp3'

    if response.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
        return filename
    else:
        raise Exception(f"Gagal mendapatkan audio: {response.status_code} {response.text}")
