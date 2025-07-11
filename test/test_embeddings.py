from embeddings.generate import classify_document, classify_document_2
from embeddings.generate import DocumentType


def test_classify_document_basic():
    text = "Dear Hiring Manager, please find my resume attached."
    label, confidence = classify_document(text)

    assert isinstance(confidence, float)
    if label:
        assert isinstance(label, DocumentType)


def test_classify_document_2_basic():
    text = "This is a scientific publication about AI from 2020."
    label, confidence = classify_document_2(text)

    assert isinstance(label, DocumentType)
    assert isinstance(confidence, float)
