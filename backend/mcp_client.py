import asyncio
import sys
from pathlib import Path
from langchain_mcp_adapters.client import MultiServerMCPClient


async def main():

    server_path = (
        Path(__file__).parent
        / "mcp_servers"
        / "geography_server.py"
    )

    client = MultiServerMCPClient({
        "geography": {
            "command": sys.executable,
            "args": [str(server_path)],
            "transport": "stdio"
        }
    })

    tools = await client.get_tools()

    print("Available tools:")

    for tool in tools:
        print(tool.name)

    country_tool = next(
        tool for tool in tools
        if tool.name == "get_random_country"
    )

    result = await country_tool.ainvoke({
        "region": "Europe"
    })

    print(result)


if __name__ == "__main__":
    asyncio.run(main())