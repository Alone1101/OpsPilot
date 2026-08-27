import asyncio
from mcp.client.streamable_http import streamable_http_client
from mcp import ClientSession

async def main():
    url = "http://127.0.0.1:8001/mcp"

    # Open MCP HTTP connection
    async with streamable_http_client(url) as (read_stream, write_stream):

        # Create MCP session on top of transport streams
        async with ClientSession(read_stream, write_stream) as session:

            # MCP handshake
            await session.initialize()

            tools = await session.list_tools()

            print("Available tools:")

            for tool in tools.tools:
                print(f"- {tool.name}")

            order_result = await session.call_tool("get_order", {"order_id": "NC-1002"})

            print("\n get_order result:")

            for content in order_result.content:
                print(content.text)

            tracking_result = await session.call_tool("get_tracking_status_mcp", {"order_id": "NC-1002"})

            print("\n get_tracking_status_mcp result:")

            for content in tracking_result.content:
                print(content.text)

if __name__ == "__main__":
    asyncio.run(main())