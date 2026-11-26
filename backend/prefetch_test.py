import time

from backend.workflows.prefetch import (
    prefetch_question,
    get_prefetched_question
)


session_id = "test-player"

prefetch_question(session_id)

print("Player is answering the current question...")

time.sleep(15)

start = time.perf_counter()

question = get_prefetched_question(session_id)

print(question)

print(
    f"Question retrieval time: "
    f"{time.perf_counter() - start:.4f}s"
)