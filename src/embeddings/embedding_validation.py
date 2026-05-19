# ============================================================
# EMBEDDING VALIDATION
# Financial Semantic Intelligence Platform
# ============================================================

import os
import json
import hashlib

import numpy as np
import pandas as pd

from collections import Counter

import matplotlib.pyplot as plt

from sklearn.metrics.pairwise import cosine_similarity

# ============================================================
# CONFIG
# ============================================================

EMBEDDINGS_DIR = "outputs/embeddings"

OUTPUT_DIR = "outputs/embedding_validation"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# FILES
# ============================================================

FILES = [

    {
        "name": "summary",
        "embedding_file":
            f"{EMBEDDINGS_DIR}/summary_embeddings.npy",

        "metadata_file":
            f"{EMBEDDINGS_DIR}/summary_metadata.csv",

        "text_column":
            "summary"
    },

    {
        "name": "takeaways",
        "embedding_file":
            f"{EMBEDDINGS_DIR}/takeaways_embeddings.npy",

        "metadata_file":
            f"{EMBEDDINGS_DIR}/takeaways_metadata.csv",

        "text_column":
            "takeaways"
    }
]

# ============================================================
# HASH FUNCTION
# ============================================================

def hash_text(text):

    text = str(text).strip().lower()

    return hashlib.md5(
        text.encode()
    ).hexdigest()

# ============================================================
# ANALYSIS LOOP
# ============================================================

for item in FILES:

    name = item["name"]

    print("\n===================================================")
    print(f"VALIDATING: {name}")
    print("===================================================\n")

    # ------------------------------------------------
    # LOAD DATA
    # ------------------------------------------------

    embeddings = np.load(
        item["embedding_file"]
    )

    metadata = pd.read_csv(
        item["metadata_file"]
    )

    text_column = item["text_column"]

    texts = metadata[text_column].fillna("").astype(str)

    # ------------------------------------------------
    # BASIC STATS
    # ------------------------------------------------

    print(f"Embeddings shape: {embeddings.shape}")

    print(f"Total texts: {len(texts):,}")

    # ------------------------------------------------
    # TEXT LENGTH
    # ------------------------------------------------

    text_lengths = texts.apply(
        lambda x: len(x.split())
    )

    # ------------------------------------------------
    # EMPTY TEXTS
    # ------------------------------------------------

    empty_count = (text_lengths == 0).sum()

    print(f"\nEmpty texts: {empty_count}")

    # ------------------------------------------------
    # HASH DUPLICATES
    # ------------------------------------------------

    print("\nChecking exact duplicate texts...")

    hashes = texts.apply(hash_text)

    hash_counter = Counter(hashes)

    duplicate_hashes = {

        h: c

        for h, c in hash_counter.items()

        if c > 1
    }

    total_duplicate_texts = sum(

        c for c in duplicate_hashes.values()
    )

    print(f"Duplicate text groups: {len(duplicate_hashes)}")

    print(f"Total duplicated texts: {total_duplicate_texts}")

    # ------------------------------------------------
    # IDENTICAL EMBEDDINGS
    # ------------------------------------------------

    print("\nChecking identical embeddings...")

    embedding_hashes = [

        hashlib.md5(
            emb.tobytes()
        ).hexdigest()

        for emb in embeddings
    ]

    embedding_counter = Counter(
        embedding_hashes
    )

    duplicate_embeddings = {

        h: c

        for h, c in embedding_counter.items()

        if c > 1
    }

    total_duplicate_embeddings = sum(

        c for c in duplicate_embeddings.values()
    )

    print(
        f"Duplicate embedding groups: "
        f"{len(duplicate_embeddings)}"
    )

    print(
        f"Total duplicated embeddings: "
        f"{total_duplicate_embeddings}"
    )

    # ------------------------------------------------
    # UNIQUE RATIO
    # ------------------------------------------------

    unique_text_ratio = (

        texts.nunique() / len(texts)
    )

    print(
        f"\nUnique text ratio: "
        f"{unique_text_ratio:.4f}"
    )

    # ------------------------------------------------
    # TEXT LENGTH STATS
    # ------------------------------------------------

    print("\n==============================")
    print("TEXT LENGTH STATS")
    print("==============================\n")

    print(text_lengths.describe())

    # ------------------------------------------------
    # SAMPLE DUPLICATES
    # ------------------------------------------------

    print("\n==============================")
    print("TOP DUPLICATE TEXTS")
    print("==============================\n")

    duplicate_examples = []

    for dup_hash, count in sorted(

        duplicate_hashes.items(),

        key=lambda x: x[1],

        reverse=True

    )[:10]:

        sample_text = texts[

            hashes == dup_hash

        ].iloc[0]

        duplicate_examples.append({

            "count":
                count,

            "sample":
                sample_text[:300]
        })

        print(f"\nCOUNT: {count}")

        print(f"SAMPLE: {sample_text[:300]}")

        print("\n-------------------------")

    # ------------------------------------------------
    # COSINE MATRIX SAMPLE
    # ------------------------------------------------

    print("\nCalculating cosine sample...")

    sample_size = min(1000, len(embeddings))

    sample_embeddings = embeddings[:sample_size]

    cosine_matrix = cosine_similarity(
        sample_embeddings
    )

    upper_triangle = cosine_matrix[
        np.triu_indices(
            sample_size,
            k=1
        )
    ]

    # ------------------------------------------------
    # HISTOGRAM - COSINE
    # ------------------------------------------------

    plt.figure(figsize=(12, 6))

    # remove nan/inf

upper_triangle = upper_triangle[
    np.isfinite(upper_triangle)
]

# avoid histogram crash

if len(np.unique(upper_triangle)) > 1:

    plt.hist(
        upper_triangle,
        bins=50
    )

else:

    plt.hist(
        upper_triangle,
        bins=1
    )

    plt.title(
        f"Cosine Similarity Sample - {name}"
    )

    plt.xlabel("Cosine Similarity")

    plt.ylabel("Frequency")

    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_DIR}/{name}_cosine_validation.png"
    )

    plt.close()

    # ------------------------------------------------
    # HISTOGRAM - LENGTHS
    # ------------------------------------------------

    plt.figure(figsize=(12, 6))

    plt.hist(
        text_lengths,
        bins=50
    )

    plt.title(
        f"Text Length Distribution - {name}"
    )

    plt.xlabel("Word Count")

    plt.ylabel("Frequency")

    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_DIR}/{name}_length_distribution.png"
    )

    plt.close()

    # ------------------------------------------------
    # SAVE REPORT
    # ------------------------------------------------

    report = {

        "dataset":
            name,

        "total_texts":
            len(texts),

        "empty_texts":
            int(empty_count),

        "unique_text_ratio":
            float(unique_text_ratio),

        "duplicate_text_groups":
            len(duplicate_hashes),

        "total_duplicate_texts":
            int(total_duplicate_texts),

        "duplicate_embedding_groups":
            len(duplicate_embeddings),

        "total_duplicate_embeddings":
            int(total_duplicate_embeddings),

        "avg_text_length":
            float(text_lengths.mean()),

        "median_text_length":
            float(text_lengths.median()),

        "top_duplicate_examples":
            duplicate_examples
    }

    with open(

        f"{OUTPUT_DIR}/{name}_validation_report.json",

        "w"

    ) as f:

        json.dump(
            report,
            f,
            indent=4
        )

# ============================================================
# DONE
# ============================================================

print("\n===================================================")
print("EMBEDDING VALIDATION COMPLETED")
print("===================================================")

print(f"\nOutputs saved to: {OUTPUT_DIR}")

print("\nCosine sample stats:\n")

print(pd.Series(upper_triangle).describe())