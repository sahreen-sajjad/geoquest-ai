from uuid import uuid4

from backend.storage.supabase_store import (
    load_player_state,
    update_player
)

player_id = str(uuid4())

print("Player ID:", player_id)

state = load_player_state(player_id)

print("Initial state:", state)

update_player(
    player_id,
    score=100,
    round_number=2
)

state = load_player_state(player_id)

print("Updated state:", state)