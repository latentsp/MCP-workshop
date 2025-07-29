import os
import json
from datetime import datetime
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP(
    name="Travel Booking Server",
    host="0.0.0.0",  # only used for SSE transport (localhost)
    port=8051,  # only used for SSE transport (set this to any port)
)

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
    recommendations = {
        "paris": {
            "low": "Visit free museums, walk along Seine, picnic in parks",
            "medium": "Eiffel Tower, Louvre, Seine river cruise, local bistros",
            "high": "Luxury hotels, Michelin restaurants, private tours, shopping"
        },
        "tokyo": {
            "low": "Temple visits, street food, public gardens, local markets",
            "medium": "Tokyo Skytree, traditional ryokan, sushi restaurants, theme parks",
            "high": "Luxury hotels in Ginza, kaiseki dining, private cultural experiences"
        },
        "new york": {
            "low": "Central Park, free museums, food trucks, Brooklyn Bridge walk",
            "medium": "Broadway shows, Empire State Building, nice restaurants, shopping",
            "high": "Luxury hotels, fine dining, helicopter tours, exclusive experiences"
        },
        "london": {
            "low": "Free museums, Hyde Park, Camden Market, pub food",
            "medium": "Tower Bridge, West End shows, afternoon tea, historic tours",
            "high": "Luxury hotels, Michelin dining, private tours, exclusive experiences"
        }
    }
    
    dest_lower = destination.lower()
    budget_tier = "low" if budget < 1000 else "medium" if budget < 3000 else "high"
    
    if dest_lower in recommendations:
        activities = recommendations[dest_lower][budget_tier]
        return f"Trip recommendation for {destination} ({duration_days} days, ${budget} budget):\n{activities}"
    else:
        return f"For {destination} with a ${budget} budget for {duration_days} days, I recommend researching local attractions, cultural sites, regional cuisine, and accommodation options that fit your budget tier ({budget_tier})."

@mcp.tool()
def book_trip(traveler_name: str, destination: str, start_date: str, end_date: str, budget: int) -> str:
    """Book a trip and save the booking details to a file.
    
    Args:
        traveler_name: Full name of the traveler
        destination: Destination city/country
        start_date: Trip start date in YYYY-MM-DD format
        end_date: Trip end date in YYYY-MM-DD format
        budget: Total budget in USD
        
    Returns:
        Booking confirmation details including booking ID
    """
    booking_data = {
        "booking_id": "CURRENT_TRIP",
        "traveler_name": traveler_name,
        "destination": destination,
        "start_date": start_date,
        "end_date": end_date,
        "budget": budget,
        "booking_date": datetime.now().isoformat(),
        "status": "confirmed"
    }
    
    # Ensure the bookings directory exists
    bookings_dir = os.path.join(os.path.dirname(__file__), "bookings")
    os.makedirs(bookings_dir, exist_ok=True)
    
    # Save booking to file (always overwrite the same file)
    filename = os.path.join(bookings_dir, "current_trip.json")
    with open(filename, 'w') as f:
        json.dump(booking_data, f, indent=2)
    
    return f"Trip booked successfully!\nBooking ID: {booking_data['booking_id']}\nTraveler: {traveler_name}\nDestination: {destination}\nDates: {start_date} to {end_date}\nBudget: ${budget}\nBooking saved to: current_trip.json"

@mcp.tool()
def book_transportation(booking_id: str, transport_type: str, departure: str, arrival: str, departure_time: str) -> str:
    """Book transportation for a trip.
    
    Args:
        booking_id: The trip booking ID to link transportation to
        transport_type: Type of transport (flight, train, bus, car)
        departure: Departure location
        arrival: Arrival location  
        departure_time: Departure date and time in YYYY-MM-DD HH:MM format
        
    Returns:
        Transportation booking confirmation details
    """
    transport_data = {
        "transport_booking_id": "CURRENT_TRANSPORT",
        "trip_booking_id": booking_id,
        "transport_type": transport_type,
        "departure": departure,
        "arrival": arrival,
        "departure_time": departure_time,
        "booking_date": datetime.now().isoformat(),
        "status": "confirmed"
    }
    
    # Ensure the bookings directory exists
    bookings_dir = os.path.join(os.path.dirname(__file__), "bookings")
    os.makedirs(bookings_dir, exist_ok=True)
    
    # Save transportation booking to file (always overwrite the same file)
    filename = os.path.join(bookings_dir, "current_transport.json")
    with open(filename, 'w') as f:
        json.dump(transport_data, f, indent=2)
    
    return f"Transportation booked successfully!\nTransport ID: {transport_data['transport_booking_id']}\nType: {transport_type}\nRoute: {departure} → {arrival}\nDeparture: {departure_time}\nLinked to trip: {booking_id}\nBooking saved to: current_transport.json"

# Run the server
if __name__ == "__main__":
    mcp.run(transport="stdio") 