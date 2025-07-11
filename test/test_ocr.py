#import pytest
from PIL import Image
import numpy as np
from ocr.extract_text_2 import enhance_and_threshold, read_image_with_easyocr, read_image

def test_read_image_with_easyocr():
    image = read_image("processed_documents\\test\\email\\527792930+-2930.jpg")
    image = enhance_and_threshold(image)
    ocr_result = read_image_with_easyocr(image)

    expected_keywords = [
        "From", "Miller", "Tompson", "Smith", "Powell", "1996", "08.55.00", "tobacco", "polls"
    ]

    for keyword in expected_keywords:
        assert keyword in ocr_result, f"Expected keyword '{keyword}' not found in OCR output."

    assert len(ocr_result.strip()) > 50, "OCR output is unexpectedly short."