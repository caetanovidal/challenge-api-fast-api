from embeddings.generate import classify_document, classify_document_2
from embeddings.generate import DocumentType


def test_classify_document_basic():
    text = """iv;ledsuies\nVANTAGE\n41a\nGIECET\n1\nVANTAGE"""
    label, confidence = classify_document(text)

    assert label is not None, "Label is None"
    assert isinstance(label, DocumentType), f"Label is not a DocumentType: {label}"
    assert isinstance(confidence, float)
    #assert confidence > 0.6, f"Confidence too low: {confidence}"
