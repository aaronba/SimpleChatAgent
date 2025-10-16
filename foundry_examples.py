"""
Azure AI Foundry Agent Service Examples
Based on: https://github.com/microsoft/agent-framework/tree/main/python/samples/getting_started

These examples show different ways to use Azure AI Foundry Agent Service.
"""

import os
import asyncio
from pathlib import Path
from typing import Annotated
from pydantic import Field
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)


# ============================================================================
# Example 1: Basic Azure AI Agent (Simplest)
# ============================================================================
async def example_basic_agent():
    """
    Create a simple agent that auto-creates and auto-deletes.
    Reference: azure_ai_with_explicit_settings.py
    """
    from agent_framework.azure import AzureAIAgentClient
    from azure.identity.aio import AzureCliCredential
    
    print("\n=== Example 1: Basic Azure AI Agent ===\n")
    
    async with (
        AzureCliCredential() as credential,
        AzureAIAgentClient(
            async_credential=credential,
            # These can also come from environment variables:
            # project_endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
            # model_deployment_name=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
        ).create_agent(
            instructions="You are a helpful assistant.",
        ) as agent,
    ):
        result = await agent.run("Tell me a joke about programming")
        print(f"Agent: {result}\n")


# ============================================================================
# Example 2: Agent with Function Tools
# ============================================================================
async def example_agent_with_tools():
    """
    Create an agent with function calling capabilities.
    Reference: azure_ai_with_function_tools.py
    """
    from agent_framework import ChatAgent
    from agent_framework.azure import AzureAIAgentClient
    from azure.identity.aio import AzureCliCredential
    
    print("\n=== Example 2: Agent with Function Tools ===\n")
    
    # Define a tool function
    def get_weather(
        location: Annotated[str, Field(description="The city name")]
    ) -> str:
        """Get the current weather for a location."""
        # This is a mock implementation
        return f"The weather in {location} is sunny and 72°F"
    
    async with (
        AzureCliCredential() as credential,
        ChatAgent(
            chat_client=AzureAIAgentClient(async_credential=credential),
            instructions="You are a helpful weather assistant.",
            tools=[get_weather],  # Add function tools
            store=True,  # Enable conversation storage (suppresses warning)
        ) as agent,
    ):
        result = await agent.run("What's the weather in Seattle?")
        print(f"Agent: {result}\n")


# ============================================================================
# Example 3: Agent with MCP Tools
# ============================================================================
async def example_agent_with_mcp():
    """
    Create an agent with Model Context Protocol tools.
    Reference: azure_ai_with_local_mcp.py
    """
    from agent_framework import ChatAgent, MCPStreamableHTTPTool
    from agent_framework.azure import AzureAIAgentClient
    from azure.identity.aio import AzureCliCredential
    
    print("\n=== Example 3: Agent with MCP Tools ===\n")
    
    async with (
        AzureCliCredential() as credential,
        ChatAgent(
            chat_client=AzureAIAgentClient(async_credential=credential),
            instructions="You can search Microsoft documentation.",
            tools=MCPStreamableHTTPTool(
                name="Microsoft Learn MCP",
                url="https://learn.microsoft.com/api/mcp",
            ),
            store=True,  # Enable conversation storage (suppresses warning)
        ) as agent,
    ):
        result = await agent.run(
            "How to create an Azure storage account using az cli?"
        )
        print(f"Agent: {result}\n")


# ============================================================================
# Example 4: Azure OpenAI Responses Client (Alternative)
# ============================================================================
async def example_responses_client():
    """
    Use Azure OpenAI Responses client directly (alternative to Azure AI).
    Reference: azure_responses_client_with_explicit_settings.py
    Note: This example uses sync credential as ResponsesClient doesn't support async.
    """
    from agent_framework.azure import AzureOpenAIResponsesClient
    from azure.identity import AzureCliCredential
    
    print("\n=== Example 4: Azure OpenAI Responses Client ===\n")
    
    # Requires different environment variables:
    # AZURE_OPENAI_ENDPOINT
    # AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME
    
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    deployment = os.environ.get("AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME")
    
    if not endpoint or not deployment:
        print("⚠️  Skipping: AZURE_OPENAI_ENDPOINT or AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME not set\n")
        return
    
    # ResponsesClient uses sync credential
    credential = AzureCliCredential()
    try:
        async with AzureOpenAIResponsesClient(
            deployment_name=deployment,
            endpoint=endpoint,
            credential=credential,
        ).create_agent(
            instructions="You are a helpful assistant.",
        ) as agent:
            result = await agent.run("What is Azure AI Foundry?")
            print(f"Agent: {result}\n")
    finally:
        credential.close()


# ============================================================================
# Example 5: Integration with Bot Framework (Your Use Case)
# ============================================================================
async def example_bot_framework_integration():
    """
    Show how to integrate with Microsoft Bot Framework.
    This is the pattern used in your app_with_foundry.py
    """
    from agent_framework.azure import AzureAIAgentClient
    from azure.identity.aio import AzureCliCredential
    
    print("\n=== Example 5: Bot Framework Integration ===\n")
    
    # This simulates your bot receiving a message
    user_message = "What can you help me with?"
    
    # Use async context managers for proper cleanup
    async with (
        AzureCliCredential() as credential,
        AzureAIAgentClient(
            async_credential=credential,
            agent_name="SimpleChatAgent",
        ).create_agent(
            instructions="You are a helpful assistant in a chat bot.",
        ) as agent,
    ):
        # Process user message
        result = await agent.run(user_message)
        print(f"User: {user_message}")
        print(f"Bot: {result}\n")


# ============================================================================
# Main - Run Examples
# ============================================================================
async def main():
    """Run all 5 examples."""
    print("\n" + "="*70)
    print("Azure AI Foundry Agent Service Examples (5 patterns)")
    print("="*70)
    
    # Check environment
    endpoint = os.environ.get("AZURE_AI_PROJECT_ENDPOINT")
    model = os.environ.get("AZURE_AI_MODEL_DEPLOYMENT_NAME")
    
    if not endpoint or not model:
        print("\n⚠️  WARNING: Required environment variables not set!")
        print("\nPlease set:")
        print("  AZURE_AI_PROJECT_ENDPOINT")
        print("  AZURE_AI_MODEL_DEPLOYMENT_NAME")
        print("\nAnd run: az login")
        print("\nSome examples will be skipped.\n")
    else:
        print(f"\n✓ Project Endpoint: {endpoint}")
        print(f"✓ Model: {model}")
        print("\nMake sure you've run: az login\n")
    
    # Run examples
    try:
        await example_basic_agent()
    except Exception as e:
        print(f"❌ Example 1 failed: {e}\n")
    
    try:
        await example_agent_with_tools()
    except Exception as e:
        print(f"❌ Example 2 failed: {e}\n")
    
    try:
        await example_agent_with_mcp()
    except Exception as e:
        print(f"❌ Example 3 failed: {e}\n")
    
    try:
        await example_responses_client()
    except Exception as e:
        print(f"❌ Example 4 failed: {e}\n")
    
    try:
        await example_bot_framework_integration()
    except Exception as e:
        print(f"❌ Example 5 failed: {e}\n")
    
    print("="*70)
    print("Examples completed!")
    print("="*70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
