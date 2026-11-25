"""Local embeddings (sentence-transformers) and the Chroma vector store."""

from functools import lru_cache

import chromadb
from sentence_transformers import SentenceTransformer

import config


@lru_cache(maxsize=1)
def _embedder() -> SentenceTransformer:
    return SentenceTransformer(config.EMBEDDING_MODEL)


@lru_cache(maxsize=1)
def _client() -> chromadb.api.ClientAPI:
    return chromadb.PersistentClient(path=str(config.CHROMA_DIR))


def _collection():
    # Embeddings are computed here, so the collection gets no embedding function.
    return _client().get_or_create_collection(
        config.COLLECTION,
        embedding_function=None,
        configuration={"hnsw": {"space": "cosine"}},
    )


def rebuild(ids: list[str], texts: list[str], metadatas: list[dict]) -> int:
    """Replace the whole collection with the given chunks. Returns the stored count."""
    client = _client()
    if config.COLLECTION in [c.name for c in client.list_collections()]:
        client.delete_collection(config.COLLECTION)
    vectors = _embedder().encode(
        texts, normalize_embeddings=True, show_progress_bar=True
    ).tolist()
    collection = _collection()
    collection.add(ids=ids, embeddings=vectors, documents=texts, metadatas=metadatas)
    return collection.count()


def search(query: str, k: int) -> list[dict]:
    """Top-k chunks for the query: text, metadata and cosine similarity."""
    vector = _embedder().encode(
        [config.EMBEDDING_QUERY_PREFIX + query], normalize_embeddings=True
    ).tolist()
    result = _collection().query(
        query_embeddings=vector,
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )
    return [
        {"text": text, **meta, "score": round(1 - distance, 4)}
        for text, meta, distance in zip(
            result["documents"][0], result["metadatas"][0], result["distances"][0]
        )
    ]
