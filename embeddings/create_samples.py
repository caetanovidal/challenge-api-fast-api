from ocr import extract_text_2
import os
import random
import shutil
import json

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


    folder_path = f"D:/caetano/appz/Estudos/challenge-api-fast-api/sample_documents/{x}"
    all_paths = []

    for root, dirs, files in os.walk(folder_path):
        for name in dirs + files:
            full_path = os.path.join(root, name)
            all_paths.append(full_path)


    samples = []

    for file in all_paths:

        img = extract_text_2.read_image(file)
        img = extract_text_2.enhance_and_threshold(img)
        text = extract_text_2.read_image_with_easyocr(img)
        text = text.replace('\n', '\\n')
        samples.append({
            "text": text,
            "label": f"{x}"
        })

    # Optional: Save to JSON
    import json
    with open(f"samples_{x}.json", "w", encoding="utf-8") as f:
        json.dump(samples, f, indent=2, ensure_ascii=False)
