from typing import List, Dict, Any
import json

from backend.app.research_pipeline.ingestion.speaker_parser import (
    SpeakerNormalizer
)


class SemanticDocumentRouter:

    COLLECTIONS = {
        "summary": "earnings_summary",
        "takeaways": "earnings_takeaways",
        "full_transcript": "earnings_full_transcript",
        "speaker_turns": "earnings_speaker_turns",
        "glossary": "earnings_glossary",
    }

    def __init__(self):

        self.speaker_normalizer = (
            SpeakerNormalizer()
        )

    @staticmethod
    def base_metadata(
        row: Dict[str, Any]
    ) -> Dict:

        return {
            "ticker": row.get("ticker"),
            "company": row.get("company"),
            "quarter": row.get("quarter"),
            "earnings_year": row.get(
                "earnings_year"
            ),
            "call_date": row.get(
                "call_date"
            ),
        }

    def route_row(
        self,
        row: Dict[str, Any],
    ) -> List[Dict]:

        documents = []

        semantic_fields = [
            "summary",
            "takeaways",
            "full_transcript",
            "glossary",
        ]

        for field in semantic_fields:

            content = row.get(field)

            if not content:
                continue

            if str(content).strip() == "":
                continue

            documents.append(
                {
                    "collection": self.COLLECTIONS[
                        field
                    ],
                    "text": str(content),
                    "metadata": {
                        **self.base_metadata(
                            row
                        ),
                        "semantic_layer": field,
                    },
                }
            )

        speaker_turns = row.get(
            "speaker_turns"
        )

        if speaker_turns:

            try:

                if isinstance(
                    speaker_turns,
                    str,
                ):

                    speaker_turns = json.loads(
                        speaker_turns
                    )

                for turn in speaker_turns:

                    turn = (
                        self.speaker_normalizer.normalize(
                            turn
                        )
                    )

                    content = turn.get(
                        "content"
                    )

                    if not content:
                        continue

                    if (
                        str(content).strip()
                        == ""
                    ):
                        continue

                    documents.append(
                        {
                            "collection": self.COLLECTIONS[
                                "speaker_turns"
                            ],
                            "text": str(content),
                            "metadata": {
                                **self.base_metadata(
                                    row
                                ),

                                "semantic_layer": "speaker_turn",

                                "speaker": turn.get(
                                    "speaker"
                                ),

                                "role": turn.get(
                                    "role"
                                ),

                                "speaker_type": turn.get(
                                    "speaker_type"
                                ),

                                "section": turn.get(
                                    "section"
                                ),

                                "sequence": turn.get(
                                    "sequence"
                                ),
                            },
                        }
                    )

            except Exception as e:

                print(
                    f"Speaker parsing error: {e}"
                )

        return documents