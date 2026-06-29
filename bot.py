#!/usr/bin/env python3
"""
Termux Discord AI Bot
A Discord bot powered by AI running on Termux
"""

import discord
from discord.ext import commands
import json
import os
import asyncio
import aiohttp
from datetime import datetime

# Load configuration
def load_config():
    if not os.path.exists('config.json'):
        print("❌ config.json not found. Please copy config.example.json to config.json")
        exit(1)
    
    with open('config.json', 'r') as f:
        return json.load(f)

CONFIG = load_config()

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.dm_messages = True

bot = commands.Bot(command_prefix=CONFIG['prefix'], intents=intents)

class AIModel:
    """Handle AI model interactions"""
    
    def __init__(self, config):
        self.config = config
        self.model_type = config.get('ai_model', 'ollama')
        self.model_name = config.get('model_name', 'llama2')
        self.api_url = config.get('ai_api_url', 'http://localhost:11434')
    
    async def generate_response(self, prompt: str) -> str:
        """Generate AI response for given prompt"""
        try:
            if self.model_type == 'ollama':
                return await self._ollama_response(prompt)
            else:
                return "❌ Unknown AI model type"
        except Exception as e:
            print(f"Error generating response: {e}")
            return f"❌ Error: {str(e)}"
    
    async def _ollama_response(self, prompt: str) -> str:
        """Get response from Ollama"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_url}/api/generate",
                    json={
                        "model": self.model_name,
                        "prompt": prompt,
                        "stream": False,
                        "temperature": CONFIG.get('temperature', 0.7),
                    },
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data.get('response', 'No response generated')
                    else:
                        return f"❌ Ollama error: {resp.status}"
        except asyncio.TimeoutError:
            return "❌ AI response timeout. Try a simpler question."
        except Exception as e:
            return f"❌ Connection error: {str(e)}"

# Initialize AI model
ai_model = AIModel(CONFIG)

@bot.event
async def on_ready():
    """Bot is ready"""
    print(f"✅ Bot logged in as {bot.user}")
    print(f"🤖 AI Model: {ai_model.model_name}")
    print(f"📡 API URL: {ai_model.api_url}")
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Error syncing commands: {e}")

@bot.command(name='ping')
async def ping(ctx):
    """Check if bot is alive"""
    latency = bot.latency * 1000
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Latency: {latency:.2f}ms",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

@bot.command(name='ask')
async def ask(ctx, *, question: str = None):
    """Ask the AI a question"""
    if not question:
        await ctx.send("❌ Please provide a question. Usage: `!ask <your question>`")
        return
    
    # Show typing indicator
    async with ctx.typing():
        # Truncate question if too long
        if len(question) > 500:
            await ctx.send("❌ Question too long (max 500 characters)")
            return
        
        response = await ai_model.generate_response(question)
        
        # Split long responses
        if len(response) > 2000:
            chunks = [response[i:i+1900] for i in range(0, len(response), 1900)]
            for chunk in chunks:
                await ctx.send(chunk)
        else:
            embed = discord.Embed(
                title="🤖 AI Response",
                description=response,
                color=discord.Color.blue(),
                timestamp=datetime.now()
            )
            embed.set_footer(text=f"Model: {ai_model.model_name}")
            await ctx.send(embed=embed)

@bot.command(name='status')
async def status(ctx):
    """Show AI model status"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{ai_model.api_url}/api/tags") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    models = [m['name'] for m in data.get('models', [])]
                    embed = discord.Embed(
                        title="🤖 AI Model Status",
                        description=f"✅ Connected to {ai_model.model_type}",
                        color=discord.Color.green()
                    )
                    embed.add_field(name="Current Model", value=ai_model.model_name)
                    embed.add_field(name="Available Models", value="\n".join(models) or "None")
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f"❌ Error: {resp.status}")
    except Exception as e:
        embed = discord.Embed(
            title="❌ Connection Error",
            description=f"Cannot connect to {ai_model.api_url}\n\n{str(e)}",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

@bot.event
async def on_message(message):
    """Handle all messages"""
    # Don't respond to bot messages
    if message.author == bot.user:
        return
    
    # Process commands
    await bot.process_commands(message)

if __name__ == '__main__':
    try:
        bot.run(CONFIG['discord_token'])
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        print("Make sure your Discord token is valid in config.json")
