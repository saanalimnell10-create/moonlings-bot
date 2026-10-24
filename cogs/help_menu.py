import discord
from discord.ext import commands

class HelpSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Welcome & Goodbye", description="Configure custom welcome and goodbye messages", emoji="👋"),
            discord.SelectOption(label="Moderation", description="Standard moderation commands (warn, kick, ban)", emoji="🔨"),
            discord.SelectOption(label="Safety", description="Advanced moderation (isolate, endbeef, forcename)", emoji="🛡️"),
            discord.SelectOption(label="Threat Security", description="Dynamic pressure tracking, toggles, and modes", emoji="🚨"),
            discord.SelectOption(label="Security & Anti-Nuke", description="Anti-nuke, anti-raid, and whitelist settings", emoji="🔒"),
            discord.SelectOption(label="Channel Management", description="Lock, unlock, purge, and slowmode commands", emoji="🌊"),
            discord.SelectOption(label="Tickets", description="Support ticket panel and management commands", emoji="🎫"),
            discord.SelectOption(label="Staff Applications", description="Staff apply panel and application controls", emoji="🌸"),
            discord.SelectOption(label="Bump System", description="Configure bump tracking and reminders", emoji="💥"),
            discord.SelectOption(label="Server Tools", description="Emoji steal and channel cloning tools", emoji="🧰"),
            discord.SelectOption(label="Games", description="Counting game, Truth or Dare, and TOD commands", emoji="🎮"),
            discord.SelectOption(label="Audit Logs", description="Configure server event logging", emoji="📜"),
            discord.SelectOption(label="Stats & AFK", description="Activity tracking and AFK status", emoji="📊"),
            discord.SelectOption(label="Fake Permissions", description="Custom role-based permissions setup", emoji="🔑"),
        ]
        super().__init__(placeholder="Select a category to view commands...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        selected = self.values[0]
        embed = discord.Embed(color=discord.Color.from_rgb(230, 210, 240))
        embed.set_footer(text="Moonlings Help Desk 🌸")

        if selected == "Welcome & Goodbye":
            embed.title = "👋 Welcome & Goodbye System"
            embed.description = "Configure custom welcome and goodbye messages, channels, and placeholders."
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??setwelcomechannel [#channel]` - Sets the welcome message channel.\n"
                    "`??setwelcometext <text>` - Sets custom welcome text (Use `{user}` & `{server}`).\n"
                    "`??setgoodbyechannel [#channel]` - Sets the goodbye message channel.\n"
                    "`??setgoodbyetext <text>` - Sets custom goodbye text (Use `{user}` & `{server}`)."
                ),
                inline=False
            )

        elif selected == "Threat Security":
            embed.title = "🚨 Dynamic Threat Security System"
            embed.description = "Automated pressure tracking and dynamic threat mode controls."
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??threatlevel` - Views current threat score, active gear, and security status.\n"
                    "`??setthreatmode [mode]` - Overrides security mode (auto/normal/elevated/lockdown).\n"
                    "`??togglethreat [on/off]` - Toggles the dynamic threat monitoring system on or off."
                ),
                inline=False
            )

        elif selected == "Security & Anti-Nuke":
            embed.title = "🔒 Security & Anti-Nuke"
            embed.description = "General protection, anti-nuke, anti-raid, and whitelist controls."
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

        elif selected == "Moderation":
            embed.title = "🔨 Moderation Tools"
            embed.description = "Essential server moderation commands."
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??warn [@user] [reason]` - Issues a warning to a member.\n"
                    "`??kick [@user] [reason]` - Kicks a member from the server.\n"
                    "`??ban [@user] [reason]` - Bans a member from the server."
                ),
                inline=False
            )

        elif selected == "Safety":
            embed.title = "🛡️ Safety & Advanced Moderation"
            embed.description = "Advanced user isolation and restriction tools."
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??isolate [@user]` - Isolates a user from text channels.\n"
                    "`??endbeef [@user]` - Ends the isolation for a user.\n"
                    "`??forcename [@user] [name]` - Enforces a specific nickname on a user."
                ),
                inline=False
            )

        elif selected == "Channel Management":
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

        elif selected == "Bump System":
            embed.title = "💥 Bump System"
            embed.description = "Track bumps and set reminder notifications."
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??setbumpchannel [#channel]` - Sets the bump tracking channel.\n"
                    "`??setbumprole [@role]` - Sets the role to ping for bumps.\n"
                    "`??bumptime` - Checks time remaining until next bump."
                ),
                inline=False
            )

        elif selected == "Server Tools":
            embed.title = "🧰 Server Tools"
            embed.description = "Utility tools for emojis and channels."
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??steal [emoji/url]` - Steals an emoji to the server.\n"
                    "`??clone [#channel]` - Clones an existing channel."
                ),
                inline=False
            )

        elif selected == "Games":
            embed.title = "🎮 Games"
            embed.description = "Fun games including Counting and Truth or Dare."
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??setcounting [#channel]` - Sets up the counting channel.\n"
                    "`??truth` - Gets a random Truth question.\n"
                    "`??dare` - Gets a random Dare challenge.\n"
                    "`??tod` - Asks to choose Truth or Dare."
                ),
                inline=False
            )

        elif selected == "Audit Logs":
            embed.title = "📜 Audit Logs"
            embed.description = "Server logging configuration."
            embed.add_field(
                name="📜 Commands",
                value=(
                    "`??setlogs [#channel]` - Sets the audit logging channel.\n"
                    "`??togglelogs` - Toggles server event logging on/off."
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

        elif selected == "Fake Permissions":
            embed.title = "🔑 Fake Permissions"
            embed.description = "Configure custom role permissions."
            embed.add_field(
                name="📜 Commands",
                value=(
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
        super().__init__(timeout=300)  # Asetettu tasan 5 minuuttiin (300 sekuntia)
        self.add_item(HelpSelect())

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx):
        """Displays the interactive Moonlings help menu."""
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        except discord.HTTPException:
            pass
            
        embed = discord.Embed(
            title="🌸 Moonlings Bot Help Menu",
            description="Welcome to Moonlings! Please select a category from the dropdown menu below to view available commands.",
            color=discord.Color.from_rgb(230, 210, 240)
        )
        embed.set_footer(text="Moonlings Help Desk 🌸")
        await ctx.send(embed=embed, view=HelpView())

async def setup(bot):
    await bot.add_cog(Help(bot))
