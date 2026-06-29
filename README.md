# Termux Discord AI Bot

A Discord bot that runs on Termux (Android) and uses AI to respond to messages.

## Features
- 🤖 AI-powered responses using local models or APIs
- 📱 Runs on Termux (Android terminal)
- 💬 Responds to Discord messages in real-time
- ⚙️ Customizable AI model and parameters
- 🔒 Secure token management

## Prerequisites
- Termux app installed on Android
- Python 3.8+ or Node.js
- Discord bot token
- AI model access (Ollama local, OpenAI API, etc.)
- Stable internet connection

## Installation

### 1. Set up Termux
```bash
pkg update && pkg upgrade
pkg install python git curl
```

### 2. Clone this repository
```bash
git clone https://github.com/krikitgt/Termux-discord-bot.git
cd Termux-discord-bot
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure the bot
```bash
cp config.example.json config.json
# Edit config.json with your settings
```

## Configuration

Create a `config.json` file:
```json
{
  "discord_token": "YOUR_BOT_TOKEN",
  "ai_model": "ollama",
  "model_name": "llama2",
  "ai_api_url": "http://localhost:11434",
  "prefix": "!",
  "description": "Discord AI Bot"
}
```

## Running the Bot
```bash
python bot.py
```

## Commands
- `!ping` - Check if bot is alive
- `!ask <question>` - Ask the AI a question
- `!status` - Show AI model status

## Getting a Discord Bot Token
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Go to "Bot" section and click "Add Bot"
4. Copy the token and add to your `config.json`
5. Enable "Message Content Intent" in Privileged Gateway Intents
6. Invite the bot to your server using the OAuth2 URL

## Troubleshooting
- **Bot not responding**: Check if token is valid and Message Content Intent is enabled
- **AI timeouts**: Ensure Ollama is running or API is accessible
- **Termux crashes**: Increase available storage and RAM

## Contributing
Feel free to submit issues and PRs!

## License
MIT