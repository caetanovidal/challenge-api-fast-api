from embeddings.generate import classify_document, classify_document_2
from ocr.extract_text import read_image, enhance_and_threshold, read_image_with_tesseract



test_classified_doc = "sample_documents\\scientific_publication\\00381007_00381012.jpg"

test = "docs_to_test\\2082697943_specification.jpg"
test_2 = "docs_to_test\\PUBLICATIONS057049-7_scientific_publication.jpg"
test_3 = "docs_to_test\\2505946475_scientific_report.jpg"
test_4 = "docs_to_test\\2505322605_2607_resume.jpg"
test_5 = "docs_to_test\\ton01426.85_advertisement.jpg"
test_6 = "docs_to_test\\2505955923_5924_email.jpg"
test_7 = "docs_to_test\\2505620113_file_folder.jpg"
test_8 = "docs_to_test\\524385089+-5089_handwritten.jpg"

img = read_image(test_4)
img = enhance_and_threshold(img)
text = read_image_with_tesseract(img)

predicted_class, confidence = classify_document_2(text)

print(predicted_class)
print(confidence)
