import discord
from discord.ext import commands
from discord.ui import Select, View

class HelpSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Moderation & Transparency",
                description="Warns, bans, kicks, and timeouts with DM logs.",
                emoji="🛡️",
                value="moderation"
            ),
            discord.SelectOption(
                label="Audit Log & Event Logging",
                description="Real-time event logging, channel tracking, and toggles.",
                emoji="📜",
                value="audit"
            ),
            discord.SelectOption(
                label="Conflict & Safety Suite",
                description="Isolate arguments, forced names, and member safety.",
                emoji="🕊️",
                value="conflict"
            ),
            discord.SelectOption(
                label="Custom Fake Permissions",
                description="Manage safe role permissions without native admin rights.",
                emoji="🔒",
                value="fakeperms"
            ),
            discord.SelectOption(
                label="Server Tools",
                description="Steal emojis and clone channel settings.",
                emoji="🛠️",
                value="servertools"
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
                description="Truth or Dare, counting game, and message stats.",
                emoji="✨",
                value="games"
            ),
            discord.SelectOption(
                label="Bump & Reminders",
                description="Star bumps, roles, and custom message settings.",
                emoji="🚀",
                value="bump"
            ),
            discord.SelectOption(
                label="Utility & Tools",
                description="AFK, voice stats, and direct replies.",
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
                name="📜 Commands",
                value=(
                    "`??ban [@user] [reason]` – Bans a member from the server with a transparent DM log.\n"
                    "`??kick [@user] [reason]` – Kicks a member from the server.\n"
                    "`??mute [@user] [time] [reason]` – Temporarily mutes or timeouts a member.\n"
                    "`??clearwarns [@user]` – Clears all warnings for the specified user."
                ),
                inline=False
            )

        # --- 2. AUDIT LOG & EVENT LOGGING ---
        elif selection == "audit":
            embed = discord.Embed(
                title="📜 Audit Log & Event Logging",
                description="Real-time audit log events and automatic channel setup.",
                color=0xFFB6C1
            )
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??setlogs [#channel]` – Sets the audit log channel (creates `#audit-logs` automatically if left empty).\n"
                    "`??logevents` – View and toggle which events are currently logged.\n"
                    "`??logs [on/off]` – Quickly enables or disables the logging system."
                ),
                inline=False
            )

        # --- 3. CONFLICT & SAFETY SUITE ---
        elif selection == "conflict":
            embed = discord.Embed(
                title="🕊️ Conflict & Safety Suite",
                description="Specialized tools for resolving disputes and protecting members.",
                color=0xFFB6C1
            )
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??isolate [@user1] [@user2] [reason]` – Isolates arguing members into a temporary private channel.\n"
                    "`??endbeef [@user1] [@user2]` – Ends the isolation and deletes the temporary channel.\n"
                    "`??forcename [@user] [nickname]` – Forces a nickname on a member and automatically re-applies it if changed.\n"
                    "`??forcename [@user] remove` – Removes the forced nickname lock."
                ),
                inline=False
            )

        # --- 4. CUSTOM FAKE PERMISSIONS ---
        elif selection == "fakeperms":
            embed = discord.Embed(
                title="🔒 Custom Fake Permissions System",
                description="Safely grant bot command permissions to roles without Discord admin powers.",
                color=0xFFB6C1
            )
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??fakepermissions grant [@role] [permissions]` – Grants specific bot command permissions to a role.\n"
                    "`??fakepermissions list [@role]` – Views all fake permissions granted to a specific role.\n"
                    "`??fakepermissions remove [@role] [permissions]` – Revokes specific fake permissions from a role.\n"
                    "`??fakepermissions reset [@role]` – Resets all fake permissions assigned to a role."
                ),
                inline=False
            )

        # --- 5. SERVER TOOLS ---
        elif selection == "servertools":
            embed = discord.Embed(
                title="🛠️ Server Tools",
                description="Handy tools for managing server assets and channels.",
                color=0xFFB6C1
            )
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??steal [emoji]` – Copies a custom emoji from another server.\n"
                    "`??clone` – Clones the current channel's settings and permissions."
                ),
                inline=False
            )

        # --- 6. CHANNEL MANAGEMENT ---
        elif selection == "channels":
            embed = discord.Embed(
                title="🌊 Channel Management",
                description="Tools for keeping chat clean and controlled.",
                color=0xFFB6C1
            )
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??purge [amount]` – Mass deletes messages from the channel.\n"
                    "`??purgebots` – Deletes the latest messages sent by bots.\n"
                    "`??lock / ??unlock` – Locks or unlocks the current text channel."
                ),
                inline=False
            )

        # --- 7. TICKET SYSTEM ---
        elif selection == "tickets":
            embed = discord.Embed(
                title="🎫 Ticket System",
                description="Support tickets and transcript logging.",
                color=0xFFB6C1
            )
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??ticket` – Opens a new support ticket channel.\n"
                    "`??close` – Closes the current active ticket and saves a transcript.\n"
                    "`??add [@user]` – Adds a user to the ticket channel.\n"
                    "`??remove [@user]` – Removes a user from the ticket channel."
                ),
                inline=False
            )

        # --- 8. COMMUNITY & GAMES ---
        elif selection == "games":
            embed = discord.Embed(
                title="✨ Galaxy Community & Games",
                description="Let's giggle, count shooting stars, and play together! ☁️✨",
                color=0xFFB6C1
            )
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??setcounting` / `??resetcount` – Start or reset the chill star-counting game.\n"
                    "`??top [daily/weekly/all]` / `??messages [@user]` – View message leaderboards or check message count.\n"
                    "`??tod` / `??truth` / `??dare` – Play Truth or Dare with cute glowing buttons or space questions."
                ),
                inline=False
            )

        # --- 9. BUMP & REMINDERS ---
        elif selection == "bump":
            embed = discord.Embed(
                title="🚀 Bump & Reminders",
                description="Customizable Disboard bump system with reminders and thank-you messages.",
                color=0xFFB6C1
            )
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??bump` – Logs a Disboard bump and starts the 2-hour reminder timer.\n"
                    "`??bumptime` – Checks how much cooldown time is left until the next bump.\n"
                    "`??setbumpchannel [#channel]` – Sets the channel for bump reminders and thank-you messages.\n"
                    "`??setbumprole [@role]` – Sets the role to be pinged during bump reminders.\n"
                    "`??setbumpmsg [message]` – Customizes the reminder message sent after 2 hours.\n"
                    "`??setthanksmsg [message]` – Customizes the thank-you message sent when someone bumps."
                ),
                inline=False
            )

        # --- 10. UTILITY & TOOLS ---
        elif selection == "utility":
            embed = discord.Embed(
                title="🌙 Utility & Tools",
                description="Handy tools and helpers for everyone in the cosmos~",
                color=0xFFB6C1
            )
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??afk [reason]` – Sets your AFK status with automatic nickname tagging.\n"
                    "`??vctop` – View voice channel time leaderboards.\n"
                    "`??reply [message_id]` – Reply directly to a specific message ID."
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
                "to explore all available commands."
            ),
            color=0xFFB6C1
        )
        embed.set_footer(text="Moonlings Bot • Cozy Space & Sea Aesthetic 🌸")
        await ctx.send(embed=embed, view=HelpMenuView())


async def setup(bot):
    await bot.add_cog(HelpMenuCog(bot))
