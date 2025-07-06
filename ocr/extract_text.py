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

class DocumentType(Enum):
    Specification = 1
    Email = 2
    Advertisement = 3
    Handwritten = 4
    Scientific_Report = 5
    Budget = 6
    Scientific_Publication = 7
    Presentation = 8
    File_Folder = 9
    Memo = 10
    Resume = 11
    Invoice = 12
    Letter = 13
    Questionnaire = 14
    Form = 15
    News_Article = 16

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

def read_pdf_with_tesseract(file_path):
    pages = convert_from_path(
        file_path,
        dpi=300,
        poppler_path='C:/Users/caetano/Downloads/Release-24.08.0-0/poppler-24.08.0/Library/bin'
    )

    text = ""
    for i, page in enumerate(pages):
        np_image = np.array(page.convert('L'))
        text += read_image_with_tesseract(np_image) + "\n"

    return text

def enhance_and_threshold(image_path):
    # Step 1: Enhance image (your function)
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)

    enhancer = ImageEnhance.Sharpness(img_pil)
    img_sharp = enhancer.enhance(2.0)

    enhancer = ImageEnhance.Brightness(img_sharp)
    img_bright = enhancer.enhance(1.2)

    enhancer = ImageEnhance.Contrast(img_bright)
    img_contrast = enhancer.enhance(1.5)

    img_cv = cv2.cvtColor(np.array(img_contrast), cv2.COLOR_RGB2BGR)
    img_denoised = cv2.fastNlMeansDenoisingColored(img_cv, None, 10, 10, 7, 21)

    # Step 2: Grayscale + Threshold (for OCR)
    gray = cv2.cvtColor(img_denoised, cv2.COLOR_BGR2GRAY)
    denoised = cv2.GaussianBlur(gray, (3, 3), 0)
    _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return thresh



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
            img = enhance_and_threshold(temp_path)
            text = read_image_with_tesseract(img)
        else:
            text = read_pdf_with_tesseract(temp_path)
    finally:
        os.remove(temp_path)

    return text.strip()