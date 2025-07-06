import os
from pdf2image import convert_from_path
import numpy as np
from enum import Enum
import cv2
import pytesseract
from PIL import Image, ImageEnhance
import uuid
import shutil

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)



def pdf_or_image(file_path):
    valid_image_exts = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')
    file_ext = os.path.splitext(file_path)[1].lower()

    if file_ext in valid_image_exts:
        return "image"
    elif file_ext == '.pdf':
        return "pdf"

    raise ValueError(f"Unsupported file format: '{file_ext}'. Only images and PDFs are allowed.")


def read_image_with_tesseract(image_input):
    custom_config = r'--oem 3 --psm 6'
    return pytesseract.image_to_string(image_input, config=custom_config)


def read_image(image_path):
    image = Image.open(image_path)
    return image

def read_image_from_pdf(file_path):
    images = convert_from_path(file_path, dpi=300, poppler_path='C:/Users/caetano/Downloads/Release-24.08.0-0/poppler-24.08.0/Library/bin')

    text = ""
    for img in images:
        enchaced_image = enhance_and_threshold(img)
        text += read_image_with_tesseract(enchaced_image)

    return text


def enhance_and_threshold(image):
    
    img = np.array(image.convert("RGB"))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Resize (scale up small text)
    scale_factor = 1.5
    width = int(img.shape[1] * scale_factor)
    height = int(img.shape[0] * scale_factor)
    img = cv2.resize(img, (width, height), interpolation=cv2.INTER_CUBIC)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Denoising while preserving edges
    filtered = cv2.bilateralFilter(gray, d=11, sigmaColor=75, sigmaSpace=75)

    # Adaptive thresholding for uneven lighting
    thresh = cv2.adaptiveThreshold(
        filtered, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 21, 10
    )

    # Optional: Morphological operations to enhance characters
    kernel = np.ones((2, 2), np.uint8)
    processed = cv2.dilate(thresh, kernel, iterations=1)

    return processed


def extract_text_from_upload(upload_file) -> str:
    """
    Save the uploaded file temporarily, run OCR, delete file, return extracted text.
    """
    _, ext = os.path.splitext(upload_file.filename)
    ext = ext.lower()

    if ext not in ('.pdf', '.png', '.jpg', '.jpeg', '.bmp', '.tiff'):
        raise ValueError("Unsupported file type.")

    temp_filename = f"{uuid.uuid4().hex}{ext}"
    temp_path = os.path.join(UPLOAD_DIR, temp_filename)

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    try:
        if pdf_or_image(temp_path) == 'image':
            img = read_image(temp_path)
            img = enhance_and_threshold(img)
            text = read_image_with_tesseract(img)
        else:
            
            text = read_image_from_pdf(temp_path)
    finally:
        os.remove(temp_path)

    return text.strip()