import discord
from discord.ext import commands
from datetime import timedelta

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 1. KICK COMMAND (Söpö & pehmeä tyyli)
    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick_command(self, ctx, member: discord.Member, *, reason="No reason provided~ 🌸"):
        await ctx.message.delete()
        await member.kick(reason=reason)
        
        embed = discord.Embed(
            title="🚀 ∙ Member Kicked",
            description=f"**{member.mention}** has been gently guided back to Earth~ ☁️",
            color=discord.Color.from_rgb(255, 182, 193) # Light Pink
        )
        embed.add_field(name="Reason", value=f"```{reason}```", inline=False)
        embed.set_footer(text=f"Action taken by {ctx.author.display_name} 🌸", icon_url=ctx.author.display_avatar.url)
        
        await ctx.send(embed=embed)

    # 2. BAN COMMAND
    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban_command(self, ctx, member: discord.Member, *, reason="No reason provided~ 🌙"):
        await ctx.message.delete()
        await member.ban(reason=reason)
        
        embed = discord.Embed(
            title="🪐 ∙ Member Banned",
            description=f"**{member.mention}** has been sent far away into deep space ✨",
            color=discord.Color.from_rgb(230, 230, 250) # Lavender
        )
        embed.add_field(name="Reason", value=f"```{reason}```", inline=False)
        embed.set_footer(text=f"Action taken by {ctx.author.display_name} 🌙", icon_url=ctx.author.display_avatar.url)
        
        await ctx.send(embed=embed)

    # 3. MUTE / TIMEOUT COMMAND
    @commands.command(name="mute")
    @commands.has_permissions(moderate_members=True)
    async def mute_command(self, ctx, member: discord.Member, minutes: int, *, reason="No reason provided~ ☁️"):
        await ctx.message.delete()
        duration = timedelta(minutes=minutes)
        await member.timeout(duration, reason=reason)
        
        embed = discord.Embed(
            title="☁️ ∙ Member Muted",
            description=f"**{member.mention}** has been given a quiet zero-gravity timeout for **{minutes} minutes**~ 🌸",
            color=discord.Color.from_rgb(176, 224, 230) # Soft Blue
        )
        embed.add_field(name="Reason", value=f"```{reason}```", inline=False)
        embed.set_footer(text=f"Action taken by {ctx.author.display_name} ✨", icon_url=ctx.author.display_avatar.url)
        
        await ctx.send(embed=embed)

    # 4. LOCK & HIDE CHANNEL COMMAND
    @commands.command(name="lock")
    @commands.has_permissions(manage_channels=True)
    async def lock_command(self, ctx):
        await ctx.message.delete()
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False, view_channel=False)
        
        embed = discord.Embed(
            title="🔒 ∙ Channel Locked & Hidden",
            description="This starry channel has been safely locked and hidden away~ 🌌✨",
            color=discord.Color.from_rgb(255, 182, 193)
        )
        await ctx.send(embed=embed)

    # 5. UNLOCK & UNHIDE CHANNEL COMMAND
    @commands.command(name="unlock")
    @commands.has_permissions(manage_channels=True)
    async def unlock_command(self, ctx):
        await ctx.message.delete()
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True, view_channel=True)
        
        embed = discord.Embed(
            title="🔓 ∙ Channel Unlocked",
            description="The channel is open again, welcome back star-farers! 🚀🌸",
            color=discord.Color.from_rgb(152, 251, 152)
        )
        await ctx.send(embed=embed)

    # 6. PURGE COMMAND (Mass message deletion)
    @commands.command(name="purge")
    @commands.has_permissions(manage_messages=True)
    async def purge_command(self, ctx, amount: int):
        await ctx.message.delete()
        deleted = await ctx.channel.purge(limit=amount)
        
        embed = discord.Embed(
            title="🧹 ∙ Cleaned Up!",
            description=f"Swept away **{len(deleted)}** messy messages into space dust~ ✨",
            color=discord.Color.from_rgb(255, 218, 185) # Peach
        )
        await ctx.send(embed=embed, delete_after=5)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
