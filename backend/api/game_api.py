from uuid import uuid4

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.workflows.game_graph import game_graph
from backend.workflows.adaptive_difficulty import get_difficulty
from backend.workflows.prefetch import (
    prefetch_question,
    get_prefetched_question
)
from backend.storage.supabase_store import (
    load_player_state,
    save_round,
    update_player
)
from collections import defaultdict

from backend.storage.supabase_store import (
    get_player,
    get_player_history
)

router = APIRouter(prefix="/game", tags=["Game"])

sessions = {}


class StartRequest(BaseModel):
    mode: str = "Landscape"
    session_id: str | None = None


class HintRequest(BaseModel):
    session_id: str


class AnswerRequest(BaseModel):
    session_id: str
    answer: str


def get_session(session_id):
    if session_id not in sessions:
        raise HTTPException(404, "Session not found")

    return sessions[session_id]


@router.post("/start")
@router.post("/start")
@router.post("/start")
def start_game(request: StartRequest):

    session_id = request.session_id or str(uuid4())

    if session_id in sessions:
        state = sessions[session_id]
    else:
        state = load_player_state(session_id)

    state["action"] = "quiz"
    state["mode"] = request.mode

    state["difficulty"] = get_difficulty(
        state["history"]
    )

    if request.mode == "Street View":

        prefetched = get_prefetched_question(session_id)

        if prefetched is not None:
            state.update(prefetched)

        else:
            state = game_graph.invoke(state)

        prefetch_question(session_id)

    else:

        state = game_graph.invoke(state)

    state["answered"] = False

    sessions[session_id] = state

    return {
        "session_id": session_id,
        "question": state["question"],
        "options": state["options"],
        "difficulty": state["difficulty"],
        "round_number": state["round_number"],
        "score": state["score"],
        "image_url": state.get("image_url"),
        "image_creator": state.get("image_creator")
    }


@router.post("/hint")
def request_hint(request: HintRequest):

    state = get_session(request.session_id)

    if state["answered"]:
        raise HTTPException(400, "Round already completed")

    if state["hints_used"] >= 3:
        raise HTTPException(400, "Hint limit reached")

    state["action"] = "hint"

    state = game_graph.invoke(state)
    state["answered"] = False

    sessions[request.session_id] = state

    return {
        "hint": state["hints"][-1],
        "hints_used": state["hints_used"]
    }


@router.post("/answer")
@router.post("/answer")
def submit_answer(request: AnswerRequest):

    state = get_session(request.session_id)

    if state["answered"]:
        raise HTTPException(
            status_code=400,
            detail="Round already completed"
        )

    if request.answer not in state["options"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid answer"
        )

    state["action"] = "evaluate"
    state["player_answer"] = request.answer

    state = game_graph.invoke(state)

    state["answered"] = True
    state["round_number"] += 1

    # Save completed round to Supabase

    save_round(request.session_id, state)

    # Update persistent player progress

    update_player(
        player_id=request.session_id,
        score=state["score"],
        round_number=state["round_number"]
    )

    sessions[request.session_id] = state

    return {
        "is_correct": state["is_correct"],
        "correct_answer": state["correct_answer"],
        "feedback": state["feedback"],
        "score": state["score"],
        "training_recommendation":
            state["training_recommendation"],
        "image_source_url":
            state.get("image_source_url")
    }
@router.get("/stats")
def get_stats(session_id: str):

    player = get_player(session_id)

    if player is None:
        raise HTTPException(
            status_code=404,
            detail="Player not found"
        )

    history = get_player_history(session_id)

    total = len(history)

    correct = sum(
        item["is_correct"] for item in history
    )

    total_hints = sum(
        item["hints_used"] for item in history
    )

    mode_stats = defaultdict(
        lambda: {"played": 0, "correct": 0}
    )

    country_stats = defaultdict(
        lambda: {"played": 0, "correct": 0}
    )

    for item in history:

        mode = item["mode"]
        country = item["correct_answer"]

        mode_stats[mode]["played"] += 1
        mode_stats[mode]["correct"] += int(item["is_correct"])

        country_stats[country]["played"] += 1
        country_stats[country]["correct"] += int(item["is_correct"])

    for stats in mode_stats.values():

        stats["accuracy"] = round(
            stats["correct"] / stats["played"] * 100, 2
        )

    for stats in country_stats.values():

        stats["accuracy"] = round(
            stats["correct"] / stats["played"] * 100, 2
        )

    return {
        "rounds_played": total,
        "correct_answers": correct,
        "incorrect_answers": total - correct,
        "accuracy": round(correct / total * 100, 2) if total else 0,
        "score": player["score"],
        "average_hints": round(total_hints / total, 2) if total else 0,
        "mode_performance": dict(mode_stats),
        "country_performance": dict(country_stats),
        "recent_history": history[-10:][::-1]
    }