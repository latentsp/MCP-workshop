import os
import json
from datetime import datetime
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP(name="Travel Server")

@mcp.tool()
def recommend_trip(destination: str, budget: int, duration_days: int) -> str:
    """Recommend a trip based on destination, budget, and duration.
    
    Args:
        destination: The destination city/country for the trip
        budget: The total budget in USD
        duration_days: Number of days for the trip
        
    Returns:
        A formatted string with trip recommendations
    """
    #TODO: fix it by addiing premade recommendations
    recommendations = 
    
    #TODO: fix it by making up business logic to use recommendations based on business logic

    
@mcp.tool()
def book_trip(traveler_name: str, destination: str, start_date: str, end_date: str, budget: int) -> str:
    #TODO: fix it by saving the trip details to a file
# Run the server
if __name__ == "__main__":
    mcp.run(transport="stdio") 