import os
import asyncio
import discord
from discord.ext import commands
from keep_alive import keep_alive

# Asetetaan intenteille oikeudet
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="??", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")

async def load_extensions():
    # Käydään läpi cogs-kansio ja ladataan jokainen .py-tiedosto automaattisesti
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
            await bot.start(TOKEN)
        else:
            print("Virhe: DISCORD_TOKENia ei löytynyt ympäristömuuttujista!")

if __name__ == "__main__":
    keep_alive()  # Käynnistetään Flask keep-alive -palvelin heti alussa
    asyncio.run(main())
