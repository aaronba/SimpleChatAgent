# SimpleChatAgent - Azure AI Foundry Integration

## 🎯 What You Have

A working Bot Framework chat agent integrated with **Azure AI Foundry Agent Service**.

## ✅ Current Status

**FULLY WORKING** - Production ready!

- ✅ Azure AI Foundry integration complete
- ✅ Automatic agent lifecycle management
- ✅ Azure CLI authentication
- ✅ Fallback to echo bot if Azure not configured
- ✅ Function calling support ready
- ✅ MCP tools integration ready
- ✅ 5 working example patterns

## 📁 Essential Files

```
app_with_foundry.py       - Main application with Azure AI integration
start_server.py           - Server setup
.env                      - Your Azure configuration
requirements_foundry.txt  - Dependencies
```

## 🚀 Quick Start

1. **Install dependencies:**
   ```powershell
   pip install -r requirements_foundry.txt
   ```

2. **Configure .env file:**
   ```env
   AZURE_AI_PROJECT_CONNECTION_STRING=your_connection_string
   AZURE_AI_MODEL_DEPLOYMENT_NAME=your_model_name
   ```

3. **Run:**
   ```powershell
   python app_with_foundry.py
   ```

4. **Test:**
   ```powershell
   python test_setup.py
   ```

## 📚 Learning Resources

- **Examples**: Run `python foundry_examples.py` to see 6 patterns
- **Documentation**: See `README_FOUNDRY.md` and `GETTING_STARTED.md`
- **File Guide**: See `WHAT_FILES_DO_I_NEED.md`

## 🔧 What It Does

1. User sends message to bot
2. Bot creates an Azure AI agent on-demand
3. Agent processes the message with AI
4. Response sent back to user
5. Agent deleted after conversation

**Why no persistent agents?** The Azure AI Projects SDK doesn't currently support persistent conversation threads, but the non-persistent approach works great and provides full AI capabilities.

## 🎓 Example Patterns Available

1. **Basic Agent** - Simple AI responses
2. **Function Tools** - Add custom Python functions the agent can call
3. **MCP Tools** - Integrate external Model Context Protocol tools
4. **Responses Client** - Alternative Azure OpenAI integration
5. **Bot Framework** - Your current implementation

## 📦 Dependencies

Key packages:
- `agent-framework==0.4.0` - Microsoft Agent Framework
- `azure-ai-projects==1.1.0b2` - Azure AI Projects SDK
- `azure-identity==1.23.0` - Azure authentication
- `python-dotenv==1.0.1` - Environment variables
- `aiohttp==3.11.11` - Async HTTP server

## 🌐 Bot Framework Integration

Works with Bot Framework channels:
- Teams
- Slack
- Web Chat
- SMS
- And more...

Your agent automatically integrates with any Bot Framework channel!

## 🎯 Next Steps

1. ✅ **Test your setup**: `python test_setup.py`
2. ✅ **Run examples**: `python foundry_examples.py`
3. 🔨 **Add custom functions**: Modify `app_with_foundry.py` to add tools
4. 🔨 **Add MCP tools**: Integrate external tools
5. 🚀 **Deploy**: Use Azure App Service or Container Apps

## 💡 Tips

- **Fallback mode**: If Azure isn't configured, it works as echo bot
- **Function calling**: Add custom Python functions as tools
- **Error handling**: Built-in error handling and logging
- **Testing**: `test_setup.py` verifies your Azure setup
- **Clean project**: Only essential files needed

## 📖 Documentation Files

- `README_FOUNDRY.md` - Complete documentation
- `GETTING_STARTED.md` - Quick start guide
- `WHAT_FILES_DO_I_NEED.md` - File organization guide
- `PROJECT_SUMMARY.md` - This file!

## ✨ You're All Set!

Your Azure AI Foundry integration is complete and working. Time to build something awesome! 🚀
