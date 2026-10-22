import discord
from discord.ext import commands, tasks
import asyncio

class BumpReminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Esimerkki: ajastin tai tarkistus, jos teet automaattista muistutusta
        # Voit säätää aikaa tarpeen mukaan (esim. 2 tuntia Disboardin bump-ajastimen mukaan)
        
    @commands.command(name="bump")
    async def bump_command(self, ctx):
        # Esimerkkikomento manuaaliseen bump-kehotukseen tai ohjeistukseen
        embed = discord.Embed(
            title="🌸 Star Bump Reminder 🌸",
            description="Kiitos kun haluat nostaa palvelintamme! Kirjoita **`/bump`** (jos Disboard on käytössä) tai muistuta muita.",
            color=0xFFB7C5  # Söpö pastellivaaleanpunainen
        )
        embed.set_footer(text="Moonlings Bot • Cozy Space")
        await ctx.send(embed=embed)

    # Esimerkki funktiosta, joka lähettää muistutuksen ilmaneveryone-pingejä
    async def send_bump_reminder(self, channel_id):
        channel = self.bot.get_channel(channel_id)
        if not channel:
            return

        # Etsitään palvelimelta rooli nimeltä "Bump Reminder" (vältetääneveryone kokonaan!)
        guild = channel.guild
        bump_role = discord.utils.get(guild.roles, name="Bump Reminder")
        
        role_mention = bump_role.mention if bump_role else ""

        embed = discord.Embed(
            title="⏰ Aika nostaa palvelinta! ✨",
            description="Hei tähtityypit! Nyt voi taas käyttää `/bump`-komentoa ja auttaa Moonlingsiä loistamaan kirkkaammin! 🌙💫",
            color=0xFFD1DC
        )
        
        # Lähetetään viesti, jossa mainitaan vain haluttu rooli (tai ei roolia ollenkaan, jos roolia ei löydy)
        content = f"{role_mention} Pienen muistutuksen aika!" if role_mention else "Pienen muistutuksen aika! ✨"
        
        await channel.send(content=content, embed=embed)

async def setup(bot):
    await bot.add_cog(BumpReminder(bot))
