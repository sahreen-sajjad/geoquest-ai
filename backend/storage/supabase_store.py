from datetime import datetime, timezone

from backend.storage.database import supabase


# Create a new player

def create_player(player_id):

    response = (
        supabase
        .table("players")
        .insert({
            "id": player_id,
            "score": 0,
            "round_number": 1
        })
        .execute()
    )

    return response.data[0]


# Retrieve an existing player

def get_player(player_id):

    response = (
        supabase
        .table("players")
        .select("*")
        .eq("id", player_id)
        .execute()
    )

    return response.data[0] if response.data else None


# Retrieve player history

def get_player_history(player_id):

    response = (
        supabase
        .table("game_history")
        .select("*")
        .eq("player_id", player_id)
        .order("created_at")
        .execute()
    )

    return response.data


# Update player progress

def update_player(player_id, score, round_number):

    supabase.table("players").update({
        "score": score,
        "round_number": round_number,
        "updated_at": datetime.now(timezone.utc).isoformat()
    }).eq("id", player_id).execute()


# Save a completed round

def save_round(player_id, state):

    round_result = state["history"][-1]

    supabase.table("game_history").insert({
        "player_id": player_id,
        "mode": state["mode"],
        "difficulty": state["difficulty"],
        "question": state["question"],
        "player_answer": state["player_answer"],
        "correct_answer": state["correct_answer"],
        "is_correct": state["is_correct"],
        "hints_used": state["hints_used"],
        "points": round_result["points"],
        "feedback": state["feedback"],
        "training_recommendation": state["training_recommendation"]
    }).execute()


# Restore player state

def load_player_state(player_id):

    player = get_player(player_id)

    if player is None:
        player = create_player(player_id)

    return {
        "score": player["score"],
        "round_number": player["round_number"],
        "history": get_player_history(player_id)
    }