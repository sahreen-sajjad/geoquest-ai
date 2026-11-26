from pathlib import Path

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

ROOT = Path(__file__).resolve().parents[2]

KNOWLEDGE_FILE = ROOT / "knowledge_base" / "geography.txt"
INDEX_PATH = ROOT / "knowledge_base" / "faiss_index"


def build_index():

    text = KNOWLEDGE_FILE.read_text(encoding="utf-8")

    chunks = [
        chunk.strip()
        for chunk in text.split("\n\n")
        if chunk.strip()
    ]

    documents = [
        Document(page_content=chunk)
        for chunk in chunks
    ]

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"}
    )

    vector_store = FAISS.from_documents(
        documents,
        embeddings
    )

    vector_store.save_local(str(INDEX_PATH))

    print(f"Indexed {len(documents)} documents successfully.")


if __name__ == "__main__":
    build_index()