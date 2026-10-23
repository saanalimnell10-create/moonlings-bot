import discord
from discord.ext import commands

class ChannelManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="lock")
    @commands.has_permissions(manage_channels=True)
    async def lock_channel(self, ctx, *, reason: str = "No reason provided"):
        """Locks the current channel so regular members cannot send messages."""
        await ctx.message.delete()
        try:
            await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False, reason=reason)
            embed = discord.Embed(
                title="🔒 Channel Locked",
                description=f"This channel has been locked.\n**Reason:** {reason}",
                color=discord.Color.from_rgb(255, 182, 193)
            )
            embed.set_footer(text="Moonlings Channel Management 🌸")
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("❌ I don't have permissions to manage permissions in this channel.", delete_after=5)

    @commands.command(name="unlockchannel")
    @commands.has_permissions(manage_channels=True)
    async def unlock_channel(self, ctx):
        """Unlocks the current channel, restoring regular messaging permissions."""
        await ctx.message.delete()
        try:
            await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True, reason=f"Unlocked by {ctx.author}")
            embed = discord.Embed(
                title="🔓 Channel Unlocked",
                description="This channel has been unlocked. Normal chatting is restored~ 🌸",
                color=discord.Color.from_rgb(152, 251, 152)
            )
            embed.set_footer(text="Moonlings Channel Management 🌸")
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("❌ I don't have permissions to manage permissions in this channel.", delete_after=5)

    @commands.command(name="purge")
    @commands.has_permissions(manage_messages=True)
    async def purge_messages(self, ctx, amount: int):
        """Deletes a specified number of messages from the channel."""
        await ctx.message.delete()
        if amount <= 0:
            await ctx.send("❌ Please specify a number greater than 0.", delete_after=5)
            return
        
        deleted = await ctx.channel.purge(limit=amount)
        embed = discord.Embed(
            title="🧹 Messages Purged",
            description=f"Successfully deleted {len(deleted)} messages.",
            color=discord.Color.from_rgb(230, 210, 240)
        )
        embed.set_footer(text="Moonlings Channel Management 🌸")
        msg = await ctx.send(embed=embed)
        await msg.delete(delay=5)

    @commands.command(name="slowmode")
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int = 0):
        """Sets a slowmode delay for the current channel."""
        await ctx.message.delete()
        try:
            await ctx.channel.edit(slowmode_delay=seconds)
            if seconds == 0:
                desc = "Slowmode has been disabled."
            else:
                desc = f"Slowmode set to {seconds} seconds."
            
            embed = discord.Embed(
                title="⏳ Slowmode Updated",
                description=desc,
                color=discord.Color.from_rgb(230, 210, 240)
            )
            embed.set_footer(text="Moonlings Channel Management 🌸")
            await ctx.send(embed=embed, delete_after=5)
        except discord.Forbidden:
            await ctx.send("❌ I don't have permissions to change slowmode in this channel.", delete_after=5)

async def setup(bot):
    await bot.add_cog(ChannelManagement(bot))
