import os
import glob
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from chromadb.utils import embedding_functions

KB_SOURCES_DIR = os.path.join("kb", "sources")
CHROMA_PATH = os.path.join("kb", "chroma_data")
COLLECTION_NAME = "owasp_security_rules"

def ingest_knowledge_base():
    # 1. Text Splitter: 500 chars, 50 overlap
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""]
    )

    source_files = glob.glob(os.path.join(KB_SOURCES_DIR, "*.txt"))
    if not source_files:
        print(f"Error: No source files found in {KB_SOURCES_DIR}")
        return

    documents = []
    metadatas = []
    ids = []
    chunk_counter = 0

    print(f"Reading {len(source_files)} source files from {KB_SOURCES_DIR}...")
    for filepath in source_files:
        filename = os.path.basename(filepath)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        topic = "SQL Injection" if "sqli" in filename.lower() else "Secrets Management"
        chunks = splitter.split_text(content)

        for i, chunk in enumerate(chunks):
            chunk_id = f"{filename}_chunk_{i}"
            documents.append(chunk)
            metadatas.append({
                "source": filename,
                "topic": topic,
                "chunk_index": i
            })
            ids.append(chunk_id)
            chunk_counter += 1

    print(f"Generated {chunk_counter} chunks. Initializing embedding function (all-MiniLM-L6-v2)...")
    ef = embedding_functions.DefaultEmbeddingFunction()

    print(f"Storing embeddings into persistent ChromaDB at {CHROMA_PATH}...")
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    try:
        client.delete_collection(name=COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=ef,
        metadata={"hnsw:space": "cosine"}
    )

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

    print(f"✅ Ingestion Complete! Successfully indexed {len(ids)} chunks into ChromaDB.")

if __name__ == "__main__":
    ingest_knowledge_base()