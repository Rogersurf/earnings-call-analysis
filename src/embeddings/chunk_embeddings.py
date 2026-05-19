# ============================================================
# FILE: src/embeddings/chunk_embeddings.py
# ============================================================

import os
import numpy as np
import pandas as pd

from tqdm import tqdm
from sentence_transformers import SentenceTransformer

# ============================================================
# CONFIG
# ============================================================

INPUT_PATH = "outputs/chunks/semantic_chunks.parquet"

OUTPUT_PATH = (
    "outputs/chunks/"
    "semantic_chunks_embeddings.parquet"
)

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

BATCH_SIZE = 64

# ============================================================
# LOAD MODEL
# ============================================================

print("\n===================================================")
print("LOADING SENTENCE TRANSFORMER")
print("===================================================\n")

model = SentenceTransformer(MODEL_NAME)

# ============================================================
# LOAD DATA
# ============================================================

print("\n===================================================")
print("LOADING CHUNKS")
print("===================================================\n")

df = pd.read_parquet(INPUT_PATH)

print(df.shape)

# ============================================================
# CLEAN TEXT
# ============================================================

df["chunk_text"] = (
    df["chunk_text"]
    .fillna("")
    .astype(str)
    .str.strip()
)

df = df[df["chunk_text"] != ""]

df = df.reset_index(drop=True)

print("\nAfter cleaning:")
print(df.shape)

# ============================================================
# GENERATE EMBEDDINGS
# ============================================================

print("\n===================================================")
print("GENERATING EMBEDDINGS")
print("===================================================\n")

texts = df["chunk_text"].tolist()

embeddings = model.encode(
    texts,
    batch_size=BATCH_SIZE,
    show_progress_bar=True,
    convert_to_numpy=True,
    normalize_embeddings=True
)

print("\nEmbeddings shape:")
print(embeddings.shape)

# ============================================================
# SAVE EMBEDDINGS
# ============================================================

df["embedding"] = embeddings.tolist()

# ============================================================
# SAVE OUTPUT
# ============================================================

os.makedirs(
    "outputs/chunks",
    exist_ok=True
)

df.to_parquet(
    OUTPUT_PATH,
    index=False
)

print("\n===================================================")
print("CHUNK EMBEDDINGS COMPLETED")
print("===================================================\n")

print("Saved to:\n")
print(OUTPUT_PATH)