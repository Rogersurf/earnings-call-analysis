# ============================================================
# TRANSCRIPT LINGUISTIC ANALYSIS
# Earnings Call Semantic Intelligence Platform
# ============================================================

import os
import re
import json
import pandas as pd

from collections import Counter

import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import CountVectorizer

from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

# ============================================================
# CONFIG
# ============================================================

DATA_PATH = "data/database/transcripts_clean.parquet"

OUTPUT_DIR = "outputs/eda/transcript_analysis"
FIGURES_DIR = "outputs/figures/transcript_analysis"

TEXT_COLUMN = "transcript"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)

# ============================================================
# LOAD DATA
# ============================================================

print("\nLoading transcripts dataset...")

df = pd.read_parquet(DATA_PATH)

print(f"Dataset loaded: {len(df):,} rows")

# ============================================================
# VALIDATION
# ============================================================

required_columns = [
    "company",
    "ticker",
    "quarter",
    "earnings_year",
    TEXT_COLUMN
]

missing_cols = [
    c for c in required_columns
    if c not in df.columns
]

if missing_cols:

    raise ValueError(
        f"Missing required columns: {missing_cols}"
    )

# ============================================================
# TRANSCRIPT NORMALIZATION
# ============================================================

def normalize_text(text):

    text = str(text).lower()

    text = re.sub(r"\n", " ", text)

    text = re.sub(r"\r", " ", text)

    text = re.sub(r"\t", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()

print("\nNormalizing transcripts...")

df["normalized_transcript"] = (
    df[TEXT_COLUMN]
    .astype(str)
    .apply(normalize_text)
)

# ============================================================
# WORD COUNTS
# ============================================================

print("\nCalculating transcript sizes...")

df["word_count"] = (
    df["normalized_transcript"]
    .apply(lambda x: len(x.split()))
)

print("\n==============================")
print("WORD COUNT DISTRIBUTION")
print("==============================")

print(df["word_count"].describe())

# ============================================================
# STOPWORDS
# ============================================================

financial_stopwords = {

    "operator",
    "morning",
    "afternoon",
    "thank",
    "thanks",
    "please",
    "conference",
    "call",
    "questions",
    "question",
    "answer",
    "answers",
    "quarter",
    "year",
    "good",
    "today",
    "joining",
    "joined"
}

stopwords = set(ENGLISH_STOP_WORDS)

stopwords.update(financial_stopwords)

# ============================================================
# TOKENIZATION
# ============================================================

print("\nTokenizing transcripts...")

vocab_counter = Counter()

for text in df["normalized_transcript"]:

    words = re.findall(r"\b[a-zA-Z]{3,}\b", text)

    filtered_words = [

        word for word in words

        if word not in stopwords
    ]

    vocab_counter.update(filtered_words)

# ============================================================
# VOCABULARY
# ============================================================

print("\n==============================")
print("VOCABULARY ANALYSIS")
print("==============================")

vocab_size = len(vocab_counter)

print(f"Vocabulary size: {vocab_size:,}")

top_words = vocab_counter.most_common(100)

top_words_df = pd.DataFrame(
    top_words,
    columns=["word", "frequency"]
)

print("\nTop 30 meaningful words:")

print(top_words_df.head(30))

top_words_df.to_csv(
    f"{OUTPUT_DIR}/top_meaningful_words.csv",
    index=False
)

# ============================================================
# BIGRAM ANALYSIS
# ============================================================

print("\nRunning bigram analysis...")

vectorizer_bigram = CountVectorizer(

    stop_words=list(stopwords),

    ngram_range=(2, 2),

    max_features=100,

    min_df=10
)

X_bigram = vectorizer_bigram.fit_transform(
    df["normalized_transcript"]
)

bigram_counts = X_bigram.sum(axis=0).A1

bigram_df = pd.DataFrame({

    "bigram":
        vectorizer_bigram.get_feature_names_out(),

    "count":
        bigram_counts
})

bigram_df = bigram_df.sort_values(
    by="count",
    ascending=False
)

print("\nTop 30 bigrams:")

print(bigram_df.head(30))

bigram_df.to_csv(
    f"{OUTPUT_DIR}/top_bigrams.csv",
    index=False
)

# ============================================================
# TRIGRAM ANALYSIS
# ============================================================

print("\nRunning trigram analysis...")

vectorizer_trigram = CountVectorizer(

    stop_words=list(stopwords),

    ngram_range=(3, 3),

    max_features=100,

    min_df=10
)

X_trigram = vectorizer_trigram.fit_transform(
    df["normalized_transcript"]
)

trigram_counts = X_trigram.sum(axis=0).A1

trigram_df = pd.DataFrame({

    "trigram":
        vectorizer_trigram.get_feature_names_out(),

    "count":
        trigram_counts
})

trigram_df = trigram_df.sort_values(
    by="count",
    ascending=False
)

print("\nTop 30 trigrams:")

print(trigram_df.head(30))

trigram_df.to_csv(
    f"{OUTPUT_DIR}/top_trigrams.csv",
    index=False
)

# ============================================================
# COMPANY ANALYSIS
# ============================================================

print("\nRunning company analysis...")

company_counts = (
    df["company"]
    .value_counts()
    .head(50)
)

company_df = pd.DataFrame({

    "company":
        company_counts.index,

    "count":
        company_counts.values
})

company_df.to_csv(
    f"{OUTPUT_DIR}/top_companies.csv",
    index=False
)

# ============================================================
# LONGEST TRANSCRIPTS
# ============================================================

longest_df = df[[
    "company",
    "ticker",
    "earnings_year",
    "quarter",
    "word_count"
]].sort_values(
    by="word_count",
    ascending=False
)

longest_df.head(100).to_csv(
    f"{OUTPUT_DIR}/longest_transcripts.csv",
    index=False
)

# ============================================================
# FIGURE - WORD DISTRIBUTION
# ============================================================

print("\nGenerating figures...")

plt.figure(figsize=(12, 6))

plt.hist(
    df["word_count"],
    bins=60
)

plt.title("Transcript Word Count Distribution")

plt.xlabel("Word Count")

plt.ylabel("Frequency")

plt.tight_layout()

plt.savefig(
    f"{FIGURES_DIR}/word_count_distribution.png"
)

plt.close()

# ============================================================
# FIGURE - TOP WORDS
# ============================================================

top20 = top_words_df.head(20)

plt.figure(figsize=(12, 8))

plt.barh(
    top20["word"][::-1],
    top20["frequency"][::-1]
)

plt.title("Top 20 Meaningful Financial Terms")

plt.xlabel("Frequency")

plt.tight_layout()

plt.savefig(
    f"{FIGURES_DIR}/top_words.png"
)

plt.close()

# ============================================================
# SAVE REPORT
# ============================================================

report = {

    "total_transcripts":
        int(len(df)),

    "vocabulary_size":
        int(vocab_size),

    "avg_words":
        round(df["word_count"].mean(), 2),

    "median_words":
        round(df["word_count"].median(), 2),

    "top_words":
        top_words[:30]
}

with open(
    f"{OUTPUT_DIR}/transcript_report.json",
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
print("TRANSCRIPT ANALYSIS COMPLETED")
print("==============================")

print(f"\nOutputs saved to: {OUTPUT_DIR}")

print(f"Figures saved to: {FIGURES_DIR}")