import asyncio
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent

load_dotenv()


async def main():

    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0,
        timeout=60,
        max_retries=1
    )
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

    print("Connecting to MCP server...", flush=True)

    tools = await client.get_tools()

    print("MCP tools loaded successfully", flush=True)

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=(
            "You are GeoQuest AI, an expert geography "
            "assistant and GeoGuessr coach. "
            "Use the available tools to retrieve "
            "geographical information when relevant."
        )
    )
    print("Sending request to Gemini agent...", flush=True)

    result = await agent.ainvoke({
        "messages": [
            {
                "role": "user",
                "content": (
                    "Use your tools to retrieve Iceland's country "
                    "coordinates and generate a Street View link "
                    "using those coordinates."
                )
            }
        ]
    })

    for message in result["messages"]:
        message.pretty_print()


if __name__ == "__main__":
    asyncio.run(main())