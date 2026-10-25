import discord
from discord.ext import commands
import json
import os
from threading import RLock

SETTINGS_FILE = "welcome_settings.json"
SETTINGS_LOCK = RLock()

def _read_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def _write_settings(settings):
    temporary_file = SETTINGS_FILE + ".tmp"
    with open(temporary_file, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4)
    os.replace(temporary_file, SETTINGS_FILE)

def load_settings():
    with SETTINGS_LOCK:
        return _read_settings()

def save_settings(settings):
    with SETTINGS_LOCK:
        _write_settings(settings)

def update_guild_settings(guild_id, values):
    with SETTINGS_LOCK:
        settings = _read_settings()
        settings.setdefault(str(guild_id), {}).update(values)
        _write_settings(settings)

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        settings = load_settings()
        guild_id = str(member.guild.id)
        if guild_id not in settings:
            return

        data = settings[guild_id]
        channel_id = data.get("welcome_channel")
        text = data.get("welcome_text", "Welcome to the server, {user}! 🎉")

        if channel_id:
            channel = member.guild.get_channel(int(channel_id))
            if channel:
                # Muutetaan tagit oikeiksi arvoiksi
                formatted_text = text.replace("{user}", member.mention).replace("{server}", member.guild.name)
                
                embed = discord.Embed(
                    title="✨ New Member Joined!",
                    description=formatted_text,
                    color=discord.Color.from_rgb(230, 210, 240)
                )
                if member.avatar:
                    embed.set_thumbnail(url=member.avatar.url)
                embed.set_footer(text="Moonlings Welcome System 🌸")
                await channel.send(embed=embed, allowed_mentions=discord.AllowedMentions(users=[member], roles=False, everyone=False, replied_user=False))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        settings = load_settings()
        guild_id = str(member.guild.id)
        if guild_id not in settings:
            return

        data = settings[guild_id]
        channel_id = data.get("goodbye_channel")
        text = data.get("goodbye_text", "Goodbye, {user}. We'll miss you! 👋")

        if channel_id:
            channel = member.guild.get_channel(int(channel_id))
            if channel:
                formatted_text = text.replace("{user}", member.name).replace("{server}", member.guild.name)
                
                embed = discord.Embed(
                    title="👋 Member Left",
                    description=formatted_text,
                    color=discord.Color.from_rgb(240, 210, 210)
                )
                embed.set_footer(text="Moonlings Goodbye System 🌸")
                await channel.send(embed=embed, allowed_mentions=discord.AllowedMentions.none())

    @commands.command(name="setwelcomechannel")
    @commands.has_permissions(administrator=True)
    async def set_welcome_channel(self, ctx, channel: discord.TextChannel):
        """Sets the channel for welcome messages."""
        guild_id = str(ctx.guild.id)
        update_guild_settings(guild_id, {"welcome_channel": channel.id})
        await ctx.send(f"🌸 Welcome channel set to {channel.mention}!")

    @commands.command(name="setwelcometext")
    @commands.has_permissions(administrator=True)
    async def set_welcome_text(self, ctx, *, text: str):
        """Sets the custom welcome message. Use {user} and {server}."""
        guild_id = str(ctx.guild.id)
        update_guild_settings(guild_id, {"welcome_text": text})
        await ctx.send(f"✨ Welcome text updated to:\n`{text}`")

    @commands.command(name="setgoodbyechannel")
    @commands.has_permissions(administrator=True)
    async def set_goodbye_channel(self, ctx, channel: discord.TextChannel):
        """Sets the channel for goodbye messages."""
        guild_id = str(ctx.guild.id)
        update_guild_settings(guild_id, {"goodbye_channel": channel.id})
        await ctx.send(f"🌸 Goodbye channel set to {channel.mention}!")

    @commands.command(name="setgoodbyetext")
    @commands.has_permissions(administrator=True)
    async def set_goodbye_text(self, ctx, *, text: str):
        """Sets the custom goodbye message. Use {user} and {server}."""
        guild_id = str(ctx.guild.id)
        update_guild_settings(guild_id, {"goodbye_text": text})
        await ctx.send(f"✨ Goodbye text updated to:\n`{text}`")

async def setup(bot):
    await bot.add_cog(Welcome(bot))
