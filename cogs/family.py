import discord
from discord.ext import commands
import json
import os

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
            await ctx.send(f"🌸 {member.mention} is already your child!")
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
        """Calculates compatibility between two members with cute commentary."""
        if not user2:
            user2 = ctx.author

        ship_score = (user1.id + user2.id) % 101
        missing_score = 100 - ship_score

        if ship_score >= 90:
            comment = "A perfect match! Soulmates! 💞✨"
        elif ship_score >= 70:
            comment = "A really cute couple together! 🥰🌸"
        elif ship_score >= 40:
            comment = "Good chances, chemistry found! 😊"
        elif ship_score >= 20:
            comment = "Maybe better as friends? 😅"
        else:
            comment = "Opposites attract... maybe? 💔"

        filled = int(ship_score / 10)
        bar = "💖" * filled + "🖤" * (10 - filled)

        embed = discord.Embed(
            title="💞 Compatibility Love Meter",
            description=(
                f"**{user1.mention}** x **{user2.mention}**\n\n"
                f"**Score:** {ship_score}%\n"
                f"[{bar}]\n"
                f"**Away from 100%:** {missing_score}%\n\n"
                f"*{comment}*"
            ),
            color=discord.Color.from_rgb(255, 190, 210)
        )
        embed.set_footer(text="Moonlings Ship System 🌸")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(StarFamily(bot))

