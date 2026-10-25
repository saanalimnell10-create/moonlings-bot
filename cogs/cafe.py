import discord
from discord.ext import commands
import json
import os
import random

DATA_FILE = "cafe_inventories.json"

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

class Cafe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="brew")
    async def brew(self, ctx, *, drink: str = None):
        """Brews a cozy virtual hot drink."""
        drinks = ["Matcha Latte 🍵", "Chai Tea ☕", "Chamomile Tea 🌼", "Caramel Macchiato ☕", "Strawberry Boba Tea 🧋", "Hot Chocolate 🍫"]
        
        selected_drink = drink.title() if drink else random.choice(drinks)
        user_id = str(ctx.author.id)

        data = load_data()
        if user_id not in data:
            data[user_id] = {"pantry": {}}

        pantry = data[user_id]["pantry"]
        pantry[selected_drink] = pantry.get(selected_drink, 0) + 1
        save_data(data)

        embed = discord.Embed(
            title="☕ Freshly Brewed!",
            description=f"{ctx.author.mention} just brewed a warm and cozy **{selected_drink}**! 🌸",
            color=discord.Color.from_rgb(255, 220, 230)
        )
        embed.set_footer(text="Added to your personal pantry! Check with ??pantry ✨")
        await ctx.send(embed=embed)

    @commands.command(name="bake")
    async def bake(self, ctx, *, pastry: str = None):
        """Bakes a sweet treat."""
        pastries = ["Cinnamon Roll 🥮", "Strawberry Shortcake 🍰", "Blueberry Muffin 🧁", "Croissant 🥐", "Matcha Cookie 🍪", "Pancake Stack 🥞"]
        
        selected_pastry = pastry.title() if pastry else random.choice(pastries)
        user_id = str(ctx.author.id)

        data = load_data()
        if user_id not in data:
            data[user_id] = {"pantry": {}}

        pantry = data[user_id]["pantry"]
        pantry[selected_pastry] = pantry.get(selected_pastry, 0) + 1
        save_data(data)

        embed = discord.Embed(
            title="🍰 Fresh From the Oven!",
            description=f"{ctx.author.mention} baked a delicious **{selected_pastry}**! 🌸",
            color=discord.Color.from_rgb(255, 230, 210)
        )
        embed.set_footer(text="Added to your personal pantry! Check with ??pantry ✨")
        await ctx.send(embed=embed)

    @commands.command(name="serve")
    async def serve(self, ctx, member: discord.Member, *, item: str):
        """Sends a lovely pastel embed serving a drink or pastry to a friend."""
        if member == ctx.author:
            await ctx.send("🌸 You can't serve yourself! Serve a friend to brighten their day ✨")
            return

        user_id = str(ctx.author.id)
        data = load_data()

        if user_id not in data or not data[user_id].get("pantry"):
            await ctx.send("🌸 Your pantry is empty! Brew or bake something first with `??brew` or `??bake`.")
            return

        pantry = data[user_id]["pantry"]
        
        # Esitellään tuotteen nimen joustava haku (case-insensitive)
        matched_item = None
        for key in pantry.keys():
            if item.lower() in key.lower():
                matched_item = key
                break

        if not matched_item or pantry[matched_item] <= 0:
            await ctx.send(f"🌸 You don't have **{item}** in your pantry! Check `??pantry` to see what you have.")
            return

        # Vähennetään tuote tarjoilijan varastosta
        pantry[matched_item] -= 1
        if pantry[matched_item] == 0:
            del pantry[matched_item]
        save_data(data)

        embed = discord.Embed(
            title="🍵 Cozy Cafe Delivery!",
            description=f"Dear {member.mention},\n\n{ctx.author.mention} served you a special **{matched_item}**! 🌸✨\n\n*Hope this brightens your day!*",
            color=discord.Color.from_rgb(230, 210, 240)
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text="Moonlings Cozy Cafe 🌸")
        await ctx.send(embed=embed)

    @commands.command(name="pantry")
    async def pantry(self, ctx, member: discord.Member = None):
        """Displays your personal inventory of cozy cafe items."""
        target = member or ctx.author
        user_id = str(target.id)

        data = load_data()
        user_pantry = data.get(user_id, {}).get("pantry", {})

        embed = discord.Embed(
            title=f"🧺 {target.display_name}'s Cozy Pantry",
            color=discord.Color.from_rgb(230, 210, 240)
        )

        if not user_pantry:
            embed.description = "The pantry is currently empty! Use `??brew` or `??bake` to stock up ☕🍰"
        else:
            description_lines = []
            for item_name, count in user_pantry.items():
                description_lines.append(f"• **{item_name}** x{count}")
            embed.description = "\n".join(description_lines)

        embed.set_footer(text="Moonlings Cozy Cafe 🌸")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Cafe(bot))
