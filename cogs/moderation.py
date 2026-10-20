import discord
from discord.ext import commands
from datetime import timedelta

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warnings = {}  # Tallennetut varoitukset muistiin
        self.warn_expiry_days = 30  # Oletuksena varoitukset vanhenevat 30 päivässä

    # 1. KICK COMMAND
    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick_command(self, ctx, member: discord.Member, *, reason="No reason provided~ 🌸"):
        await ctx.message.delete()
        await member.kick(reason=reason)
        
        embed = discord.Embed(
            title="🚀 ∙ Member Kicked",
            description=f"**{member.mention}** has been gently guided back to Earth~ ☁️",
            color=discord.Color.from_rgb(255, 182, 193)
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
            color=discord.Color.from_rgb(230, 230, 250)
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
            color=discord.Color.from_rgb(176, 224, 230)
        )
        embed.add_field(name="Reason", value=f"```{reason}```", inline=False)
        embed.set_footer(text=f"Action taken by {ctx.author.display_name} ✨", icon_url=ctx.author.display_avatar.url)
        
        await ctx.send(embed=embed)

    # 4. WARN COMMAND (Anna varoitus)
    @commands.command(name="warn")
    @commands.has_permissions(moderate_members=True)
    async def warn_command(self, ctx, member: discord.Member, *, reason="No reason provided~ ⚠️"):
        await ctx.message.delete()
        
        if member.id not in self.warnings:
            self.warnings[member.id] = []
            
        self.warnings[member.id].append(reason)
        count = len(self.warnings[member.id])
        
        embed = discord.Embed(
            title="⚠️ ∙ Member Warned",
            description=f"**{member.mention}** received a gentle warning~ 🫧\nTotal active warnings: **{count}**",
            color=discord.Color.from_rgb(255, 218, 185)
        )
        embed.add_field(name="Reason", value=f"```{reason}```", inline=False)
        embed.set_footer(text=f"Warned by {ctx.author.display_name} 🌸", icon_url=ctx.author.display_avatar.url)
        
        await ctx.send(embed=embed)

    # 5. UNWARN COMMAND (Poista varoitus)
    @commands.command(name="unwarn")
    @commands.has_permissions(moderate_members=True)
    async def unwarn_command(self, ctx, member: discord.Member):
        await ctx.message.delete()
        
        if member.id in self.warnings and len(self.warnings[member.id]) > 0:
            self.warnings[member.id].pop()  # Poistaa viimeisimmän varoituksen
            count = len(self.warnings[member.id])
            
            embed = discord.Embed(
                title="✨ ∙ Warning Removed",
                description=f"A warning was removed from **{member.mention}**~ 🌸\nRemaining active warnings: **{count}**",
                color=discord.Color.from_rgb(152, 251, 152)
            )
        else:
            embed = discord.Embed(
                title="🌸 ∙ No Warnings Found",
                description=f"**{member.mention}** doesn't have any active warnings to remove~ 🫧",
                color=discord.Color.from_rgb(230, 230, 250)
            )
            
        embed.set_footer(text=f"Action taken by {ctx.author.display_name} ✨", icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)

    # 6. WARNINGS COMMAND (Tarkista varoitukset)
    @commands.command(name="warnings")
    async def warnings_command(self, ctx, member: discord.Member = None):
        await ctx.message.delete()
        target = member or ctx.author
        
        user_warns = self.warnings.get(target.id, [])
        count = len(user_warns)
        
        embed = discord.Embed(
            title=f"🌸 ∙ Warnings for {target.display_name}",
            description=f"Total active warnings: **{count}**~ ✨",
            color=discord.Color.from_rgb(230, 230, 250)
        )
        
        if user_warns:
            warn_list = "\n".join([f"• {w}" for w in user_warns])
            embed.add_field(name="Warning History", value=f"```{warn_list}```", inline=False)
        else:
            embed.add_field(name="Warning History", value="```No warnings found! Such a good star-farer~ 🫧```", inline=False)
            
        await ctx.send(embed=embed)

    # 7. WARN EXPIRY COMMAND
    @commands.command(name="warnexpiry")
    @commands.has_permissions(administrator=True)
    async def warn_expiry_command(self, ctx, option: str):
        await ctx.message.delete()
        
        if option.lower() == "off":
            self.warn_expiry_days = None
            msg = "Warning expiration is now **turned off**! Warnings will stay forever~ 🔒"
        else:
            try:
                days = int(option)
                self.warn_expiry_days = days
                msg = f"Warnings will now automatically expire after **{days} days**~ 🌸✨"
            except ValueError:
                await ctx.send("❌ Please provide a valid number of days or 'off'!", delete_after=5)
                return

        embed = discord.Embed(
            title="⏳ ∙ Warn Expiry Updated",
            description=msg,
            color=discord.Color.from_rgb(175, 238, 238)
        )
        await ctx.send(embed=embed)

    # 8. LOCK & HIDE CHANNEL
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

    # 9. UNLOCK & UNHIDE CHANNEL
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

    # 10. PURGE COMMAND
    @commands.command(name="purge")
    @commands.has_permissions(manage_messages=True)
    async def purge_command(self, ctx, amount: int):
        await ctx.message.delete()
        deleted = await ctx.channel.purge(limit=amount)
        
        embed = discord.Embed(
            title="🧹 ∙ Cleaned Up!",
            description=f"Swept away **{len(deleted)}** messy messages into space dust~ ✨",
            color=discord.Color.from_rgb(255, 218, 185)
        )
        await ctx.send(embed=embed, delete_after=5)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
