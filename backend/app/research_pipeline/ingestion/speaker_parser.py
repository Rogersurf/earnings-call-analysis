import re
from typing import Dict
from backend.app.research_pipeline.ingestion.discourse_cleaner import (
    DiscourseCleaner
)

class SpeakerNormalizer:

    """
    Normalize speaker metadata from earnings call transcripts.
    """

    ANALYST_PATTERNS = [
        r"analyst",
        r"research",
        r"capital markets",
        r"securities",
        r"baird",
        r"morgan stanley",
        r"goldman",
        r"jpmorgan",
        r"barclays",
        r"william blair",
    ]

    EXECUTIVE_PATTERNS = [
        r"chief",
        r"ceo",
        r"cfo",
        r"coo",
        r"president",
        r"director",
        r"executive",
        r"founder",
    ]

    MODERATOR_PATTERNS = [
        r"operator",
        r"moderator",
    ]

    @staticmethod
    def clean_text(text: str) -> str:

        text = str(text)

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    def detect_speaker_type(
        self,
        speaker_text: str,
    ) -> str:

        speaker_text = self.clean_text(
            speaker_text
        ).lower()

        for pattern in self.MODERATOR_PATTERNS:

            if re.search(pattern, speaker_text):
                return "moderator"

        for pattern in self.ANALYST_PATTERNS:

            if re.search(pattern, speaker_text):
                return "analyst"

        for pattern in self.EXECUTIVE_PATTERNS:

            if re.search(pattern, speaker_text):
                return "executive"

        return "unknown"

    def normalize(
        self,
        turn: Dict,
    ) -> Dict:

        raw_speaker = turn.get(
            "speaker",
            ""
        )

        speaker = (
            DiscourseCleaner.extract_primary_speaker(
                raw_speaker
            )
        )

        speaker = self.clean_text(
            speaker
        )

        role = self.clean_text(
            turn.get("role", "")
        )

        combined_text = (
            f"{speaker} {role}"
        )

        detected_type = self.detect_speaker_type(
            combined_text
        )

        turn["speaker"] = speaker

        turn["role"] = role

        turn["speaker_type"] = detected_type

        return turn