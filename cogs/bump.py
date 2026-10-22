import discord
from discord.ext import commands
import asyncio

class BumpReminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bump_channels = {}

    @commands.command(name="setbumpchannel")
    @commands.has_permissions(manage_guild=True)
    async def setbumpchannel(self, ctx, channel: discord.TextChannel = None):
        """Configures the channel for Star Bump reminders."""
        if not channel:
            channel = ctx.channel
        
        self.bump_channels[ctx.guild.id] = channel.id
        
        embed = discord.Embed(
            title="⭐ Star Bumps Channel Set!",
            description=f"This cozy channel ({channel.mention}) is now our official bump spot!\nI'll keep track of the 2-hour orbit and call out the pookies when it's time~ 🌸",
            color=0xFFB7C5
        )
        await ctx.send(embed=embed)

    @commands.command(name="bump")
    async def bump_command(self, ctx):
        """Manual bump reminder info."""
        embed = discord.Embed(
            title="🌸 Star Bump Reminder 🌸",
            description="Use Disboard's **`/bump`** command to help our server shine brighter! ✨",
            color=0xFFB7C5
        )
        embed.set_footer(text="Moonlings Bot • Cozy Space")
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        # Listen to Disboard bot (ID: 302050872383242240)
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
                    title="✨ Yay, Bump Successful!",
                    description="Thank you for boosting our star power! I've set the 2-hour timer for the next orbit. 🌙",
                    color=0xFFB7C5
                )
                await target_channel.send(embed=embed)
                
                # Schedule the 2-hour reminder (7200 seconds)
                self.bot.loop.create_task(self.schedule_bump_reminder(target_channel))

    async def schedule_bump_reminder(self, channel):
        await asyncio.sleep(7200)

        guild = channel.guild
        bump_role = discord.utils.get(guild.roles, name="Bump Reminder")
        role_mention = bump_role.mention if bump_role else ""

        embed = discord.Embed(
            title="⏰ Time to Bump the Moon! ✨",
            description="Hey pookies! It's time to run `/bump` again and help Moonlings glow! 🌙💫",
            color=0xFFD1DC
        )
        
        content = f"{role_mention} Time to bump!" if role_mention else "Time to bump! ✨"
        await channel.send(content=content, embed=embed)

async def setup(bot):
    await bot.add_cog(BumpReminder(bot))
