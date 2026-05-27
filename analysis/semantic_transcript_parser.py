import json
import re
import sqlite3

import pandas as pd

from rich import print


# ============================================================
# CONFIG
# ============================================================

INPUT_DB = "data/database/transcripts.db"

OUTPUT_DB = "data/database/transcripts_clean.db"


# ============================================================
# SECTION EXTRACTION
# ============================================================

def extract_section(
    text: str,
    start: str,
    end: str,
):

    """
    Extract semantic section
    between two markers.
    """

    if start in text and end in text:

        try:

            return (
                text
                .split(start)[1]
                .split(end)[0]
                .strip()
            )

        except Exception:

            return ""

    return ""


# ============================================================
# FULL TRANSCRIPT EXTRACTION
# ============================================================

def extract_full_transcript(
    text: str,
):

    """
    Extract full conference call transcript.
    """

    marker = (
        "Full Conference Call Transcript"
    )

    if marker in text:

        try:

            return (
                text
                .split(marker)[1]
                .split("Read Next")[0]
                .strip()
            )

        except Exception:

            return text

    return text

# ============================================================
# TRANSCRIPT NORMALIZATION
# ============================================================

def normalize_transcript(
    transcript: str,
):

    """
    Normalize transcript formatting
    before discourse parsing.
    """

    if not transcript:

        return ""

    # ========================================================
    # NORMALIZE LINE BREAKS
    # ========================================================

    transcript = transcript.replace(
        "\r",
        "\n"
    )

    # ========================================================
    # REMOVE MULTIPLE EMPTY LINES
    # ========================================================

    transcript = re.sub(
        r"\n{3,}",
        "\n\n",
        transcript
    )

    # ========================================================
    # CLEAN OPERATOR TRANSITIONS
    # ========================================================

    transcript = re.sub(

        r"Operator\nThank you\.",

        "Operator -- Moderator",

        transcript
    )

    transcript = re.sub(

        r"Questions & Answers:",

        "\n\nQUESTIONS_AND_ANSWERS\n\n",

        transcript
    )

    # ========================================================
    # CLEAN COMMON TRANSITIONS
    # ========================================================

    transition_patterns = [

        r"Thank you and now I'll turn it over to",

        r"Thank you\. And now I'll turn the call over to",

        r"Operator, we'll take the next question",

        r"Your line is now open",

        r"Please go ahead",

        r"\[Operator instructions\]",

        r"\[Operator signoff\]",
    ]

    for pattern in transition_patterns:

        transcript = re.sub(
            pattern,
            "",
            transcript,
            flags=re.IGNORECASE
        )

    return transcript.strip()


# ============================================================
# SPEAKER HEADER NORMALIZATION
# ============================================================

def normalize_speaker_headers(
    transcript: str,
):

    """
    Normalize malformed speaker blocks.
    """

    if not transcript:

        return ""

    # ========================================================
    # NORMALIZE:
    #
    # Name
    # --
    # Company
    #
    # INTO:
    #
    # Name -- Company
    # ========================================================

    transcript = re.sub(

        r"\n([A-Z][A-Za-z\s\.\-']+)\n--\n([^\n]+)",

        r"\n\1 -- \2",

        transcript
    )

    return transcript


# ============================================================
# SPEAKER TURN EXTRACTION
# ============================================================

def extract_speaker_turns(
    transcript: str,
):

    """
    Extract discourse-aware speaker turns.
    """

    speaker_turns = []

    if not transcript:

        return speaker_turns

    # ========================================================
    # NORMALIZATION
    # ========================================================

    transcript = normalize_transcript(
        transcript
    )

    transcript = normalize_speaker_headers(
        transcript
    )

    # ========================================================
    # SPEAKER REGEX
    # ========================================================

    speaker_pattern = re.compile(

        r"(?:\n|^)"

        r"([A-Z][A-Za-z\s\.\-']+)"

        r"(?:\s--\s([^\n]+))?"

        r":?\n",

        re.MULTILINE
    )

    matches = list(
        speaker_pattern.finditer(transcript)
    )

    if not matches:

        return speaker_turns

    # ========================================================
    # TURN EXTRACTION
    # ========================================================

    for idx, match in enumerate(matches):

        speaker_name = (
            match.group(1)
            .strip()
        )

        speaker_role = (

            match.group(2).strip()

            if match.group(2)

            else "Unknown"
        )

        # ====================================================
        # CLEAN SPEAKER NAME
        # ====================================================

        speaker_name = re.sub(

            r"^(Thank you\.?|Yes\.?|Sure\.?)",

            "",

            speaker_name,

            flags=re.IGNORECASE
        ).strip()

        # ====================================================
        # CONTENT RANGE
        # ====================================================

        start_pos = match.end()

        if idx < len(matches) - 1:

            end_pos = (
                matches[idx + 1].start()
            )

        else:

            end_pos = len(transcript)

        content = (
            transcript[start_pos:end_pos]
            .strip()
        )

        # ====================================================
        # REMOVE VERY SHORT NOISE
        # ====================================================

        if len(content) < 20:

            continue

        # ====================================================
        # SPEAKER TYPE
        # ====================================================

        role_lower = speaker_role.lower()

        speaker_lower = speaker_name.lower()


        # ====================================================
        # OPERATOR DETECTION
        # ====================================================

        if (

            "operator" in role_lower

            or

            "moderator" in role_lower

            or

            speaker_lower == "operator"
        ):

            speaker_type = "operator"


        # ====================================================
        # ANALYST DETECTION
        # ====================================================

        elif any(

            keyword in role_lower

            for keyword in [

                "analyst",
                "research",
                "capital",
                "partners",
                "securities",
                "investments",
                "morgan",
                "goldman",
                "ubs",
                "bernstein",
            ]
        ):

            speaker_type = "analyst"


        # ====================================================
        # DEFAULT
        # ====================================================

        else:

            speaker_type = "executive"

        # ====================================================
        # QA DETECTION
        # ====================================================

        if "QUESTIONS_AND_ANSWERS" in transcript:

            qa_position = transcript.find(
                "QUESTIONS_AND_ANSWERS"
            )

            section = (

                "qa_section"

                if start_pos > qa_position

                else "prepared_remarks"
            )

        else:

            section = "prepared_remarks"

        # ====================================================
        # STORE TURN
        # ====================================================

        speaker_turns.append({

            "sequence": idx,

            "speaker": speaker_name,

            "role": speaker_role,

            "speaker_type": speaker_type,

            "section": section,

            "content": content,
        })

    return speaker_turns


# ============================================================
# MAIN
# ============================================================

def main():

    print(
        "\n[bold cyan]"
        "Loading database..."
        "[/bold cyan]"
    )

    conn = sqlite3.connect(INPUT_DB)

    query = """
    SELECT *
    FROM transcripts
    """

    df = pd.read_sql_query(
        query,
        conn,
    )

    conn.close()

    print(
        f"\n[bold green]"
        f"Loaded {len(df)} rows"
        f"[/bold green]"
    )

    # ========================================================
    # SEMANTIC EXTRACTION
    # ========================================================

    article_intro = []

    takeaways = []

    summaries = []

    glossaries = []

    full_transcripts = []

    speaker_turns_list = []

    print(
        "\n[bold yellow]"
        "Starting semantic parsing..."
        "[/bold yellow]"
    )

    # ========================================================
    # PROCESS LOOP
    # ========================================================

    for idx, row in df.iterrows():

        text = str(
            row.get("transcript", "")
        )

        # ====================================================
        # SECTION EXTRACTION
        # ====================================================

        intro = extract_section(

            text,

            "Earnings Call Transcript",

            "TAKEAWAYS",
        )

        takeaway = extract_section(

            text,

            "TAKEAWAYS",

            "SUMMARY",
        )

        summary = extract_section(

            text,

            "SUMMARY",

            "INDUSTRY GLOSSARY",
        )

        glossary = extract_section(

            text,

            "INDUSTRY GLOSSARY",

            "Full Conference Call Transcript",
        )

        # ====================================================
        # FULL TRANSCRIPT
        # ====================================================

        full_transcript = (
            extract_full_transcript(text)
        )

        # ====================================================
        # SPEAKER TURNS
        # ====================================================

        speaker_turns = (
            extract_speaker_turns(
                full_transcript
            )
        )

        # ====================================================
        # STORE
        # ====================================================

        article_intro.append(intro)

        takeaways.append(takeaway)

        summaries.append(summary)

        glossaries.append(glossary)

        full_transcripts.append(
            full_transcript
        )

        speaker_turns_list.append(
            json.dumps(speaker_turns)
        )

        # ====================================================
        # LOGGING
        # ====================================================

        if idx % 500 == 0:

            print(
                f"[yellow]"
                f"Processed {idx:,}"
                f"[/yellow]"
            )

    # ========================================================
    # NEW COLUMNS
    # ========================================================

    df["article_intro"] = article_intro

    df["takeaways"] = takeaways

    df["summary"] = summaries

    df["glossary"] = glossaries

    df["full_transcript"] = (
        full_transcripts
    )

    df["speaker_turns"] = (
        speaker_turns_list
    )

    # ========================================================
    # SAVE CLEAN DATABASE
    # ========================================================

    print(
        "\n[bold cyan]"
        "Saving clean database..."
        "[/bold cyan]"
    )

    clean_conn = sqlite3.connect(
        OUTPUT_DB
    )

    df.to_sql(

        "transcripts",

        clean_conn,

        if_exists="replace",

        index=False,
    )

    clean_conn.close()

    # ========================================================
    # FINAL OUTPUT
    # ========================================================

    print(
        "\n[bold green]"
        "CLEAN DATABASE SAVED"
        "[/bold green]"
    )

    print(
        f"\n[bold cyan]"
        f"OUTPUT:"
        f" {OUTPUT_DB}"
        f"[/bold cyan]"
    )


if __name__ == "__main__":

    main()