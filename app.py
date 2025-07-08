from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import time
import os
from fastapi.staticfiles import StaticFiles
from ocr.extract_text_2 import extract_text_from_upload
from embeddings.generate import classify_document_2
from api_llm import send_to_llm

app = FastAPI()

# CORS (optional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    start_time = time.time()    

    try:
        raw_text = extract_text_from_upload(file)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR failed: {str(e)}")
    
    document_type, confidence = classify_document_2(raw_text)

    entities = send_to_llm(document_type, raw_text)

    print(entities)
    print(raw_text)

    processing_time = round(time.time() - start_time, 2)
    return JSONResponse(content={
        "document_type": f"{document_type.name}",
        "confidence": f"{confidence}",
        "entities": entities,
        "processing_time": f"{processing_time}s"
    })


# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Route for root path
@app.get("/")
def root():
    return FileResponse("static/index.html")
