# SimpleChatAgent with Azure AI Foundry Integration

This project integrates the Microsoft Agent Framework with Azure AI Foundry Agent Service.

## Prerequisites

1. **Azure AI Foundry Project**: Create a project at [Azure AI Foundry Portal](https://ai.azure.com)
2. **Model Deployment**: Deploy a model (e.g., gpt-4o, gpt-4o-mini) in your project
3. **Azure CLI**: Install and authenticate with `az login`
4. **Python 3.8+**: Ensure you have Python installed

## Setup Instructions

### 1. Install Dependencies

```powershell
# Install Azure AI Foundry packages
pip install agent-framework azure-identity azure-ai-projects

# Or use the requirements file
pip install -r requirements_foundry.txt
```

### 2. Configure Environment Variables

Copy the example environment file and fill in your values:

```powershell
# Copy the template
Copy-Item .env.example .env

# Edit .env and set:
# - AZURE_AI_PROJECT_ENDPOINT (from Azure AI Foundry portal)
# - AZURE_AI_MODEL_DEPLOYMENT_NAME (your model deployment name)
```

**Finding your Azure AI Project Endpoint:**
1. Go to https://ai.azure.com
2. Select your project
3. Go to "Settings" → "Project overview"
4. Copy the "Project endpoint" URL

**Example values:**
```
AZURE_AI_PROJECT_ENDPOINT=https://your-project.services.ai.azure.com/api/projects/your-project-id
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4o-mini
```

### 3. Authenticate with Azure

```powershell
# Login with Azure CLI
az login

# Verify you're logged in
az account show
```

### 4. Run the Agent

```powershell
# Run the Foundry-integrated version
python app_with_foundry.py

# Or run the original echo version
python app.py
```

The server will start on `http://localhost:3978` (or the PORT you specified).

## Features

### Azure AI Foundry Integration

When properly configured, the agent will:
- ✓ Connect to Azure AI Foundry Agent Service
- ✓ Use your deployed model for intelligent responses
- ✓ Automatically manage agent lifecycle
- ✓ Handle authentication via Azure CLI credentials

### Fallback Mode

If Azure AI Foundry is not configured, the agent runs in "echo mode":
- Simple echo responses for testing
- No external dependencies required

## Architecture

```
User Message
    ↓
Microsoft Agent Framework (Bot Framework)
    ↓
SimpleChatAgent (app_with_foundry.py)
    ↓
Azure AI Foundry Agent Service (AzureAIAgentClient)
    ↓
Your Deployed Model (e.g., GPT-4o)
    ↓
Response back to user
```

## Code Structure

- **`app_with_foundry.py`**: Main application with Azure AI Foundry integration
- **`app.py`**: Original echo agent (no Azure dependencies)
- **`start_server.py`**: Server setup and HTTP endpoint configuration
- **`requirements_foundry.txt`**: Python dependencies for Foundry integration

## Key Components

### AzureAIAgentClient

The core client for interacting with Azure AI Foundry:

```python
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential

# Initialize client
azure_ai_client = AzureAIAgentClient(
    async_credential=AzureCliCredential(),
    agent_name="SimpleChatAgent",
)

# Create and use agent
agent = azure_ai_client.create_agent(
    instructions="You are a helpful assistant.",
)
result = await agent.run(user_message)
```

## Advanced Options

### Adding Tools/Functions

You can add function calling capabilities:

```python
from typing import Annotated
from pydantic import Field

def get_weather(
    location: Annotated[str, Field(description="City name")]
) -> str:
    """Get weather for a location."""
    return f"The weather in {location} is sunny, 72°F"

# Create agent with tools
agent = azure_ai_client.create_agent(
    instructions="You are a helpful assistant with weather access.",
    tools=[get_weather],
)
```

### Using MCP Tools

Add Model Context Protocol tools:

```python
from agent_framework import MCPStreamableHTTPTool

# Create agent with MCP tool
agent = azure_ai_client.create_agent(
    instructions="You can search Microsoft documentation.",
    tools=MCPStreamableHTTPTool(
        name="Microsoft Learn MCP",
        url="https://learn.microsoft.com/api/mcp",
    ),
)
```

## Troubleshooting

### "Azure CLI credential authentication failed"

**Solution**: Run `az login` to authenticate

### "AZURE_AI_PROJECT_ENDPOINT is not set"

**Solution**: Set the environment variable in your `.env` file or PowerShell:
```powershell
$env:AZURE_AI_PROJECT_ENDPOINT="https://your-endpoint.com"
```

### "Model deployment not found"

**Solution**: Verify the model deployment name in Azure AI Foundry portal

### Import errors

**Solution**: Install dependencies:
```powershell
pip install agent-framework azure-identity azure-ai-projects
```

## References

- [Microsoft Agent Framework GitHub](https://github.com/microsoft/agent-framework)
- [Azure AI Foundry Documentation](https://learn.microsoft.com/azure/ai-foundry/)
- [Azure AI Foundry Portal](https://ai.azure.com)
- [Getting Started Samples](https://github.com/microsoft/agent-framework/tree/main/python/samples/getting_started)

## Next Steps

1. Explore [Azure AI Agent samples](https://github.com/microsoft/agent-framework/tree/main/python/samples/getting_started/agents/azure_ai)
2. Add [function tools](https://github.com/microsoft/agent-framework/tree/main/python/samples/getting_started/agents/azure_ai/azure_ai_with_function_tools.py)
3. Implement [MCP tools](https://github.com/microsoft/agent-framework/tree/main/python/samples/getting_started/agents/azure_ai/azure_ai_with_local_mcp.py)
4. Try [workflow patterns](https://github.com/microsoft/agent-framework/tree/main/python/samples/getting_started/workflows)
