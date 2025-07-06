import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from enum import Enum
import os

class DocumentType(Enum):
    Specification = 1
    Email = 2
    Advertisement = 3
    Handwritten = 4
    Scientific_Report = 5
    Budget = 6
    Scientific_Publication = 7
    Presentation = 8
    File_Folder = 9
    Memo = 10
    Resume = 11
    Invoice = 12
    Letter = 13
    Questionnaire = 14
    Form = 15
    News_Article = 16

#embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

sample_documents = {
    DocumentType.Advertisement: ["Technical requirements for the new product..."],
    DocumentType.Budget: ["Dear John, I hope this email finds you well..."],
    DocumentType.Email: ["Buy now and get 50% off!"],
    DocumentType.File_Folder: ["Buy now and get 50% off!"],
    DocumentType.Form: ["Buy now and get 50% off!"],
    DocumentType.Handwritten: ["Buy now and get 50% off!"],
    DocumentType.Invoice: ["Buy now and get 50% off!"],
    DocumentType.Letter: ["Buy now and get 50% off!"],
    DocumentType.Memo: ["Buy now and get 50% off!"],
    DocumentType.News_Article: ["Buy now and get 50% off!"],
    DocumentType.Presentation: ["Buy now and get 50% off!"],
    DocumentType.Questionnaire: ["Buy now and get 50% off!"],
    DocumentType.Resume: ["Buy now and get 50% off!"],
    DocumentType.Scientific_Publication: ["Buy now and get 50% off!"],
    DocumentType.Scientific_Report: ["Buy now and get 50% off!"],
    DocumentType.Specification: ["Buy now and get 50% off!"],

}





