import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
PLAYER_FILE = DATA_DIR / "player_history.json"


def load_player() -> dict:

    if not PLAYER_FILE.exists():
        return {
            "score": 0,
            "history": [],
            "round_number": 1
        }

    with open(PLAYER_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_player(state: dict):

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    player_data = {
        "score": state.get("score", 0),
        "history": state.get("history", []),
        "round_number": state.get("round_number", 1)
    }

    with open(PLAYER_FILE, "w", encoding="utf-8") as file:
        json.dump(player_data, file, indent=4)