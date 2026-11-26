from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
import json
from backend.mcp_tools import get_random_country
from backend.rag.retriever import retrieve_knowledge

load_dotenv()


class QuizQuestion(BaseModel):

    question: str
    options: list[str] = Field(
        min_length=4,
        max_length=4
    )
    correct_answer: str


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.7,
    timeout=60,
    max_retries=1
)

quiz_model = llm.with_structured_output(QuizQuestion)


def generate_quiz(state: dict) -> dict:
    country = get_random_country()

    if "error" in country:
        raise ValueError(country["error"])

    print("MCP country data:", country)

    query = f"{country['name']} {state['mode']}"

    knowledge = retrieve_knowledge(
    query,
    country=country["name"],
    k=3
)

    print("RAG retrieved knowledge:", knowledge)

    prompt = f"""
    You are an expert geography quiz generator
    and GeoGuessr coach.

    Generate one geography question.

    Mode: {state["mode"]}
    Difficulty: {state["difficulty"]}

    MCP geographical information:
    {json.dumps(country, indent=2)}

    RAG retrieved knowledge:
    {knowledge}

    Requirements:
    - The correct answer must be {country["name"]}.
    - Provide four distinct country options.
    - Exactly one option must be correct.
    - Do not reveal the answer in the question.
    - Use retrieved geographical facts.
    - Do not attribute another country's characteristics
      to the correct country.
    - Ignore irrelevant retrieved knowledge.
    - If specialised knowledge is unavailable,
      generate a general geography question.
    - Do not invent geographical facts.
    - If no relevant specialised knowledge is available,
      use only the facts explicitly provided by MCP.
    - Do not introduce facts from your own knowledge.
    """

    result = quiz_model.invoke(prompt)
    if result.correct_answer != country["name"]:
        raise ValueError("Answer does not match MCP data")

    if result.correct_answer not in result.options:
        raise ValueError("Correct answer missing from options")

    if len(set(result.options)) != 4:
        raise ValueError("Duplicate quiz options")

    return {
        "question": result.question,
        "options": result.options,
        "correct_answer": result.correct_answer,
        "hints": [],
        "hints_used": 0,
        "image_url": None,
        "image_id": None,
        "image_creator": None,
        "image_source_url": None
    }


if __name__ == "__main__":

    result = generate_quiz({
        "mode": "Landscape",
        "difficulty": "Medium"
    })

    print(result)