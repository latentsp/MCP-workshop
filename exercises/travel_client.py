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
    print("🔧 Connecting to MCP server to discover available tools...")
    server_params = StdioServerParameters(
        command="python",
        args=["travel_server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("✅ Connected to MCP server successfully")
            
            tools_result = await session.list_tools()
            tools = [
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
            print(f"📋 Discovered {len(tools)} tools: {', '.join([t['function']['name'] for t in tools])}")
            return tools

async def call_mcp_tool(tool_name: str, arguments: dict) -> str:
    """Call an MCP tool with the given arguments."""
    print(f"🛠️  Executing tool: {tool_name} with arguments: {arguments}")
    server_params = StdioServerParameters(
        command="python",
        args=["travel_server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            result = await session.call_tool(tool_name, arguments)
            tool_result = result.content[0].text if result.content else "No result"
            print(f"✅ Tool {tool_name} completed successfully")
            return tool_result

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
    print("📝 Adding user message to conversation history")
    conversation_history.append({
        "role": "user",
        "content": user_input
    })
    
    # Use the full conversation history for context
    messages = conversation_history.copy()
    print(f"💭 Using conversation history with {len(messages)} messages for context")
    
    # Make initial request to OpenAI
    print("🤖 Sending request to OpenAI GPT-4...")
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    print("✅ Received response from OpenAI")
    
    message = response.choices[0].message
    
    # Handle tool calls if any
    if message.tool_calls:
        print(f"🔧 OpenAI wants to call {len(message.tool_calls)} tool(s): {[tc.function.name for tc in message.tool_calls]}")
        
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
        for i, tool_call in enumerate(message.tool_calls, 1):
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            print(f"🔄 Executing tool {i}/{len(message.tool_calls)}: {function_name}")
            
            # Call the MCP tool
            tool_result = await call_mcp_tool(function_name, function_args)
            
            # Add tool result to messages
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_result
            })
        
        print("🤖 Sending tool results back to OpenAI for final response...")
        # Get final response from OpenAI
        final_response = client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )
        
        assistant_response = final_response.choices[0].message.content
        
        # Add final assistant response to conversation history
        print("💾 Updating conversation history with tool calls and final response")
        conversation_history.extend(messages[len(conversation_history):])  # Add any new messages from tool calls
        conversation_history.append({
            "role": "assistant",
            "content": assistant_response
        })
        
        return assistant_response, conversation_history
    
    # No tool calls, add assistant response directly to conversation history
    print("💬 No tool calls needed, responding directly")
    assistant_response = message.content
    print("💾 Updating conversation history with direct response")
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
    
    print("🚀 Initializing travel assistant...")
    
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
    
    print("="*100)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye! Have a great trip! ✈️")
                break
                
            if not user_input:
                continue
                
            print(f"\n🔄 Processing your request: '{user_input}'")
            print("-" * 100)
            response, conversation_history = await process_user_query(user_input, conversation_history)
            print("-" * 100)
            print(f"\nAssistant: {response}")
            print("="*100)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye! Have a great trip! ✈️")
            break
        except Exception as e:
            print(f"❌ Error occurred: {e}")
            print("🔄 Please try again or type 'quit' to exit")

if __name__ == "__main__":
    asyncio.run(main()) 