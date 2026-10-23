import discord
from discord.ext import commands
import json
import os

PREFIXES_FILE = "prefixes.json"

def load_prefixes():
    if os.path.exists(PREFIXES_FILE):
        try:
            with open(PREFIXES_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_prefixes(prefixes):
    with open(PREFIXES_FILE, "w") as f:
        json.dump(prefixes, f, indent=4)

def get_prefix_for_guild(bot, message):
    if not message.guild:
        return "??"
    prefixes = load_prefixes()
    return prefixes.get(str(message.guild.id), "??")

class Prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setprefix")
    @commands.has_permissions(administrator=True)
    async def set_prefix(self, ctx, new_prefix: str):
        """Sets a custom command prefix for the server."""
        if len(new_prefix) > 5:
            await ctx.send("❌ Prefix cannot be longer than 5 characters.")
            return

        prefixes = load_prefixes()
        prefixes[str(ctx.guild.id)] = new_prefix
        save_prefixes(prefixes)

        embed = discord.Embed(
            title="✨ Prefix Updated",
            description=f"The command prefix for **{ctx.guild.name}** has been set to: `{new_prefix}`",
            color=discord.Color.from_rgb(230, 210, 240)
        )
        embed.set_footer(text="Moonlings Bot Configuration 🌸")
        await ctx.send(embed=embed)

    @commands.command(name="prefix")
    async def show_prefix(self, ctx):
        """Shows the current command prefix for the server."""
        current = get_prefix_for_guild(self.bot, ctx.message)
        await ctx.send(f"🌸 Current command prefix in this server is: `{current}`")

async def setup(bot):
    await bot.add_cog(Prefix(bot))
