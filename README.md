# MCP Step-by-Step Tutorial

This repository provides a step-by-step guide to understanding the MCP (Meta-Call Protocol) using the `fastmcp` library.

## Introduction

This project is based on the official `fastmcp` [quickstart guide](https://gofastmcp.com/getting-started/quickstart) and is intended to provide a hands-on learning experience for anyone new to MCP.

## Getting Started

Follow these steps to get the project up and running on your local machine.

### Prerequisites

* Python 3.7+
* `pip` or `pip3`

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/mcp-step-by-step.git
    cd mcp-step-by-step
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Example

1.  **Start the MCP server:**
    Open a terminal and run the following command:
    ```bash
    python my_server.py
    ```
    This will start the MCP server and wait for incoming connections.

2.  **Run the client:**
    Open a *new* terminal and run the following command:
    ```bash
    python my_client.py
    ```
    You should see the following output in the client terminal:
    ```
    Hello, Ford!
    ```

## How It Works

*   `my_server.py`: This file defines a simple MCP server with a single tool called `greet`. The `@mcp.tool` decorator registers the `greet` function as a tool that can be called by clients.
*   `my_client.py`: This file creates an MCP client that connects to the server defined in `my_server.py`. It then calls the `greet` tool with the name "Ford" and prints the result.

## Next Steps

Now that you have a basic MCP server and client running, you can start experimenting! Here are a few ideas:

*   Add more tools to `my_server.py`.
*   Modify `my_client.py` to call the new tools.
*   Explore the `fastmcp` documentation to learn about more advanced features. 