import discord
from discord.ext import commands

class HelpSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Channel Management", description="Lock, unlock, purge, and slowmode commands", emoji="🌊"),
            discord.SelectOption(label="Security & Anti-Nuke", description="Anti-nuke, anti-raid, and whitelist settings", emoji="🚨"),
            discord.SelectOption(label="Tickets", description="Support ticket panel and management commands", emoji="🎫"),
            discord.SelectOption(label="Staff Applications", description="Staff apply panel and application controls", emoji="🌸"),
            discord.SelectOption(label="Moderation & Advanced Mod", description="Warn, kick, ban, isolate, force-name", emoji="🔨"),
            discord.SelectOption(label="Audit Logs & Bump System", description="Log channels and bump reminders", emoji="📜"),
            discord.SelectOption(label="Stats & AFK", description="Activity tracking and AFK status", emoji="📊"),
            discord.SelectOption(label="Games & Server Tools", description="Truth or Dare, emoji steal, and clone", emoji="🎮"),
            discord.SelectOption(label="Counting & Fake Perms", description="Counting game and custom role permissions", emoji="🔢"),
        ]
        super().__init__(placeholder="Select a category to view commands...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        selected = self.values[0]
        embed = discord.Embed(color=discord.Color.from_rgb(230, 210, 240))
        embed.set_footer(text="Moonlings Help Desk 🌸")

        if selected == "Channel Management":
            embed.title = "🌊 Channel Management Tools"
            embed.description = "Manage channel permissions, cleanup, and slowmode."
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??lock [reason]` - Locks the current channel.\n"
                    "`??unlock` - Unlocks the current channel.\n"
                    "`??purge [amount]` - Delete a specified number of messages.\n"
                    "`??slowmode [time]` - Set a custom slowmode delay."
                ),
                inline=False
            )

        elif selected == "Security & Anti-Nuke":
            embed.title = "🚨 Security & Anti-Nuke Suite"
            embed.description = "Protect your server with anti-nuke, anti-raid, and whitelist controls."
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??antinuke [on/off]` - Toggle Anti-Nuke protection.\n"
                    "`??antiraid [on/off]` - Toggle Anti-Raid protection.\n"
                    "`??whitelist add [@user]` - Add a user to anti-nuke whitelist.\n"
                    "`??whitelist remove [@user]` - Remove a user from whitelist.\n"
                    "`??whitelisted` - Show whitelisted staff members."
                ),
                inline=False
            )

        elif selected == "Tickets":
            embed.title = "🎫 Support Tickets"
            embed.description = "Open and manage support tickets."
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??ticketpanel` - Sends the ticket creation panel (Admin).\n"
                    "`??close` - Closes the active ticket channel.\n"
                    "`??add [@user]` - Adds a user to the ticket.\n"
                    "`??remove [@user]` - Removes a user from the ticket.\n"
                    "`??block [@user]` - Blocks a user from the ticket."
                ),
                inline=False
            )

        elif selected == "Staff Applications":
            embed.title = "🌸 Staff Applications"
            embed.description = "Apply for staff and manage applications."
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??staffapplypanel` - Sends the staff application panel (Admin).\n"
                    "`??applyclose` - Closes the application and generates a transcript."
                ),
                inline=False
            )

        elif selected == "Moderation & Advanced Mod":
            embed.title = "🔨 Moderation & Advanced Controls"
            embed.description = "Standard moderation and user isolation tools."
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??warn [@user] [reason]` - Issues a warning to a member.\n"
                    "`??kick [@user] [reason]` - Kicks a member from the server.\n"
                    "`??ban [@user] [reason]` - Bans a member from the server.\n"
                    "`??isolate [@user]` - Isolates a user from text channels.\n"
                    "`??endbeef [@user]` - Ends the isolation for a user.\n"
                    "`??forcename [@user] [name]` - Enforces a specific nickname on a user."
                ),
                inline=False
            )

        elif selected == "Audit Logs & Bump System":
            embed.title = "📜 Audit Logs & Bump Reminders"
            embed.description = "Configure event logging and bump tracking."
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??setlogs [#channel]` - Sets the audit logging channel.\n"
                    "`??togglelogs` - Toggles server event logging on/off.\n"
                    "`??setbumpchannel [#channel]` - Sets the bump tracking channel.\n"
                    "`??setbumprole [@role]` - Sets the role to ping for bumps.\n"
                    "`??bumptime` - Checks time remaining until next bump."
                ),
                inline=False
            )

        elif selected == "Stats & AFK":
            embed.title = "📊 Stats & AFK System"
            embed.description = "Track server activity and set AFK status."
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??afk [reason]` - Sets your status as AFK.\n"
                    "`??topmessages` - Shows leaderboard for most active text users.\n"
                    "`??checkmessages [@user]` - Shows message stats for a user.\n"
                    "`??vctop` - Shows leaderboard for voice channel activity.\n"
                    "`??resetstats` - Resets stats tracking data (Admin)."
                ),
                inline=False
            )

        elif selected == "Games & Server Tools":
            embed.title = "🎮 Games & Server Tools"
            embed.description = "Fun games and emoji management."
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??truth` - Gets a random Truth question.\n"
                    "`??dare` - Gets a random Dare challenge.\n"
                    "`??tod` - Asks to choose Truth or Dare.\n"
                    "`??steal [emoji/url]` - Steals an emoji to the server.\n"
                    "`??clone [#channel]` - Clones an existing channel."
                ),
                inline=False
            )

        elif selected == "Counting & Fake Perms":
            embed.title = "🔢 Counting Game & Fake Permissions"
            embed.description = "Counting channel setup and custom command permissions."
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??setcounting [#channel]` - Sets up the counting game channel.\n"
                    "`??grantperm [@role] [perm]` - Grants custom permission to a role.\n"
                    "`??removeperm [@role] [perm]` - Removes custom permission from a role.\n"
                    "`??listperms` - Lists custom role permission settings.\n"
                    "`??resetperms` - Resets all fake permission settings."
                ),
                inline=False
            )

        await interaction.response.edit_message(embed=embed)

class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(HelpSelect())

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx):
        """Displays the interactive Moonlings help menu."""
        await ctx.message.delete()
        embed = discord.Embed(
            title="🌸 Moonlings Bot Help Menu",
            description="Welcome to Moonlings! Please select a category from the dropdown menu below to view available commands.",
            color=discord.Color.from_rgb(230, 210, 240)
        )
        embed.set_footer(text="Moonlings Help Desk 🌸")
        await ctx.send(embed=embed, view=HelpView())

async def setup(bot):
    await bot.add_cog(Help(bot))
