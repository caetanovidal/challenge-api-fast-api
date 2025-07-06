def classify_document(text: str) -> DocumentType:
    query_vec = embedding_model.encode([text])
    D, I = index.search(query_vec, k=1)
    closest_index = I[0][0]
    class_value = doc_labels[closest_index]
    return DocumentType(class_value)
