import discord
from discord.ext import commands
import random

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Söpöt ja kiltit totuuskysymykset
        self.truths = [
            "What is your absolute favorite cozy game or movie? 🎮🍿",
            "If you could have any magical creature as a pet, what would it be? ✨",
            "What is the silliest nickname you've ever been called? 🤭",
            "If you could instantly teleport anywhere in the world right now, where would you go? ✈️",
            "What is your ultimate comfort food? 🍜🍰",
            "What's a fun hobby you've started recently or want to try? 🎨",
            "If you were a star in the galaxy, what color would you glow? 🌟",
            "What is your favorite memory on Discord so far? 💬"
        ]

        # Söpöt ja helpot tehtävät
        self.dares = [
            "Send the cutest emoji you have in your list right now! 🌸",
            "Compliment the person who messaged right before you in this channel~ ✨",
            "Change your status or type your next three messages using only star/space emojis! 🌌",
            "Share a picture of a cozy corner in your room or your favorite snack! 🍰",
            "Type out a warm encouragement message to everyone reading this channel right now! 💖",
            "Tell a quick, silly joke to make everyone smile! 🤭",
            "Send a GIF that represents your current mood today! 🫧"
        ]

    @commands.command(name="truth")
    async def truth_command(self, ctx):
        await ctx.message.delete()
        question = random.choice(self.truths)

        embed = discord.Embed(
            title="🌸 ∙ Truth or Dare: Truth",
            description=f"**{ctx.author.mention}**, here is your question:\n\n```{question}```",
            color=discord.Color.from_rgb(255, 182, 193)
        )
        embed.set_footer(text="Moonlings Games ☁️", icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.command(name="dare")
    async def dare_command(self, ctx):
        await ctx.message.delete()
        dare = random.choice(self.dares)

        embed = discord.Embed(
            title="✨ ∙ Truth or Dare: Dare",
            description=f"**{ctx.author.mention}**, here is your challenge:\n\n```{dare}```",
            color=discord.Color.from_rgb(175, 238, 238)
        )
        embed.set_footer(text="Moonlings Games ☁️", icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Games(bot))
