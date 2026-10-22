import discord
from discord.ext import commands, tasks
import asyncio

class BumpReminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Kuunnellaan kaikkia kanavan viestejä siltä varalta, että Disboard lähettää bump-vahvistuksen
    @commands.Cog.listener()
    async def on_message(self, message):
        # Tarkistetaan, että viesti on Disboard-botilta (ID: 302050872383242240)
        if message.author.id == 302050872383242240:
            # Tarkistetaanko löytyykö viestistä tai sen embedeistä maininta onnistuneesta bumpista
            is_successful_bump = False
            
            if message.content and "Bump done!" in message.content:
                is_successful_bump = True
            elif message.embeds:
                for embed in message.embeds:
                    if embed.description and "Bump done!" in embed.description:
                        is_successful_bump = True

            if is_successful_bump:
                # Lähetetään kiitos ja ilmoitetaan että ajastin alkaa (esim. 2 tuntia)
                embed = discord.Embed(
                    title="🌸 Kiitos bumpista! ✨",
                    description="Moonlings on merkannut uuden bumpin muistiin! Muistuttelen teitä taas 2 tunnin päästä. 🌙💫",
                    color=0xFFB7C5
                )
                await message.channel.send(embed=embed)
                
                # Käynnistetään 2 tunnin ajastin taustalle (2 hours = 7200 seconds)
                self.bot.loop.create_task(self.schedule_bump_reminder(message.channel))

    async def schedule_bump_reminder(self, channel):
        # Odotetaan 2 tuntia (7200 sekuntia)
        await asyncio.sleep(7200)

        # Haetaan mahdollinen Bump Reminder -rooli turvallisesti
        guild = channel.guild
        bump_role = discord.utils.get(guild.roles, name="Bump Reminder")
        role_mention = bump_role.mention if bump_role else ""

        embed = discord.Embed(
            title="⏰ Aika nostaa palvelinta! ✨",
            description="Hei tähtityypit! Nyt voi taas käyttää `/bump`-komentoa ja auttaa Moonlingsiä loistamaan kirkkaammin! 🌙💫",
            color=0xFFD1DC
        )
        
        content = f"{role_mention} Uuden bumpin aika!" if role_mention else "Uuden bumpin aika! ✨"
        await channel.send(content=content, embed=embed)

async def setup(bot):
    await bot.add_cog(BumpReminder(bot))
