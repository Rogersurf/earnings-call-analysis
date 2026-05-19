# ============================================================
# ADVANCED STREAMING EDA
# Earnings Call Semantic Intelligence Platform
# ============================================================

import os
import re
import json
import math
import pandas as pd

from collections import Counter

import matplotlib.pyplot as plt

# ============================================================
# CONFIG
# ============================================================

DATA_PATH = "data/database/transcripts_clean.parquet"

OUTPUT_DIR = "outputs/advanced_eda"

FIGURES_DIR = f"{OUTPUT_DIR}/figures"

TEXT_COLUMN = "transcript"

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
    "make", "made", "well", "being",
    "does", "doing", "done", "said",

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
    "good",
    "today",
    "joining",
    "joined",

    # scraping garbage

    "https",
    "http",
    "www",
    "fool",
    "foolcom",
    "motley",
    "motleyfool",
    "imageobject",
    "image",
    "source",
    "url",
    "org",
    "wiki",
    "cdn",
    "foolcdn",
    "transcribing",
    "com",
    "html",
    "est",

    # weak finance fillers

    "quarter",
    "year",
    "years",
    "company",
    "business",
    "market",
    "million"
}

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

    "company",
    "ticker",
    "quarter",
    "earnings_year",
    TEXT_COLUMN
]

missing = [

    c for c in required_columns
    if c not in df.columns
]

if missing:

    raise ValueError(
        f"Missing columns: {missing}"
    )

# ============================================================
# GLOBAL VARIABLES
# ============================================================

word_counter = Counter()

bigram_counter = Counter()

trigram_counter = Counter()

word_counts = []

lexical_diversities = []

entropy_scores = []

total_tokens = 0

# ============================================================
# TOKENIZER
# ============================================================

def tokenize(text):

    text = str(text).lower()

    text = re.sub(r"\s+", " ", text)

    words = re.findall(
        r"\b[a-zA-Z]{3,}\b",
        text
    )

    words = [

        w for w in words
        if w not in STOPWORDS
    ]

    return words

# ============================================================
# ENTROPY
# ============================================================

def calculate_entropy(tokens):

    if len(tokens) == 0:
        return 0

    counts = Counter(tokens)

    total = len(tokens)

    entropy = 0

    for freq in counts.values():

        p = freq / total

        entropy -= p * math.log2(p)

    return entropy

# ============================================================
# STREAMING ANALYSIS
# ============================================================

print("\nRunning advanced streaming NLP analysis...\n")

for idx, transcript in enumerate(df[TEXT_COLUMN]):

    tokens = tokenize(transcript)

    # --------------------------------
    # COUNTS
    # --------------------------------

    token_count = len(tokens)

    total_tokens += token_count

    word_counts.append(token_count)

    # --------------------------------
    # VOCABULARY
    # --------------------------------

    word_counter.update(tokens)

    # --------------------------------
    # BIGRAMS
    # --------------------------------

    bigrams = zip(tokens, tokens[1:])

    bigram_counter.update(bigrams)

    # --------------------------------
    # TRIGRAMS
    # --------------------------------

    trigrams = zip(
        tokens,
        tokens[1:],
        tokens[2:]
    )

    trigram_counter.update(trigrams)

    # --------------------------------
    # LEXICAL DIVERSITY
    # --------------------------------

    if token_count > 0:

        lexical_diversity = (
            len(set(tokens)) / token_count
        )

        lexical_diversities.append(
            lexical_diversity
        )

    # --------------------------------
    # ENTROPY
    # --------------------------------

    entropy = calculate_entropy(tokens)

    entropy_scores.append(entropy)

    # --------------------------------
    # PROGRESS
    # --------------------------------

    if idx % 500 == 0:

        print(
            f"Processed: {idx:,} transcripts"
        )

# ============================================================
# BASIC STATS
# ============================================================

print("\n==============================")
print("BASIC STATISTICS")
print("==============================")

stats = {

    "total_transcripts":
        len(df),

    "total_tokens":
        total_tokens,

    "avg_words":
        round(sum(word_counts) / len(word_counts), 2),

    "max_words":
        max(word_counts),

    "min_words":
        min(word_counts),

    "vocabulary_size":
        len(word_counter),

    "avg_lexical_diversity":
        round(sum(lexical_diversities) / len(lexical_diversities), 4),

    "avg_entropy":
        round(sum(entropy_scores) / len(entropy_scores), 4)
}

for k, v in stats.items():

    print(f"{k}: {v}")

# ============================================================
# TOP WORDS
# ============================================================

top_words = word_counter.most_common(100)

top_words_df = pd.DataFrame(
    top_words,
    columns=["word", "count"]
)

print("\nTop 30 words:\n")

print(top_words_df.head(30))

top_words_df.to_csv(
    f"{OUTPUT_DIR}/top_words.csv",
    index=False
)

# ============================================================
# TOP BIGRAMS
# ============================================================

top_bigrams = [

    (" ".join(k), v)

    for k, v in bigram_counter.most_common(100)
]

bigram_df = pd.DataFrame(
    top_bigrams,
    columns=["bigram", "count"]
)

print("\nTop 30 bigrams:\n")

print(bigram_df.head(30))

bigram_df.to_csv(
    f"{OUTPUT_DIR}/top_bigrams.csv",
    index=False
)

# ============================================================
# TOP TRIGRAMS
# ============================================================

top_trigrams = [

    (" ".join(k), v)

    for k, v in trigram_counter.most_common(100)
]

trigram_df = pd.DataFrame(
    top_trigrams,
    columns=["trigram", "count"]
)

print("\nTop 30 trigrams:\n")

print(trigram_df.head(30))

trigram_df.to_csv(
    f"{OUTPUT_DIR}/top_trigrams.csv",
    index=False
)

# ============================================================
# ZIPF DISTRIBUTION
# ============================================================

print("\nGenerating Zipf distribution...")

zipf_df = pd.DataFrame({

    "rank":
        range(1, len(word_counter) + 1),

    "frequency":
        [x[1] for x in word_counter.most_common()]
})

zipf_df.to_csv(
    f"{OUTPUT_DIR}/zipf_distribution.csv",
    index=False
)

plt.figure(figsize=(10, 6))

plt.loglog(
    zipf_df["rank"],
    zipf_df["frequency"]
)

plt.title("Zipf Distribution")

plt.xlabel("Rank")

plt.ylabel("Frequency")

plt.tight_layout()

plt.savefig(
    f"{FIGURES_DIR}/zipf_distribution.png"
)

plt.close()

# ============================================================
# HEAPS LAW
# ============================================================

print("\nGenerating Heaps Law plot...")

vocab_growth = []

running_vocab = set()

running_tokens = 0

for word, freq in word_counter.items():

    running_tokens += freq

    running_vocab.add(word)

    vocab_growth.append(
        (
            running_tokens,
            len(running_vocab)
        )
    )

heaps_df = pd.DataFrame(
    vocab_growth,
    columns=["tokens", "vocab_size"]
)

heaps_df.to_csv(
    f"{OUTPUT_DIR}/heaps_law.csv",
    index=False
)

plt.figure(figsize=(10, 6))

plt.plot(
    heaps_df["tokens"],
    heaps_df["vocab_size"]
)

plt.title("Heaps Law")

plt.xlabel("Tokens")

plt.ylabel("Vocabulary Size")

plt.tight_layout()

plt.savefig(
    f"{FIGURES_DIR}/heaps_law.png"
)

plt.close()

# ============================================================
# WORD DISTRIBUTION
# ============================================================

plt.figure(figsize=(12, 6))

plt.hist(
    word_counts,
    bins=50
)

plt.title(
    "Transcript Word Distribution"
)

plt.xlabel("Words")

plt.ylabel("Frequency")

plt.tight_layout()

plt.savefig(
    f"{FIGURES_DIR}/word_distribution.png"
)

plt.close()

# ============================================================
# LEXICAL DIVERSITY DISTRIBUTION
# ============================================================

plt.figure(figsize=(12, 6))

plt.hist(
    lexical_diversities,
    bins=50
)

plt.title(
    "Lexical Diversity Distribution"
)

plt.xlabel("Lexical Diversity")

plt.ylabel("Frequency")

plt.tight_layout()

plt.savefig(
    f"{FIGURES_DIR}/lexical_diversity.png"
)

plt.close()

# ============================================================
# ENTROPY DISTRIBUTION
# ============================================================

plt.figure(figsize=(12, 6))

plt.hist(
    entropy_scores,
    bins=50
)

plt.title(
    "Entropy Distribution"
)

plt.xlabel("Entropy")

plt.ylabel("Frequency")

plt.tight_layout()

plt.savefig(
    f"{FIGURES_DIR}/entropy_distribution.png"
)

plt.close()

# ============================================================
# COMPANY STATISTICS
# ============================================================

company_stats = df.groupby("company").size()

company_stats_df = pd.DataFrame({

    "company":
        company_stats.index,

    "transcript_count":
        company_stats.values
})

company_stats_df.to_csv(
    f"{OUTPUT_DIR}/company_statistics.csv",
    index=False
)

# ============================================================
# SAVE REPORT
# ============================================================

report = {

    "statistics":
        stats,

    "top_words":
        top_words[:30],

    "top_bigrams":
        top_bigrams[:30],

    "top_trigrams":
        top_trigrams[:30]
}

with open(
    f"{OUTPUT_DIR}/advanced_report.json",
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
print("ADVANCED EDA COMPLETED")
print("==============================")

print(f"\nOutputs: {OUTPUT_DIR}")

print(f"Figures: {FIGURES_DIR}")