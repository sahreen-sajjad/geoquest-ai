import time

from backend.mcp_servers.imagery_server import get_street_image

start = time.perf_counter()

result = get_street_image(
    lat=-33.9249,
    lon=18.4241
)

print(f"Total execution: {time.perf_counter() - start:.2f}s")
print(f"Image found: {bool(result.get('image_url'))}")