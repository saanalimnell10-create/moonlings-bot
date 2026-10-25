import discord
from discord.ext import commands
import json
import os

SETTINGS_FILE = "boycott_settings.json"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

class MemberProtection(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="setupboycott", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def setupboycott(self, ctx):
        """Main command for the Member Protection & Watchlist System."""
        prefix = ctx.prefix
        embed = discord.Embed(
            title="🛡️ Member Protection & Watchlist System",
            description="Manage server user protection, flagging, and watchlists.",
            color=discord.Color.from_rgb(230, 210, 240)
        )
        embed.add_field(
            name="📜 Subcommands",
            value=(
                f"`{prefix}setupboycott setup [#channel]` - Set alert channel for flags\n"
                f"`{prefix}setupboycott mark [@user] [reason]` - Mark a user on the watchlist\n"
                f"`{prefix}setupboycott unmark [@user]` - Remove a user from the watchlist\n"
                f"`{prefix}setupboycott list` - List all currently marked users"
            ),
            inline=False
        )
        embed.set_footer(text="Moonlings Protection Suite 🌸")
        await ctx.send(embed=embed)

    @setupboycott.command(name="setup")
    @commands.has_permissions(administrator=True)
    async def boycott_setup(self, ctx, channel: discord.TextChannel):
        """Sets the alert channel for protection and watchlist notices."""
        settings = load_settings()
        guild_id = str(ctx.guild.id)
        if guild_id not in settings:
            settings[guild_id] = {"channel": None, "marked_users": {}}
        
        settings[guild_id]["channel"] = channel.id
        save_settings(settings)
        await ctx.send(f"🛡️ Protection alert channel successfully set to {channel.mention}!")

    @setupboycott.command(name="mark")
    @commands.has_permissions(administrator=True)
    async def boycott_mark(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        """Flags and marks a user on the protection watchlist."""
        settings = load_settings()
        guild_id = str(ctx.guild.id)
        if guild_id not in settings:
            settings[guild_id] = {"channel": None, "marked_users": {}}
        
        settings[guild_id]["marked_users"][str(member.id)] = {
            "name": str(member),
            "reason": reason,
            "moderator": str(ctx.author)
        }
        save_settings(settings)

        embed = discord.Embed(
            title="🚨 User Flagged & Protected",
            description=f"**{member.mention}** has been added to the protection watchlist.",
            color=discord.Color.from_rgb(240, 100, 100)
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.set_footer(text=f"Marked by {ctx.author}")
        await ctx.send(embed=embed)

        # Lähetetään hälytys erilliselle lokikanavalle, jos se on asetettu
        channel_id = settings[guild_id].get("channel")
        if channel_id:
            log_channel = ctx.guild.get_channel(int(channel_id))
            if log_channel:
                await log_channel.send(embed=embed)

    @setupboycott.command(name="unmark")
    @commands.has_permissions(administrator=True)
    async def boycott_unmark(self, ctx, member: discord.Member):
        """Removes a user from the protection watchlist."""
        settings = load_settings()
        guild_id = str(ctx.guild.id)
        if guild_id in settings and str(member.id) in settings[guild_id]["marked_users"]:
            del settings[guild_id]["marked_users"][str(member.id)]
            save_settings(settings)
            await ctx.send(f"✅ Removed {member.mention} from the protection watchlist.")
        else:
            await ctx.send(f"⚠️ {member.mention} was not found on the watchlist.")

    @setupboycott.command(name="list")
    @commands.has_permissions(administrator=True)
    async def boycott_list(self, ctx):
        """Lists all users currently on the watchlist."""
        settings = load_settings()
        guild_id = str(ctx.guild.id)
        if guild_id not in settings or not settings[guild_id].get("marked_users"):
            await ctx.send("🛡️ No users are currently marked on the watchlist.")
            return

        embed = discord.Embed(
            title="🛡️ Server Protection Watchlist",
            description="List of flagged or monitored users:",
            color=discord.Color.from_rgb(230, 210, 240)
        )
        for user_id, data in settings[guild_id]["marked_users"].items():
            embed.add_field(
                name=f"User: {data['name']} (ID: {user_id})",
                value=f"**Reason:** {data['reason']}\n**Marked by:** {data['moderator']}",
                inline=False
            )
        embed.set_footer(text="Moonlings Protection Suite 🌸")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(MemberProtection(bot))
