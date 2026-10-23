import discord
from discord.ext import commands, tasks
import json
import os
import asyncio
from datetime import datetime, timedelta

CONFIG_FILE = "bump_config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)

class BumpSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = load_config()
        self.bump_cooldowns = {}  # Tallennettu cooldown per serveri

    def get_server_config(self, guild_id):
        guild_str = str(guild_id)
        if guild_str not in self.config:
            self.config[guild_str] = {
                "bump_channel_id": None,
                "bump_role_id": None,
                "reminder_msg": "Time to bump the server! 🚀",
                "thanks_msg": "Thanks for the bump, legend! 🌸"
            }
            save_config(self.config)
        return self.config[guild_str]

    # --- ASETUSKOMENNOT ---

    @commands.command(name="setbumpchannel")
    @commands.has_permissions(manage_guild=True)
    async def set_bump_channel(self, ctx, channel: discord.TextChannel):
        """Asettaa kanavan bump-muistutuksille ja kiitoksille."""
        server_cfg = self.get_server_config(ctx.guild.id)
        server_cfg["bump_channel_id"] = channel.id
        save_config(self.config)

        embed = discord.Embed(
            title="🌸 Bump Channel Updated!",
            description=f"Bump reminders will now be sent to {channel.mention}!",
            color=0xFFB6C1
        )
        await ctx.send(embed=embed)

    @commands.command(name="setbumprole")
    @commands.has_permissions(manage_guild=True)
    async def set_bump_role(self, ctx, role: discord.Role):
        """Asettaa roolin, jota tägätään muistutuksen yhteydessä."""
        server_cfg = self.get_server_config(ctx.guild.id)
        server_cfg["bump_role_id"] = role.id
        save_config(self.config)

        embed = discord.Embed(
            title="🌸 Bump Role Updated!",
            description=f"The role {role.mention} will be pinged when it's time to bump!",
            color=0xFFB6C1
        )
        await ctx.send(embed=embed)

    @commands.command(name="setbumpmsg")
    @commands.has_permissions(manage_guild=True)
    async def set_bump_msg(self, ctx, *, message: str):
        """Asettaa mukautetun muistutusviestin (2h kuluttua)."""
        server_cfg = self.get_server_config(ctx.guild.id)
        server_cfg["reminder_msg"] = message
        save_config(self.config)

        embed = discord.Embed(
            title="🌸 Bump Reminder Message Updated!",
            description=f"**New Message:**\n{message}",
            color=0xFFB6C1
        )
        await ctx.send(embed=embed)

    @commands.command(name="setthanksmsg")
    @commands.has_permissions(manage_guild=True)
    async def set_thanks_msg(self, ctx, *, message: str):
        """Asettaa mukautetun kiitosviestin."""
        server_cfg = self.get_server_config(ctx.guild.id)
        server_cfg["thanks_msg"] = message
        save_config(self.config)

        embed = discord.Embed(
            title="🌸 Bump Thank You Message Updated!",
            description=f"**New Message:**\n{message}",
            color=0xFFB6C1
        )
        await ctx.send(embed=embed)

    @commands.command(name="bumptime")
    async def bump_time(self, ctx):
        """Tarkistaa kuinka paljon aikaa on jäljellä seuraavaan bumpatiin."""
        guild_id = ctx.guild.id
        if guild_id in self.bump_cooldowns:
            ready_time = self.bump_cooldowns[guild_id]
            now = datetime.utcnow()
            if now < ready_time:
                remaining = ready_time - now
                minutes, seconds = divmod(int(remaining.total_seconds()), 60)
                hours, minutes = divmod(minutes, 60)
                time_str = f"{hours}h {minutes}m {seconds}s" if hours > 0 else f"{minutes}m {seconds}s"
                
                embed = discord.Embed(
                    title="⏳ Bump Cooldown",
                    description=f"You can bump again in **{time_str}**!",
                    color=0xFFB6C1
                )
                await ctx.send(embed=embed)
                return

        embed = discord.Embed(
            title="🚀 Ready to Bump!",
            description="The server is ready to be bumped right now!",
            color=0xFFB6C1
        )
        await ctx.send(embed=embed)

    # --- AUTOMAATTINEN DISBOARD BUMP -HAHAVAINNOINTI ---

    @commands.Cog.listener()
    async def on_message(self, message):
        # Tarkistetaan onko viesti Disboard-botilta ja sisältääkö se bump-onnistumisen
        if message.author.id == 302050872383242240:  # Disboard Bot ID
            if message.embeds:
                embed = message.embeds[0]
                # Disboard näyttää yleensä "Bump done!" tai vastaavaa embedissä
                if "Bump done" in str(embed.description) or "Bump done" in str(embed.title):
                    guild = message.guild
                    if not guild:
                        return

                    server_cfg = self.get_server_config(guild.id)
                    bump_channel_id = server_cfg.get("bump_channel_id") or message.channel.id
                    channel = guild.get_channel(bump_channel_id)

                    if channel:
                        # 1. Lähetetään kiitosviesti
                        thanks_text = server_cfg.get("thanks_msg", "Thanks for the bump, legend! 🌸")
                        thanks_embed = discord.Embed(
                            title="💖 Server Bumped!",
                            description=thanks_text,
                            color=0xFFB6C1
                        )
                        await channel.send(embed=thanks_embed)

                        # 2. Asetetaan 2 tunnin cooldown
                        ready_time = datetime.utcnow() + timedelta(hours=2)
                        self.bump_cooldowns[guild.id] = ready_time

                        # 3. Odotetaan 2 tuntia taustalla ja lähetetään muistutus
                        await asyncio.sleep(7200)  # 7200 sekuntia = 2 tuntia

                        role_id = server_cfg.get("bump_role_id")
                        role_ping = f"<@&{role_id}>" if role_id else ""
                        reminder_text = server_cfg.get("reminder_msg", "Time to bump the server! 🚀")

                        reminder_embed = discord.Embed(
                            title="🔔 Time to Bump!",
                            description=reminder_text,
                            color=0xFFB6C1
                        )
                        await channel.send(content=role_ping, embed=reminder_embed)

                        # Poistetaan cooldown muistista
                        if guild.id in self.bump_cooldowns:
                            del self.bump_cooldowns[guild.id]


async def setup(bot):
    await bot.add_cog(BumpSystem(bot))
