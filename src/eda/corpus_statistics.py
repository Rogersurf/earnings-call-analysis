# ============================================================
# CORPUS STATISTICS
# Earnings Call Semantic Intelligence Platform
# ============================================================

import os
import re
import json
import pandas as pd

from collections import Counter

import matplotlib.pyplot as plt

# ============================================================
# CONFIG
# ============================================================

DATA_PATH = "data/database/transcripts_clean.parquet"

OUTPUT_DIR = "outputs/eda"
FIGURES_DIR = "outputs/figures"

DATE_COLUMN = "call_date"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)

# ============================================================
# LOAD DATASET
# ============================================================

print("\nLoading dataset...")

df = pd.read_parquet(DATA_PATH)

print(f"Dataset loaded: {len(df):,} rows")

# ============================================================
# DATASET STRUCTURE
# ============================================================

print("\n==============================")
print("DATASET STRUCTURE")
print("==============================")

print(df.info())

# ============================================================
# REQUIRED COLUMNS
# ============================================================

required_columns = [
    "company",
    "ticker",
    "quarter",
    "earnings_year",
    DATE_COLUMN,
    "transcript"
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
# SAMPLE ROW
# ============================================================

print("\n==============================")
print("SAMPLE ROW")
print("==============================")

print(
    df.iloc[0][
        [
            "company",
            "ticker",
            "quarter",
            "earnings_year"
        ]
    ]
)

# ============================================================
# TRANSCRIPT VALIDATION
# ============================================================

print("\n==============================")
print("TRANSCRIPT VALIDATION")
print("==============================")

empty_transcripts = (
    df["transcript"]
    .astype(str)
    .str.len()
    .eq(0)
    .sum()
)

print(f"Empty transcripts: {empty_transcripts:,}")

# ============================================================
# LIGHT TEXT NORMALIZATION
# ============================================================

# IMPORTANT:
# Dataset already cleaned.
# We ONLY normalize for statistics.

def normalize_text(text):

    text = str(text).lower()

    text = re.sub(r"\s+", " ", text)

    return text.strip()

print("\nNormalizing text...")

df["normalized_text"] = (
    df["transcript"]
    .apply(normalize_text)
)

# ============================================================
# WORD COUNTS
# ============================================================

print("\nCalculating word counts...")

df["word_count"] = (
    df["normalized_text"]
    .apply(lambda x: len(x.split()))
)

# ============================================================
# WORD COUNT DISTRIBUTION
# ============================================================

print("\n==============================")
print("WORD COUNT DISTRIBUTION")
print("==============================")

print(df["word_count"].describe())

# ============================================================
# BASIC STATISTICS
# ============================================================

stats = {

    "total_transcripts":
        int(len(df)),

    "total_companies":
        int(df["company"].nunique()),

    "total_tickers":
        int(df["ticker"].nunique()),

    "total_years":
        int(df["earnings_year"].nunique()),

    "avg_words":
        round(df["word_count"].mean(), 2),

    "median_words":
        round(df["word_count"].median(), 2),

    "std_words":
        round(df["word_count"].std(), 2),

    "max_words":
        int(df["word_count"].max()),

    "min_words":
        int(df["word_count"].min())
}

print("\n==============================")
print("BASIC STATISTICS")
print("==============================")

for k, v in stats.items():

    print(f"{k}: {v}")

# ============================================================
# VOCABULARY ANALYSIS
# ============================================================

print("\n==============================")
print("VOCABULARY ANALYSIS")
print("==============================")

vocab_counter = Counter()

for text in df["normalized_text"]:

    vocab_counter.update(text.split())

vocab_size = len(vocab_counter)

print(f"Vocabulary size: {vocab_size:,}")

top_words = vocab_counter.most_common(100)

top_words_df = pd.DataFrame(
    top_words,
    columns=["word", "frequency"]
)

print("\nTop 20 words:")

print(top_words_df.head(20))

top_words_df.to_csv(
    f"{OUTPUT_DIR}/top_words.csv",
    index=False
)

# ============================================================
# TEMPORAL ANALYSIS
# ============================================================

print("\n==============================")
print("TEMPORAL ANALYSIS")
print("==============================")

df[DATE_COLUMN] = pd.to_datetime(
    df[DATE_COLUMN],
    errors="coerce"
)

df["year"] = df[DATE_COLUMN].dt.year

year_counts = (
    df["year"]
    .value_counts()
    .sort_index()
)

year_counts_df = pd.DataFrame({
    "year": year_counts.index,
    "count": year_counts.values
})

print(year_counts_df)

year_counts_df.to_csv(
    f"{OUTPUT_DIR}/transcripts_per_year.csv",
    index=False
)

# ============================================================
# QUARTER ANALYSIS
# ============================================================

print("\n==============================")
print("QUARTER ANALYSIS")
print("==============================")

quarter_counts = (
    df["quarter"]
    .value_counts()
)

quarter_counts_df = pd.DataFrame({
    "quarter": quarter_counts.index,
    "count": quarter_counts.values
})

print(quarter_counts_df)

quarter_counts_df.to_csv(
    f"{OUTPUT_DIR}/transcripts_per_quarter.csv",
    index=False
)

# ============================================================
# COMPANY ANALYSIS
# ============================================================

print("\n==============================")
print("COMPANY ANALYSIS")
print("==============================")

company_counts = (
    df["company"]
    .value_counts()
    .head(50)
)

company_counts_df = pd.DataFrame({
    "company": company_counts.index,
    "count": company_counts.values
})

print(company_counts_df.head(20))

company_counts_df.to_csv(
    f"{OUTPUT_DIR}/top_companies.csv",
    index=False
)

# ============================================================
# SHORT TRANSCRIPTS
# ============================================================

print("\n==============================")
print("QUALITY CHECK")
print("==============================")

short_transcripts = df[
    df["word_count"] < 500
]

print(f"Short transcripts (<500 words): {len(short_transcripts):,}")

# ============================================================
# HISTOGRAM - WORD COUNTS
# ============================================================

print("\nGenerating figures...")

plt.figure(figsize=(12, 6))

plt.hist(
    df["word_count"],
    bins=50
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
# HISTOGRAM - TRANSCRIPTS PER YEAR
# ============================================================

plt.figure(figsize=(12, 6))

year_counts.plot(kind="bar")

plt.title("Transcripts per Year")

plt.xlabel("Year")

plt.ylabel("Count")

plt.tight_layout()

plt.savefig(
    f"{FIGURES_DIR}/transcripts_per_year.png"
)

plt.close()

# ============================================================
# TOP WORDS CHART
# ============================================================

top20 = top_words_df.head(20)

plt.figure(figsize=(12, 8))

plt.barh(
    top20["word"][::-1],
    top20["frequency"][::-1]
)

plt.title("Top 20 Most Frequent Words")

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

    "basic_statistics":
        stats,

    "vocabulary_size":
        int(vocab_size),

    "top_20_words":
        top_words[:20]
}

with open(
    f"{OUTPUT_DIR}/corpus_report.json",
    "w"
) as f:

    json.dump(
        report,
        f,
        indent=4
    )

# ============================================================
# FINAL MESSAGE
# ============================================================

print("\n==============================")
print("EDA COMPLETED")
print("==============================")

print(f"\nOutputs saved to: {OUTPUT_DIR}")

print(f"Figures saved to: {FIGURES_DIR}")

print("\nGenerated files:")

generated_files = [

    "top_words.csv",
    "top_companies.csv",
    "transcripts_per_year.csv",
    "transcripts_per_quarter.csv",
    "corpus_report.json",
    "word_count_distribution.png",
    "transcripts_per_year.png",
    "top_words.png"
]

for file in generated_files:

    print(f" - {file}")