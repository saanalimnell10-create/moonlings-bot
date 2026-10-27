import discord
from discord.ext import commands
import json
import os
import io
import aiohttp
import random
from PIL import Image, ImageDraw

DATA_FILE = "star_family.json"

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

def ensure_user(data, user_id):
    if user_id not in data:
        data[user_id] = {
            "spouses": [],
            "children": [],
            "parents": []
        }

class ProposalView(discord.ui.View):
    def __init__(self, proposer: discord.Member, target: discord.Member):
        super().__init__(timeout=120)
        self.proposer = proposer
        self.target = target

    @discord.ui.button(label="Accept 💖", style=discord.ButtonStyle.success)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.target.id:
            await interaction.response.send_message("🌸 This proposal is not for you!", ephemeral=True)
            return

        data = load_data()
        p_id = str(self.proposer.id)
        t_id = str(self.target.id)

        ensure_user(data, p_id)
        ensure_user(data, t_id)

        if t_id not in data[p_id]["spouses"]:
            data[p_id]["spouses"].append(t_id)
        if p_id not in data[t_id]["spouses"]:
            data[t_id]["spouses"].append(p_id)

        save_data(data)

        for item in self.children:
            item.disabled = True

        await interaction.response.edit_message(
            content=f"💍 **OOH!** {self.target.mention} accepted {self.proposer.mention}'s proposal! Congratulations to the happy couple! 🎉💖🌸",
            embed=None,
            view=self
        )

    @discord.ui.button(label="Decline 💔", style=discord.ButtonStyle.danger)
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.target.id:
            await interaction.response.send_message("🌸 This proposal is not for you!", ephemeral=True)
            return

        for item in self.children:
            item.disabled = True

        await interaction.response.edit_message(
            content=f"💔 {self.target.mention} declined {self.proposer.mention}'s proposal...",
            embed=None,
            view=self
        )

class StarFamily(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="propose")
    async def propose(self, ctx, member: discord.Member):
        """Proposes to a member with interactive buttons."""
        if member == ctx.author:
            await ctx.send("🌸 You cannot propose to yourself!")
            return
        if member.bot:
            await ctx.send("🌸 You cannot propose to a bot!")
            return

        data = load_data()
        p_id = str(ctx.author.id)
        t_id = str(member.id)

        if p_id in data and t_id in data[p_id].get("spouses", []):
            await ctx.send(f"🌸 You are already married to {member.mention}!")
            return

        view = ProposalView(ctx.author, member)
        await ctx.send(
            f"💍 {member.mention}, **{ctx.author.mention}** has proposed to you! 🌸 Do you accept?",
            view=view
        )

    @commands.command(name="adopt")
    async def adopt(self, ctx, member: discord.Member):
        """Adopts another member into your star family as a child."""
        if member == ctx.author:
            await ctx.send("🌸 You cannot adopt yourself!")
            return
        if member.bot:
            await ctx.send("🌸 You cannot adopt a bot!")
            return

        data = load_data()
        p_id = str(ctx.author.id)
        c_id = str(member.id)

        ensure_user(data, p_id)
        ensure_user(data, c_id)

        if c_id in data[p_id]["children"]:
            await ctx.send(f"🌸 {member.mention} is already your child! 💕")
            return

        data[p_id]["children"].append(c_id)
        if p_id not in data[c_id]["parents"]:
            data[c_id]["parents"].append(p_id)

        save_data(data)
        await ctx.send(f"👶 🎉 **{ctx.author.mention}** has adopted **{member.mention}** into their star family! 🌸✨")

    @commands.command(name="divorce")
    async def divorce(self, ctx, member: discord.Member):
        """Amicably dissolves a relationship with a specific partner."""
        data = load_data()
        p_id = str(ctx.author.id)
        t_id = str(member.id)

        if p_id not in data or t_id not in data[p_id].get("spouses", []):
            await ctx.send(f"🌸 You are not married to {member.mention}.")
            return

        data[p_id]["spouses"].remove(t_id)
        if t_id in data and p_id in data[t_id].get("spouses", []):
            data[t_id]["spouses"].remove(p_id)

        save_data(data)
        await ctx.send(f"💔 **{ctx.author.mention}** and **{member.mention}** have amicably divorced. ✨")

    @commands.command(name="family")
    async def family(self, ctx, member: discord.Member = None):
        """Displays a pastel embed showing all family members."""
        target = member or ctx.author
        data = load_data()
        u_id = str(target.id)

        user_data = data.get(u_id, {"spouses": [], "children": [], "parents": []})

        spouses = [f"<@{s}>" for s in user_data.get("spouses", [])]
        children = [f"<@{c}>" for c in user_data.get("children", [])]
        parents = [f"<@{p}>" for p in user_data.get("parents", [])]

        embed = discord.Embed(
            title=f"🌸 {target.display_name}'s Star Family Tree",
            color=discord.Color.from_rgb(230, 210, 240)
        )
        embed.set_thumbnail(url=target.display_avatar.url)

        embed.add_field(name="💍 Spouses / Partners", value=", ".join(spouses) if spouses else "*None*", inline=False)
        embed.add_field(name="👶 Children", value=", ".join(children) if children else "*None*", inline=False)
        embed.add_field(name="👑 Parents", value=", ".join(parents) if parents else "*None*", inline=False)

        embed.set_footer(text="Moonlings Star Family 🌸")
        await ctx.send(embed=embed)

    @commands.command(name="ship")
    async def ship(self, ctx, user1: discord.Member, user2: discord.Member = None):
        """Calculates galactic compatibility and generates a cute pookie ship card!"""
        if not user2:
            user2 = ctx.author

        score = (user1.id + user2.id) % 101
        missing = 100 - score

        if score >= 90:
            comment = "✨ absolute pookie soulmates floating in the galaxy! 💖"
        elif score >= 70:
            comment = "🌸 super cute cosmic besties & partners! 🥰"
        elif score >= 40:
            comment = "💫 starry vibes, good chemistry! 😊"
        elif score >= 20:
            comment = "🌙 cute friendly space travel buds! 🛸"
        else:
            comment = "🪐 drifting in different orbits... but still cute! 🤍"

        # Luodaan galaktinen ja söpö kortti
        width, height = 600, 240
        image = Image.new("RGBA", (width, height), (25, 15, 35, 255)) # Galaxy dark purple
        draw = ImageDraw.Draw(image)

        # Piirretään satunnaisia pieniä "tähtiä" taivaalle (galactic dust)
        for _ in range(35):
            rx = random.randint(10, width - 10)
            ry = random.randint(10, height - 10)
            draw.point((rx, ry), fill=(255, 240, 250, random.randint(100, 220)))

        # Söpö pastellinen reuna
        draw.rounded_rectangle([10, 10, width-10, height-10], radius=18, outline=(255, 180, 220), width=3)

        async def fetch_avatar(user):
            url = user.display_avatar.with_size(128).url
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        data = await resp.read()
                        return Image.open(io.BytesIO(data)).convert("RGBA")
            return Image.new("RGBA", (100, 100), (150, 150, 150, 255))

        av1 = await fetch_avatar(user1)
        av2 = await fetch_avatar(user2)

        def make_circle_avatar(av):
            av = av.resize((90, 90))
            mask = Image.new("L", (90, 90), 0)
            ImageDraw.Draw(mask).ellipse((0, 0, 90, 90), fill=255)
            
            output = Image.new("RGBA", (90, 90), (0, 0, 0, 0))
            output.paste(av, (0, 0), mask=mask)
            
            # Söpö vaaleanpunainen reunus avatarille
            ring = Image.new("RGBA", (98, 98), (0, 0, 0, 0))
            ImageDraw.Draw(ring).ellipse((0, 0, 98, 98), fill=(255, 160, 200, 255))
            ring.paste(output, (4, 4), mask=output)
            return ring

        circle1 = make_circle_avatar(av1)
        circle2 = make_circle_avatar(av2)

        image.paste(circle1, (50, 55), circle1)
        image.paste(circle2, (452, 55), circle2)

        # Sydän keskelle prosentilla
        draw.ellipse((260, 55, 340, 125), fill=(255, 110, 160, 255))
        draw.text((285, 82), f"{score}%", fill=(255, 255, 255, 255))

        # Latauspalkki (pastelli vaaleanpunainen)
        bx1, by1, bx2, by2 = 175, 150, 425, 166
        draw.rounded_rectangle([bx1, by1, bx2, by2], radius=8, fill=(45, 30, 55, 255))
        fill_w = int((bx2 - bx1) * (score / 100))
        if fill_w > 0:
            draw.rounded_rectangle([bx1, by1, bx1 + fill_w, by2], radius=8, fill=(255, 150, 200, 255))

        # Nimet, galaktinen teema ja puuttuvat prosentit
        draw.text((170, 25), f"🌌 [ {user1.name} + {user2.name} ] 🪐", fill=(255, 220, 240, 255))
        draw.text((170, 185), f"{comment}", fill=(230, 200, 220, 255))
        draw.text((195, 210), f"✨ Missing to 100%: {missing}% ✨", fill=(180, 160, 200, 255))

        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)

        file = discord.File(buffer, filename="galaxy_ship.png")
        await ctx.send(file=file)

async def setup(bot):
    await bot.add_cog(StarFamily(bot))

