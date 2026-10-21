import discord
from discord.ext import commands
import datetime

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warnings = {}  # {user_id: [{"reason": syy, "moderator": mod, "time": aika}]}

    # 1. KICK KOMENTO
    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick_user(self, ctx, member: discord.Member, *, reason: str = "No reason provided~ 🌸"):
        await ctx.message.delete()
        if member.top_role >= ctx.author.top_role:
            await ctx.send("❌ You cannot kick someone with an equal or higher role, cutie~", delete_after=5)
            return

        await member.kick(reason=reason)

        embed = discord.Embed(
            title="👢 ∙ Member Kicked",
            description=f"**{member.display_name}** has been kicked from the cosmos~ ✨",
            color=discord.Color.from_rgb(255, 182, 193)
        )
        embed.add_field(name="Reason", value=f"```{reason}```", inline=False)
        embed.set_footer(text="Moonlings Moderation 🛡️", icon_url=self.bot.user.display_avatar.url)
        await ctx.send(embed=embed)

    # 2. BAN KOMENTO
    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban_user(self, ctx, member: discord.Member, *, reason: str = "No reason provided~ 🌸"):
        await ctx.message.delete()
        if member.top_role >= ctx.author.top_role:
            await ctx.send("❌ You cannot ban someone with an equal or higher role, cutie~", delete_after=5)
            return

        await member.ban(reason=reason)

        embed = discord.Embed(
            title="🔨 ∙ Member Banned",
            description=f"**{member.display_name}** has been banned from the galaxy~ 🌌",
            color=discord.Color.from_rgb(255, 105, 180)
        )
        embed.add_field(name="Reason", value=f"```{reason}```", inline=False)
        embed.set_footer(text="Moonlings Moderation 🛡️", icon_url=self.bot.user.display_avatar.url)
        await ctx.send(embed=embed)

    # 3. MUTE KOMENTO (TIMEOUT)
    @commands.command(name="mute")
    @commands.has_permissions(moderate_members=True)
    async def mute_user(self, ctx, member: discord.Member, minutes: int = 10, *, reason: str = "Taking a quiet time-out~ ☁️"):
        await ctx.message.delete()
        if member.top_role >= ctx.author.top_role:
            await ctx.send("❌ You cannot mute someone with an equal or higher role, cutie~", delete_after=5)
            return

        duration = datetime.timedelta(minutes=minutes)
        await member.timeout(duration, reason=reason)

        embed = discord.Embed(
            title="🤐 ∙ Member Muted",
            description=f"**{member.display_name}** has been muted for **{minutes} minutes**~ 🌸",
            color=discord.Color.from_rgb(230, 230, 250)
        )
        embed.add_field(name="Reason", value=f"```{reason}```", inline=False)
        embed.set_footer(text="Moonlings Moderation 🛡️", icon_url=self.bot.user.display_avatar.url)
        await ctx.send(embed=embed)

    # 4. WARN KOMENTO
    @commands.command(name="warn")
    @commands.has_permissions(manage_messages=True)
    async def warn_user(self, ctx, member: discord.Member, *, reason: str = "Please follow the cozy rules~ 🌸"):
        await ctx.message.delete()
        if member.id not in self.warnings:
            self.warnings[member.id] = []

        warn_data = {
            "reason": reason,
            "moderator": ctx.author.display_name,
            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        self.warnings[member.id].append(warn_data)

        embed = discord.Embed(
            title="⚠️ ∙ Warning Issued",
            description=f"**{member.mention}** received a gentle warning~ ☁️",
            color=discord.Color.from_rgb(255, 218, 185)
        )
        embed.add_field(name="Reason", value=f"```{reason}```", inline=False)
        embed.add_field(name="Total Warnings", value=f"**{len(self.warnings[member.id])}**", inline=True)
        embed.set_footer(text="Moonlings Moderation 🛡️", icon_url=self.bot.user.display_avatar.url)
        await ctx.send(embed=embed)

    # 5. WARNINGS CHECK KOMENTO
    @commands.command(name="warnings")
    @commands.has_permissions(manage_messages=True)
    async def check_warnings(self, ctx, member: discord.Member):
        await ctx.message.delete()
        user_warns = self.warnings.get(member.id, [])

        if not user_warns:
            embed = discord.Embed(
                title="✨ ∙ Warning History",
                description=f"**{member.display_name}** has a clean record! No warnings found~ 🌸",
                color=discord.Color.from_rgb(175, 238, 238)
            )
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(
            title=f"📜 ∙ Warning History for {member.display_name}",
            description=f"Total warnings: **{len(user_warns)}**",
            color=discord.Color.from_rgb(255, 182, 193)
        )

        for idx, warn in enumerate(user_warns, 1):
            embed.add_field(
                name=f"Warning #{idx}",
                value=f"**Reason:** {warn['reason']}\n**By:** {warn['moderator']} ({warn['time']})",
                inline=False
            )

        await ctx.send(embed=embed)

    # 6. UNWARN KOMENTO
    @commands.command(name="unwarn")
    @commands.has_permissions(manage_messages=True)
    async def unwarn_user(self, ctx, member: discord.Member):
        await ctx.message.delete()
        if member.id in self.warnings and self.warnings[member.id]:
            self.warnings[member.id].pop()
            msg = f"Removed the latest warning for **{member.display_name}**~ 🌸"
        else:
            msg = f"**{member.display_name}** has no warnings to remove~ 🫧"

        embed = discord.Embed(
            title="✨ ∙ Warning Removed",
            description=msg,
            color=discord.Color.from_rgb(175, 238, 238)
        )
        await ctx.send(embed=embed)

    # Virheiden hallinta
    @kick_user.error
    @ban_user.error
    @mute_user.error
    @warn_user.error
    async def mod_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to use this command, sweetie~", delete_after=5)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ Please mention a member to use this command~", delete_after=5)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
