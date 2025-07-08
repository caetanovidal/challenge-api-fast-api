from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import time
import os
from fastapi.staticfiles import StaticFiles
from ocr.extract_text_2 import extract_text_from_upload
from embeddings.generate import classify_document_2

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

    processing_time = round(time.time() - start_time, 2)
    return JSONResponse(content={
        "raw_text": raw_text,
        "document_type": f"{document_type.name}",
        "confidence": f"{confidence}",
        "entities": {
            "invoice_number": "INV-12345",
            "date": "2024-01-01",
            "total_amount": "$450.00",
            "vendor_name": "ABC Corp"
        },
        "processing_time": f"{processing_time}s"
    })


# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Route for root path
@app.get("/")
def root():
    return FileResponse("static/index.html")
