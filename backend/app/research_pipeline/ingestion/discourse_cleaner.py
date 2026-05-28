import re


class DiscourseCleaner:

    """
    Clean noisy speaker metadata from earnings call transcripts.
    """

    @staticmethod
    def clean_speaker_block(
        speaker_text: str,
    ) -> str:

        speaker_text = str(
            speaker_text
        )

        speaker_text = re.split(
            r"Operator -- Moderator",
            speaker_text,
        )[0]

        speaker_text = re.split(
            r"\n\n",
            speaker_text,
        )[0]

        speaker_text = re.sub(
            r"\s+",
            " ",
            speaker_text,
        )

        return speaker_text.strip()

    @staticmethod
    def extract_primary_speaker(
        speaker_text: str,
    ) -> str:

        cleaned = (
            DiscourseCleaner.clean_speaker_block(
                speaker_text
            )
        )

        lines = cleaned.split("--")

        if len(lines) > 0:

            return lines[0].strip()

        return cleaned.strip()