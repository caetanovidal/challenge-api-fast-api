from api_llm import send_to_llm
from embeddings.generate import DocumentType


def test_send_to_llm_basic(monkeypatch):
    # Mock OpenAI call
    def mock_create(*args, **kwargs):
        class MockResponse:
            class Choice:
                message = type("msg", (), {"content": '{"topic": "AI", "year": "2020"}'})
            choices = [Choice()]
        return MockResponse()

    monkeypatch.setattr("openai.OpenAI.chat.completions.create", mock_create)

    document_type = DocumentType.scientific_publication
    text = "This is a scientific publication about AI published in 2020."
    entities = send_to_llm(document_type, text)

    assert "topic" in entities
    assert "year" in entities
