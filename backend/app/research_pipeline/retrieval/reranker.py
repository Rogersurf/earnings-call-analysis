from typing import List, Dict


class FinancialReranker:

    """
    Lightweight financial retrieval reranker.

    Goal:
    improve semantic retrieval quality using:
    - section weighting
    - speaker weighting
    - semantic layer weighting
    """

    SECTION_WEIGHTS = {
        "prepared_remarks": 1.15,
        "qa_section": 1.0,
    }

    SPEAKER_TYPE_WEIGHTS = {
        "executive": 1.2,
        "analyst": 0.95,
        "operator": 0.8,
        "unknown": 1.0,
    }

    LAYER_WEIGHTS = {
        "speaker_turn": 1.15,
        "full_transcript": 1.0,
        "summary": 1.25,
        "takeaways": 1.3,
        "glossary": 0.9,
    }

    def rerank(
        self,
        results: List[Dict],
    ) -> List[Dict]:

        reranked_results = []

        for result in results:

            metadata = result.get(
                "metadata",
                {},
            )

            base_score = result.get(
                "score",
                0.0,
            )

            section = str(
                metadata.get(
                    "section",
                    "unknown",
                )
            ).lower()

            speaker_type = str(
                metadata.get(
                    "speaker_type",
                    "unknown",
                )
            ).lower()

            semantic_layer = str(
                metadata.get(
                    "semantic_layer",
                    "unknown",
                )
            ).lower()

            section_weight = (
                self.SECTION_WEIGHTS.get(
                    section,
                    1.0,
                )
            )

            speaker_weight = (
                self.SPEAKER_TYPE_WEIGHTS.get(
                    speaker_type,
                    1.0,
                )
            )

            layer_weight = (
                self.LAYER_WEIGHTS.get(
                    semantic_layer,
                    1.0,
                )
            )

            final_score = (
                base_score
                * section_weight
                * speaker_weight
                * layer_weight
            )

            result["reranked_score"] = final_score

            reranked_results.append(result)

        reranked_results.sort(
            key=lambda x: x["reranked_score"],
            reverse=True,
        )

        return reranked_results