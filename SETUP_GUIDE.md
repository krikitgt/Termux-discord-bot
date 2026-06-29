# Termux Discord AI Bot - Complete Setup Guide

## Step 1: Prepare Your Android Device

### Install Termux
- Download [Termux](https://f-droid.org/en/packages/com.termux/) from F-Droid (recommended) or Play Store
- Open Termux and run initial setup

### Grant Storage Permissions (Optional but recommended)
```bash
termux-setup-storage
```

## Step 2: Set Up Python in Termux

```bash
# Update package manager
pkg update && pkg upgrade -y

# Install Python and required tools
pkg install python git curl vim

# Verify Python installation
python --version
```

## Step 3: Clone the Repository

```bash
# Navigate to home directory
cd ~

# Clone the repo
git clone https://github.com/krikitgt/Termux-discord-bot.git

# Enter directory
cd Termux-discord-bot
```

## Step 4: Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt

# Verify installations
python -c "import discord; print('discord.py OK')"
```

## Step 5: Get Your Discord Bot Token

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **New Application** and give it a name
3. Go to **Bot** section → Click **Add Bot**
4. Under **TOKEN**, click **Copy** (this is your token)
5. Go to **OAuth2** → **Scopes**: Select `bot`
6. Go to **OAuth2** → **Permissions**: Select:
   - Send Messages
   - Read Messages/View Channels
   - Read Message History
7. Copy the generated URL and open it to invite bot to your server

## Step 6: Configure the Bot

```bash
# Copy example config
cp config.example.json config.json

# Edit with your token (use nano or vim)
nano config.json
```

Update the file:
```json
{
  "discord_token": "YOUR_BOT_TOKEN_HERE",
  "ai_model": "ollama",
  "model_name": "llama2",
  "ai_api_url": "http://localhost:11434",
  "prefix": "!",
  "respond_to_mentions": true,
  "temperature": 0.7,
  "max_tokens": 500
}
```

## Step 7: Set Up AI Model (Choose One)

### Option A: Use Ollama (Local, No Internet Required)

```bash
# Install Ollama
pkg install ollama

# Start Ollama server (in another Termux session)
ollama serve

# Pull a model (in another session)
ollama pull llama2
```

### Option B: Use OpenAI API (Cloud-based)

1. Get API key from [OpenAI](https://platform.openai.com/api-keys)
2. Update `config.json`:
```json
{
  "ai_model": "openai",
  "openai_api_key": "sk-...",
  "model_name": "gpt-3.5-turbo"
}
```

## Step 8: Run the Bot

```bash
# Start the bot
python bot.py

# You should see:
# ✅ Bot logged in as YourBotName#1234
# 🤖 AI Model: llama2
# 📡 API URL: http://localhost:11434
```

## Step 9: Test It!

In your Discord server, try:
```
!ping           # Check if bot responds
!ask Hello      # Ask a simple question
!status         # Check AI model status
```

## Running Multiple Termux Sessions

To keep the bot running while you use Termux for other things:

1. **Session 1**: Run Ollama (if using local model)
   ```bash
   ollama serve
   ```

2. **Session 2**: Run the bot
   ```bash
   cd ~/Termux-discord-bot
   python bot.py
   ```

**To switch between sessions**: Swipe from left edge or use keyboard shortcut

## Keeping Bot Running 24/7

The bot will only run while Termux is active. For 24/7 operation:

### Option 1: Use Termux:Boot (runs on startup)
```bash
# Install Termux:Boot addon from Play Store/F-Droid
mkdir -p ~/.termux/boot
# Create ~/.termux/boot/start-bot with your startup commands
```

### Option 2: Use Screen/tmux
```bash
# Install tmux
pkg install tmux

# Create a session
tmux new-session -d -s discord "cd ~/Termux-discord-bot && python bot.py"

# View session
tmux attach -t discord

# Detach (keep running)
# Press Ctrl+B then D
```

## Troubleshooting

### Bot not responding
- Check Discord token is correct in `config.json`
- Enable **Message Content Intent** in [Developer Portal](https://discord.com/developers/applications) → Bot → Privileged Gateway Intents
- Make sure bot has permission to send messages in the channel

### AI timeouts
- Check internet connection
- If using Ollama, ensure it's running in another Termux session
- Try a simpler question or reduce `max_tokens` in config

### "No module named discord"
```bash
# Reinstall packages
pip install --upgrade -r requirements.txt
```

### Storage issues
```bash
# Check available space
df -h

# Clean up
pkg clean
```

## Advanced: Custom Commands

Edit `bot.py` to add your own commands. Example:

```python
@bot.command(name='hello')
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.name}!")
```

## Tips & Tricks

- **Longer responses**: Split messages over 2000 characters automatically
- **Rate limiting**: Add delays to avoid Discord API limits
- **Monitoring**: Check logs in Termux for debugging
- **Security**: Never share your `config.json` or Discord token

## Support & Issues

Having problems? Check:
1. Do you have an internet connection?
2. Is your Discord token valid?
3. Are the dependencies installed? (`pip list`)
4. Is the AI service running? (if using Ollama)

Good luck! 🚀
