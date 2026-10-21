import discord
from discord.ext import commands
import asyncio

class BumpReminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bump_channel_id = None

    @commands.command(name="setbumpchannel")
    @commands.has_permissions(administrator=True)
    async def set_bump_channel(self, ctx):
        await ctx.message.delete()
        self.bump_channel_id = ctx.channel.id

        embed = discord.Embed(
            title="🌌 ∙ Star Bumps Channel Set!",
            description="This cozy channel is now our official bump spot! ✨\nI'll keep track of the 2-hour orbit and call out the pookies when it's time~ 🌸",
            color=discord.Color.from_rgb(175, 238, 238)
        )
        embed.set_footer(text="Moonlings Star Bumps ☁️", icon_url=self.bot.user.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        # Tarkistetaan että viesti on Disboard-botilta (ID: 302050872383242240)
        if message.author.id == 302050872383242240:
            if message.embeds:
                channel = self.bot.get_channel(self.bump_channel_id) if self.bump_channel_id else message.channel

                success_embed = discord.Embed(
                    title="🌟 ∙ Star Bump Successful!",
                    description="Thank you so much for the bump, pookies! 💖\nI've set a cozy 2-hour timer in the stars. I'll remind everyone when it's time again~ 🚀✨",
                    color=discord.Color.from_rgb(255, 182, 193)
                )
                success_embed.set_footer(text="Moonlings Orbit Timer 🌙", icon_url=self.bot.user.display_avatar.url)
                await channel.send(embed=success_embed)

                # Odotetaan 2 tuntia (7200 sekuntia)
                await asyncio.sleep(7200)

                reminder_embed = discord.Embed(
                    title="⏰ ∙ Time to Bump, Pookies!",
                    description="Hey hey pookies! 🌌 It's time to bump our cozy home again using `/bump` or `!bump` to help Moonlings shine brighter across the galaxy! ✨💫",
                    color=discord.Color.from_rgb(230, 230, 250)
                )
                reminder_embed.set_footer(text="Moonlings Star Bumps ☁️", icon_url=self.bot.user.display_avatar.url)
                
                # Etsitään "Bump Reminder" -rooli palvelimelta
                bump_role = discord.utils.get(channel.guild.roles, name="Bump Reminder")
                
                if bump_role:
                    # Pingaa roolia suoraan (allowed_mentions varmistaa että ilmoitus menee perille)
                    await channel.send(
                        content=f"✨ {bump_role.mention} Wake up pookies, time for a new Star Bump! 🌸",
                        embed=reminder_embed,
                        allowed_mentions=discord.AllowedMentions(roles=True)
                    )
                else:
                    # Jos roolia ei löydy, pingaa @everyone
                    await channel.send(
                        content="✨ **@everyone** Wake up pookies, time for a new Star Bump! 🌸",
                        embed=reminder_embed
                    )

async def setup(bot):
    await bot.add_cog(BumpReminder(bot))
