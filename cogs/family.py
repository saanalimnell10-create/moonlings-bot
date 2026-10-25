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

# Napit kosintaa varten
class ProposalView(discord.ui.View):
    def __init__(self, proposer: discord.Member, target: discord.Member):
        super().__init__(timeout=120)
        self.proposer = proposer
        self.target = target

    @discord.ui.button(label="Accept 💖", style=discord.ButtonStyle.success)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.target.id:
            await interaction.response.send_message("🌸 Tämä kosinta ei ole sinulle!", ephemeral=True)
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

        # Lähetetään tavallinen tekstiviesti Embedin sijaan!
        await interaction.response.edit_message(
            content=f"💍 **OOH!** {self.target.mention} hyväksyi käyttäjän {self.proposer.mention} kosinnan! Onnea uudelle avioparille! 🎉💖🌸",
            embed=None,
            view=self
        )

    @discord.ui.button(label="Decline 💔", style=discord.ButtonStyle.danger)
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.target.id:
            await interaction.response.send_message("🌸 Tämä kosinta ei ole sinulle!", ephemeral=True)
            return

        for item in self.children:
            item.disabled = True

        await interaction.response.edit_message(
            content=f"💔 {self.target.mention} kieltäytyi käyttäjän {self.proposer.mention} kosinnasta...",
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
            await ctx.send("🌸 Et voi kosia itseäsi!")
            return
        if member.bot:
            await ctx.send("🌸 Et voi kosia bottia!")
            return

        data = load_data()
        p_id = str(ctx.author.id)
        t_id = str(member.id)

        if p_id in data and t_id in data[p_id].get("spouses", []):
            await ctx.send(f"🌸 Olet jo naimisissa käyttäjän {member.mention} kanssa!")
            return

        view = ProposalView(ctx.author, member)
        await ctx.send(
            f"💍 {member.mention}, käyttäjä **{ctx.author.mention}** on kosinut sinua! 🌸 Hyväksytkö?",
            view=view
        )

    @commands.command(name="adopt")
    async def adopt(self, ctx, member: discord.Member):
        """Adopts another member into your star family as a child."""
        if member == ctx.author:
            await ctx.send("🌸 Et voi adoptoida itseäsi!")
            return
        if member.bot:
            await ctx.send("🌸 Et voi adoptoida bottia!")
            return

        data = load_data()
        p_id = str(ctx.author.id)
        c_id = str(member.id)

        ensure_user(data, p_id)
        ensure_user(data, c_id)

        if c_id in data[p_id]["children"]:
            await ctx.send(f"🌸 {member.mention} on jo lapsesi!")
            return

        data[p_id]["children"].append(c_id)
        if p_id not in data[c_id]["parents"]:
            data[c_id]["parents"].append(p_id)

        save_data(data)
        await ctx.send(f"👶 🎉 **{ctx.author.mention}** adoptoi käyttäjän **{member.mention}** tähtiperheeseensä! 🌸✨")

    @commands.command(name="divorce")
    async def divorce(self, ctx, member: discord.Member):
        """Amicably dissolves a relationship with a specific partner."""
        data = load_data()
        p_id = str(ctx.author.id)
        t_id = str(member.id)

        if p_id not in data or t_id not in data[p_id].get("spouses", []):
            await ctx.send(f"🌸 Et ole naimisissa käyttäjän {member.mention} kanssa.")
            return

        data[p_id]["spouses"].remove(t_id)
        if t_id in data and p_id in data[t_id].get("spouses", []):
            data[t_id]["spouses"].remove(p_id)

        save_data(data)
        await ctx.send(f"💔 **{ctx.author.mention}** ja **{member.mention}** ovat eronneet sovussa. ✨")

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

        if ship_score >= 90:
            comment = "Täydellinen pari! Sielunkumppanit! 💞✨"
        elif ship_score >= 70:
            comment = "Todella söpö pari yhdessä! 🥰🌸"
        elif ship_score >= 40:
            comment = "Hyvät mahdollisuudet, kemiaa löytyy! 😊"
        elif ship_score >= 20:
            comment = "Ehkä kavereina parempia? 😅"
        else:
            comment = "Vastakohdat täydentävät toisiaan... ehkä? 💔"

        filled = int(ship_score / 10)
        bar = "💖" * filled + "🖤" * (10 - filled)

        embed = discord.Embed(
            title="💞 Compatibility Love Meter",
            description=f"**{user1.mention}** x **{user2.mention}**\n\n**Score:** {ship_score}%\n[{bar}]\n\n*{comment}*",
            color=discord.Color.from_rgb(255, 190, 210)
        )
        embed.set_footer(text="Moonlings Ship System 🌸")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(StarFamily(bot))
