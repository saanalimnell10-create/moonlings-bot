import discord
from discord.ext import commands
import asyncio

class BumpReminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Tallennetaan kanavakohtainen muistutuskanava väliaikaisesti muistiin
        self.bump_channels = {}

    @commands.command(name="setbumpchannel")
    @commands.has_permissions(manage_guild=True)
    async def setbumpchannel(self, ctx, channel: discord.TextChannel = None):
        """Asettaa kanavan,neen jonne bump-muistutukset lähetetään."""
        if not channel:
            channel = ctx.channel
        
        self.bump_channels[ctx.guild.id] = channel.id
        
        embed = discord.Embed(
            title="🌸 Bump-kanava asetettu! ✨",
            description=f"Tästä lähtien bump-muistutukset lähetetään tälle kanavalle: {channel.mention} 🌙",
            color=0xFFB7C5
        )
        await ctx.send(embed=embed)

    @commands.command(name="bump")
    async def bump_command(self, ctx):
        """Muistuttaa miten palvelinta nostetaan."""
        embed = discord.Embed(
            title="🌸 Star Bump Reminder 🌸",
            description="Käytä Disboardin **`/bump`**-komentoa nostaaksesi palvelintamme! ✨",
            color=0xFFB7C5
        )
        embed.set_footer(text="Moonlings Bot • Cozy Space")
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        # Kuunnellaan Disboard-bottia (ID: 302050872383242240)
        if message.author.id == 302050872383242240:
            is_successful_bump = False
            
            if message.content and "Bump done!" in message.content:
                is_successful_bump = True
            elif message.embeds:
                for embed in message.embeds:
                    if embed.description and "Bump done!" in embed.description:
                        is_successful_bump = True

            if is_successful_bump:
                guild_id = message.guild.id
                target_channel = self.bot.get_channel(self.bump_channels.get(guild_id, message.channel.id))
                if not target_channel:
                    target_channel = message.channel

                embed = discord.Embed(
                    title="🌸 Kiitos bumpista! ✨",
                    description="Moonlings on merkannut onnistuneen bumpin muistiin! Palaan asiaan 2 tunnin päästä. 🌙💫",
                    color=0xFFB7C5
                )
                await target_channel.send(embed=embed)
                
                # Ajastetaan uusi muistutus 2 tunnin päähän (7200 sekuntia)
                self.bot.loop.create_task(self.schedule_bump_reminder(target_channel))

    async def schedule_bump_reminder(self, channel):
        await asyncio.sleep(7200)

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
