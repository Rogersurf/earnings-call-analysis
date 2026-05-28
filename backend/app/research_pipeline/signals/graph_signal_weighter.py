# ============================================================
# FILE:
# backend/app/research_pipeline/signals/graph_signal_weighter.py
# ============================================================

from backend.app.research_pipeline.signals.signal_extractor import (
    SignalExtractor
)


class GraphSignalWeighter:

    """
    Enrich graph relationships using
    business propagation signals.
    """

    def __init__(self):

        self.extractor = SignalExtractor()

    def compute_signal_overlap(
        self,
        source_text: str,
        target_text: str,
    ):

        source_signals = self.extractor.extract(
            source_text
        )

        target_signals = self.extractor.extract(
            target_text
        )

        overlap = set(
            source_signals.keys()
        ).intersection(
            set(target_signals.keys())
        )

        overlap_score = 0.0

        for signal in overlap:

            overlap_score += (
                source_signals[signal]
                + target_signals[signal]
            )

        return {
            "shared_signals": list(overlap),
            "overlap_score": overlap_score,
        }

    def weight_edges(
        self,
        nodes,
        edges,
    ):

        node_lookup = {
            node["node_id"]: node
            for node in nodes
        }

        enriched_edges = []

        for edge in edges:

            source_id = edge["source"]

            target_id = edge["target"]

            source_node = node_lookup.get(
                source_id
            )

            target_node = node_lookup.get(
                target_id
            )

            if not source_node or not target_node:
                continue

            signal_analysis = (
                self.compute_signal_overlap(
                    source_node["text"],
                    target_node["text"],
                )
            )

            enriched_edge = {
                **edge,

                "shared_signals": (
                    signal_analysis[
                        "shared_signals"
                    ]
                ),

                "signal_overlap_score": (
                    signal_analysis[
                        "overlap_score"
                    ]
                ),
            }

            enriched_edges.append(
                enriched_edge
            )

        return enriched_edges