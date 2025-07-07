import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from enum import Enum
import os
import json

class DocumentType(Enum):
    specification = 1
    email = 2
    advertisement = 3
    handwritten = 4
    scientific_report = 5
    budget = 6
    scientific_publication = 7
    presentation = 8
    file_folder = 9
    memo = 10
    resume = 11
    invoice = 12
    letter = 13
    questionnaire = 14
    form = 15
    news_article = 16

json_folder = "sample_documents\\sample_json"

file_paths = [os.path.join(json_folder, filename) for filename in os.listdir(json_folder)]

doc_texts = []
doc_labels = []

for path in file_paths:
    with open(path, "r", encoding="utf-8") as f:
        try:
            data_list = json.load(f)
        except json.JSONDecodeError:
            print(f"Invalid JSON in file: {path}")
            continue

        for item in data_list:
            doc_type_str = item.get("label")
            text = item.get("text")
            if not doc_type_str or not text:
                continue
            try:
                doc_type = DocumentType[doc_type_str]  # Match enum naming
            except KeyError:
                print(f"Unknown document type '{doc_type_str}' in {path}")
                continue
            doc_texts.append(text)
            doc_labels.append(doc_type.value)




# --- Generate embeddings and index with FAISS ---
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = embedding_model.encode(doc_texts, convert_to_numpy=True)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)