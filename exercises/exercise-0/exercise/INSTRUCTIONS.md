**Instructions**

This is a one-time script, not a chat application.

You need to create two files: `client.py` and `server.py`.

- Run the program using: `python client.py`
- This will automatically start `server.py` in the background.

**Requirements:**

- `server.py` should implement an [MCP server](https://gofastmcp.com/getting-started/quickstart).
- The server must expose a "weather" tool that uses the [Open-Meteo API](https://open-meteo.com/).

**What `client.py` should do automatically:**

1. Start the server.
2. List all available tools.
3. If the weather tool exists, call it and print the result.
   - You can assume you know the schema for the weather tool - https://gofastmcp.com/servers/tools
   - If you assume this then the list_tools call is just for practice
