import pytest
from PIL import Image
import numpy as np
from ocr.extract_text_2 import enhance_and_threshold, read_image_with_easyocr

def test_read_image_with_easyocr():
    image = Image.fromarray(np.uint8(np.random.rand(100, 100, 3) * 255))
    image = enhance_and_threshold(image)
    text = read_image_with_easyocr(image)

    assert isinstance(text, str)
