from typing import TypedDict
from backend.storage.player_store import (
    load_player,
    save_player
)

from backend.workflows.adaptive_difficulty import (
    get_difficulty
)

class GameState(TypedDict):
    mode: str
    difficulty: str
    question: str
    correct_answer: str
    options: list[str]
    player_answer: str
    hints: list[str]
    hints_used: int
    is_correct: bool
    feedback: str
    score: int
    round_number: int
    action: str
    history: list[dict]
    training_recommendation: str
    image_url: str | None
    image_id: str | None
    image_creator: dict | None
    image_source_url: str | None