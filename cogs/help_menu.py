import discord
import discord
from discord.ext import commands

class HelpSelect(discord.ui.Select):
    def __init__(self, bot):
        self.bot = bot
        options = [
            discord.SelectOption(label="Moderation & Transparency", description="Warns, bans, kicks, mutes, DM logs, and warn expiry.", emoji="🛡️"),
            discord.SelectOption(label="Advanced Moderation & Conflict", description="Isolate, endbeef, and forcename tools.", emoji="⚔️"),
            discord.SelectOption(label="Custom Fake Permissions", description="Manage safe role permissions without native admin rights.", emoji="🔒"),
            discord.SelectOption(label="Anti-Nuke & Anti-Raid", description="Mass deletion limits, whitelist, and server lockdown.", emoji="🚨"),
            discord.SelectOption(label="Audit Log & Event Logging", description="Real time event logging, channel tracking, and toggles.", emoji="📜"),
            discord.SelectOption(label="Conflict & Safety Suite", description="Isolate arguments, forced names, and member safety.", emoji="🌿"),
            discord.SelectOption(label="Server Tools", description="Steal emojis and clone channel settings.", emoji="🛠️"),
            discord.SelectOption(label="Channel Management", description="Lock, unlock, purge messages, and slowmode.", emoji="🌊"),
            discord.SelectOption(label="Ticket System", description="Support tickets, staff applications, and transcript logging.", emoji="🎫"),
            discord.SelectOption(label="Community & Games", description="Truth or Dare, chill-counting, and message stats.", emoji="✨"),
            discord.SelectOption(label="Bump & Reminders", description="Star bumps, roles, and custom message settings.", emoji="🚀"),
            discord.SelectOption(label="Utility & Tools", description="AFK system, bot/server info, and reply commands.", emoji="🌙"),
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
                    "`??ticketpanel` - Sends the support ticket panel with a drop-down menu (Admin).\n"
                    "`??applypanel` - Sends the Staff Application panel (Admin).\n"
                    "`??close` - Closes the active ticket/application and generates a transcript.\n"
                    "`??add [user]` - Adds a user to the active ticket channel.\n"
                    "`??remove [user]` - Removes a user from the active ticket channel.\n"
                    "`??block [user]` - Blocks a specific user from viewing the ticket channel."
                ),
                inline=False
            )

        elif selected == "Moderation & Transparency":
            embed.title = "🛡️ Moderation & Transparency"
            embed.description = "Warns, bans, kicks, timeouts, warning expiration settings, and transparent DM logs."
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??ban [user] [reason]` - Permanently ban a member from the server.\n"
                    "`??unban [user_id]` - Unban a member using their user ID.\n"
                    "`??kick [user] [reason]` - Kick a member from the server.\n"
                    "`??mute [user] [time] [reason]` - Timeout/Mute a member for a set duration.\n"
                    "`??unmute [user]` - Remove a mute/timeout from a member.\n"
                    "`??warn [@user] [reason]` - Gives a warning to a member.\n"
                    "`??warnings [@user]` - Checks how many active warnings a member has.\n"
                    "`??warnexpiry [days / off]` - Sets how long warnings stay active before they automatically expire (e.g., `??warnexpiry 30`), or turns it off (`??warnexpiry off`) to keep them forever."
                ),
                inline=False
            )
            embed.add_field(
                name="📋 Transparent Moderation DM System",
                value=(
                    "Automatically sends a neat pastel embed to a punished member's DMs containing:\n"
                    "• **Who did it:** The moderator's name for full accountability.\n"
                    "• **Attached evidence:** Links or files provided by the moderator.\n"
                    "• **The message it was about:** Captures and displays the exact rule-breaking message.\n"
                    "• **Case reference:** A unique tracking reference for appeals or inquiries."
                ),
                inline=False
            )

        elif selected == "Advanced Moderation & Conflict":
            embed.title = "⚔️ Advanced Moderation & Conflict Tools"
            embed.description = "Isolating arguing members and forcing safe nicknames."
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??isolate [@user1] [@user2] [reason]` - Isolates arguing members into a temporary private channel to settle their disagreement privately.\n"
                    "`??endbeef [@user1] [@user2]` - Ends the isolation and deletes the temporary private channel.\n"
                    "`??forcename [@user] [nickname]` - Forces a nickname on a member and automatically re-applies it if they try to change it!\n"
                    "`??forcename [@user] remove` - Removes the forced nickname lock."
                ),
                inline=False
            )

        elif selected == "Custom Fake Permissions":
            embed.title = "🔒 Custom Fake Permissions System"
            embed.description = "Manage safe role permissions without native admin rights."
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??fakepermissions grant [@role] [permissions]` - Grants specific bot command permissions to a role without giving them native, potentially dangerous Discord administrator permissions.\n"
                    "`??fakepermissions list [@role]` - Views all fake permissions granted to a specific role.\n"
                    "`??fakepermissions remove [@role] [permissions]` - Revokes specific fake permissions from a role.\n"
                    "`??fakepermissions reset [@role]` - Resets all fake permissions."
                ),
                inline=False
            )

        elif selected == "Audit Log & Event Logging":
            embed.title = "📜 Audit Log & Event Logging"
            embed.description = "Real time event logging, channel tracking, and toggles."
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??setlogs [#channel]` - Sets the designated channel where the bot sends real-time audit log events.\n"
                    "`??logevents` - Allows staff to toggle which events are logged (e.g., message deletes, message edits, member joins/leaves, role changes, channel modifications, and ban/kick actions).\n"
                    "`??logs [on/off]` - Quickly enables or disables the logging system."
                ),
                inline=False
            )

        elif selected == "Server Tools":
            embed.title = "🛠️ Server Tools"
            embed.description = "Steal emojis and clone channel settings."
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??steal [emoji]` - Copies an emoji from another server to this server.\n"
                    "`??clone` - Clones the current channel's permissions and settings into a fresh channel."
                ),
                inline=False
            )

        elif selected == "Channel Management":
            embed.title = "🌊 Channel Management & Single Channel Lock Tools"
            embed.description = "Purge messages, lock/unlock, and hide channels."
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??lock [reason]` - Locks and hides the current channel so regular members cannot view or send messages.\n"
                    "`??unlock` - Unlocks and unhides the current channel, restoring normal visibility and chatting.\n"
                    "`??purge [amount]` - Delete a specified number of messages from the channel.\n"
                    "`??slowmode [time]` - Set a custom slowmode delay for the channel."
                ),
                inline=False
            )

        elif selected == "Community & Games":
            embed.title = "✨ Community & Games"
            embed.description = "Truth or Dare, chill-counting game, and message/voice activity statistics."
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??setcounting` - Sets the current channel as the counting channel. (Mistakes don't reset the count—the bot corrects the number and the game continues!)\n"
                    "`??tod` - Opens interactive buttons to choose between Truth or Dare.\n"
                    "`??truth` - Randomly picks a truth question.\n"
                    "`??dare` - Randomly picks a dare challenge.\n"
                    "`??top daily` - Shows the most active chatters of the day.\n"
                    "`??top weekly` - Shows the most active chatters of the week.\n"
                    "`??top all` - Shows all-time message statistics.\n"
                    "`??vctop` - Shows who has spent the most time in voice channels."
                ),
                inline=False
            )

        elif selected == "Bump & Reminders":
            embed.title = "🚀 Bump & Reminders"
            embed.description = "Star bumps, reminder roles, and custom message settings."
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??bumprole [@role]` - Sets the ping role for DISBOARD/server bump reminders.\n"
                    "`??bumpchannel [#channel]` - Sets the designated channel for bump notifications.\n"
                    "`??bumpmsg [text]` - Customizes the reminder message sent when it's time to bump.\n"
                    "`??bumptest` - Sends a test bump reminder message to check your configuration."
                ),
                inline=False
            )

        elif selected == "Utility & Tools":
            embed.title = "🌙 Utility & Tools"
            embed.description = "AFK system, general bot information, user profiles, server details, and reply tools."
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??afk [reason]` - Sets you as AFK, automatically adds [AFK] to your nickname, and when you return, it removes the tag and shows a list of everyone who pinged you while you were away.\n"
                    "`??reply [message_id] [message]` - Makes the bot reply directly to a specific message ID using Discord's native reply feature, optionally styled with a cozy embed.\n"
                    "`??help` - Opens this interactive help menu.\n"
                    "`??userinfo [user]` - Displays user information (join dates, roles, ID).\n"
                    "`??serverinfo` - Displays server details (owner, member count, channels).\n"
                    "`??botinfo` - Shows Moonlings bot statistics, latency, and versions.\n"
                    "`??ping` - Checks the bot's current response latency."
                ),
                inline=False
            )

        elif selected == "Anti-Nuke & Anti-Raid":
            embed.title = "🚨 Anti-Nuke & Anti-Raid"
            embed.description = "Mass deletion limits, whitelist, and server protection."
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??anti-nuke [on/off]` - Toggle anti-nuke protection system.\n"
                    "*(Additional security parameters can be configured directly from the Dashboard)*"
                ),
                inline=False
            )

        else:
            embed.title = f"✨ {selected}"
            embed.description = "The settings and modules for this category are managed conveniently through the Dashboard or are currently under active development!"

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
