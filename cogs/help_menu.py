import discord
from discord.ext import commands

class HelpSelect(discord.ui.Select):
    def __init__(self, bot):
        self.bot = bot
        options = [
            discord.SelectOption(label="Moderation & Transparency", description="Warns, bans, kicks, mutes, and purges.", emoji="🛡️"),
            discord.SelectOption(label="Anti-Nuke & Anti-Raid", description="Mass deletion limits, whitelist, and server lockdown.", emoji="🚨"),
            discord.SelectOption(label="Audit Log & Event Logging", description="Real time event logging, channel tracking, and toggles.", emoji="📜"),
            discord.SelectOption(label="Conflict & Safety Suite", description="Isolate arguments, forced names, and member safety.", emoji="🌿"),
            discord.SelectOption(label="Custom Fake Permissions", description="Manage safe role permissions without native admin rights.", emoji="🔒"),
            discord.SelectOption(label="Server Tools", description="Steal emojis and clone channel settings.", emoji="🛠️"),
            discord.SelectOption(label="Channel Management", description="Purge messages, lock and unlock channels.", emoji="🌊"),
            discord.SelectOption(label="Ticket System", description="Support tickets, staff applications, and transcript logging.", emoji="🎫"),
            discord.SelectOption(label="Community & Games", description="Truth or Dare, counting game, and message stats.", emoji="✨"),
            discord.SelectOption(label="Bump & Reminders", description="Star bumps, roles, and custom message settings.", emoji="🚀"),
            discord.SelectOption(label="Utility & Tools", description="Bot, server, and user info commands.", emoji="🌙"),
        ]
        super().__init__(placeholder="Select a category to explore~ 🌸", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        selected = self.values[0]
        embed = discord.Embed(color=discord.Color.from_rgb(230, 210, 240))

        if selected == "Ticket System":
            embed.title = "🎫 Ticket System & Applications"
            embed.description = "Support tickets, staff applications, and transcript logging."
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??ticketpanel` - Lähettää tikettipaneelin alasvetovalikolla (Admin).\n"
                    "`??applypanel` - Lähettää Staff Application -hakemuspaneelin (Admin).\n"
                    "`??close` - Sulkee tiketin/hakemuksen ja luo automaattisesti transcriptin.\n"
                    "`??add [käyttäjä]` - Lisää käyttäjän mukaan aktiiviseen tikettiin.\n"
                    "`??remove [käyttäjä]` - Poistaa käyttäjän aktiivisesta tiketistä.\n"
                    "`??block [käyttäjä]` - Estää tiettyä käyttäjää näkemästä tikettiä."
                ),
                inline=False
            )

        elif selected == "Moderation & Transparency":
            embed.title = "🛡️ Moderation & Transparency"
            embed.description = "Warns, bans, kicks, and timeouts with DM logs."
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??ban [käyttäjä] [syy]` - Bannaa käyttäjän palvelimelta.\n"
                    "`??unban [käyttäjä_id]` - Poistaa käyttäjän bännit.\n"
                    "`??kick [käyttäjä] [syy]` - Potkaisee käyttäjän palvelimelta.\n"
                    "`??mute [käyttäjä] [aika] [syy]` - Mykistää käyttäjän määräajaksi.\n"
                    "`??unmute [käyttäjä]` - Poistaa käyttäjän mykistyksen.\n"
                    "`??warn [käyttäjä] [syy]` - Annetaan varoitus käyttäjälle.\n"
                    "`??warnings [käyttäjä]` - Näyttää käyttäjän saamat varoitukset."
                ),
                inline=False
            )

        elif selected == "Channel Management":
            embed.title = "🌊 Channel Management"
            embed.description = "Purge messages, lock and unlock channels."
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??purge [määrä]` - Poistaa halutun määrän viestejä kanavalta.\n"
                    "`??lockdown` - Lukitsee kanavan väliaikaisesti.\n"
                    "`??unlock` - Avaa lukitun kanavan.\n"
                    "`??slowmode [aika]` - Asettaa kanavalle viestiviiveen."
                ),
                inline=False
            )

        elif selected == "Utility & Tools":
            embed.title = "🌙 Utility & Tools"
            embed.description = "General bot information, user profiles, and server status."
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??help` - Avaa tämän interaktiivisen ohjevalikon.\n"
                    "`??userinfo [käyttäjä]` - Näyttää valitun käyttäjän tiedot (roolit, liittymispäivät jne.).\n"
                    "`??serverinfo` - Näyttää tietoja palvelimesta (omistaja, jäsenet, kanavat jne.).\n"
                    "`??botinfo` - Näyttää Moonlings-botin tilastot, pingin ja versiotiedot.\n"
                    "`??ping` - Näyttää botin nykyisen viiveen."
                ),
                inline=False
            )

        elif selected == "Anti-Nuke & Anti-Raid":
            embed.title = "🚨 Anti-Nuke & Anti-Raid"
            embed.description = "Mass deletion limits, whitelist, and server protection."
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??anti-nuke [on/off]` - Kytkee anti-nuke-suojauksen päälle/pois.\n"
                    "*(Muita suojausasetuksia hallitaan suoraan Dashboardista)*"
                ),
                inline=False
            )

        else:
            embed.title = f"✨ {selected}"
            embed.description = f"Tämän kategorian asiat ja asetukset hallitaan kätevästi Dashboardin kautta tai ne ovat kehityksessä!"

        embed.set_footer(text="Moonlings Bot • Cozy Space & Sea Aesthetic 🌸")
        await interaction.response.edit_message(embed=embed)


class HelpView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=120)
        self.add_item(HelpSelect(bot))


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")

    @commands.command(name="help")
    async def help_command(self, ctx):
        embed = discord.Embed(
            title="🌸 Moonlings Help Center",
            description="Welcome to Moonlings! Select a category below from the drop-down menu to view commands.",
            color=discord.Color.from_rgb(230, 210, 240)
        )
        embed.set_footer(text="Moonlings Bot • Cozy Space & Sea Aesthetic 🌸")
        await ctx.send(embed=embed, view=HelpView(self.bot))

async def setup(bot):
    await bot.add_cog(Help(bot))
