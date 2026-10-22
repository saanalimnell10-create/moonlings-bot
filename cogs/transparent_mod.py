import discord
from discord.ext import commands
import random

class TransparentMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_punishment_dm(self, member: discord.Member, moderator: discord.Member, action: str, reason: str, evidence: str = "None provided", original_message: str = None):
        """Helper function to send a transparent, cozy pastel punishment DM to a member."""
        case_id = random.randint(1000, 9999) # Yksilöllinen tapausnumero (Case ID)
        
        embed = discord.Embed(
            title=f"🌸 Moderation Notice • Case #{case_id}",
            description=f"You received a **{action}** in Moonlings Cozy Space.",
            color=0xFFB7C5  # Söpö pastellivaaleanpunainen
        )
        
        embed.add_field(name="🛡️ Moderator", value=moderator.mention, inline=True)
        embed.add_field(name="📌 Action Type", value=action, inline=True)
        embed.add_field(name="📝 Reason", value=reason, inline=False)
        
        if original_message:
            embed.add_field(name="💬 The Message", value=f"> {original_message}", inline=False)
            
        if evidence and evidence != "None provided":
            embed.add_field(name="🔗 Attached Evidence", value=evidence, inline=False)
            
        embed.set_footer(text=f"Moonlings Moderation System • If you wish to appeal, reference Case #{case_id}")

        try:
            await member.send(embed=embed)
        except discord.Forbidden:
            # Jos käyttäjällä on DMs kiinni, botti ei kaadu vaan ohittaa sen kiltisti
            pass

    @commands.command(name="warn")
    @commands.has_permissions(kick_members=True)
    async def warn_command(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        """Warns a member and sends a transparent DM log."""
        
        # Lähetetään läpinäkyvä DM käyttäjälle
        await self.send_punishment_dm(
            member=member,
            moderator=ctx.author,
            action="Warning",
            reason=reason
        )

        embed = discord.Embed(
            title="🌸 Member Warned",
            description=f"Successfully warned {member.mention}. Transparent DM log sent!",
            color=0xB5EAD7  # Mintunvihreä onnistumiselle
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(TransparentMod(bot))
