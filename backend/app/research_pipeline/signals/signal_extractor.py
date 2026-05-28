# ============================================================
# FILE:
# backend/app/research_pipeline/signals/signal_extractor.py
# ============================================================

import re

from typing import Dict

from backend.app.research_pipeline.signals.business_ontology import (
    SIGNAL_DEFINITIONS,
)

from backend.app.research_pipeline.signals.semantic_signal_mapper import (
    SemanticSignalMapper
)


class SignalExtractor:

    """
    Extract business propagation signals
    from semantic retrieval chunks.
    """

    def __init__(self):

        self.semantic_mapper = (
            SemanticSignalMapper()
        )

    @staticmethod
    def normalize_text(
        text: str,
    ) -> str:

        return str(text).lower()

    @staticmethod
    def count_matches(
        text: str,
        terms: list,
    ) -> int:

        total = 0

        for term in terms:

            pattern = (
                r"(?<![A-Za-z0-9])"
                + re.escape(term)
                + r"(?![A-Za-z0-9])"
            )

            matches = re.findall(
                pattern,
                text,
                flags=re.IGNORECASE,
            )

            total += len(matches)

        return total

    @staticmethod
    def contains_any(
        text: str,
        terms: list,
    ) -> bool:

        text = str(text).lower()

        return any(
            term.lower() in text
            for term in terms
        )

    def extract(
        self,
        text: str,
    ) -> Dict:

        text = self.normalize_text(text)

        extracted = {}

        # ====================================================
        # EXPLICIT SIGNAL EXTRACTION
        # ====================================================

        for signal_name, config in SIGNAL_DEFINITIONS.items():

            keywords = config["keywords"]

            context_terms = config["context_terms"]

            keyword_score = self.count_matches(
                text,
                keywords,
            )

            has_context = self.contains_any(
                text,
                context_terms,
            )

            if keyword_score > 0 and has_context:

                extracted[
                    signal_name
                ] = keyword_score

        # ====================================================
        # IMPLICIT SEMANTIC SIGNAL EXTRACTION
        # ====================================================

        semantic_signals = (
            self.semantic_mapper.map_semantic_signals(
                text
            )
        )

        for signal_name, score in (
            semantic_signals.items()
        ):

            if signal_name not in extracted:

                extracted[
                    signal_name
                ] = 0

            extracted[
                signal_name
            ] += score

        return extracted