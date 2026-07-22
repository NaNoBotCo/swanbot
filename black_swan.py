import discord
import os
import signal
import sys
import asyncio
from dotenv import load_dotenv
from agent import run_black_swan

# === LOAD ENV ===
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))

# === DISCORD SETUP ===
intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.members = True

discord_client = discord.Client(intents=intents)
message_lock = asyncio.Lock()

def graceful_exit(sig, frame):
    print("🖤 Black Swan signing off...")
    sys.exit(0)

signal.signal(signal.SIGINT, graceful_exit)

@discord_client.event
async def on_ready():
    print(f"🖤 Black Swan is live as {discord_client.user.name}")

@discord_client.event
async def on_message(message):
    if message.author == discord_client.user:
        return

    if message.content.lower().startswith("swan"):
        prompt = message.content[len("swan"):].strip()
        async with message_lock:
            try:
                reply = await run_black_swan(prompt)
                await message.channel.send(reply)
            except Exception as e:
                await message.channel.send(f"🖤 Error: `{type(e).__name__}`")
                raise

if __name__ == "__main__":
    print("🖤 Launching Black Swan...")
    discord_client.run(DISCORD_TOKEN)
