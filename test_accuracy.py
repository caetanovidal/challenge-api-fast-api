import os
import json
from collections import defaultdict
from embeddings.generate import classify_document

# Path to directory with JSON files
json_dir = "processed_documents\\json_test"

# Dictionaries to count total and correct predictions per label
label_totals = defaultdict(int)
label_correct = defaultdict(int)

# Loop through all JSON files
for filename in os.listdir(json_dir):
    if filename.endswith('.json'):
        file_path = os.path.join(json_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

            for entry in data:
                text = entry.get("text", "")
                true_label = entry.get("label", "").strip().lower()

                try:
                    predicted_class, confidence = classify_document(text)
                    predicted_label = predicted_class.name.lower()
                except Exception as e:
                    print(f"Error processing file {filename}: {e}")
                    continue

                label_totals[true_label] += 1
                if predicted_label == true_label:
                    label_correct[true_label] += 1

# Print accuracy per label
print("Per-label Accuracy:")
print("--------------------")
for label in sorted(label_totals.keys()):
    total = label_totals[label]
    correct = label_correct.get(label, 0)
    accuracy = (correct / total) * 100 if total else 0
    print(f"{label:<15} — Accuracy: {accuracy:.2f}% ({correct}/{total})")

# Optional: overall accuracy
total_samples = sum(label_totals.values())
total_correct = sum(label_correct.values())
overall_accuracy = (total_correct / total_samples) * 100 if total_samples else 0
print("\nOverall Accuracy:")
print(f"{overall_accuracy:.2f}% ({total_correct}/{total_samples})")
