from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import time
import os
from fastapi.staticfiles import StaticFiles


app = FastAPI()

# CORS (optional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Allowed file types
ALLOWED_EXTENSIONS = {".pdf", '.png', '.jpg', '.jpeg', '.bmp', '.tiff'}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    start_time = time.time()
    
    _, ext = os.path.splitext(file.filename)
    ext = ext.lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Unsupported file type.")
    
    # Placeholder for future processing
    # For now, just returning the JSON template
    processing_time = round(time.time() - start_time, 2)
    
    return JSONResponse(content={
        "document_type": "Invoice",
        "confidence": 0.92,
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
