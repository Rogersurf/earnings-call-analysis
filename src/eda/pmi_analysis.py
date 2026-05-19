# ============================================================
# PMI ANALYSIS
# Financial Semantic Collocation Discovery
# ============================================================

import os
import re
import math
import json
import pandas as pd

from collections import Counter

import matplotlib.pyplot as plt

# ============================================================
# CONFIG
# ============================================================

DATA_PATH = "data/database/transcripts_clean.parquet"

OUTPUT_DIR = "outputs/pmi_analysis"

FIGURES_DIR = f"{OUTPUT_DIR}/figures"

TEXT_COLUMN = "transcript"

MIN_WORD_FREQ = 20

MIN_BIGRAM_FREQ = 100

MAX_PMI = 15

TOP_N = 200

os.makedirs(OUTPUT_DIR, exist_ok=True)

os.makedirs(FIGURES_DIR, exist_ok=True)

# ============================================================
# STOPWORDS
# ============================================================

STOPWORDS = {

    # generic english

    "the", "and", "for", "that", "with",
    "this", "from", "have", "will", "your",
    "about", "there", "their", "would",
    "could", "should", "into", "than",
    "then", "they", "them", "been",
    "were", "what", "when", "where",
    "which", "while", "because",

    "just", "very", "some", "more",
    "like", "really", "know", "think",
    "going", "much", "many", "also",

    # earnings call garbage

    "operator",
    "morning",
    "afternoon",
    "conference",
    "call",
    "question",
    "questions",
    "answer",
    "answers",
    "thank",
    "thanks",
    "please",

    # scraping garbage

    "https",
    "http",
    "www",
    "fool",
    "motley",
    "imageobject",
    "image",
    "source",
    "url",
    "org",
    "wiki",
    "cdn",
    "transcribing",
    "datepublished",
    "datemodified",
    "tickersymbol",

    # weak fillers

    "company",
    "business",
    "market",
    "quarter",
    "year",
    "million"
}

# ============================================================
# BAD TERMS
# ============================================================

BAD_TERMS = {

    "chief",
    "officer",
    "executive",
    "president",
    "analyst",
    "operator",
    "email",
    "protected",
    "chairman",
    "vice",
    "line",
    "next",
    "comes",
    "person",
    "author",
    "name"
}

# ============================================================
# TOKENIZER
# ============================================================

def tokenize(text):

    text = str(text).lower()

    text = re.sub(r"\s+", " ", text)

    tokens = re.findall(
        r"\b[a-zA-Z]{3,}\b",
        text
    )

    tokens = [

        t for t in tokens

        if t not in STOPWORDS
    ]

    return tokens

# ============================================================
# LOAD DATA
# ============================================================

print("\nLoading dataset...")

df = pd.read_parquet(DATA_PATH)

print(f"Dataset loaded: {len(df):,} rows")

# ============================================================
# COUNTERS
# ============================================================

word_counter = Counter()

bigram_counter = Counter()

total_tokens = 0

# ============================================================
# STREAMING PREPARATION
# ============================================================

print("\nRunning streaming PMI preparation...\n")

for idx, transcript in enumerate(df[TEXT_COLUMN]):

    tokens = tokenize(transcript)

    total_tokens += len(tokens)

    # --------------------------------
    # WORD COUNTS
    # --------------------------------

    word_counter.update(tokens)

    # --------------------------------
    # BIGRAM COUNTS
    # --------------------------------

    bigrams = zip(tokens, tokens[1:])

    bigram_counter.update(bigrams)

    # --------------------------------
    # PROGRESS
    # --------------------------------

    if idx % 500 == 0:

        print(f"Processed: {idx:,}")

# ============================================================
# VALID WORDS
# ============================================================

print("\nFiltering low-frequency terms...")

valid_words = {

    word

    for word, freq in word_counter.items()

    if freq >= MIN_WORD_FREQ
}

# ============================================================
# PMI CALCULATION
# ============================================================

print("\nCalculating PMI scores...\n")

results = []

for (w1, w2), bigram_freq in bigram_counter.items():

    # --------------------------------
    # FREQUENCY FILTERS
    # --------------------------------

    if bigram_freq < MIN_BIGRAM_FREQ:

        continue

    if w1 not in valid_words:

        continue

    if w2 not in valid_words:

        continue

    # --------------------------------
    # BAD TERMS FILTER
    # --------------------------------

    if w1 in BAD_TERMS:

        continue

    if w2 in BAD_TERMS:

        continue

    # --------------------------------
    # PROBABILITIES
    # --------------------------------

    p_w1 = word_counter[w1] / total_tokens

    p_w2 = word_counter[w2] / total_tokens

    p_bigram = bigram_freq / total_tokens

    # --------------------------------
    # PMI
    # --------------------------------

    pmi = math.log2(
        p_bigram / (p_w1 * p_w2)
    )

    # --------------------------------
    # REMOVE EXTREME PMI
    # --------------------------------

    if pmi > MAX_PMI:

        continue

    results.append({

        "bigram":
            f"{w1} {w2}",

        "frequency":
            bigram_freq,

        "pmi":
            round(pmi, 4)
    })

# ============================================================
# DATAFRAME
# ============================================================

pmi_df = pd.DataFrame(results)

pmi_df = pmi_df.sort_values(
    by="pmi",
    ascending=False
)

# ============================================================
# SAVE CSV
# ============================================================

pmi_df.to_csv(
    f"{OUTPUT_DIR}/pmi_results.csv",
    index=False
)

# ============================================================
# TOP RESULTS
# ============================================================

top_pmi = pmi_df.head(TOP_N)

print("\n==============================")
print("TOP PMI BIGRAMS")
print("==============================\n")

print(top_pmi.head(50))

# ============================================================
# PMI HISTOGRAM
# ============================================================

plt.figure(figsize=(12, 6))

plt.hist(
    pmi_df["pmi"],
    bins=50
)

plt.title("PMI Distribution")

plt.xlabel("PMI Score")

plt.ylabel("Frequency")

plt.tight_layout()

plt.savefig(
    f"{FIGURES_DIR}/pmi_distribution.png"
)

plt.close()

# ============================================================
# TOP PMI BARPLOT
# ============================================================

top20 = top_pmi.head(20)

plt.figure(figsize=(12, 8))

plt.barh(
    top20["bigram"][::-1],
    top20["pmi"][::-1]
)

plt.title("Top PMI Financial Bigrams")

plt.xlabel("PMI Score")

plt.tight_layout()

plt.savefig(
    f"{FIGURES_DIR}/top_pmi_bigrams.png"
)

plt.close()

# ============================================================
# REPORT
# ============================================================

report = {

    "total_tokens":
        total_tokens,

    "total_unique_words":
        len(word_counter),

    "total_bigrams":
        len(bigram_counter),

    "filtered_bigrams":
        len(pmi_df),

    "top_pmi":
        top_pmi.head(30).to_dict(
            orient="records"
        )
}

with open(
    f"{OUTPUT_DIR}/pmi_report.json",
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

print("\n==============================")
print("PMI ANALYSIS COMPLETED")
print("==============================")

print(f"\nOutputs: {OUTPUT_DIR}")

print(f"Figures: {FIGURES_DIR}")