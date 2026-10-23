import os
import asyncio
import traceback
import discord
from discord.ext import commands
from keep_alive import keep_alive

# Tuodaan dynaaminen prefix-funktio prefix-cogista
from cogs.prefix import get_prefix_for_guild

# Asetetaan tarvittavat intentit (vaaditaan mm. viestien lukemiseen ja jäseniin)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Luodaan botti-instanssi dynaamisella etuliitteellä ja poistetaan oletushelp käytöstä
bot = commands.Bot(command_prefix=get_prefix_for_guild, intents=intents, help_command=None)

@bot.event
async def on_ready():
    """Tulostetaan viesti konsoliin, kun botti on käynnistynyt onnistuneesti."""
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    print("Moonlings is online and cozy! 🌸✨")

async def load_extensions():
    """Lataa automaattisesti kaikki cogs-kansion alaiset .py-tiedostot."""
    if not os.path.exists("./cogs"):
        print("⚠️ Varoitus: 'cogs'-kansiota ei löytynyt!")
        return

    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            cog_name = filename[:-3]
            try:
                await bot.load_extension(f"cogs.{cog_name}")
                print(f"✅ Ladattu cog: {filename}")
            except Exception as e:
                print(f"❌ Virhe ladattaessa cogia {filename}:")
                traceback.print_exc()  # Tulostaa tarkan virheen ja rivinumeron lokeihin

async def main():
    """Pääfunktio, joka lataa cogit ja käynnistää botin turvallisesti."""
    async with bot:
        await load_extensions()
        TOKEN = os.getenv("DISCORD_TOKEN")
        
        if TOKEN:
            await bot.start(TOKEN)
        else:
            print("❌ Virhe: DISCORD_TOKENia ei löytynyt ympäristömuuttujista!")

if __name__ == "__main__":
    # Käynnistetään Flask keep-alive -palvelin (Renderiä varten) ja botti
    keep_alive()
    asyncio.run(main())
