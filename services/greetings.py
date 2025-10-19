def generate_greeting(results):
    greetings = []

    # Looping setiap hasil deteksi wajah
    for result in results:
        name = result.get("name").split(" - ")[0]
        first_name = name.split(" ")[0]

        emotion = result.get("emotion")

        # Menentukan sapaan berdasarkan emosi
        if emotion == "happy":
            greeting = f"halo Dinusian, sepertinya hari ini sedang bahagia ya, apakah ada yang bisa saya bantu?"
        elif emotion == "sad":
            greeting = f"halo Dinusian, mengapa wajahmu terlihat sedih, coba sini ceritakan padaku"
        elif emotion == "angry":
            greeting = f"halo Dinusian, mengapa wajahmu terlihat marah, tenang dulu ya"
        elif emotion == "surprise":
            greeting = f"halo Dinusian, wah ada suprise apa hari ini? ada yang bisa saya bantu?"
        else:
            greeting = f"halo Dinusian, saya bengbot, asisten pribadi anda. Ada yang bisa saya bantu?"

        # Menambahkan sapaan ke daftar
        greetings.append(greeting)

    # Menggabungkan semua sapaan menjadi satu teks
    return ", ".join(greetings)


# def generate_greeting(results):
#     greetings = []

#     if results:
#         name = results[0].get("name").split(" - ")[0]

#         # Mengambil nama lengkap dari hasil
# full_name = results[0].get("name")

# # Memisahkan nama berdasarkan spasi dan mengambil nama pertama
# first_name = full_name.split(" ")[0]
#         emotion = results[0].get("emotion")

#         if emotion == "happy":
#             greeting = f"halo {name}, sepertinya hari ini cerah sekali ya, semoga harimu selalu menyenangkan"
#         elif emotion == "sad":
#             greeting = f"halo {name}, mengapa wajahmu terlihat sedih, senyum dong"
#         elif emotion == "angry":
#             greeting = f"halo {name}, mengapa wajahmu terlihat murung, senyum dong"
#         elif emotion == "surprise":
#             greeting = f"halo {name}, ada kabar apa hari ini"
#         else:
#             greeting = f"halo {name}, saya bengbot, asisten pribadi anda. Ada yang bisa saya bantu?"

#         greetings.append(greeting)

#     return " ".join(greetings)
