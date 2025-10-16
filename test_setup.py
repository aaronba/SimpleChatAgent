"""
Simple test script to verify Azure AI Foundry setup
Run this to check if your configuration is working correctly
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)
print(f"Loading .env from: {env_path}")
if env_path.exists():
    print(f"✓ .env file found")
else:
    print(f"⚠ .env file not found at {env_path}")


def print_header(text):
    """Print a formatted header."""
    print("\n" + "="*60)
    print(text)
    print("="*60)


def check_environment_variables():
    """Check if required environment variables are set."""
    print_header("Checking Environment Variables")
    
    required_vars = {
        "AZURE_AI_PROJECT_ENDPOINT": "Your Azure AI project endpoint",
        "AZURE_AI_MODEL_DEPLOYMENT_NAME": "Your model deployment name"
    }
    
    all_set = True
    for var, description in required_vars.items():
        value = os.environ.get(var)
        if value:
            # Mask the endpoint URL for security
            if "ENDPOINT" in var:
                display_value = value[:30] + "..." if len(value) > 30 else value
            else:
                display_value = value
            print(f"✓ {var}={display_value}")
        else:
            print(f"✗ {var} - NOT SET")
            print(f"  ({description})")
            all_set = False
    
    return all_set


def check_packages():
    """Check if required Python packages are installed."""
    print_header("Checking Python Packages")
    
    required_packages = [
        "agent_framework",
        "azure.identity",
        "azure.ai.projects",
    ]
    
    all_installed = True
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} - NOT INSTALLED")
            all_installed = False
    
    if not all_installed:
        print("\nInstall missing packages with:")
        print("  pip install agent-framework azure-identity azure-ai-projects")
    
    return all_installed


def check_azure_cli():
    """Check if Azure CLI is installed and user is logged in."""
    print_header("Checking Azure CLI")
    
    import subprocess
    import shutil
    
    # Check if az command exists using shutil.which (more reliable on Windows)
    az_path = shutil.which("az")
    if not az_path:
        # Try common installation paths on Windows
        common_paths = [
            r"C:\Program Files (x86)\Microsoft SDKs\Azure\CLI2\wbin\az.cmd",
            r"C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin\az.cmd",
        ]
        for path in common_paths:
            if os.path.exists(path):
                az_path = path
                break
    
    if not az_path:
        print("✗ Azure CLI is NOT installed")
        print("  Download from: https://aka.ms/azure-cli")
        return False
    
    print(f"✓ Azure CLI is installed")
    print(f"  Location: {az_path}")
    
    # Check if logged in
    try:
        # Use shell=True on Windows for better compatibility
        result = subprocess.run(
            "az account show",
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print("✓ Logged in to Azure")
            # Parse account info
            import json
            try:
                account_info = json.loads(result.stdout)
                print(f"  Account: {account_info.get('user', {}).get('name', 'Unknown')}")
                print(f"  Subscription: {account_info.get('name', 'Unknown')}")
            except:
                pass
            return True
        else:
            print("✗ Not logged in to Azure")
            print("  Run: az login")
            return False
    except Exception as e:
        print(f"✗ Error checking Azure login: {e}")
        return False


async def test_azure_ai_connection():
    """Test actual connection to Azure AI Foundry."""
    print_header("Testing Azure AI Foundry Connection")
    
    try:
        from agent_framework.azure import AzureAIAgentClient
        from azure.identity.aio import AzureCliCredential
        
        print("Attempting to connect to Azure AI Foundry...")
        
        # Properly manage all async resources with context managers
        async with AzureCliCredential() as credential:
            async with AzureAIAgentClient(
                async_credential=credential,
                agent_name="TestAgent",
            ) as client:
                print("✓ Successfully created AzureAIAgentClient")
                
                # Try to create a simple agent
                print("Creating a test agent...")
                async with client.create_agent(
                    instructions="You are a test assistant. Just say 'Hello!'",
                ) as agent:
                    print("✓ Successfully created test agent")
                    
                    # Try a simple query
                    print("Sending test query...")
                    result = await agent.run("Say hello")
                    
                    # Convert result to string properly
                    result_str = str(result)
                    preview = result_str[:100] if len(result_str) > 100 else result_str
                    print(f"✓ Successfully received response: {preview}...")
                    
                    # Agent will be automatically deleted when exiting the context manager
                    print("✓ Test agent cleaned up")
            
            return True
            
    except ImportError as e:
        print(f"✗ Import error: {e}")
        print("  Install packages: pip install agent-framework azure-identity")
        return False
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        print("\nPossible issues:")
        print("  - Check your AZURE_AI_PROJECT_ENDPOINT is correct")
        print("  - Check your AZURE_AI_MODEL_DEPLOYMENT_NAME exists")
        print("  - Verify you have access to the Azure AI project")
        print("  - Run: az login")
        return False


def main():
    """Run all checks."""
    print("\n" + "🔍 Azure AI Foundry Setup Verification".center(60))
    
    # Run checks
    env_ok = check_environment_variables()
    packages_ok = check_packages()
    azure_cli_ok = check_azure_cli()
    
    # Summary
    print_header("Summary")
    
    if env_ok and packages_ok and azure_cli_ok:
        print("✓ All prerequisites are met!")
        print("\nRunning connection test...")
        
        # Test actual connection
        import asyncio
        connection_ok = asyncio.run(test_azure_ai_connection())
        
        if connection_ok:
            print_header("🎉 SUCCESS!")
            print("Your Azure AI Foundry setup is working correctly!")
            print("\nNext steps:")
            print("  1. Run examples: python foundry_examples.py")
            print("  2. Start your agent: python app_with_foundry.py")
        else:
            print_header("⚠️  PARTIAL SUCCESS")
            print("Prerequisites are installed but connection failed.")
            print("Please check the error messages above.")
    else:
        print("✗ Some prerequisites are missing.")
        print("\nPlease address the issues above and run this test again.")
        print("\nQuick fixes:")
        if not packages_ok:
            print("  pip install agent-framework azure-identity azure-ai-projects")
        if not env_ok:
            print("  Edit .env file with your Azure AI settings")
        if not azure_cli_ok:
            print("  Run: az login")
    
    print("\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)
