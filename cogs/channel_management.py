import discord
from discord.ext import commands

class ChannelManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 1. PURGE KOMENTO (Poistaa viestejä)
    @commands.command(name="purge")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int = 10):
        await ctx.message.delete()
        deleted = await ctx.channel.purge(limit=amount)
        
        embed = discord.Embed(
            title="🧹 ∙ Channel Purged",
            description=f"Successfully cleaned up **{len(deleted)}** messages~ 🌸✨",
            color=discord.Color.from_rgb(255, 182, 193)
        )
        await ctx.send(embed=embed, delete_after=5)

    # 2. LOCK KOMENTO (Lukitsee kanavan)
    @commands.command(name="lock")
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx):
        await ctx.message.delete()
        
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

        embed = discord.Embed(
            title="🔒 ∙ Channel Locked",
            description="This channel has been locked for a cozy break~ ☁️✨",
            color=discord.Color.from_rgb(255, 182, 193)
        )
        await ctx.send(embed=embed)

    # 3. UNLOCK KOMENTO (Avaa lukituksen)
    @commands.command(name="unlock")
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        await ctx.message.delete()

        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

        embed = discord.Embed(
            title="🔓 ∙ Channel Unlocked",
            description="This channel is now unlocked and open for chatting~ 🌸✨",
            color=discord.Color.from_rgb(175, 238, 238)
        )
        await ctx.send(embed=embed)

    # Virheiden käsittely (jos oikeudet puuttuvat tai numero puuttuu)
    @purge.error
    @lock.error
    @unlock.error
    async def channel_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to use this command, sweetie~", delete_after=5)
        elif isinstance(error, commands.BadArgument):
            await ctx.send("❌ Please enter a valid number for purge (e.g. `??purge 10`)~", delete_after=5)

async def setup(bot):
    await bot.add_cog(ChannelManagement(bot))
