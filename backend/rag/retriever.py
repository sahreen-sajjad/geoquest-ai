from pathlib import Path
from functools import lru_cache

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

ROOT = Path(__file__).resolve().parents[2]
INDEX_PATH = ROOT / "knowledge_base" / "faiss_index"


@lru_cache(maxsize=1)
def load_vector_store():

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"}
    )

    return FAISS.load_local(
        str(INDEX_PATH),
        embeddings,
        allow_dangerous_deserialization=True
    )


def retrieve_knowledge(
    query: str,
    country: str,
    k: int = 3
):
    vector_store = load_vector_store()

    documents = vector_store.similarity_search(
        query,
        k=8
    )

    relevant_documents = [
        doc for doc in documents
        if doc.page_content.splitlines()[0].strip().casefold()
        == f"COUNTRY: {country}".casefold()
    ]

    if not relevant_documents:
        return "No relevant specialised knowledge available."

    return "\n\n".join(
        doc.page_content
        for doc in relevant_documents[:k]
    )


if __name__ == "__main__":

    result = retrieve_knowledge(
        "Iceland landscape characteristics",
        k=2
    )

    print(result)