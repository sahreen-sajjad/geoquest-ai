import os
import random
import requests

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
import time
import sys

load_dotenv()

mcp = FastMCP("GeoQuest Imagery")

ACCESS_TOKEN = os.getenv("MAPILLARY_ACCESS_TOKEN")
BASE_URL = "https://graph.mapillary.com"


@mcp.tool()
def get_street_image(
    lat: float,
    lon: float,
    radius: float = 0.005
) -> dict:
    """Retrieve a random street-level image near coordinates."""

    if not ACCESS_TOKEN:
        return {"error": "Mapillary access token missing"}

    bbox = (
        f"{lon - radius},{lat - radius},"
        f"{lon + radius},{lat + radius}"
    )

    params = {
        "access_token": ACCESS_TOKEN,
        "fields": "id,thumb_1024_url,computed_geometry,creator",
        "bbox": bbox,
        "limit": 10
    }
    start = time.perf_counter()
    

    response = requests.get(
        f"{BASE_URL}/images",
        params=params,
        timeout=30
    )
    print(
    f"Mapillary API time: {time.perf_counter() - start:.2f}s",
    file=sys.stderr,
        flush=True
    )

    print(
        f"Mapillary status: {response.status_code}",
        file=sys.stderr,
        flush=True
    )

    if response.status_code != 200:
        return {
            "error": "Mapillary request failed",
            "status_code": response.status_code
        }

    images = [
        image for image in response.json().get("data", [])
        if image.get("thumb_1024_url")
    ]

    if not images:
        return {"error": "No images found"}

    image = random.choice(images)

    return {
        "image_id": image["id"],
        "image_url": image["thumb_1024_url"],
        "coordinates": image.get("computed_geometry"),
        "creator": image.get("creator"),
        "source": "Mapillary",
        "source_url": (
            f"https://www.mapillary.com/app/?pKey={image['id']}"
        )
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")