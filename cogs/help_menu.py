import discord
from discord.ext import commands
from discord.ui import Select, View

class HelpSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Moderation & Transparency",
                description="Warns with DM logs, kicks, and bans.",
                emoji="🛡️",
                value="moderation"
            ),
            discord.SelectOption(
                label="Channel Management",
                description="Purge messages, lock and unlock channels.",
                emoji="🌊",
                value="channels"
            ),
            discord.SelectOption(
                label="Ticket System",
                description="Support tickets and transcript logging.",
                emoji="🎫",
                value="tickets"
            ),
            discord.SelectOption(
                label="Community & Games",
                description="Chill Counting game.",
                emoji="✨",
                value="games"
            ),
            discord.SelectOption(
                label="Utility & Bumps",
                description="AFK and general utilities.",
                emoji="🌙",
                value="utility"
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

        # --- 1. MODERATION & TRANSPARENCY ---
        if selection == "moderation":
            embed = discord.Embed(
                title="🛡️ Moderation & Transparency",
                description="Transparent moderation tools with automated DM logs.",
                color=0xFFB6C1
            )
            embed.add_field(
                name="`??ban [@user] [reason]`",
                value="Bans a member from the server with a transparent DM log.",
                inline=False
            )
            embed.add_field(
                name="`??kick [@user] [reason]`",
                value="Kicks a member from the server.",
                inline=False
            )
            embed.add_field(
                name="`??mute [@user] [time] [reason]`",
                value="Temporarily mutes or timeouts a member.",
                inline=False
            )
            embed.add_field(
                name="`??clearwarns [@user]`",
                value="Clears all warnings for the specified user.",
                inline=False
            )

        # --- 2. CHANNEL MANAGEMENT ---
        elif selection == "channels":
            embed = discord.Embed(
                title="🌊 Channel Management",
                description="Tools for keeping chat clean and controlled.",
                color=0xFFB6C1
            )
            embed.add_field(
                name="`??purge [amount]`",
                value="Mass deletes messages from the channel.",
                inline=False
            )
            embed.add_field(
                name="`??purgebots`",
                value="Deletes the latest messages sent by bots.",
                inline=False
            )
            embed.add_field(
                name="`??lock / ??unlock`",
                value="Locks or unlocks the current text channel.",
                inline=False
            )

        # --- 3. TICKET SYSTEM ---
        elif selection == "tickets":
            embed = discord.Embed(
                title="🎫 Ticket System",
                description="Support tickets and transcript logging.",
                color=0xFFB6C1
            )
            embed.add_field(
                name="`??ticket`",
                value="Opens a new support ticket channel.",
                inline=False
            )
            embed.add_field(
                name="`??close`",
                value="Closes the current active ticket and saves a transcript.",
                inline=False
            )
            embed.add_field(
                name="`??add [@user]` / `??remove [@user]`",
                value="Adds or removes a user from the ticket.",
                inline=False
            )

        # --- 4. COMMUNITY & GAMES ---
        elif selection == "games":
            embed = discord.Embed(
                title="✨ Community & Games",
                description="Fun activities and cozy server games.",
                color=0xFFB6C1
            )
            embed.add_field(
                name="`??setcounting`",
                value="Sets up the channel for the Chill Counting game.",
                inline=False
            )

        # --- 5. UTILITY & BUMPS ---
        elif selection == "utility":
            embed = discord.Embed(
                title="🌙 Utility & Bumps",
                description="AFK and general utilities.",
                color=0xFFB6C1
            )
            embed.add_field(
                name="`??afk [reason]`",
                value="Sets your status to AFK with an optional reason.",
                inline=False
            )
            embed.add_field(
                name="`??ping`",
                value="Checks the bot's response latency.",
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
                "to explore all available commands."
            ),
            color=0xFFB6C1
        )
        embed.set_footer(text="Moonlings Bot • Cozy Space & Sea Aesthetic 🌸")
        await ctx.send(embed=embed, view=HelpMenuView())


async def setup(bot):
    await bot.add_cog(HelpMenuCog(bot))
