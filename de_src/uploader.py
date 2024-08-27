from langchain_community.document_loaders import UnstructuredPDFLoader, OnlinePDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from langchain_community.vectorstores import FAISS
import os

loader = TextLoader("data/raw_data/mergeddocument.txt",autodetect_encoding=True)
data = loader.load_and_split()

context = "\n".join(str(p.page_content) for p in data)
print("The total number of words in the context:", len(context))
text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=200)
context = "\n\n".join(str(p.page_content) for p in data)

texts = text_splitter.split_text(context)

GOOGLE_API_KEY = "AIzaSyBPNlxK0jsb9Et0bjViu4zOuy8d13-50P8"
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")

vector_index = FAISS.from_texts(texts, embeddings)
vector_index.save_local("data/faiss_index")