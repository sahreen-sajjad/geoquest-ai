from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.3,
    timeout=60,
    max_retries=1
)


def evaluate_answer(state: dict) -> dict:

    player_answer = state["player_answer"]
    correct_answer = state["correct_answer"]

    is_correct = (
        player_answer.strip().casefold()
        == correct_answer.strip().casefold()
    )

    hints_used = state.get("hints_used", 0)

    points = (
        max(0, 100 - hints_used * 25)
        if is_correct else 0
    )

    prompt = f"""
    You are an expert GeoGuessr coach.

    Question: {state["question"]}
    Player's answer: {player_answer}
    Correct answer: {correct_answer}
    Is correct: {is_correct}
    Hints used: {hints_used}

    Provide educational feedback.

    Requirements:
    - Explain why the correct answer is right.
    - If incorrect, explain how to distinguish
      the two countries.
    - Provide a useful GeoGuessr tip.
    - Keep the feedback under 100 words.
    """

    response = llm.invoke(prompt)

    history = state.get("history", [])

    round_result = {
        "mode": state["mode"],
        "difficulty": state["difficulty"],
        "question": state["question"],
        "player_answer": player_answer,
        "correct_answer": correct_answer,
        "is_correct": is_correct,
        "hints_used": hints_used,
        "points": points
        }

    return {
        "is_correct": is_correct,
        "feedback": response.text,
        "score": state.get("score", 0) + points,
        "history": history + [round_result]
    }