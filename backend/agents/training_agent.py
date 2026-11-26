import json

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.3,
    timeout=60,
    max_retries=1
)


def recommend_training(state: dict) -> dict:

    history = state.get("history", [])

    if not history:
        return {
            "training_recommendation":
                "Complete a quiz to receive recommendations."
        }

    prompt = f"""
    You are a personalised GeoGuessr training coach.

    Analyse the player's recent performance:

    {json.dumps(history[-20:], indent=2)}

    Identify:
    - Strengths demonstrated by the player.
    - Weaknesses and recurring mistakes.
    - Countries the player confuses.
    - Reliance on hints.
    - Recommended training exercises.
    - Recommended difficulty for future quizzes.

    Do not infer recurring patterns from insufficient data.
    Keep your recommendations practical and concise.
    """

    response = llm.invoke(prompt)

    return {
        "training_recommendation": response.text
    }