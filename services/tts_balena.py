import requests
from datetime import datetime

def balena_text_to_speech(text):
    output_file = f"balena_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
    
    # Membuat permintaan ke Balena TTS API
    url = f"https://tts.api.cloud.balena.io/tts?voice=id-ID&text={text}"
    response = requests.get(url)
    
    # Simpan file audio jika respons berhasil
    if response.status_code == 200:
        with open(output_file, 'wb') as f:
            f.write(response.content)
        print(f"Audio telah disimpan di: {output_file}")
        return output_file
    else:
        print("Gagal membuat TTS.")
        return None

