# MCP Step-by-Step Tutorial

This repository provides a step-by-step guide to understanding the MCP (Meta-Call Protocol) using the `fastmcp` library.

This project is based on the official `fastmcp` [quickstart guide](https://gofastmcp.com/getting-started/quickstart) and is intended to provide a hands-on learning experience for anyone new to MCP.

## Getting Started

Follow these steps to get the project up and running on your local machine.

### Prerequisites

* Python 3.7+
* `pip` or `pip3`

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/latentsp/MCP-workshop.git
    cd MCP-workshop
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

1.  **Run the client:**
    Open a *new* terminal and run the following command:
    ```bash
    cd module-0
    python my_client.py
    ```
    You should see the following output in the client terminal:
    ```
    Hello, Ford!
    ```

## How It Works

*   `my_server.py`: This file defines a simple MCP server with a single tool called `greet`. The `@mcp.tool` decorator registers the `greet` function as a tool that can be called by clients.
*   `my_client.py`: This file creates an MCP client that connects to the server defined in `my_server.py`. It then calls the `greet` tool with the name "Ford" and prints the result.