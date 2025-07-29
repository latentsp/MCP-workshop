import asyncio
from fastmcp import Client

# It's recommended to run the server in a separate terminal
# so that you can see the server logs and interact with the client
# at the same time.
#
# To run the server, execute the following command in your terminal:
# python server.py
#
# Then, you can run this client to interact with the server.

async def list_tools():


async def call_weather_tool(latitude: float, longitude: float):


async def main():
    """
    Main function that demonstrates listing tools and calling the weather tool.
    """
    # List available tools
    await list_tools()
    
    # Call the weather tool with example coordinates (New York City)
    print("\nCalling weather tool for New York City (40.7128, -74.0060):")
    await call_weather_tool(40.7128, -74.0060)

if __name__ == "__main__":
    asyncio.run(main()) 