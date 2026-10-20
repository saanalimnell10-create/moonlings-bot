import discord
from discord.ext import commands

class Security(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.antinuke_enabled = True
        self.antiraid_enabled = True
        self.whitelisted_users = []  # Voit lisätä ID:itä tänne

    # 1. ANTINUKE TOGGLE
    @commands.command(name="antinuke")
    @commands.has_permissions(administrator=True)
    async def antinuke_command(self, ctx, status: str = None):
        await ctx.message.delete()
        if status and status.lower() == "off":
            self.antinuke_enabled = False
            state_text = "disabled ❌"
            color = discord.Color.from_rgb(255, 182, 193)
        else:
            self.antinuke_enabled = True
            state_text = "enabled & protecting our galaxy! 🛡️✨"
            color = discord.Color.from_rgb(152, 251, 152)

        embed = discord.Embed(
            title="🚀 ∙ Anti-Nuke System",
            description=f"Anti-Nuke protection is now **{state_text}**",
            color=color
        )
        await ctx.send(embed=embed)

    # 2. ANTIRAID TOGGLE
    @commands.command(name="antiraid")
    @commands.has_permissions(administrator=True)
    async def antiraid_command(self, ctx, status: str = None):
        await ctx.message.delete()
        if status and status.lower() == "off":
            self.antiraid_enabled = False
            state_text = "disabled ❌"
            color = discord.Color.from_rgb(255, 182, 193)
        else:
            self.antiraid_enabled = True
            state_text = "enabled & monitoring joins! 🛸✨"
            color = discord.Color.from_rgb(152, 251, 152)

        embed = discord.Embed(
            title="🛸 ∙ Anti-Raid System",
            description=f"Anti-Raid protection is now **{state_text}**",
            color=color
        )
        await ctx.send(embed=embed)

    # 3. LOCKDOWN (Lukitsee kaikki kanavat kerralla)
    @commands.command(name="lockdown")
    @commands.has_permissions(administrator=True)
    async def lockdown_command(self, ctx):
        await ctx.message.delete()
        
        for channel in ctx.guild.text_channels:
            try:
                await channel.set_permissions(ctx.guild.default_role, send_messages=False)
            except Exception:
                pass

        embed = discord.Embed(
            title="🚨 ∙ Server Lockdown Activated",
            description="All channels have been locked down to protect our starry home~ 🪐",
            color=discord.Color.from_rgb(255, 105, 180)
        )
        await ctx.send(embed=embed)

    # 4. UNLOCKDOWN (Avaa kaikki kanavat)
    @commands.command(name="unlockdown")
    @commands.has_permissions(administrator=True)
    async def unlockdown_command(self, ctx):
        await ctx.message.delete()
        
        for channel in ctx.guild.text_channels:
            try:
                await channel.set_permissions(ctx.guild.default_role, send_messages=True)
            except Exception:
                pass

        embed = discord.Embed(
            title="✨ ∙ Server Lockdown Lifted",
            description="All channels are open again! Welcome back, star-farers~ 🌸🚀",
            color=discord.Color.from_rgb(152, 251, 152)
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Security(bot))
