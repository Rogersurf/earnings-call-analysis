import os
import re
import ast
import json
import numpy as np
import pandas as pd

from tqdm import tqdm

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# =========================================================
# CONFIG
# =========================================================

INPUT_PATH = "data/database/transcripts_clean.parquet"

OUTPUT_DIR = "outputs/chunks"

EMBEDDINGS_DIR = "outputs/embeddings"

os.makedirs(
    EMBEDDINGS_DIR,
    exist_ok=True
)

TEXT_COLUMNS = [
    "summary",
    "takeaways",
]

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

MIN_SENTENCES_PER_CHUNK = 3

SIMILARITY_THRESHOLD = 0.55

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

# =========================================================
# LOAD MODEL
# =========================================================

print(
    "\nLoading SentenceTransformer model...\n"
)

model = SentenceTransformer(
    MODEL_NAME
)

# =========================================================
# LOAD DATA
# =========================================================

print(
    "Loading dataset...\n"
)

df = pd.read_parquet(
    INPUT_PATH
)

print(df.shape)

# =========================================================
# CLEAN FUNCTIONS
# =========================================================

def clean_text(text):

    if pd.isna(text):

        return ""

    text = str(text)

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()

# =========================================================
# SENTENCE SPLIT
# =========================================================

def split_sentences(text):

    text = clean_text(text)

    if len(text) == 0:

        return []

    sentences = re.split(

        r'(?<=[.!?])\s+',

        text
    )

    sentences = [

        s.strip()

        for s in sentences

        if len(s.strip()) > 20
    ]

    return sentences

# =========================================================
# SEMANTIC CHUNKING
# =========================================================

def build_semantic_chunks(
    sentences
):

    if len(sentences) == 0:

        return []

    if len(sentences) <= MIN_SENTENCES_PER_CHUNK:

        return [
            " ".join(sentences)
        ]

    sentence_embeddings = model.encode(

        sentences,

        show_progress_bar=False,

        normalize_embeddings=True
    )

    chunks = []

    current_chunk = [
        sentences[0]
    ]

    current_embedding = (
        sentence_embeddings[0]
    )

    for i in range(
        1,
        len(sentences)
    ):

        sim = cosine_similarity(

            [current_embedding],

            [sentence_embeddings[i]]

        )[0][0]

        if sim >= SIMILARITY_THRESHOLD:

            current_chunk.append(
                sentences[i]
            )

            current_embedding = np.mean(

                sentence_embeddings[
                    max(
                        0,
                        i-len(current_chunk)+1
                    ):i+1
                ],

                axis=0
            )

        else:

            if len(current_chunk) >= MIN_SENTENCES_PER_CHUNK:

                chunks.append(

                    " ".join(
                        current_chunk
                    )
                )

            current_chunk = [
                sentences[i]
            ]

            current_embedding = (
                sentence_embeddings[i]
            )

    if len(current_chunk) > 0:

        chunks.append(

            " ".join(
                current_chunk
            )
        )

    return chunks

# =========================================================
# SPEAKER TURN PARSER
# =========================================================

def parse_speaker_turns(
    speaker_turns
):

    if pd.isna(speaker_turns):

        return []

    try:

        if isinstance(
            speaker_turns,
            str
        ):

            return json.loads(
                speaker_turns
            )

        return speaker_turns

    except Exception:

        return []

# =========================================================
# PROCESS
# =========================================================
all_embeddings = {

    "summary": [],

    "takeaways": [],

    "speaker_turn": [],
}

all_chunks = []

print(
    "\nStarting semantic chunking...\n"
)

for idx, row in tqdm(

    df.iterrows(),

    total=len(df)
):

    company = row.get(
        "company",
        ""
    )

    ticker = row.get(
        "ticker",
        ""
    )

    # =====================================================
    # SUMMARY + TAKEAWAYS
    # =====================================================

    for column in TEXT_COLUMNS:

        text = row.get(
            column,
            ""
        )

        text = clean_text(text)

        if len(text) < 50:

            continue

        sentences = split_sentences(
            text
        )

        if len(sentences) == 0:

            continue

        semantic_chunks = (
            build_semantic_chunks(
                sentences
            )
        )

        if len(semantic_chunks) == 0:

            continue

        chunk_embeddings = model.encode(

            semantic_chunks,

            show_progress_bar=False,

            normalize_embeddings=True
        )

        # =================================================
        # STORE EMBEDDINGS
        # =================================================

        all_embeddings[
            column
        ].extend(
            chunk_embeddings
        )

        for chunk_id, (
            chunk_text,
            emb
        ) in enumerate(

            zip(
                semantic_chunks,
                chunk_embeddings
            )
        ):

            all_chunks.append({

                "company": company,

                "ticker": ticker,

                "source_layer": column,

                "speaker": None,

                "speaker_type": None,

                "section": column,

                "sequence": None,

                "chunk_id": (
                    f"{ticker}_{column}_{chunk_id}"
                ),

                "chunk_text": chunk_text,

                "chunk_size_chars": len(
                    chunk_text
                ),

                "chunk_size_words": len(
                    chunk_text.split()
                ),
            })

    # =====================================================
    # SPEAKER-AWARE CHUNKING
    # =====================================================

    speaker_turns = parse_speaker_turns(

        row.get(
            "speaker_turns",
            "[]"
        )
    )

    for turn in speaker_turns:

        content = clean_text(

            turn.get(
                "content",
                ""
            )
        )

        if len(content) < 50:

            continue

        sentences = split_sentences(
            content
        )

        if len(sentences) == 0:

            continue

        semantic_chunks = (
            build_semantic_chunks(
                sentences
            )
        )

        if len(semantic_chunks) == 0:

            continue

        chunk_embeddings = model.encode(

            semantic_chunks,

            show_progress_bar=False,

            normalize_embeddings=True
        )

        # =================================================
        # STORE EMBEDDINGS
        # =================================================

        all_embeddings[
            "speaker_turn"
        ].extend(
            chunk_embeddings
        )

        for chunk_id, (
            chunk_text,
            emb
        ) in enumerate(

            zip(
                semantic_chunks,
                chunk_embeddings
            )
        ):

            all_chunks.append({

                "company": company,

                "ticker": ticker,

                "source_layer": "speaker_turn",

                "speaker": turn.get(
                    "speaker",
                    ""
                ),

                "speaker_type": turn.get(
                    "speaker_type",
                    ""
                ),

                "section": turn.get(
                    "section",
                    ""
                ),

                "sequence": turn.get(
                    "sequence",
                    None
                ),

                "chunk_id": (

                    f"{ticker}_"

                    f"{turn.get('sequence', 0)}_"

                    f"{chunk_id}"
                ),

                "chunk_text": chunk_text,

                "chunk_size_chars": len(
                    chunk_text
                ),

                "chunk_size_words": len(
                    chunk_text.split()
                ),
            })

chunks_df = pd.DataFrame(
    all_chunks
)

print(
    "\nFinal chunks dataframe:\n"
)

print(
    chunks_df.shape
)

# =========================================================
# SAVE PARQUET
# =========================================================

parquet_path = os.path.join(

    OUTPUT_DIR,

    "semantic_chunks_metadata.parquet"
)

chunks_df.to_parquet(
    parquet_path
)

# =========================================================
# SAVE SAMPLE CSV
# =========================================================

sample_path = os.path.join(

    OUTPUT_DIR,

    "semantic_chunks_sample.csv"
)

chunks_df.head(1000).to_csv(

    sample_path,

    index=False
)

print(
    "\nSaved outputs:\n"
)

print(parquet_path)

print(sample_path)

# =========================================================
# STATS
# =========================================================

print("\n==============================")

print("CHUNKING STATS")

print("==============================\n")

print(

    chunks_df[
        "source_layer"
    ].value_counts()
)

print(
    "\nAverage chunk size (words):\n"
)

print(

    chunks_df[
        "chunk_size_words"
    ].describe()
)

print(
    "\nTop companies by chunk count:\n"
)

print(

    chunks_df[
        "company"
    ]
    .value_counts()
    .head(20)
)

# =========================================================
# DISCOURSE STATS
# =========================================================

print(
    "\nSpeaker types:\n"
)

print(

    chunks_df[
        "speaker_type"
    ]
    .value_counts(
        dropna=False
    )
)

print(
    "\nSections:\n"
)

print(

    chunks_df[
        "section"
    ]
    .value_counts(
        dropna=False
    )
)

# =========================================================
# SAMPLE VALIDATION
# =========================================================

print(
    "\n=============================="
)

print(
    "SAMPLE CHUNKS"
)

print(
    "==============================\n"
)

print(

    chunks_df.sample(10)[

        [
            "ticker",
            "speaker",
            "speaker_type",
            "section",
            "chunk_text",
        ]
    ]
)

print(
    "\nSemantic chunking completed.\n"
)