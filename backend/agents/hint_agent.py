from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.3,
    timeout=60,
    max_retries=1
)


def generate_hint(state: dict) -> dict:

    hints_used = state.get("hints_used", 0)
    previous_hints = state.get("hints", [])

    if hints_used >= 3:
        return {}

    prompt = f"""
    You are an expert GeoGuessr coach.

    Question: {state["question"]}
    Correct answer: {state["correct_answer"]}
    Options: {state["options"]}
    Previous hints: {previous_hints}

    Generate hint number {hints_used + 1} out of 3.

    Rules:
    - Hint 1 should be subtle.
    - Hint 2 should be more specific.
    - Hint 3 should be a strong clue.
    - Never explicitly reveal the correct answer.
    - Do not repeat previous hints.
    - Return only one short hint.
    """

    response = llm.invoke(prompt)

    return {
        "hints": previous_hints + [response.text],
        "hints_used": hints_used + 1
    }