"""
Help-document search index.

build_index() reads the help documents in the docs folder, cuts them into small
parts, turns each part into numbers (an "embedding") with Gemini, and saves them
in a Chroma database so the agent can search them later.
"""

from pathlib import Path

import chromadb
from dotenv import load_dotenv
from google import genai
from google.genai import types

# The embedding model is set in ONE place: here.
EMBEDDING_MODEL = "gemini-embedding-001"

# Folders and sizes (all in the project folder).
PROJECT_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_DIR / "docs"
CHROMA_DIR = PROJECT_DIR / "chroma_db"
COLLECTION_NAME = "help_docs"
MIN_CHARS = 500    # join small pieces until a part is about this long
MAX_CHARS = 1000   # never let a part get longer than this
BATCH_SIZE = 50    # how many parts we send to Gemini at once

# Read the Gemini key from the .env file (it is never written in code).
load_dotenv()


def split_text(text):
    """Cut one file's text into parts of about 500-1,000 characters."""
    # First split by heading: every line starting with # begins a new section.
    sections, current = [], []
    for line in text.splitlines():
        if line.startswith("#") and current:
            sections.append("\n".join(current))
            current = []
        current.append(line)
    if current:
        sections.append("\n".join(current))

    # Then split each section by paragraph, and cut any paragraph that is too long.
    pieces = []
    for section in sections:
        for paragraph in section.split("\n\n"):
            paragraph = paragraph.strip()
            while len(paragraph) > MAX_CHARS:
                cut = paragraph.rfind(" ", 0, MAX_CHARS)
                cut = cut if cut > 0 else MAX_CHARS
                pieces.append(paragraph[:cut].strip())
                paragraph = paragraph[cut:].strip()
            if paragraph:
                pieces.append(paragraph)

    # Join neighbouring small pieces so parts are not tiny.
    parts, buffer = [], ""
    for piece in pieces:
        if buffer and len(buffer) + len(piece) + 2 > MAX_CHARS:
            parts.append(buffer)
            buffer = ""
        buffer = (buffer + "\n\n" + piece) if buffer else piece
        if len(buffer) >= MIN_CHARS:
            parts.append(buffer)
            buffer = ""
    if buffer:
        parts.append(buffer)
    return parts


def build_index():
    """Rebuild the search index. Returns (number of parts saved, number of files read)."""
    # Read every .md and .txt file in docs and remember which file each part came from.
    files = sorted(p for p in DOCS_DIR.iterdir() if p.suffix.lower() in (".md", ".txt"))
    texts, sources = [], []
    for file in files:
        for part in split_text(file.read_text(encoding="utf-8")):
            texts.append(part)
            sources.append(file.name)

    # Turn the parts into embeddings, in batches.
    client = genai.Client()
    embeddings = []
    for start in range(0, len(texts), BATCH_SIZE):
        result = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=texts[start:start + BATCH_SIZE],
            config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT"),
        )
        embeddings.extend(e.values for e in result.embeddings)

    # Save in Chroma, replacing any old index.
    db = chromadb.PersistentClient(path=str(CHROMA_DIR))
    try:
        db.delete_collection(COLLECTION_NAME)
    except Exception:
        pass  # there was no old index
    collection = db.create_collection(COLLECTION_NAME)
    if texts:
        collection.add(
            ids=[f"part-{i}" for i in range(len(texts))],
            documents=texts,
            embeddings=embeddings,
            metadatas=[{"source": s} for s in sources],
        )
    return len(texts), len(files)


def search_help_docs(question: str) -> dict:
    """Search DemoKart's help documents (FAQs and policies) for the parts closest to the question.

    Call this before answering any question about DemoKart's business, such as
    returns, refunds, shipping, delivery, warranty, repairs or payments.

    Args:
        question: The customer's question, in their own words.

    Returns:
        A dict with "results": a list of the 3 closest parts, each with the
        "text" of the part and the "source" file name it came from.
    """
    # Turn the question into numbers with the SAME model, but as a question (RETRIEVAL_QUERY).
    client = genai.Client()
    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=question,
        config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY"),
    )
    query_embedding = result.embeddings[0].values

    # Ask Chroma for the 3 closest parts.
    db = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = db.get_collection(COLLECTION_NAME)
    found = collection.query(query_embeddings=[query_embedding], n_results=3)

    # Return each part's text together with the file it came from.
    results = [
        {"text": text, "source": meta["source"]}
        for text, meta in zip(found["documents"][0], found["metadatas"][0])
    ]
    return {"results": results}
