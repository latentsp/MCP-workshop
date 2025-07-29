import asyncio
import json
import os
from typing import List, Dict, Any, Tuple
from openai import OpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv
# Load environment variables
load_dotenv("../.env")

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def get_mcp_tools() -> List[Dict[str, Any]]:
    """Get available tools from the MCP server in OpenAI format.

    Returns:
        A list of tools in OpenAI format.
    """
    server_params = StdioServerParameters(
        command="python",
        args=["travel_server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            tools_result = await session.list_tools()
            return [
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema,
                    },
                }
                for tool in tools_result.tools
            ]

async def call_mcp_tool(tool_name: str, arguments: dict) -> str:
    """Call an MCP tool with the given arguments."""
    server_params = StdioServerParameters(
        command="python",
        args=["travel_server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            result = await session.call_tool(tool_name, arguments)
            return result.content[0].text if result.content else "No result"

async def process_user_query(user_input: str, conversation_history: List[Dict[str, Any]]) -> Tuple[str, List[Dict[str, Any]]]:
    """Process user input with OpenAI and handle any tool calls.
    
    Args:
        user_input: The user's input message
        conversation_history: Previous conversation messages
        
    Returns:
        Tuple of (assistant_response, updated_conversation_history)
    """
    
    # Get available tools dynamically from MCP server
    tools = await get_mcp_tools()
    
    # Add user input to conversation history
    conversation_history.append({
        "role": "user",
        "content": user_input
    })
    
    # Use the full conversation history for context
    messages = conversation_history.copy()
    
    # Make initial request to OpenAI
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    
    message = response.choices[0].message
    
    # Handle tool calls if any
    if message.tool_calls:
        # Add assistant message to conversation
        messages.append({
            "role": "assistant",
            "content": message.content,
            "tool_calls": [
                {
                    "id": tool_call.id,
                    "type": "function",
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments
                    }
                }
                for tool_call in message.tool_calls
            ]
        })
        
        # Execute each tool call
        for tool_call in message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            # Call the MCP tool
            tool_result = await call_mcp_tool(function_name, function_args)
            
            # Add tool result to messages
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_result
            })
        
        # Get final response from OpenAI
        final_response = client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )
        
        assistant_response = final_response.choices[0].message.content
        
        # Add final assistant response to conversation history
        conversation_history.extend(messages[len(conversation_history):])  # Add any new messages from tool calls
        conversation_history.append({
            "role": "assistant",
            "content": assistant_response
        })
        
        return assistant_response, conversation_history
    
    # No tool calls, add assistant response directly to conversation history
    assistant_response = message.content
    conversation_history.append({
        "role": "assistant",
        "content": assistant_response
    })
    
    return assistant_response, conversation_history

async def main():
    """Main chat loop for the travel assistant."""
    print("🌍 Travel Booking Assistant")
    print("Ask me anything about travel recommendations, booking trips, or transportation!")
    print("Type 'quit' to exit.\n")
    
    # Initialize conversation history with system message
    conversation_history = [
        {
            "role": "system",
            "content": """You are a helpful travel booking assistant. You can help users with:
            1. Getting travel recommendations based on destination, budget, and duration
            2. Booking trips with traveler details and dates
            3. Booking transportation linked to existing trip bookings
            
            Always be helpful and ask for clarification if needed. When booking trips, generate reasonable booking IDs if not provided.
            You have access to the user's conversation history, so you can reference previous bookings and recommendations.
            """
        }
    ]
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Goodbye! Have a great trip! ✈️")
                break
                
            if not user_input:
                continue
                
            print("\nAssistant: ", end="")
            response, conversation_history = await process_user_query(user_input, conversation_history)
            print(response)
            
        except KeyboardInterrupt:
            print("\nGoodbye! Have a great trip! ✈️")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 