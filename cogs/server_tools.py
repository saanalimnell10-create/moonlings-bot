import discord
from discord.ext import commands
import re
import aiohttp

class ServerTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="steal")
    @commands.has_permissions(manage_emojis=True)
    async def steal(self, ctx, emoji: str):
        """Copies a custom emoji from another server."""
        # Etsitään custom emojin tiedot merkkijonosta (<:nimi:id> tai <a:nimi:id>)
        match = re.search(r"<(a?):([a-zA-Z0-9\_]+):([0-9]+)>", emoji)
        if not match:
            await ctx.send("❌ Please provide a valid custom emoji from another server!", delete_after=5)
            return

        animated, name, emoji_id = match.groups()
        extension = "gif" if animated else "png"
        url = f"https://cdn.discordapp.com/emojis/{emoji_id}.{extension}"

        # Ladataan emojin tiedostokuva netistä
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    await ctx.send("❌ Could not download the emoji image.", delete_after=5)
                    return
                data = await resp.read()

        try:
            new_emoji = await ctx.guild.create_custom_emoji(name=name, image=data, reason=f"Emoji stolen by {ctx.author}")
            embed = discord.Embed(
                title="✨ Emoji Stolen!",
                description=f"Successfully added {new_emoji} (`:{name}:`) to the server!",
                color=0xFFB6C1
            )
            await ctx.send(embed=embed)
        except discord.HTTPException as e:
            await ctx.send(f"❌ Failed to create emoji: {e}", delete_after=5)

    @commands.command(name="clone")
    @commands.has_permissions(manage_channels=True)
    async def clone(self, ctx):
        """Clones the current channel's settings and permissions."""
        channel = ctx.channel
        new_channel = await channel.clone(reason=f"Channel cloned by {ctx.author}")
        
        embed = discord.Embed(
            title="🌊 Channel Cloned",
            description=f"Successfully cloned this channel into {new_channel.mention}!",
            color=0xFFB6C1
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(ServerTools(bot))
