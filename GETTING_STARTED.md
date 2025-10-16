# Azure AI Foundry Integration - Quick Start

## What Was Added

I've integrated Microsoft Agent Framework code from the [getting_started samples](https://github.com/microsoft/agent-framework/tree/main/python/samples/getting_started) to enable your bot to call the Azure AI Foundry Agent Service.

## New Files Created

1. **`app_with_foundry.py`** - Enhanced version of your agent with Azure AI Foundry integration
2. **`foundry_examples.py`** - 6 example patterns showing different ways to use Azure AI Foundry
3. **`requirements_foundry.txt`** - Python dependencies for Azure AI Foundry
4. **`.env.example`** - Template for configuration
5. **`README_FOUNDRY.md`** - Comprehensive documentation
6. **`setup_foundry.ps1`** - Automated setup script for PowerShell

## Quick Setup (3 Steps)

### 1. Run Setup Script
```powershell
.\setup_foundry.ps1
```

This will:
- Install required packages (`agent-framework`, `azure-identity`, `azure-ai-projects`)
- Check Azure CLI installation
- Create `.env` file from template

### 2. Configure Your Settings

Edit the `.env` file and add:
```
AZURE_AI_PROJECT_ENDPOINT=https://your-project.services.ai.azure.com/api/projects/your-project-id
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4o-mini
```

**Where to find these values:**
1. Go to https://ai.azure.com
2. Select your project
3. Go to Settings → Project overview
4. Copy the "Project endpoint" URL
5. Note your model deployment name (from Deployments section)

### 3. Authenticate and Run
```powershell
# Login to Azure
az login

# Test the examples
python foundry_examples.py

# Run your agent with Foundry integration
python app_with_foundry.py
```

## Testing Your Agent

### Install Microsoft 365 Agents Playground

From a terminal (while keeping the agent running), install the test tool:

```powershell
npm install -g @microsoft/teams-app-test-tool
```

### Run the Playground

```powershell
teamsapptester
```

This will:
- Open your default browser
- Connect to your agent at `http://localhost:3978`
- Let you chat with your agent interactively

You can now send messages to test the Azure AI Foundry integration!

**Reference:** [Microsoft 365 Agents SDK Quickstart](https://learn.microsoft.com/en-us/microsoft-365/agents-sdk/quickstart-python)

## How It Works

The integration uses the `AzureAIAgentClient` from the Microsoft Agent Framework:

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

## Key Features

✅ **Automatic Agent Management** - Agents are created and deleted automatically  
✅ **Azure CLI Authentication** - Uses your Azure login credentials  
✅ **Fallback Mode** - Works as echo bot if Azure AI Foundry not configured  
✅ **Function Calling** - Can add custom tools/functions  
✅ **MCP Tools** - Can integrate Model Context Protocol servers  

## Example Patterns Included

The `foundry_examples.py` file demonstrates:

1. **Basic Agent** - Simplest usage pattern
2. **Agent with Function Tools** - Add custom Python functions
3. **Agent with MCP Tools** - Integrate external tools
4. **Responses Client** - Alternative Azure OpenAI approach
5. **Bot Framework Integration** - Your specific use case

## Architecture

```
User Message
    ↓
Microsoft Bot Framework (your existing code)
    ↓
app_with_foundry.py (new integration layer)
    ↓
Azure AI Foundry Agent Service (AzureAIAgentClient)
    ↓
Your Deployed Model (GPT-4o, etc.)
    ↓
Response
```

## Original vs. Enhanced

**Original (`app.py`):**
- Simple echo bot
- No AI capabilities
- No external dependencies

**Enhanced (`app_with_foundry.py`):**
- Full AI conversation capabilities
- Azure AI Foundry integration
- Fallback to echo if not configured

## Troubleshooting

**Issue: Import errors**
```powershell
pip install agent-framework azure-identity azure-ai-projects
```

**Issue: Authentication failed**
```powershell
az login
az account show
```

**Issue: Agent creation failed**
- Verify AZURE_AI_PROJECT_ENDPOINT is correct
- Verify AZURE_AI_MODEL_DEPLOYMENT_NAME exists in your project
- Check you have permissions to the project

## References

- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [Getting Started Samples](https://github.com/microsoft/agent-framework/tree/main/python/samples/getting_started)
- [Azure AI Foundry Portal](https://ai.azure.com)
- [Azure AI Foundry Docs](https://learn.microsoft.com/azure/ai-foundry/)

## Next Steps

1. **Run the examples**: `python foundry_examples.py`
2. **Add function tools**: See Example 2 in `foundry_examples.py`
3. **Add MCP tools**: See Example 3 in `foundry_examples.py`
4. **Explore workflows**: Check out [workflow samples](https://github.com/microsoft/agent-framework/tree/main/python/samples/getting_started/workflows)

## Support

For issues with:
- **This integration**: Check `README_FOUNDRY.md`
- **Agent Framework**: https://github.com/microsoft/agent-framework/issues
- **Azure AI Foundry**: https://learn.microsoft.com/azure/ai-foundry/
