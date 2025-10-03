from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from models.schemas import TextRequest,ApiResponse  
from services.text_g import create_message, load_markdown_files
from services.face_r import detect_faces
from utils.helpers import create_response, audio_to_base64
from services.greetings import generate_greeting
from services.tts_edge import run_edge_tts
import re
import os
import time
import logging


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/load-markdown", response_model=dict)
async def load_markdown_files_endpoint():
    return await load_markdown_files()

@app.post("/generate",response_model=ApiResponse)
async def generate_text(request: TextRequest):
    input_text = request.text
    if not input_text:  
        intro = audio_to_base64("audio/introduction.mp3")
        return create_response(
            status="success",
            code=200,
            message="Request successful",
            data={
                "response" : "Hey dear... How was your day?",
                "audio" :  intro
            }
        )

    try:
        response = await create_message(input_text)
        response_text = response.get("response", "")
        link = response.get("link", None)
        # clean_text = re.sub(r'[^\w\s]', '', response_text)
        clean_text = re.sub(r'\n', '', response_text)
        # audio = generate_speech(clean_text)
        # audio = await run_edge_tts(clean_text)     

        # pakai edge tts
        audio = await run_edge_tts(clean_text, "audio")     
        # audio = generate_speech(clean_text)

        # pakai google tts
        # audio = gtts_text_to_speech(clean_text)

        # pakai balena tts
        # audio = balena_text_to_speech(clean_text)

        # audio_base64 = audio_to_base64(audio)
        audio_base64 = audio_to_base64(audio)
        os.remove(audio)
        if link:
            return create_response(
                status="success",
                code=200,
                message="Request successful",
                data={"response" : clean_text , "link" : link, "audio" :audio_base64}
            )
        else:
            return create_response(
                status="success",
                code=200,
                message="Request successful",
                data={"response" : clean_text, "audio" : audio_base64}
            )   
    except Exception as e:
        return create_response(
            status="error",
            code=500,
            message=str(e),
            data={}
        )


@app.post("/generate_audio",response_model=ApiResponse)
async def generate_audio(request: TextRequest):
    input_text = request.text
    if not input_text:
        return create_response(
            status="error",
            code=400,
            message="No text provided",
            data={}
        )

    try:
        # response_text, link = generate_text_response(input_text)
        # clean_text = re.sub(r'\n', '', response_text)
        audio = await run_edge_tts(input_text, "generate_audio")
        # audio = gtts_text_to_speech(input_text)
        # audio =  generate_speech(input_text)
        audio_base64 = audio_to_base64(audio)
        os.remove(audio)

        return create_response(
            status="success",
            code=200,
            message="Request successful",
            data={"response": input_text, "audio": audio_base64}
        )
      
    except Exception as e:
        return create_response(
            status="error",
            code=500,
            message=str(e),
            data={}
        )
    
@app.post("/detect/", response_model=ApiResponse)
async def detect_face(file: UploadFile = File(...)):
    try:
        if not file:
            raise ValueError("No file uploaded")

        # Mulai pengukuran waktu untuk `detect_faces`
        start_detect_faces = time.monotonic()
        result = await detect_faces(file)
        detect_faces_duration = time.monotonic() - start_detect_faces
        
        if result:
            # Mulai pengukuran waktu untuk `generate_greeting`
            start_generate_greeting = time.monotonic()
            greeting = generate_greeting(result)
            generate_greeting_duration = time.monotonic() - start_generate_greeting
            
            # Mulai pengukuran waktu untuk `run_edge_tts`
            start_run_edge_tts = time.monotonic()
            audio = await run_edge_tts(greeting, "detect")
            run_edge_tts_duration = time.monotonic() - start_run_edge_tts
            
            audio_base64 = audio_to_base64(audio)
            os.remove(audio)

        # Logging durasi waktu masing-masing fungsi
        logging.info(f"detect_faces duration: {detect_faces_duration:.2f} seconds")
        logging.info(f"generate_greeting duration: {generate_greeting_duration:.2f} seconds")
        logging.info(f"run_edge_tts duration: {run_edge_tts_duration:.2f} seconds")

        return create_response(
            status="success",
            code=200,
            message="Face detection successful",
            data={
                "results": result, 
                "response": greeting,
                "audio": audio_base64
            }
        )
    except ValueError as ve:
        logging.error(f"ValueError: {ve}")
        return create_response(
            status="error",
            code=400,
            message=str(ve),
            data={}
        )
    except Exception as e:
        logging.error(f"Unexpected error during face detection: {e}")
        return create_response(
            status="error",
            code=500,
            message="Error in face detection",
            data={}
        )


# @app.post("/detect/", response_model=ApiResponse)
# async def detect_face(file: UploadFile = File(...)):
#     try:
#         if not file:
#             raise ValueError("No file uploaded")

#         result = await detect_faces(file)
#         if result :
#             greeting = generate_greeting(result)
#             audio = await run_edge_tts(greeting)     
#             audio_base64 = audio_to_base64(audio)
#             os.remove(audio)

#         return create_response(
#             status="success",
#             code=200,
#             message="Face detection successful",
#             # data={"results": result, "audio": audio_base64, "response": greeting}
#             data={"results": result,  "response": greeting}
#         )
#     except ValueError as ve:
#         logging.error(f"ValueError: {ve}")
#         return create_response(
#             status="error",
#             code=400,
#             message=str(ve),
#             data={}
#         )
#     except Exception as e:
#         logging.error(f"Unexpected error during face detection: {e}")
#         return create_response(
#             status="error",
#             code=500,
#             message="Error in face detection",
#             data={}
#         )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8085)


# const voiceId = "8EkOjt4xTPGMclNlh1pk"; // Replace with the desired voice ID
#   const voiceSettings = {
#     stability: 0.8,
#     similarity_boost: 0.6,
#     style: 0.4,
#   };