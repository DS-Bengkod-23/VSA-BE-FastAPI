from gtts import gTTS
from datetime import datetime
import random

def gtts_text_to_speech(text, name_file=None):
    # Tentukan bahasa Indonesia
    language = "id"

    rand_number = random.randint(0, 100000)
    rand_number_str = str(rand_number)

    # Menentukan nama file berdasarkan waktu
    if name_file:
        output_file = f"gtts_output_{name_file}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
    else:
        output_file = f"gtts_output_{rand_number_str + datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
    
    # Membuat audio dan menyimpannya
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save(output_file)
    
    print(f"Audio telah disimpan di: {output_file}")
    return output_file

