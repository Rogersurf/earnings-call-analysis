# ============================================================
# FILE:
# backend/app/research_pipeline/signals/propagation_engine.py
# ============================================================

from collections import defaultdict

from backend.app.research_pipeline.signals.signal_extractor import (
    SignalExtractor,
)

from backend.app.research_pipeline.signals.business_ontology import (
    BUSINESS_TARGET_MAP,
)


class PropagationEngine:

    """
    Generate semantic propagation
    intelligence from retrieval results.
    """

    def __init__(self):

        self.extractor = SignalExtractor()

    def analyze_results(
        self,
        retrieval_results,
    ):

        propagation_scores = defaultdict(float)

        signal_details = []

        for result in retrieval_results:

            text = result.get(
                "text",
                ""
            )

            metadata = result.get(
                "metadata",
                {}
            )

            semantic_score = result.get(
                "score",
                0.0
            )

            extracted_signals = (
                self.extractor.extract(text)
            )

            for signal_name, signal_strength in (
                extracted_signals.items()
            ):

                target = BUSINESS_TARGET_MAP.get(
                    signal_name,
                    "Unknown",
                )

                weighted_score = (
                    signal_strength
                    * semantic_score
                )

                propagation_scores[target] += (
                    weighted_score
                )

                signal_details.append(
                    {
                        "signal": signal_name,
                        "target": target,
                        "company": metadata.get(
                            "company"
                        ),
                        "ticker": metadata.get(
                            "ticker"
                        ),
                        "semantic_score": semantic_score,
                        "signal_strength": signal_strength,
                        "weighted_score": weighted_score,
                    }
                )

        ranked_targets = sorted(
            propagation_scores.items(),
            key=lambda x: x[1],
            reverse=True,
        )

        return {
            "ranked_targets": ranked_targets,
            "signal_details": signal_details,
        }