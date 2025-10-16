# app_with_foundry.py
# This version integrates Azure AI Foundry Agent Service
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

from microsoft_agents.hosting.core import (
    AgentApplication,
    TurnState,
    TurnContext,
    MemoryStorage,
)
from microsoft_agents.hosting.aiohttp import CloudAdapter
from start_server import start_server

# Option 1: Using Azure AI Foundry Agent Service with agent_framework
# Requires: pip install agent-framework azure-ai-projects azure-identity
try:
    from agent_framework.azure import AzureAIAgentClient
    from azure.identity.aio import AzureCliCredential
    
    # Environment variables needed:
    # AZURE_AI_PROJECT_ENDPOINT - Your Azure AI Foundry project endpoint
    # AZURE_AI_MODEL_DEPLOYMENT_NAME - Your model deployment name (e.g., gpt-4o)
    
    FOUNDRY_ENABLED = (
        os.environ.get("AZURE_AI_PROJECT_ENDPOINT") and 
        os.environ.get("AZURE_AI_MODEL_DEPLOYMENT_NAME")
    )
except ImportError:
    print("Warning: agent-framework not installed. Install with: pip install agent-framework azure-identity")
    FOUNDRY_ENABLED = False

AGENT_APP = AgentApplication[TurnState](
    storage=MemoryStorage(), adapter=CloudAdapter()
)

# Store Azure AI client globally if enabled
azure_ai_client = None
azure_credential = None


async def _help(context: TurnContext, _: TurnState):
    if FOUNDRY_ENABLED:
        await context.send_activity(
            "Welcome to the Azure AI Foundry Agent 🚀\n"
            "Connected to Azure AI Foundry Agent Service.\n"
            "Type /help for help or send a message to interact with the AI agent."
        )
    else:
        await context.send_activity(
            "Welcome to the Echo Agent sample 🚀. "
            "Type /help for help or send a message to see the echo feature in action.\n\n"
            "To enable Azure AI Foundry integration, set:\n"
            "- AZURE_AI_PROJECT_ENDPOINT\n"
            "- AZURE_AI_MODEL_DEPLOYMENT_NAME\n"
            "And install: pip install agent-framework azure-identity"
        )


AGENT_APP.conversation_update("membersAdded")(_help)
AGENT_APP.message("/help")(_help)


@AGENT_APP.activity("message")
async def on_message(context: TurnContext, state: TurnState):
    """Handle incoming messages with Azure AI Foundry integration."""
    user_message = context.activity.text
    
    if not user_message:
        return
    
    # Check for special commands
    if user_message.lower() == "/help":
        await _help(context, state)
        return
    
    if FOUNDRY_ENABLED:
        try:
            # Use Azure AI Foundry Agent Service
            global azure_ai_client, azure_credential
            
            # Initialize client if not already done
            if azure_ai_client is None:
                if azure_credential is None:
                    azure_credential = AzureCliCredential()
                
                azure_ai_client = AzureAIAgentClient(
                    async_credential=azure_credential,
                    agent_name="SimpleChatAgent",
                )
            
            # Create an agent for this message
            # Note: Each message creates a new agent. For conversation history,
            # we'd need to implement per-user conversation tracking with store=True
            agent = azure_ai_client.create_agent(
                instructions="You are a helpful assistant. Be concise and friendly.",
            )
            
            # Get response from the agent
            result = await agent.run(user_message)
            
            # Send the response back to the user
            await context.send_activity(f"{result}")
            
        except Exception as e:
            error_msg = f"Error calling Azure AI Foundry: {str(e)}"
            print(error_msg)
            await context.send_activity(f"❌ {error_msg}")
    else:
        # Fallback to echo behavior
        await context.send_activity(f"you said: {user_message}")


if __name__ == "__main__":
    try:
        # Print configuration status
        print("\n" + "="*60)
        print("SimpleChatAgent - Azure AI Foundry Integration")
        print("="*60)
        
        if FOUNDRY_ENABLED:
            print("✓ Azure AI Foundry Agent Service: ENABLED")
            print(f"  Endpoint: {os.environ.get('AZURE_AI_PROJECT_ENDPOINT')}")
            print(f"  Model: {os.environ.get('AZURE_AI_MODEL_DEPLOYMENT_NAME')}")
            print("\nMake sure to run 'az login' for authentication!")
        else:
            print("⚠ Azure AI Foundry Agent Service: DISABLED")
            print("\nTo enable, set environment variables:")
            print("  AZURE_AI_PROJECT_ENDPOINT")
            print("  AZURE_AI_MODEL_DEPLOYMENT_NAME")
            print("\nAnd install: pip install agent-framework azure-identity")
        
        print("="*60 + "\n")
        
        start_server(AGENT_APP, None)
    except Exception as error:
        raise error
