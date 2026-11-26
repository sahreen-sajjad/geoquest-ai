def get_difficulty(history: list[dict]) -> str:

    if len(history) < 5:
        return "Medium"

    recent = history[-5:]

    accuracy = sum(
        item["is_correct"] for item in recent
    ) / len(recent)

    average_hints = sum(
        item["hints_used"] for item in recent
    ) / len(recent)

    if accuracy >= 0.8 and average_hints <= 1:
        return "Hard"

    if accuracy < 0.4:
        return "Easy"

    return "Medium"