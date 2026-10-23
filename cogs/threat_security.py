import discord
from discord.ext import commands
import time

class ThreatSecurity(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # System status toggle (Enabled by default)
        self.system_enabled = True
        
        # Threat level metrics tracking (Server ID -> State)
        self.threat_scores = {}
        self.join_timestamps = {}
        
        # Dashboard / Manual override configuration
        self.manual_override_mode = None  # None, "Normal", "Elevated", "Lockdown"

    def get_threat_status(self, guild_id: int):
        """Calculates current threat level or returns manual override for dashboard integration."""
        if not self.system_enabled:
            return "Disabled ⚪", 0
            
        if self.manual_override_mode:
            return f"{self.manual_override_mode} (Override)", self.threat_scores.get(guild_id, 0)
            
        score = self.threat_scores.get(guild_id, 0)
        if score >= 50:
            return "Lockdown Mode 🚨", score
        elif score >= 20:
            return "Elevated Mode ⚠️", score
        return "Normal Mode 🟢", score

    def add_threat_score(self, guild_id: int, points: int):
        """Increases server threat score if system is enabled."""
        if not self.system_enabled:
            return
        current = self.threat_scores.get(guild_id, 0)
        self.threat_scores[guild_id] = min(100, current + points)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if not self.system_enabled:
            return

        guild_id = member.guild.id
        now = time.time()
        
        if guild_id not in self.join_timestamps:
            self.join_timestamps[guild_id] = []
            
        # Clean up timestamps older than 10 seconds
        self.join_timestamps[guild_id] = [t for t in self.join_timestamps[guild_id] if now - t < 10]
        self.join_timestamps[guild_id].append(now)

        # Rapid join detection (Anti-Raid trigger)
        if len(self.join_timestamps[guild_id]) >= 5:
            self.add_threat_score(guild_id, 15)

    @commands.command(name="togglethreat")
    @commands.has_permissions(administrator=True)
    async def toggle_threat_system(self, ctx, status: str = None):
        """Toggles the dynamic threat system ON or OFF."""
        if status is None:
            self.system_enabled = not self.system_enabled
        elif status.lower() in ["on", "enable", "true"]:
            self.system_enabled = True
        elif status.lower() in ["off", "disable", "false"]:
            self.system_enabled = False
        else:
            await ctx.send("❌ Usage: `??togglethreat [on/off]`")
            return

        state_str = "ENABLED 🟢" if self.system_enabled else "DISABLED 🔴"
        await ctx.send(f"🛡️ Dynamic Threat Security System is now **{state_str}**.")

    @commands.command(name="threatlevel")
    async def threat_level(self, ctx):
        """Views current threat score, active gear, and security status."""
        status, score = self.get_threat_status(ctx.guild.id)
        
        embed = discord.Embed(
            title="🛡️ Dynamic Threat Level & Security Status",
            color=discord.Color.from_rgb(230, 210, 240)
        )
        embed.add_field(
            name="System Enabled", 
            value="🟢 Yes" if self.system_enabled else "🔴 No (Paused)", 
            inline=True
        )
        embed.add_field(name="Current Status Mode", value=f"**{status}**", inline=True)
        embed.add_field(name="Threat Points", value=f"`{score} / 100`", inline=True)
        
        embed.add_field(
            name="Active Security Controls",
            value=(
                "• **Normal Mode:** Standard filters & cozy limits\n"
                "• **Elevated Mode:** Strict spam filters & staff alerts\n"
                "• **Lockdown Mode:** Maximum Anti-Raid enforcement"
            ),
            inline=False
        )
        embed.set_footer(text="Moonlings Threat Security 🌸")
        await ctx.send(embed=embed)

    @commands.command(name="setthreatmode")
    @commands.has_permissions(administrator=True)
    async def set_threat_mode(self, ctx, mode: str):
        """Dashboard / Admin override command for security mode (normal, elevated, lockdown, auto)."""
        if not self.system_enabled:
            await ctx.send("⚠️ The threat system is currently disabled. Enable it first using `??togglethreat on`.")
            return

        mode_lower = mode.lower()
        if mode_lower == "auto":
            self.manual_override_mode = None
            await ctx.send("✅ Security mode set to **Automatic Dynamic Tracking**.")
        elif mode_lower in ["normal", "elevated", "lockdown"]:
            self.manual_override_mode = mode_lower.capitalize()
            await ctx.send(f"⚙️ Security mode manually overridden to **{self.manual_override_mode} Mode**.")
        else:
            await ctx.send("❌ Invalid mode. Choose: `normal`, `elevated`, `lockdown`, or `auto`.")

async def setup(bot):
    await bot.add_cog(ThreatSecurity(bot))
