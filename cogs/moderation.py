import discord
from discord.ext import commands
import random

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_punishment_dm(self, member: discord.Member, moderator: discord.Member, action: str, reason: str):
        """Lähettää suloisen ja läpinäkyvän pastel-DM:n rangaistusta saaneelle jäsenelle."""
        case_id = random.randint(1000, 9999)
        
        embed = discord.Embed(
            title=f"🌸 Moderation Notice • Case #{case_id}",
            description=f"You received a **{action}** in Moonlings Cozy Space.",
            color=0xFFB7C5  # Pastellivaaleanpunainen
        )
        
        embed.add_field(name="🛡️ Moderator", value=moderator.mention, inline=True)
        embed.add_field(name="📌 Action Type", value=action, inline=True)
        embed.add_field(name="📝 Reason", value=reason, inline=False)
        embed.set_footer(text=f"Moonlings Moderation System • Reference Case #{case_id}")

        try:
            await member.send(embed=embed)
            return True
        except discord.Forbidden:
            return False  # Käyttäjällä on DMs kiinni

    @commands.command(name="warn")
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        """Antaa varoituksen ja lähettää läpinäkyvän DM-lokin."""
        dm_sent = await self.send_punishment_dm(member, ctx.author, "Warning", reason)

        embed = discord.Embed(
            title="🌸 Member Warned",
            description=f"Successfully warned {member.mention}.",
            color=0xB5EAD7
        )
        embed.add_field(name="📝 Reason", value=reason, inline=False)
        embed.add_field(name="📬 DM Status", value="Transparent DM log sent successfully!" if dm_sent else "Could not send DM (User has DMs closed).", inline=False)
        
        await ctx.send(embed=embed)

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        """Potkaisee käyttäjän palvelimelta."""
        await self.send_punishment_dm(member, ctx.author, "Kick", reason)
        await member.kick(reason=reason)

        embed = discord.Embed(
            title="🌸 Member Kicked",
            description=f"Successfully kicked {member.mention} from the server.",
            color=0xFFDAC1
        )
        embed.add_field(name="📝 Reason", value=reason, inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        """Antaa porttikiellon palvelimelta."""
        await self.send_punishment_dm(member, ctx.author, "Ban", reason)
        await member.ban(reason=reason)

        embed = discord.Embed(
            title="🌸 Member Banned",
            description=f"Successfully banned {member.mention} from the server.",
            color=0xFFB7C5
        )
        embed.add_field(name="📝 Reason", value=reason, inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
