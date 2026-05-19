# ============================================================
# SBERT EMBEDDING GENERATION
# Financial Semantic Intelligence Platform
# ============================================================

import os
import numpy as np
import pandas as pd

from sentence_transformers import SentenceTransformer

# ============================================================
# CONFIG
# ============================================================

DATA_PATH = "data/database/transcripts_clean.parquet"

OUTPUT_DIR = "outputs/embeddings"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

COLUMNS_TO_EMBED = [

    "summary",
    "takeaways"
]

BATCH_SIZE = 32

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# LOAD MODEL
# ============================================================

print("\nLoading SBERT model...")

model = SentenceTransformer(MODEL_NAME)

print(f"Model loaded: {MODEL_NAME}")

# ============================================================
# LOAD DATASET
# ============================================================

print("\nLoading dataset...")

df = pd.read_parquet(DATA_PATH)

print(f"Dataset loaded: {len(df):,} rows")

# ============================================================
# VALIDATION
# ============================================================

required_columns = [

    "id",
    "company",
    "ticker"
] + COLUMNS_TO_EMBED

missing = [

    c for c in required_columns
    if c not in df.columns
]

if missing:

    raise ValueError(
        f"Missing columns: {missing}"
    )

# ============================================================
# EMBEDDING LOOP
# ============================================================

for column in COLUMNS_TO_EMBED:

    print("\n===================================================")
    print(f"GENERATING EMBEDDINGS: {column}")
    print("===================================================\n")

    # ------------------------------------------------
    # TEXTS
    # ------------------------------------------------

    # ------------------------------------------------
    # FILTER VALID TEXTS
    # ------------------------------------------------

    valid_df = df[

        df[column]
        .fillna("")
        .astype(str)
        .apply(lambda x: len(x.split()) > 30)

    ].copy()

    texts = valid_df[column] \
        .fillna("") \
        .astype(str) \
        .tolist()

    # ------------------------------------------------
    # EMBEDDINGS
    # ------------------------------------------------

    embeddings = model.encode(

        texts,

        batch_size=BATCH_SIZE,

        show_progress_bar=True,

        convert_to_numpy=True
    )

    # ------------------------------------------------
    # SAVE EMBEDDINGS
    # ------------------------------------------------

    embedding_path = (
        f"{OUTPUT_DIR}/{column}_embeddings.npy"
    )

    np.save(
        embedding_path,
        embeddings
    )

    # ------------------------------------------------
    # SAVE METADATA
    # ------------------------------------------------

    metadata = valid_df[[
        "id",
        "company",
        "ticker",
        "quarter",
        "earnings_year",
        column
    ]]

    metadata_path = (
        f"{OUTPUT_DIR}/{column}_metadata.csv"
    )

    metadata.to_csv(
        metadata_path,
        index=False
    )

    # ------------------------------------------------
    # INFO
    # ------------------------------------------------

    print(f"\nEmbeddings shape: {embeddings.shape}")

    print(f"Saved embeddings: {embedding_path}")

    print(f"Saved metadata: {metadata_path}")

# ============================================================
# DONE
# ============================================================

print("\n===================================================")
print("EMBEDDING GENERATION COMPLETED")
print("===================================================")