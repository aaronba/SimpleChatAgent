"""
Pre-flight check for SimpleChatAgent with Azure AI Foundry
Run this before starting your bot to ensure everything is configured correctly
"""

import sys
import os
from pathlib import Path

def check_python_version():
    """Check Python version >= 3.9"""
    version = sys.version_info
    print(f"\n{'='*60}")
    print("Python Version Check")
    print(f"{'='*60}")
    print(f"Current version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ FAIL: Python 3.9 or newer is required")
        return False
    else:
        print("✓ PASS: Python version is adequate")
        return True

def check_packages():
    """Check required packages are installed"""
    print(f"\n{'='*60}")
    print("Package Installation Check")
    print(f"{'='*60}")
    
    required_packages = [
        ("microsoft_agents.hosting.aiohttp", "CloudAdapter"),
        ("microsoft_agents.hosting.core", "AgentApplication"),
        ("agent_framework.azure", "AzureAIAgentClient"),
        ("azure.identity.aio", "AzureCliCredential"),
        ("dotenv", "load_dotenv"),
    ]
    
    all_passed = True
    for package, item in required_packages:
        try:
            module = __import__(package, fromlist=[item])
            getattr(module, item)
            print(f"✓ {package}.{item}")
        except ImportError as e:
            print(f"❌ {package}.{item} - NOT INSTALLED")
            all_passed = False
        except AttributeError as e:
            print(f"⚠️  {package}.{item} - Package found but {item} missing")
            all_passed = False
    
    if not all_passed:
        print("\n💡 To fix, run:")
        print("   pip install -r requirements_foundry.txt")
    
    return all_passed

def check_env_file():
    """Check .env file exists and has required variables"""
    print(f"\n{'='*60}")
    print("Environment Configuration Check")
    print(f"{'='*60}")
    
    env_path = Path(__file__).parent / '.env'
    
    if not env_path.exists():
        print("❌ FAIL: .env file not found")
        print("\n💡 To fix:")
        print("   1. Copy .env.example to .env")
        print("   2. Edit .env and add your Azure settings")
        return False
    
    print(f"✓ .env file exists: {env_path}")
    
    # Load and check variables
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=env_path)
    
    required_vars = {
        "AZURE_AI_PROJECT_ENDPOINT": "Your Azure AI project endpoint",
        "AZURE_AI_MODEL_DEPLOYMENT_NAME": "Your model deployment name (e.g., gpt-4o)",
    }
    
    all_set = True
    for var, description in required_vars.items():
        value = os.environ.get(var)
        if not value or value == "":
            print(f"❌ {var} is not set")
            print(f"   ({description})")
            all_set = False
        else:
            # Mask the value for security
            masked = value[:30] + "..." if len(value) > 30 else value
            print(f"✓ {var}={masked}")
    
    if not all_set:
        print("\n💡 To fix:")
        print("   Edit .env file and add missing values")
        print("   Get values from https://ai.azure.com")
    
    return all_set

def check_azure_cli():
    """Check Azure CLI is installed and logged in"""
    print(f"\n{'='*60}")
    print("Azure CLI Check")
    print(f"{'='*60}")
    
    import subprocess
    import platform
    
    # On Windows, we need shell=True to find .cmd files
    is_windows = platform.system() == "Windows"
    
    # Check if az is installed
    try:
        result = subprocess.run(
            ["az", "--version"],
            capture_output=True,
            text=True,
            timeout=5,
            shell=is_windows  # Only use shell on Windows
        )
        if result.returncode == 0:
            print("✓ Azure CLI is installed")
        else:
            print("❌ FAIL: Azure CLI not working properly")
            return False
    except FileNotFoundError:
        print("❌ FAIL: Azure CLI not installed")
        print("\n💡 To fix:")
        if is_windows:
            print("   Download from: https://aka.ms/azure-cli")
        else:
            print("   Install with: curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash")
            print("   Or visit: https://learn.microsoft.com/cli/azure/install-azure-cli")
        return False
    except Exception as e:
        print(f"⚠️  Could not verify Azure CLI: {e}")
        return False
    
    # Check if logged in
    try:
        result = subprocess.run(
            ["az", "account", "show"],
            capture_output=True,
            text=True,
            timeout=5,
            shell=is_windows  # Only use shell on Windows
        )
        if result.returncode == 0:
            print("✓ Logged in to Azure")
            # Try to extract account info
            import json
            try:
                account_info = json.loads(result.stdout)
                print(f"  Account: {account_info.get('user', {}).get('name', 'Unknown')}")
                print(f"  Subscription: {account_info.get('name', 'Unknown')}")
            except:
                pass
            return True
        else:
            print("❌ FAIL: Not logged in to Azure")
            print("\n💡 To fix:")
            print("   Run: az login")
            return False
    except Exception as e:
        print(f"⚠️  Could not verify Azure login: {e}")
        return False

def check_port_available():
    """Check if port 3978 is available"""
    print(f"\n{'='*60}")
    print("Port Availability Check")
    print(f"{'='*60}")
    
    import socket
    
    port = int(os.environ.get("PORT", 3978))
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        
        if result == 0:
            print(f"⚠️  WARNING: Port {port} is already in use")
            print(f"   Another instance might be running")
            return False
        else:
            print(f"✓ Port {port} is available")
            return True
    except Exception as e:
        print(f"⚠️  Could not check port: {e}")
        return True  # Assume available if we can't check

def main():
    """Run all checks"""
    print("\n" + "="*60)
    print("SimpleChatAgent - Pre-flight Check")
    print("="*60)
    
    results = {
        "Python Version": check_python_version(),
        "Required Packages": check_packages(),
        "Environment Config": check_env_file(),
        "Azure CLI": check_azure_cli(),
        "Port Availability": check_port_available(),
    }
    
    print(f"\n{'='*60}")
    print("Summary")
    print(f"{'='*60}")
    
    for check, passed in results.items():
        status = "✓ PASS" if passed else "❌ FAIL"
        print(f"{status}: {check}")
    
    all_passed = all(results.values())
    
    print(f"\n{'='*60}")
    if all_passed:
        print("✅ All checks passed! Ready to run:")
        print("   python app_with_foundry.py")
    else:
        print("⚠️  Some checks failed. Fix issues above before running.")
    print(f"{'='*60}\n")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
