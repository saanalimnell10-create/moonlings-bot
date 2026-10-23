import discord
from discord.ext import commands
from discord.ui import Select, View

class HelpSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="General & Utility",
                description="Basic server commands & utility tools",
                emoji="⚙️",
                value="general"
            ),
            discord.SelectOption(
                label="Ticket System",
                description="Support ticket creation and management",
                emoji="🎫",
                value="tickets"
            ),
            discord.SelectOption(
                label="Moderation Suite",
                description="Server moderation & safety tools",
                emoji="🛡️",
                value="moderation"
            ),
            discord.SelectOption(
                label="Games & Fun",
                description="Chill Counting game",
                emoji="🔢",
                value="games"
            ),
        ]
        super().__init__(
            placeholder="Select a category to explore~ 🌸",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        selection = self.values[0]

        # --- 1. GENERAL & UTILITY ---
        if selection == "general":
            embed = discord.Embed(
                title="⚙️ General & Utility",
                description="Essential commands for everyday server interactions.",
                color=0xFFB6C1
            )
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??help` – Opens this interactive help menu\n"
                    "`??afk [reason]` – Sets your status to AFK with an optional custom reason\n"
                    "`??ping` – Checks the bot's response latency"
                ),
                inline=False
            )

        # --- 2. TICKET SYSTEM ---
        elif selection == "tickets":
            embed = discord.Embed(
                title="🎫 Ticket System",
                description="Need help or want to talk to staff? Open a ticket below!",
                color=0xFFB6C1
            )
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??ticket` – Open a new support ticket\n"
                    "`??close` – Close the current active ticket\n"
                    "`??add [@user]` – Add a user to the ticket channel\n"
                    "`??remove [@user]` – Remove a user from the ticket channel"
                ),
                inline=False
            )
            embed.add_field(
                name="🏷️ Ticket Categories",
                value="Staff Complaint, Promo & Sponsorship, Giveaway Claim, and Staff Applications",
                inline=False
            )

        # --- 3. MODERATION SUITE ---
        elif selection == "moderation":
            embed = discord.Embed(
                title="🛡️ Moderation Suite",
                description="Transparent moderation tools with automated DM logs and Case IDs.",
                color=0xFFB6C1
            )
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??ban [@user] [reason]` – Bans a member from the server\n"
                    "`??kick [@user] [reason]` – Kicks a member from the server\n"
                    "`??mute [@user] [time] [reason]` – Temporarily mutes/timeouts a member\n"
                    "`??clearwarns [@user]` – Clears all warnings for a user\n"
                    "`??purge [amount]` – Purges specified amount of recent messages\n"
                    "`??purgebots` – Deletes recent messages sent by bots\n"
                    "`??hide` / `??lock` – Hides or locks the current channel"
                ),
                inline=False
            )

        # --- 4. GAMES & FUN ---
        elif selection == "games":
            embed = discord.Embed(
                title="🔢 Games & Chill Suite",
                description="Cozy games and interactive server activities.",
                color=0xFFB6C1
            )
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??setcounting` – Set the current channel for the Chill Counting game"
                ),
                inline=False
            )

        embed.set_footer(text="Moonlings Bot • Cozy Space & Sea Aesthetic 🌸")
        await interaction.response.edit_message(embed=embed)


class HelpMenuView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(HelpSelect())


class HelpMenuCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx):
        embed = discord.Embed(
            title="🌸 Moonlings Help Center",
            description=(
                "Welcome to **Moonlings**! Please select a category from the dropdown menu below "
                "to explore all available commands and features."
            ),
            color=0xFFB6C1
        )
        embed.set_footer(text="Moonlings Bot • Cozy Space & Sea Aesthetic 🌸")
        await ctx.send(embed=embed, view=HelpMenuView())


async def setup(bot):
    await bot.add_cog(HelpMenuCog(bot))
