from concurrent.futures import ThreadPoolExecutor
from threading import Lock

from backend.agents.image_quiz_agent import generate_image_quiz


executor = ThreadPoolExecutor(max_workers=2)

prefetched_questions = {}

lock = Lock()


def prefetch_question(session_id):

    with lock:

        if session_id not in prefetched_questions:

            prefetched_questions[session_id] = executor.submit(
                generate_image_quiz, {}
            )

            print("Prefetch started")


def get_prefetched_question(session_id):

    with lock:
        future = prefetched_questions.pop(session_id, None)

    if future is None:
        return None

    try:

        print("Using prefetched question")

        return future.result()

    except Exception as error:

        print(f"Prefetch failed: {error}")

        return None