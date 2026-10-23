import discord
from discord.ext import commands
import json
import os

CONFIG_FILE = "audit_config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)

class AuditLogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = load_config()

    def get_guild_config(self, guild_id):
        guild_str = str(guild_id)
        if guild_str not in self.config:
            self.config[guild_str] = {
                "enabled": True,
                "log_channel_id": None,
                "events": {
                    "message_delete": True,
                    "message_edit": True,
                    "member_join": True,
                    "member_remove": True,
                    "role_update": True,
                    "channel_update": True
                }
            }
            save_config(self.config)
        return self.config[guild_str]

    async def send_log(self, guild, embed, event_type):
        guild_cfg = self.get_guild_config(guild.id)
        if not guild_cfg.get("enabled"):
            return

        if not guild_cfg.get("events", {}).get(event_type, True):
            return

        channel_id = guild_cfg.get("log_channel_id")
        if channel_id:
            channel = guild.get_channel(channel_id)
            if channel:
                await channel.send(embed=embed)

    # --- KOMENNOT ---

    @commands.command(name="setlogs")
    @commands.has_permissions(manage_guild=True, manage_channels=True)
    async def set_logs(self, ctx, channel: discord.TextChannel = None):
        """Sets the log channel or creates an automatic private #audit-logs channel."""
        guild = ctx.guild
        guild_cfg = self.get_guild_config(guild.id)

        # Jos kanavaa ei määritelty, luodaan automaattisesti yksityinen #audit-logs -kanava
        if channel is None:
            # Tarkistetaan onko kanava jo olemassa
            existing_channel = discord.utils.get(guild.text_channels, name="audit-logs")
            
            if existing_channel:
                channel = existing_channel
            else:
                # Luodaan yksityinen kanava, johon vain ylläpidolla ja botilla on pääsy
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                    ctx.author: discord.PermissionOverwrite(read_messages=True, send_messages=True)
                }
                
                channel = await guild.create_text_channel(
                    name="audit-logs",
                    overwrites=overwrites,
                    reason="Automatic audit log channel setup by Moonlings Bot"
                )

        guild_cfg["log_channel_id"] = channel.id
        save_config(self.config)

        embed = discord.Embed(
            title="📜 Audit Log Channel Configured",
            description=f"Real-time audit log events will now be sent to {channel.mention}!",
            color=0xFFB6C1
        )
        embed.set_footer(text="Moonlings Security Suite 🌸")
        await ctx.send(embed=embed)

    @commands.command(name="logs")
    @commands.has_permissions(manage_guild=True)
    async def toggle_logs(self, ctx, status: str):
        """Quickly enables or disables the logging system (on/off)."""
        status_clean = status.lower()
        guild_cfg = self.get_guild_config(ctx.guild.id)

        if status_clean in ["on", "enable", "true"]:
            guild_cfg["enabled"] = True
            save_config(self.config)
            await ctx.send(embed=discord.Embed(
                title="📜 Audit Logging Enabled",
                description="The audit log system is now **active**.",
                color=0xFFB6C1
            ))
        elif status_clean in ["off", "disable", "false"]:
            guild_cfg["enabled"] = False
            save_config(self.config)
            await ctx.send(embed=discord.Embed(
                title="📜 Audit Logging Disabled",
                description="The audit log system has been **disabled**.",
                color=0xFFB6C1
            ))
        else:
            await ctx.send("❌ Invalid status! Use `??logs on` or `??logs off`.", delete_after=5)

    @commands.command(name="logevents")
    @commands.has_permissions(manage_guild=True)
    async def log_events(self, ctx):
        """Allows staff to view active log events."""
        guild_cfg = self.get_guild_config(ctx.guild.id)
        events = guild_cfg.get("events", {})

        description = "\n".join([f"• **{k}**: {'✅ Enabled' if v else '❌ Disabled'}" for k, v in events.items()])

        embed = discord.Embed(
            title="📜 Active Audit Log Events",
            description=description,
            color=0xFFB6C1
        )
        embed.set_footer(text="Moonlings Security Suite 🌸")
        await ctx.send(embed=embed)

    # --- EVENT LISTENERS ---

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot or not message.guild:
            return

        embed = discord.Embed(
            title="🗑️ Message Deleted",
            description=f"**Author:** {message.author.mention} (`{message.author.id}`)\n**Channel:** {message.channel.mention}",
            color=0xFFB6C1
        )
        if message.content:
            embed.add_field(name="Content", value=message.content[:1024], inline=False)
        embed.set_footer(text="Moonlings Audit Log 🌸")

        await self.send_log(message.guild, embed, "message_delete")

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot or not before.guild or before.content == after.content:
            return

        embed = discord.Embed(
            title="✏️ Message Edited",
            description=f"**Author:** {before.author.mention} (`{before.author.id}`)\n**Channel:** {before.channel.mention}",
            color=0xFFB6C1
        )
        embed.add_field(name="Before", value=before.content[:1024] if before.content else "*Empty*", inline=False)
        embed.add_field(name="After", value=after.content[:1024] if after.content else "*Empty*", inline=False)
        embed.set_footer(text="Moonlings Audit Log 🌸")

        await self.send_log(before.guild, embed, "message_edit")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = discord.Embed(
            title="📥 Member Joined",
            description=f"{member.mention} (`{member.name}`)",
            color=0xFFB6C1
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text="Moonlings Audit Log 🌸")

        await self.send_log(member.guild, embed, "member_join")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = discord.Embed(
            title="📤 Member Left",
            description=f"{member.mention} (`{member.name}`)",
            color=0xFFB6C1
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text="Moonlings Audit Log 🌸")

        await self.send_log(member.guild, embed, "member_remove")


async def setup(bot):
    await bot.add_cog(AuditLogs(bot))
