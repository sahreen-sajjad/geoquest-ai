import random

from backend.mcp_tools import get_street_image


LOCATIONS = [
    {"country": "Iceland", "lat": 64.1466, "lon": -21.9426},
    {"country": "Japan", "lat": 35.6762, "lon": 139.6503},
    {"country": "Norway", "lat": 59.9139, "lon": 10.7522},
    {"country": "Australia", "lat": -33.8688, "lon": 151.2093},
    {"country": "Brazil", "lat": -23.5505, "lon": -46.6333},
    {"country": "Poland", "lat": 52.2297, "lon": 21.0122},
    {"country": "Netherlands", "lat": 52.3676, "lon": 4.9041},
    {"country": "South Africa", "lat": -33.9249, "lon": 18.4241}
]


def generate_image_quiz(state: dict) -> dict:

    locations = random.sample(LOCATIONS, len(LOCATIONS))

    for location in locations:

        image = get_street_image(
            location["lat"],
            location["lon"]
        )

        if image.get("image_url"):
            break

    else:
        raise ValueError("No street imagery available")

    correct_answer = location["country"]

    other_countries = [
        loc["country"]
        for loc in LOCATIONS
        if loc["country"] != correct_answer
    ]

    options = random.sample(other_countries, 3)
    options.append(correct_answer)
    random.shuffle(options)

    return {
        "question": "Which country is shown in this image?",
        "options": options,
        "correct_answer": correct_answer,
        "image_url": image["image_url"],
        "image_id": image["image_id"],
        "image_creator": image.get("creator"),
        "image_source_url": image["source_url"],
        "hints": [],
        "hints_used": 0
    }


if __name__ == "__main__":
    print(generate_image_quiz({}))