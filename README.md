# Tutorial

if you need some help and check on my opinion:
https://youtu.be/rR9qO2GF3E4

# 🧠 EasyOCR + GPT Document Analyzer API

A FastAPI-based web service for document analysis. This API accepts PDF or image files, extracts text using OCR (EasyOCR), classifies the document using embeddings (FAISS + Sentence Transformers), and extracts structured entities using OpenAI's GPT models.

---

## 🚀 Features

* ✅ Upload image or PDF documents
* ✅ Perform OCR with EasyOCR
* ✅ Classify documents via semantic search
* ✅ Extract structured fields using GPT-3.5
* ✅ Docker support for production deployments
* ✅ CORS-enabled for frontend integration

---

## 📦 Installation Guide

### 🖥 Prerequisites

* [Python 3.9.12](https://www.python.org/downloads/release/python-3912/)
* [Git](https://git-scm.com/downloads)
* [Poppler](https://poppler.freedesktop.org/) (required for PDF processing)
* [Docker Desktop](https://www.docker.com/products/docker-desktop) (optional, for containerization)

### 🔧 Manual Setup

```bash
git clone https://github.com/caetanovidal/challenge-api-fast-api
cd challenge-api-fast-api
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
OPENAI_API_KEY="your-gpt-key-goes-here"
```

Set up Poppler path in `extract_text_2.py`:

```python
poppler_path='C:/path/to/your/poppler/bin'
```

> 📌 Make sure the Poppler binary directory is correctly set on Windows.

Optional fix for SSL issues:

```bash
python -m pip install --upgrade certifi
```

### ▶️ Run the API

```bash
uvicorn app:app --reload
```

Open your browser at:
[http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🐳 Docker Usage

1. Create the `.env` file as described above.
2. Build the Docker image:

```bash
docker build -t easyocr-api .
```

3. Run the container:

```bash
docker run -p 8000:8000 easyocr-api
```

4. Open in browser:

[http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🧪 API Reference

### `POST /upload`

Upload a document (PDF or image) and get extracted information.

#### Request

* `multipart/form-data`

  * `file`: the document file

#### Response

```json
{
  "document_type": "resume",
  "confidence": "0.95",
  "entities": {
    "name": "John Doe",
    "years of experience": "5",
    "area": "Software Engineering"
  },
  "processing_time": "3.2s"
}
```

---

## 🗂 Project Structure

```
├── app.py                     # Main FastAPI app
├── api_llm.py                 # LLM prompt + GPT entity extraction
├── embeddings/
│   └── generate.py            # Document classification using FAISS
├── ocr/
│   └── extract_text_2.py      # OCR processing with EasyOCR + image enhancement
├── static/
│   └── index.html             # Default frontend (optional)
├── temp_uploads/             # Temp storage for file processing
├── processed_documents/
│   └── json_train/           # Training data for embeddings
├── .env                       # OpenAI key (not committed)
├── requirements.txt
└── README.md
```

---

## 🧠 How it Works

1. **OCR**: Extracts text from uploaded images/PDFs using EasyOCR.
2. **Classification**: Compares embeddings of document text with training examples using FAISS to determine the type.
3. **Entity Extraction**: Sends prompt to GPT based on the document type, asking it to extract structured data.
4. **Result**: Returns document type, confidence, and extracted fields.

---

## ⚙️ Technologies

* [FastAPI](https://fastapi.tiangolo.com/)
* [EasyOCR](https://github.com/JaidedAI/EasyOCR)
* [OpenAI GPT-3.5](https://platform.openai.com/)
* [FAISS](https://github.com/facebookresearch/faiss)
* [SentenceTransformers](https://www.sbert.net/)
* [Poppler](https://poppler.freedesktop.org/)

---

## 📌 Notes

* GPU is enabled for EasyOCR (`gpu=True`), ensure CUDA is installed for best performance.
* Be cautious of malformed documents or unstructured content—OCR accuracy depends on image quality.
* Document classification is trained using the contents of `processed_documents/json_train`.

---

## 🛠️ TODOs

* [ ] Improve entity validation for GPT responses
* [ ] Add more pre-processing into images

