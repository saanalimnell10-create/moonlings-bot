import discord
from discord.ext import commands

class HelpDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Moderation & Transparency",
                description="Warns with DM logs, kicks, and bans.",
                emoji="🛡️"
            ),
            discord.SelectOption(
                label="Channel Management",
                description="Purge messages, lock and unlock channels.",
                emoji="🌊"
            ),
            discord.SelectOption(
                label="Ticket System",
                description="Support tickets and transcript logging.",
                emoji="🎫"
            ),
            discord.SelectOption(
                label="Community & Games",
                description="Truth or Dare and Chill Counting game.",
                emoji="✨"
            ),
            discord.SelectOption(
                label="Utility & Bumps",
                description="AFK, stats, star bumps, and replies.",
                emoji="🌙"
            ),
        ]
        super().__init__(placeholder="Select a category to explore~ 🌸", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "Moderation & Transparency":
            embed = discord.Embed(
                title="🛡️ Moderation & Transparency",
                description="Keeping Moonlings safe, cozy, and fair!",
                color=0xFFB7C5
            )
            embed.add_field(name="??warn [@user] [reason]", value="Warns a member and automatically sends a transparent pastel DM log containing the moderator, reason, and a unique Case ID.", inline=False)
            embed.add_field(name="??mute / ??unwarn / ??warnings", value="Mute rule-breakers or check warning history.", inline=False)
            embed.add_field(name="??kick / ??ban", value="Standard safety tools to keep rule-breakers away.", inline=False)

        elif self.values[0] == "Channel Management":
            embed = discord.Embed(
                title="🌊 Channel Management",
                description="Tools for keeping chat clean and controlled.",
                color=0xB5EAD7
            )
            embed.add_field(name="??purge [amount]", value="Mass deletes messages from the channel.", inline=False)
            embed.add_field(name="??lock / ??unlock", value="Locks or unlocks the current text channel.", inline=False)

        elif self.values[0] == "Ticket System":
            embed = discord.Embed(
                title="🎫 Ticket System",
                description="Need help or want to talk to staff?",
                color=0xFFDAC1
            )
            embed.add_field(name="Ticket Categories", value="Staff Complaint, Promo & Sponsorship, Giveaway Claim, and Staff Applications.", inline=False)
            embed.add_field(name="Transcript Logs", value="Automatic text transcripts sent to `#ticket-logs` upon closure.", inline=False)

        elif self.values[0] == "Community & Games":
            embed = discord.Embed(
                title="✨ Community & Games",
                description="Fun activities for everyone!",
                color=0xFFD1DC
            )
            embed.add_field(name="??truth / ??dare / ??tod", value="Play Truth or Dare with friends.", inline=False)
            embed.add_field(name="Chill Counting", value="Count together (`??setcounting`, `??resetcount`).", inline=False)

        elif self.values[0] == "Utility & Bumps":
            embed = discord.Embed(
                title="🌙 Utility & Bumps",
                description="Helpful tools and server boosts.",
                color=0xC7CEEA
            )
            embed.add_field(name="??afk [reason]", value="Sets your AFK status with automatic nickname tagging.", inline=False)
            embed.add_field(name="??vctop / ??stats", value="View activity stats and voice channel leaderboards.", inline=False)
            embed.add_field(name="??bump / ??setbumpchannel", value="Star bumps reminder system for Disboard.", inline=False)
            embed.add_field(name="??reply [message_id]", value="Reply directly to a specific message ID.", inline=False)

        embed.set_footer(text="Moonlings Bot • Cozy Space & Sea Aesthetic 🌸")
        await interaction.response.edit_message(embed=embed, view=self.view)

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
            description="Welcome to Moonlings! Choose a category from the dropdown menu below to explore our active features.",
            color=0xFFB7C5
        )
        embed.set_footer(text="Made with love for cozy communities ✨")
        
        view = HelpView()
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(HelpMenu(bot))
