from pathlib import Path

import pandas as pd

# ======================================================
# FIND ALL PARQUETS
# ======================================================

parquet_files = sorted(
    Path(".").rglob("*.parquet")
)

registry = []

# ======================================================
# LOOP FILES
# ======================================================

for parquet_path in parquet_files:

    try:

        df = pd.read_parquet(parquet_path)

        registry.append({

            "file":
                str(parquet_path),

            "rows":
                len(df),

            "columns":
                len(df.columns),

            "column_names":
                ", ".join(df.columns[:10]),

            "has_embedding":
                any(
                    "embed" in c.lower()
                    for c in df.columns
                ),

            "has_text":
                any(
                    c.lower() in [
                        "text",
                        "chunk",
                        "content",
                        "transcript"
                    ]
                    for c in df.columns
                ),

            "has_company":
                any(
                    "company" in c.lower()
                    for c in df.columns
                ),

            "has_sector":
                any(
                    "sector" in c.lower()
                    for c in df.columns
                ),

        })

    except Exception as error:

        registry.append({

            "file": str(parquet_path),
            "error": str(error)

        })

# ======================================================
# EXPORT
# ======================================================

registry_df = pd.DataFrame(registry)

output_path = "parquet_registry.csv"

registry_df.to_csv(
    output_path,
    index=False
)

print("\nRegistry exported:")
print(output_path)