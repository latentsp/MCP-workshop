from fastmcp import FastMCP
import requests
from typing import Dict, Any

mcp = FastMCP("Weather MCP Server")

@mcp.tool
def get_weather(latitude: float, longitude: float) -> Dict[str, Any]:
    """
    Gets current weather information for the given coordinates using Open-Meteo API.
    
    Args:
        latitude: The latitude coordinate
        longitude: The longitude coordinate
    
    Returns:
        Dictionary containing weather information
    """
    try:
        url = f"https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
            "timezone": "auto"
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        current = data.get("current", {})
        
        return {
            "location": f"{latitude}, {longitude}",
            "temperature": current.get("temperature_2m"),
            "humidity": current.get("relative_humidity_2m"),
            "wind_speed": current.get("wind_speed_10m"),
            "weather_code": current.get("weather_code"),
            "time": current.get("time"),
            "units": data.get("current_units", {})
        }
    except Exception as e:
        return {"error": f"Failed to fetch weather data: {str(e)}"}

if __name__ == "__main__":
    mcp.run() 