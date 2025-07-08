from ocr import extract_text_2
import os
import random
import shutil
import json

random.seed(42)

base_input_dir = "D:/caetano/appz/Estudos/challenge-api-fast-api/sample_documents"
base_output_dir = "D:/caetano/appz/Estudos/challenge-api-fast-api/processed_documents"

folders = [
    'advertisement',
    'budget',
    'email',
    'file_folder',
    'form',
    'handwritten',
    'invoice',
    'letter',
    'memo',
    'news_article',
    'presentation',
    'questionnaire',
    'resume',
    'scientific_publication',
    'scientific_report',
    'specification'
]

for x in folders:
    folder_path = os.path.join(base_input_dir, x)

    # List all files only (ignore dirs)
    all_files = []
    for root, dirs, files in os.walk(folder_path):
        for name in files:
            all_files.append(os.path.join(root, name))

    # Shuffle and split
    random.shuffle(all_files)
    split_index = int(0.8 * len(all_files))
    train_files = all_files[:split_index]
    test_files = all_files[split_index:]

    # Output directories
    train_dir = os.path.join(base_output_dir, 'train', x)
    test_dir = os.path.join(base_output_dir, 'test', x)
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)

    samples_train = []
    samples_test = []

    # Move files and extract OCR text
    for file in train_files:
        new_path = os.path.join(train_dir, os.path.basename(file))
        shutil.copy(file, new_path)  # Use copy() if you want to preserve originals
        img = extract_text_2.read_image(new_path)
        img = extract_text_2.enhance_and_threshold(img)
        text = extract_text_2.read_image_with_easyocr(img).replace('\n', '\\n')
        samples_train.append({"text": text, "label": x})

    for file in test_files:
        new_path = os.path.join(test_dir, os.path.basename(file))
        shutil.copy(file, new_path)
        img = extract_text_2.read_image(new_path)
        img = extract_text_2.enhance_and_threshold(img)
        text = extract_text_2.read_image_with_easyocr(img).replace('\n', '\\n')
        samples_test.append({"text": text, "label": x})

    # Save as JSON
    with open(os.path.join(base_output_dir, f"samples_train_{x}.json"), "w", encoding="utf-8") as f:
        json.dump(samples_train, f, indent=2, ensure_ascii=False)

    with open(os.path.join(base_output_dir, f"samples_test_{x}.json"), "w", encoding="utf-8") as f:
        json.dump(samples_test, f, indent=2, ensure_ascii=False)
