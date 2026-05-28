from pathlib import Path
from typing import List, Dict
from collections import defaultdict

import hashlib
import json
import re

import chromadb
import pandas as pd

from tqdm import tqdm
from sentence_transformers import SentenceTransformer

from backend.app.research_pipeline.retrieval.schema_adapter import (
    SemanticDocumentRouter,
)


DEFAULT_CHUNK_WORDS = 220
DEFAULT_CHUNK_OVERLAP = 40
MIN_CHUNK_WORDS = 40


class TranscriptChunker:

    def __init__(
        self,
        chunk_words: int = DEFAULT_CHUNK_WORDS,
        overlap_words: int = DEFAULT_CHUNK_OVERLAP,
        min_chunk_words: int = MIN_CHUNK_WORDS,
    ):

        self.chunk_words = chunk_words
        self.overlap_words = overlap_words
        self.min_chunk_words = min_chunk_words

    @staticmethod
    def clean_text(text: str) -> str:

        text = re.sub(r"\s+", " ", str(text))
        return text.strip()

    def split_into_chunks(
        self,
        text: str,
    ) -> List[str]:

        text = self.clean_text(text)

        words = text.split()

        if len(words) < self.min_chunk_words:
            return []

        chunks = []

        step = self.chunk_words - self.overlap_words

        for start in range(0, len(words), step):

            end = start + self.chunk_words

            chunk_words = words[start:end]

            if len(chunk_words) < self.min_chunk_words:
                continue

            chunk = " ".join(chunk_words)

            chunks.append(chunk)

        return chunks


class ChromaIndexBuilder:

    def __init__(
        self,
        persist_path: str = "./data/chroma",
        embedding_model: str = "all-MiniLM-L6-v2",
    ):

        self.client = chromadb.PersistentClient(
            path=persist_path
        )

        self.model = SentenceTransformer(
            embedding_model
        )

        self.chunker = TranscriptChunker()

        self.router = SemanticDocumentRouter()

    @staticmethod
    def hash_text(text: str) -> str:

        return hashlib.md5(
            text.encode("utf-8")
        ).hexdigest()

    def build_documents(
        self,
        dataframe: pd.DataFrame,
    ) -> Dict[str, List[Dict]]:

        grouped_documents = defaultdict(list)

        seen_hashes = set()

        for _, row in tqdm(
            dataframe.iterrows(),
            total=len(dataframe),
            desc="Routing semantic documents",
        ):

            row = row.to_dict()

            routed_documents = self.router.route_row(
                row
            )

            for routed_doc in routed_documents:

                collection_name = routed_doc[
                    "collection"
                ]

                chunks = self.chunker.split_into_chunks(
                    routed_doc["text"]
                )

                for chunk_idx, chunk in enumerate(chunks):

                    chunk_hash = self.hash_text(chunk)

                    if chunk_hash in seen_hashes:
                        continue

                    seen_hashes.add(chunk_hash)

                    grouped_documents[
                        collection_name
                    ].append(
                        {
                            "id": f"{chunk_hash}_{chunk_idx}",
                            "text": chunk,
                            "metadata": routed_doc[
                                "metadata"
                            ],
                        }
                    )

        return grouped_documents

    def generate_embeddings(
        self,
        documents: List[Dict],
        batch_size: int = 64,
    ) -> List[List[float]]:

        texts = [
            doc["text"]
            for doc in documents
        ]

        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True,
            normalize_embeddings=True,
        )

        return embeddings.tolist()

    def index_documents(
    self,
    grouped_documents: Dict[str, List[Dict]],
    batch_size: int = 512,
):

    for (
        collection_name,
        documents,
    ) in grouped_documents.items():

        print(
            f"\nIndexing collection: {collection_name}"
        )

        print(
            f"Documents: {len(documents)}"
        )

        collection = (
            self.client.get_or_create_collection(
                name=collection_name,
                metadata={
                    "hnsw:space": "cosine"
                },
            )
        )

        embeddings = self.generate_embeddings(
            documents
        )

        for start_idx in tqdm(
            range(
                0,
                len(documents),
                batch_size,
            ),
            desc=f"Indexing {collection_name}",
        ):

            end_idx = start_idx + batch_size

            batch_docs = documents[
                start_idx:end_idx
            ]

            batch_embeddings = embeddings[
                start_idx:end_idx
            ]

            collection.add(
                ids=[
                    doc["id"]
                    for doc in batch_docs
                ],
                documents=[
                    doc["text"]
                    for doc in batch_docs
                ],
                metadatas=[
                    doc["metadata"]
                    for doc in batch_docs
                ],
                embeddings=batch_embeddings,
            )

    def build_from_parquet(
        self,
        parquet_path: str,
    ):

        parquet_path = Path(parquet_path)

        print(
            f"\nLoading parquet: {parquet_path}"
        )

        dataframe = pd.read_parquet(
            parquet_path
        )

        print(
            f"Rows loaded: {len(dataframe)}"
        )

        grouped_documents = self.build_documents(
            dataframe
        )

        total_documents = sum(
            len(docs)
            for docs in grouped_documents.values()
        )

        print(
            f"Semantic documents generated: {total_documents}"
        )

        print("\nCollections:")

        for (
            collection_name,
            docs,
        ) in grouped_documents.items():

            print(
                f"- {collection_name}: {len(docs)}"
            )

        self.index_documents(
            grouped_documents
        )

        print(
            "\nSemantic indexing completed."
        )