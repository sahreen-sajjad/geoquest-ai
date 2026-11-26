import asyncio
import json
import sys
from pathlib import Path
import time

from langchain_mcp_adapters.client import MultiServerMCPClient

SERVER_DIR = Path(__file__).parent / "mcp_servers"


async def call_mcp_tool(server_name, tool_name, arguments):

    start = time.perf_counter()

    client = MultiServerMCPClient({
        server_name: {
            "command": sys.executable,
            "args": [
                str(SERVER_DIR / f"{server_name}_server.py")
            ],
            "transport": "stdio"
        }
    })

    tools = await client.get_tools()

    print(
        f"MCP tool discovery: "
        f"{time.perf_counter() - start:.2f}s"
    )

    tool = next(
        tool for tool in tools
        if tool.name == tool_name
    )

    invocation_start = time.perf_counter()

    result = await tool.ainvoke(arguments)

    print(
        f"MCP tool invocation: "
        f"{time.perf_counter() - invocation_start:.2f}s"
    )

    print(
        f"Total MCP execution: "
        f"{time.perf_counter() - start:.2f}s"
    )

    return json.loads(result[0]["text"])

def get_random_country(region="Any"):

    return asyncio.run(
        call_mcp_tool(
            "geography",
            "get_random_country",
            {"region": region}
        )
    )


def get_street_image(lat, lon):

    return asyncio.run(
        call_mcp_tool(
            "imagery",
            "get_street_image",
            {"lat": lat, "lon": lon}
        )
    )