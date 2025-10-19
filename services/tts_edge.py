import edge_tts
import asyncio
from datetime import datetime
import ssl
import certifi
from services.tts_google import gtts_text_to_speech

# Fungsi untuk melakukan TTS dalam bahasa Indonesia dengan nama file berdasarkan tanggal saat ini
async def text_to_speech(text, name_file, disable_ssl_verification=False):
    # Atur suara yang diinginkan (contoh: ArdiNeural untuk Bahasa Indonesia)
    voice = "id-ID-GadisNeural"  # Anda bisa mencoba "id-ID-AndikaNeural" juga
    
    # Menghasilkan nama file berdasarkan tanggal dan waktu saat ini
    output_file = f"output_{name_file}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
    
    try:
        # Konfigurasikan edge-tts dan buat output audio
        if disable_ssl_verification:
            # Set SSL context to ignore verification
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            communicate = edge_tts.Communicate(text, voice, ssl_context=ssl_context)
        else:
            # Use default SSL verification with certifi certificates
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            communicate = edge_tts.Communicate(text, voice, ssl_context=ssl_context)
            
        await communicate.save(output_file)
        print(f"Audio telah disimpan di: {output_file}")
        return output_file
    except Exception as e:
        print(f"Error with Edge TTS: {str(e)}")
        # Fallback to Google TTS if Edge TTS fails
        print("Falling back to Google TTS")
        return gtts_text_to_speech(text, name_file)

# Fungsi untuk menjalankan text_to_speech dan mengembalikan nama file
async def run_edge_tts(text, name_file):
    try:
        # First try with normal SSL verification
        return await text_to_speech(text, name_file)
    except Exception as e:
        print(f"Edge TTS failed with normal SSL settings: {str(e)}")
        # Try again with SSL verification disabled
        return await text_to_speech(text, name_file, disable_ssl_verification=True)

# Untuk menjalankan asinkron
# asyncio.run(run_edge_tts("Teks yang ingin Anda konversi menjadi suara"))
