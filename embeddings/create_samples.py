from ocr import extract_text_2
import os
import json

# Base directories
base_input_dir_train = "C:\\Users\\Caetano\\Desktop\\estudos\\challenge-api-fast-api\\processed_documents\\train"
base_input_dir_test = "C:\\Users\\Caetano\\Desktop\\estudos\\challenge-api-fast-api\\processed_documents\\test"
base_output_dir_train = "C:\\Users\\Caetano\\Desktop\\estudos\\challenge-api-fast-api\\processed_documents\\json_train"
base_output_dir_test = "C:\\Users\\Caetano\\Desktop\\estudos\\challenge-api-fast-api\\processed_documents\\json_test"

# Folder (class) names
folders = [
    'advertisement', 'budget', 'email', 'file_folder', 'form', 'handwritten',
    'invoice', 'letter', 'memo', 'news_article', 'presentation', 'questionnaire',
    'resume', 'scientific_publication', 'scientific_report', 'specification'
]

# Ensure output dirs exist
os.makedirs(base_output_dir_train, exist_ok=True)
os.makedirs(base_output_dir_test, exist_ok=True)

# Function to process a dataset split
def process_split(input_dir, output_dir, split_name):
    for label in folders:
        folder_path = os.path.join(input_dir, label)
        if not os.path.isdir(folder_path):
            continue

        samples = []

        for root, dirs, files in os.walk(folder_path):
            for filename in files:
                file_path = os.path.join(root, filename)
                try:
                    img = extract_text_2.read_image(file_path)
                    img = extract_text_2.enhance_and_threshold(img)
                    text = extract_text_2.read_image_with_easyocr(img).replace('\n', '\\n')
                    samples.append({"text": text, "label": label})
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

        # Save JSON
        output_file = os.path.join(output_dir, f"samples_{label}.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(samples, f, indent=2, ensure_ascii=False)

# Process both train and test splits
process_split(base_input_dir_train, base_output_dir_train, "train")
process_split(base_input_dir_test, base_output_dir_test, "test")
