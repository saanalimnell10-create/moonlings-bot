import discord
from discord.ext import commands

class HelpDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Moderation & Transparency",
                description="View moderation commands and transparent DM logs.",
                emoji="🛡️"
            ),
            discord.SelectOption(
                label="Channel & Management",
                description="Purge, lock, and channel controls.",
                emoji="🌊"
            ),
            discord.SelectOption(
                label="Community & Games",
                description="Counting, Truth or Dare, and mini-games.",
                emoji="✨"
            ),
            discord.SelectOption(
                label="Utility & Bumps",
                description="Star bumps, reminders, and helpful tools.",
                emoji="🌙"
            ),
        ]
        super().__init__(placeholder="Select a category to explore~ 🌸", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "Moderation & Transparency":
            embed = discord.Embed(
                title="🛡️ Moderation & Transparency",
                description="Keeping Moonlings safe and fair for everyone!",
                color=0xFFB7C5
            )
            embed.add_field(name="??warn [@user] [reason]", value="Warns a member and sends a transparent pastel DM log with case ID and evidence.", inline=False)
            embed.add_field(name="Transparent DM Logs", value="Automatically sends moderator info, reasons, and case numbers to punished members.", inline=False)
            embed.add_field(name="??kick / ??ban", value="Standard safety tools to keep rule-breakers away.", inline=False)

        elif self.values[0] == "Channel & Management":
            embed = discord.Embed(
                title="🌊 Channel Management",
                description="Tools for keeping chat clean and cozy.",
                color=0xB5EAD7
            )
            embed.add_field(name="??purge [amount]", value="Quickly cleans up messages.", inline=False)
            embed.add_field(name="??lock / ??unlock", value="Locks or unlocks a channel.", inline=False)

        elif self.values[0] == "Community & Games":
            embed = discord.Embed(
                title="✨ Community & Games",
                description="Fun activities for all the pookies in chat!",
                color=0xFFD1DC
            )
            embed.add_field(name="??truth / ??dare / ??tod", value="Play Truth or Dare with friends.", inline=False)
            embed.add_field(name="Chill Counting", value="Count together in the designated channel!", inline=False)

        elif self.values[0] == "Utility & Bumps":
            embed = discord.Embed(
                title="🌙 Utility & Bumps",
                description="Server boosts and helper commands.",
                color=0xC7CEEA
            )
            embed.add_field(name="??bump", value="Instructions for bumping the server via Disboard.", inline=False)
            embed.add_field(name="??setbumpchannel", value="Sets the official cozy bump reminder channel.", inline=False)

        embed.set_footer(text="Moonlings Bot • Cozy Space & Sea Aesthetic 🌸")
        await interaction.response.edit_message(embed=embed)

class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(HelpDropdown())

class HelpMenu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx):
        """Displays the interactive pastel help menu."""
        embed = discord.Embed(
            title="🌙 Moonlings Help Menu 🌙",
            description="Welcome to Moonlings! Choose a category from the dropdown menu below to explore our features.",
            color=0xFFB7C5
        )
        embed.set_image(url="https://i.imgur.com/example.png") # Voit vaihtaa oman bannerin tähän
        embed.set_footer(text="Made with love for cozy communities ✨")
        
        view = HelpView()
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(HelpMenu(bot))
