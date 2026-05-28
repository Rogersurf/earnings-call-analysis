# ============================================================
# FILE:
# backend/app/research_pipeline/signals/semantic_signal_mapper.py
# ============================================================

from typing import Dict


class SemanticSignalMapper:

    """
    Map implicit business semantics
    into propagation-aware signals.
    """

    SEMANTIC_SIGNAL_MAP = {

        "cloud_capacity": [

            "generative ai",

            "ai workloads",

            "enterprise ai",

            "ai infrastructure",

            "compute demand",

            "gpu demand",

            "compute scaling",

            "model training",

            "inference demand",

            "datacenter buildout",

            "high performance compute",

            "accelerator demand",

            "cluster expansion",

            "cloud expansion",

            "ai deployment",

            "server expansion",

            "infrastructure investments",
        ],

        "server_cpu_demand": [

            "server refresh",

            "enterprise infrastructure",

            "compute expansion",

            "cloud compute",

            "server demand",

            "data center growth",

            "datacenter growth",

            "server infrastructure",

            "enterprise workloads",
        ],

        "foundry_manufacturing": [

            "advanced packaging",

            "process node",

            "wafer capacity",

            "semiconductor production",

            "chip manufacturing",

            "yield improvement",

            "fab expansion",
        ],

        "margin_pressure": [

            "pricing pressure",

            "gross margin compression",

            "cost optimization",

            "operating leverage",

            "margin headwinds",

            "cost reductions",
        ],

        "supply_pressure": [

            "component shortages",

            "inventory normalization",

            "supply constraints",

            "allocation pressure",

            "supply imbalance",

            "capacity constraints",
        ],
    }

    def normalize(
        self,
        text: str,
    ) -> str:

        return str(text).lower()

    def map_semantic_signals(
        self,
        text: str,
    ) -> Dict:

        normalized_text = (
            self.normalize(text)
        )

        mapped_signals = {}

        for signal_name, semantic_patterns in (
            self.SEMANTIC_SIGNAL_MAP.items()
        ):

            score = 0

            for pattern in semantic_patterns:

                if pattern in normalized_text:

                    score += 1

            if score > 0:

                mapped_signals[
                    signal_name
                ] = score

        return mapped_signals