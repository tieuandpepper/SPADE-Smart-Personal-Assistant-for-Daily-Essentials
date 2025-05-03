from dotenv import load_dotenv
load_dotenv()
import json, os
from typing import List
from langchain.schema import Document
import glob
from langchain.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama
from langchain.chains import RetrievalQA

# CONFIG
DATA_PATH   = "data"
CHROMA_PATH = "chroma_db"

embeddings = OllamaEmbeddings(model="nomic-embed-text")
vector_store = Chroma(
    collection_name    = "my_collection",
    embedding_function = embeddings,
    persist_directory  = CHROMA_PATH,
)

def create_database():
    # LOAD all PDFs via PyPDFLoader
    raw_docs = []
    for pdf_file in glob.glob(f"{DATA_PATH}/*.pdf"):
        loader = PyPDFLoader(pdf_file)
        raw_docs.extend(loader.load())

    # LOAD text files
    for txt_path in glob.glob(f"{DATA_PATH}/*.txt"):
        loader = TextLoader(txt_path, encoding="utf8")   # or your file’s encoding
        docs = loader.load()
        for d in docs:
            d.metadata["source"] = txt_path
        raw_docs.extend(docs)

    # SPLIT into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100,
    )
    docs = splitter.split_documents(raw_docs)

    vector_store.add_documents(docs)

def retrieve_from_database(query: str) -> str:
    """
    Fetches the top-k most relevant document chunks for the given query.
    Returns a concatenated string of source + excerpt.
    """
    docs = vector_store.as_retriever().get_relevant_documents(query, k=2)
    formatted = []
    for d in docs:
        src = d.metadata.get("source", "unknown")
        snippet = d.page_content.replace("\n", " ")[:500]
        formatted.append(f"[{src}] {snippet}")
    return "\n\n".join(formatted)


def add_to_database(json_payload: str) -> str:
    """
    Accepts a JSON string representing one or more documents:
      [{"source": "file1.txt", "text": "..."}, ...]
    Converts each entry into a Document and adds it into the vector store.
    """
    try:
        records = json.loads(json_payload)
        docs = []
        for rec in records:
            docs.append(Document(page_content=rec["text"], metadata={"source": rec["source"]}))
        vector_store.add_documents(docs)
        return f"Added {len(docs)} document(s) to the RAG index."
    except Exception as e:
        return f"Failed to add documents: {e}"
    
def read_pdf(file_name: str) -> str:
    """
    Loads all pages from the given PDF and returns the full text.
    """
    loader = PyPDFLoader(os.path.join(DATA_PATH,file_name))
    docs = loader.load()  # List[Document], one per page or section
    # Concatenate into one string
    return "\n\n".join(doc.page_content for doc in docs)




# create_database()