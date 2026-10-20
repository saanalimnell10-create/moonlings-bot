import os
import asyncio
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# --- 1. FLASK SERVER (Pitää botin pystyssä 24/7 Renderissä) ---
app = Flask('')

@app.route('/')
def home():
    return "Moonlings Bot is Online!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 2. BOTIN PERUSASETUKSET ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="??", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("Moonlings bot is online and ready!")
    await bot.change_presence(activity=discord.Game(name="??help | Moonlings"))

# --- 3. AUTOMAATTINEN COGS-LATAJA (Lataa uudet tiedostot automaattisesti) ---
async def load_extensions():
    if not os.path.exists("./cogs"):
        os.makedirs("./cogs")
        
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            cog_name = filename[:-3]
            try:
                await bot.load_extension(f"cogs.{cog_name}")
                print(f"✅ Ladattu automaattisesti: {filename}")
            except Exception as e:
                print(f"❌ Virhe ladattaessa {filename}: {e}")

async def main():
    async with bot:
        await load_extensions()
        TOKEN = os.getenv("DISCORD_TOKEN")
        if TOKEN:
            keep_alive()
            await bot.start(TOKEN)
        else:
            print("Virhe: DISCORD_TOKENia ei löytynyt ympäristömuuttujista!")

if __name__ == "__main__":
    asyncio.run(main())
