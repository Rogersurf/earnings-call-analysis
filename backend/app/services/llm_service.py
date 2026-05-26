# ============================================================
# FILE: backend/app/services/llm_service.py
# ============================================================

import os

from dotenv import load_dotenv

from google import genai

from openai import OpenAI

# ============================================================
# LOAD ENV
# ============================================================

load_dotenv()

# ============================================================
# API KEYS
# ============================================================

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)

# ============================================================
# GEMINI CLIENT
# ============================================================

gemini_client = genai.Client(

    api_key=GEMINI_API_KEY
)

# ============================================================
# GROQ CLIENT
# ============================================================

groq_client = OpenAI(

    api_key=GROQ_API_KEY,

    base_url=
        "https://api.groq.com/openai/v1"
)

# ============================================================
# DEFAULT PROVIDER
# ============================================================

DEFAULT_PROVIDER = "groq"

# ============================================================
# GROQ MODEL
# ============================================================

GROQ_MODEL = (
    "llama-3.1-8b-instant"
)

# ============================================================
# GEMINI SYNTHESIS
# ============================================================

def generate_gemini_synthesis(

    prompt: str
):

    response = gemini_client.models.generate_content(

        model="gemini-2.0-flash",

        contents=prompt
    )

    return response.text

# ============================================================
# GROQ SYNTHESIS
# ============================================================

def generate_groq_synthesis(

    prompt: str
):

    response = groq_client.chat.completions.create(

        model=GROQ_MODEL,

        messages=[

            {

                "role":
                    "system",

                "content":
"""
You are a financial semantic intelligence analyst.

Your role:
- synthesize retrieved evidence
- explain semantic relationships
- identify possible propagation patterns
- avoid hallucinations
- avoid financial predictions
- avoid claiming causality
"""
            },

            {

                "role":
                    "user",

                "content":
                    prompt
            }
        ],

        temperature=0.2,

        max_tokens=500
    )

    return (

        response
        .choices[0]
        .message
        .content
    )

# ============================================================
# MAIN SYNTHESIS FUNCTION
# ============================================================

def generate_llm_synthesis(

    query: str,

    retrieved_chunks: list,

    themes: list,

    graph_stats: dict,
    
    custom_prompt: str = "",

    provider: str = DEFAULT_PROVIDER
):

    # ========================================================
    # CONTEXT
    # ========================================================

    context = "\n\n".join([

        chunk[:1200]

        for chunk in retrieved_chunks[:5]
    ])

    # ========================================================
    # PROMPT
    # ========================================================

    prompt = f"""

        {custom_prompt}

        User Query:
        {query}

        Themes:
        {themes}

        Graph Statistics:
        {graph_stats}

        Retrieved Evidence:
        {context}

        Provide a concise grounded analysis.
        """

    # ========================================================
    # GROQ PRIMARY
    # ========================================================

    if provider == "groq":

        try:

            return generate_groq_synthesis(
                prompt
            )

        except Exception as e:

            print(
                "\nGroq failed.\n"
            )

            print(e)

            if GEMINI_API_KEY:

                print(
                    "\nTrying Gemini fallback...\n"
                )

                return generate_gemini_synthesis(
                    prompt
                )

            raise e

    # ========================================================
    # GEMINI PRIMARY
    # ========================================================

    elif provider == "gemini":

        try:

            return generate_gemini_synthesis(
                prompt
            )

        except Exception as e:

            print(
                "\nGemini failed.\n"
            )

            print(e)

            if GROQ_API_KEY:

                print(
                    "\nTrying Groq fallback...\n"
                )

                return generate_groq_synthesis(
                    prompt
                )

            raise e

    else:

        raise ValueError(

            f"Unsupported provider: "
            f"{provider}"
        )

# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    output = generate_llm_synthesis(

        query=
            "AI infrastructure demand",

        retrieved_chunks=[

            "NVIDIA reported increasing "
            "AI datacenter demand.",

            "Utilities discussed higher "
            "energy requirements driven "
            "by cloud infrastructure.",

            "Cloud providers continue "
            "expanding GPU infrastructure "
            "to support AI workloads."
        ],

        themes=[
            "ai",
            "infrastructure",
            "energy"
        ],

        graph_stats={

            "nodes": 22,

            "edges": 31
        }
    )

    print("\n===================================================")
    print("LLM SYNTHESIS")
    print("===================================================\n")

    print(output)