import discord
from discord.ext import commands
import json
import os

DATA_FILE = "counting_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

class Counting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setcounting")
    @commands.has_permissions(administrator=True)
    async def set_counting(self, ctx, channel: discord.TextChannel = None):
        """Asettaa counting-kanavan."""
        channel = channel or ctx.channel
        data = load_data()
        guild_id = str(ctx.guild.id)

        if guild_id not in data:
            data[guild_id] = {}

        data[guild_id]["channel_id"] = channel.id
        data[guild_id].setdefault("current_count", 0)
        data[guild_id].setdefault("last_user_id", None)
        data[guild_id].setdefault("success_emoji", "✅")
        data[guild_id].setdefault("fail_emoji", "❌")
        save_data(data)

        embed = discord.Embed(
            title="🎮 Counting Game Started!",
            description=f"Counting channel set to {channel.mention}.\nStart counting from **1**!",
            color=discord.Color.from_rgb(230, 210, 240)
        )
        embed.set_footer(text="Moonlings Games 🌸")
        await channel.send(embed=embed)

    @commands.group(name="setcountingemoji", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def set_counting_emoji(self, ctx):
        """Ohje custom emojien vaihtoon."""
        prefix = ctx.prefix
        await ctx.send(
            f"🌸 **Counting Emoji Settings**:\n"
            f"`{prefix}setcountingemoji success <emoji>` - Set custom emoji for correct numbers\n"
            f"`{prefix}setcountingemoji fail <emoji>` - Set custom emoji for incorrect numbers"
        )

    @set_counting_emoji.command(name="success")
    @commands.has_permissions(administrator=True)
    async def emoji_success(self, ctx, emoji: str):
        """Asettaa custom emojin onnistuneelle numerolle."""
        data = load_data()
        guild_id = str(ctx.guild.id)
        if guild_id not in data:
            data[guild_id] = {}

        data[guild_id]["success_emoji"] = emoji
        save_data(data)
        await ctx.send(f"✨ Success emoji updated to {emoji}!")

    @set_counting_emoji.command(name="fail")
    @commands.has_permissions(administrator=True)
    async def emoji_fail(self, ctx, emoji: str):
        """Asettaa custom emojin väärälle numerolle."""
        data = load_data()
        guild_id = str(ctx.guild.id)
        if guild_id not in data:
            data[guild_id] = {}

        data[guild_id]["fail_emoji"] = emoji
        save_data(data)
        await ctx.send(f"✨ Fail emoji updated to {emoji}!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        data = load_data()
        guild_id = str(message.guild.id)

        if guild_id not in data:
            return

        channel_id = data[guild_id].get("channel_id")
        if message.channel.id != channel_id:
            return

        content = message.content.strip()
        if not content.isdigit():
            return

        user_number = int(content)
        current_count = data[guild_id].get("current_count", 0)
        last_user_id = data[guild_id].get("last_user_id")
        success_emoji = data[guild_id].get("success_emoji", "✅")
        fail_emoji = data[guild_id].get("fail_emoji", "❌")

        # Tarkistus: Sama käyttäjä ei voi laskea kahdesti putkeen
        if message.author.id == last_user_id:
            try:
                await message.add_reaction(fail_emoji)
            except (discord.Forbidden, discord.HTTPException):
                pass

            data[guild_id]["current_count"] = 0
            data[guild_id]["last_user_id"] = None
            save_data(data)

            await message.channel.send(
                f"{fail_emoji} {message.author.mention} counted twice in a row! Count reset to **0**. Start again from **1**!"
            )
            return

        # Tarkistus: Oikea numero
        if user_number == current_count + 1:
            try:
                await message.add_reaction(success_emoji)
            except (discord.Forbidden, discord.HTTPException):
                pass

            data[guild_id]["current_count"] = user_number
            data[guild_id]["last_user_id"] = message.author.id
            save_data(data)

        else:
            try:
                await message.add_reaction(fail_emoji)
            except (discord.Forbidden, discord.HTTPException):
                pass

            data[guild_id]["current_count"] = 0
            data[guild_id]["last_user_id"] = None
            save_data(data)

            await message.channel.send(
                f"{fail_emoji} Wrong number by {message.author.mention}! The next number was **{current_count + 1}**. Count reset to **0**. Start again from **1**!"
            )

async def setup(bot):
    await bot.add_cog(Counting(bot))
