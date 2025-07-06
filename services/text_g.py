import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import requests

# LangChain Imports
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config import API_KEY, GENERATION_CONFIG, DEFAULT_TEXT



# Load .env
load_dotenv()

# Init FastAPI
app = FastAPI()

# Inisialisasi Embedding
def get_google_embedding():
    api_key = API_KEY
    if not api_key:
        raise ValueError("GOOGLE_API_KEY tidak ditemukan di .env")
    return GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)

# Inisialisasi Chroma Vector Store
def get_chroma_vector_store():
    embedding = get_google_embedding()
    return Chroma(persist_directory="database/chroma", embedding_function=embedding)

chroma_vectors = get_chroma_vector_store()



async def create_message(text_input):
    try:
        input_text = text_input

        # Ambil dokumen relevan dari Chroma
        retriever = chroma_vectors.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 5, "lambda_mult": 0.7}
        )
        relevant_docs = retriever.get_relevant_documents(input_text)
        context = "\n".join([doc.page_content for doc in relevant_docs])

        system_message = f"""
        Halo, disini aku akan memberikan mu sebuah identitas untuk deployment mu.
        Namamu: BengBot
        Pembuat: Bengkel Koding
        Dibuat pada: Oktober 2024
        Tugas: Asisten Pribadi (Akademik) dan Teman yang Ramah dan Menyenangkan
        Catatan Penting: Maksimal Jawaban 15 Kata

        Jawablah segala pertanyaan yang diajukan oleh pengguna dengan ramah dan jelas seperti teman .

        Jangan menjawab dengan emoji dan lebih dari 15 kata. Jawablah dengan bahasa manusia yang ramah dan menyenangkan.
        Berikut informasi relevan:

        {context}

        Jawablah pertanyaan mahasiswa berikut secara padat, jelas, dan ramah.
        Jika tidak ada informasi relevan, jawab dengan informasi umum dari internet.
        """

        messages = [
            {"role": "model", "parts": [{"text": system_message}]},
            {"role": "user", "parts": [{"text": input_text}]}
        ]

        api_key = "AIzaSyDMiB8wcbyWTUg9MZspvCQpFofnZwBJans"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        payload = {"contents": messages}

        retry_strategy = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session = requests.Session()
        session.mount("https://", adapter)

        response = session.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()

        response_data = response.json()
        model_response = response_data['candidates'][0]['content']['parts'][0]['text']
        return {"response": model_response}

    except requests.exceptions.RequestException:
        raise HTTPException(status_code=503, detail="Gagal menghubungi layanan Gemini.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



async def load_markdown_files():
    try:
        data_dir = Path("data/Standardized Corpus")
        markdown_files = list(data_dir.rglob("*.md"))

        if not markdown_files:
            raise HTTPException(status_code=404, detail="Tidak ada file markdown ditemukan.")

        documents = []
        for file_path in markdown_files:
            try:
                loader = TextLoader(str(file_path), encoding="utf-8")
                loaded = loader.load()

                if loaded:
                    print(f"[INFO] Loaded {len(loaded)} doc(s) from {file_path.name}")
                    documents.extend(loaded)
                else:
                    print(f"[WARN] Kosong: {file_path.name}")

            except Exception as e:
                print(f"[ERROR] Gagal baca {file_path.name}: {e}")
                continue

        if not documents:
            raise HTTPException(status_code=400, detail="Tidak ada dokumen valid yang berhasil dimuat.")

        # Split dokumen
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        splits = text_splitter.split_documents(documents)

        if not splits or all(len(s.page_content.strip()) == 0 for s in splits):
            raise HTTPException(status_code=400, detail="Tidak ada chunk valid untuk di-embed.")

        chroma_vectors.add_documents(splits)
        chroma_vectors.persist()  # agar tersimpan setelah restart

        return {
            "message": "Documents loaded successfully",
            "files_processed": len(markdown_files),
            "chunks_created": len(splits),
            "success": True,
            "status_code": 200
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load documents: {str(e)}")

