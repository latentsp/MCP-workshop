import asyncio
from fastmcp import Client

# It's recommended to run the server in a separate terminal
# so that you can see the server logs and interact with the client
# at the same time.
#
# To run the server, execute the following command in your terminal:
# python my_server.py
#
# Then, you can run this client to interact with the server.
client = Client("my_server.py")

async def call_tool(name: str):
    """
    Calls the "greet" tool on the server with the given name.
    """
    async with client:
        result = await client.call_tool("greet", {"name": name})
        print(result)

if __name__ == "__main__":
    # In the quickstart, "Ford" is used as the example name.
    # Feel free to change it to any name you like!
    asyncio.run(call_tool("Ford")) 