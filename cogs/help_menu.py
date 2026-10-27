import discord
from discord.ext import commands

class HelpSelect(discord.ui.Select):
    def __init__(self, prefix):
        self.prefix = prefix
        options = [
            discord.SelectOption(label="Moderation", description="Standard moderation commands (warn, kick, ban)", emoji="🔨"),
            discord.SelectOption(label="Safety", description="Advanced moderation (isolate, endbeef, forcename)", emoji="⚔️"),
            discord.SelectOption(label="Member Protection", description="Watchlist and user protection suite", emoji="🛡️"),
            discord.SelectOption(label="Threat Security", description="Dynamic pressure tracking, toggles, and modes", emoji="🚨"),
            discord.SelectOption(label="Security & Anti-Nuke", description="Anti-nuke, anti-raid, and whitelist settings", emoji="🔒"),
            discord.SelectOption(label="Fake Permissions", description="Custom role-based permissions setup", emoji="🔑"),
            discord.SelectOption(label="Giveaways", description="Advanced giveaways with tickets & auto-rerolls", emoji="🎁"),
            discord.SelectOption(label="Audit Logs", description="Configure server event logging", emoji="📜"),
            discord.SelectOption(label="Server Tools", description="Emoji steal and channel cloning tools", emoji="🧰"),
            discord.SelectOption(label="Staff Applications", description="Staff apply panel and application controls", emoji="🌸"),
            discord.SelectOption(label="Channel Management", description="Lock, unlock, purge, and slowmode commands", emoji="🌊"),
            discord.SelectOption(label="Tickets", description="Support ticket panel and management commands", emoji="🎫"),
            discord.SelectOption(label="Welcome & Goodbye", description="Configure custom welcome and goodbye messages", emoji="👋"),
            discord.SelectOption(label="Cozy Café", description="Brew hot drinks, bake pastries, and serve friends", emoji="🍵"),
            discord.SelectOption(label="Star Family", description="Marriage, adoption, family tree, and love ship", emoji="💍"),
            discord.SelectOption(label="Games & Fun", description="Counting, Truth or Dare, and Rock Paper Scissors", emoji="🎮"),
            discord.SelectOption(label="Bump System", description="Configure bump tracking and reminders", emoji="💥"),
            discord.SelectOption(label="Stats & AFK", description="Activity tracking and AFK status", emoji="📊"),
        ]
        super().__init__(placeholder="Select a category to view commands...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        selected = self.values[0]
        p = self.prefix
        embed = discord.Embed(color=discord.Color.from_rgb(230, 210, 240))
        embed.set_footer(text="Moonlings Help Desk 🌸")

        if selected == "Moderation":
            embed.title = "🔨 Moderation Tools"
            embed.description = "Essential server moderation commands."
            embed.add_field(
                name="📜 Commands",
                value=(
                    f"`{p}warn [@user] [reason]` - Issues a warning to a member.\n"
                    f"`{p}kick [@user] [reason]` - Kicks a member from the server.\n"
                    f"`{p}ban [@user] [reason]` - Bans a member from the server."
                ),
                inline=False
            )

        elif selected == "Safety":
            embed.title = "⚔️ Safety & Advanced Moderation"
            embed.description = "Advanced user isolation and restriction tools."
            embed.add_field(
                name="📜 Commands",
                value=(
                    f"`{p}isolate [@user]` - Isolates a user from text channels.\n"
                    f"`{p}endbeef [@user]` - Ends the isolation for a user.\n"
                    f"`{p}forcename [@user] [name]` - Enforces a specific nickname on a user."
                ),
                inline=False
            )

        elif selected == "Member Protection":
            embed.title = "🛡️ Member Protection & Watchlist System"
            embed.description = "Track, mark, and protect server members from harassers or unwanted users."
            embed.add_field(
                name="📜 Commands",
                value=(
                    f"`{p}setupboycott setup [#channel]` - Set alert channel for flags.\n"
                    f"`{p}setupboycott mark [@user] [reason]` - Mark a user on the watchlist.\n"
                    f"`{p}setupboycott unmark [@user]` - Remove a user from the watchlist.\n"
                    f"`{p}setupboycott list` - List all currently marked users."
                ),
                inline=False
            )

        elif selected == "Threat Security":
            embed.title = "🚨 Dynamic Threat Security System"
            embed.description = "Automated pressure tracking and dynamic threat mode controls."
            embed.add_field(
                name="📜 Commands",
                value=(
                    f"`{p}threatlevel` - Views current threat score, active gear, and security status.\n"
                    f"`{p}setthreatmode [mode]` - Overrides security mode (auto/normal/elevated/lockdown).\n"
                    f"`{p}togglethreat [on/off]` - Toggles the dynamic threat monitoring system on or off."
                ),
                inline=False
            )

        elif selected == "Security & Anti-Nuke":
            embed.title = "🔒 Security & Anti-Nuke"
            embed.description = "General protection, anti-nuke, anti-raid, and whitelist controls."
            embed.add_field(
                name="📜 Commands",
                value=(
                    f"`{p}antinuke [on/off]` - Toggle Anti-Nuke protection.\n"
                    f"`{p}antiraid [on/off]` - Toggle Anti-Raid protection.\n"
                    f"`{p}whitelist add [@user]` - Add a user to anti-nuke whitelist.\n"
                    f"`{p}whitelist remove [@user]` - Remove a user from whitelist.\n"
                    f"`{p}whitelisted` - Show whitelisted staff members."
                ),
                inline=False
            )

        elif selected == "Fake Permissions":
            embed.title = "🔑 Fake Permissions"
            embed.description = "Custom role-based permissions setup."
            embed.add_field(
                name="📜 Commands",
                value=(
                    f"`{p}grantperm [@role] [perm]` - Grants custom permission to a role.\n"
                    f"`{p}removeperm [@role] [perm]` - Removes custom permission from a role.\n"
                    f"`{p}listperms` - Lists custom role permission settings.\n"
                    f"`{p}resetperms` - Resets all fake permission settings."
                ),
                inline=False
            )

        elif selected == "Giveaways":
            embed.title = "🎁 Giveaway Center"
            embed.description = "Advanced giveaways with tickets, auto-rerolls, and voucher closing."
            embed.add_field(
                name="📜 Commands",
                value=(
                    f"`/giveaway create` - Create an advanced giveaway with custom options[cite: 1, 2, 3]\n"
                    f"`/giveaway end` - End an active giveaway early using message ID[cite: 3]\n"
                    f"`/giveaway delete` - Delete a giveaway message[cite: 3]\n"
                    f"`/giveaway fix` - Force-fix or clear a stuck giveaway state[cite: 4]\n"
                    f"`/giveaway participants` - View all users who have participated[cite: 4]\n"
                    f"• *Features:* Claim time, max rerolls, auto-ticket creation, and vouch-to-close!"
                ),
                inline=False
            )

        elif selected == "Audit Logs":
            embed.title = "📜 Audit Logs"
            embed.description = "Server logging configuration."
            embed.add_field(
                name="📜 Commands",
                value=(
                    f"`{p}setlogs [#channel]` - Sets the audit logging channel.\n"
                    f"`{p}togglelogs` - Toggles server event logging on/off."
                ),
                inline=False
            )

        elif selected == "Server Tools":
            embed.title = "🧰 Server Tools"
            embed.description = "Utility tools for emojis and channels."
            embed.add_field(
                name="📜 Commands",
                value=(
                    f"`{p}steal [emoji/url]` - Steals an emoji to the server.\n"
                    f"`{p}clone [#channel]` - Clones an existing channel."
                ),
                inline=False
            )

        elif selected == "Staff Applications":
            embed.title = "🌸 Staff Applications"
            embed.description = "Apply for staff and manage applications."
            embed.add_field(
                name="📜 Commands",
                value=(
                    f"`{p}staffapplypanel` - Sends the staff application panel (Admin).\n"
                    f"`{p}applyclose` - Closes the application and generates a transcript."
                ),
                inline=False
            )

        elif selected == "Channel Management":
            embed.title = "🌊 Channel Management Tools"
            embed.description = "Manage channel permissions, cleanup, and slowmode."
            embed.add_field(
                name="📜 Commands",
                value=(
                    f"`{p}lock [reason]` - Locks the current channel.\n"
                    f"`{p}unlock` - Unlocks the current channel.\n"
                    f"`{p}purge [amount]` - Delete a specified number of messages.\n"
                    f"`{p}slowmode [time]` - Set a custom slowmode delay."
                ),
                inline=False
            )

        elif selected == "Tickets":
            embed.title = "🎫 Support Tickets"
            embed.description = "Open and manage support tickets."
            embed.add_field(
                name="📜 Commands",
                value=(
                    f"`{p}ticketpanel` - Sends the ticket creation panel (Admin).\n"
                    f"`{p}close` - Closes the active ticket channel.\n"
                    f"`{p}add [@user]` - Adds a user to the ticket.\n"
                    f"`{p}remove [@user]` - Removes a user from the ticket.\n"
                    f"`{p}block [@user]` - Blocks a user from the ticket."
                ),
                inline=False
            )

        elif selected == "Welcome & Goodbye":
            embed.title = "👋 Welcome & Goodbye System"
            embed.description = "Configure custom welcome and goodbye messages, channels, and placeholders."
            embed.add_field(
                name="📜 Commands",
                value=(
                    f"`{p}setwelcomechannel [#channel]` - Sets the welcome message channel.\n"
                    f"`{p}setwelcometext <text>` - Sets custom welcome text (Use `{{user}}` & `{{server}}`).\n"
                    f"`{p}setgoodbyechannel [#channel]` - Sets the goodbye message channel.\n"
                    f"`{p}setgoodbyetext <text>` - Sets custom goodbye text (Use `{{user}}` & `{{server}}`)."
                ),
                inline=False
            )

        elif selected == "Cozy Café":
            embed.title = "🍵 Cozy Café & Teahouse Mini-Economy"
            embed.description = "Brew, bake, and serve cozy treats to your friends!"
            embed.add_field(
                name="📜 Commands",
                value=(
                    f"`{p}brew [drink]` - Brews a cozy hot drink (Matcha, Latte, etc.).\n"
                    f"`{p}bake [pastry]` - Bakes a sweet treat (Shortcake, Cookie, etc.).\n"
                    f"`{p}serve [@user] [item]` - Serves an item from your pantry to a friend!\n"
                    f"`{p}pantry [@user]` - Displays personal cafe items and inventory."
                ),
                inline=False
            )

        elif selected == "Star Family":
            embed.title = "💍 Star Family & Poly-Marriage System"
            embed.description = "Propose, adopt, check family trees, and ship members!"
            embed.add_field(
                name="📜 Commands",
                value=(
                    f"`{p}propose [@user]` - Proposes to a member with interactive buttons.\n"
                    f"`{p}adopt [@user]` - Adopts another member as a child.\n"
                    f"`{p}divorce [@user]` - Amicably dissolves a relationship.\n"
                    f"`{p}family [@user]` - Displays family tree (spouses, children, parents).\n"
                    f"`{p}ship [@user1] [@user2]` - Calculates love compatibility!"
                ),
                inline=False
            )

        elif selected == "Games & Fun":
            embed.title = "🎮 Games & Fun Suite"
            embed.description = "Fun interactive games for everyone on the server."
            embed.add_field(
                name="📜 Commands",
                value=(
                    f"`{p}setcounting [#channel]` - Sets up the counting channel.\n"
                    f"`{p}setcountingemoji success <emoji>` - Sets custom success emoji.\n"
                    f"`{p}setcountingemoji fail <emoji>` - Sets custom fail emoji.\n"
                    f"`{p}truth` - Gets a random Truth question.\n"
                    f"`{p}dare` - Gets a random Dare challenge.\n"
                    f"`{p}tod` - Asks to choose Truth or Dare.\n"
                    f"`{p}rps [kivi/paperi/sakset]` - Play Rock Paper Scissors against the bot."
                ),
                inline=False
            )

        elif selected == "Bump System":
            embed.title = "💥 Bump System"
            embed.description = "Track bumps and set reminder notifications."
            embed.add_field(
                name="📜 Commands",
                value=(
                    f"`{p}setbumpchannel [#channel]` - Sets the bump tracking channel.\n"
                    f"`{p}setbumprole [@role]` - Sets the role to ping for bumps.\n"
                    f"`{p}bumptime` - Checks time remaining until next bump."
                ),
                inline=False
            )

        elif selected == "Stats & AFK":
            embed.title = "📊 Stats & AFK System"
            embed.description = "Track server activity and set AFK status."
            embed.add_field(
                name="📜 Commands",
                value=(
                    f"`{p}afk [reason]` - Sets your status as AFK.\n"
                    f"`{p}topmessages` - Shows leaderboard for most active text users.\n"
                    f"`{p}checkmessages [@user]` - Shows message stats for a user.\n"
                    f"`{p}vctop` - Shows leaderboard for voice channel activity.\n"
                    f"`{p}resetstats` - Resets stats tracking data (Admin)."
                ),
                inline=False
            )

        await interaction.response.edit_message(embed=embed)

class HelpView(discord.ui.View):
    def __init__(self, prefix):
        super().__init__(timeout=300)
        self.add_item(HelpSelect(prefix))

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if self.bot.help_command:
            self.bot.help_command = None

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
            description=f"Welcome to Moonlings! Please select a category from the dropdown menu below to view available commands.\nCurrent Prefix: `{ctx.prefix}`",
            color=discord.Color.from_rgb(230, 210, 240)
        )
        embed.set_footer(text="Moonlings Help Desk 🌸")
        await ctx.send(embed=embed, view=HelpView(ctx.prefix))

async def setup(bot):
    bot.remove_command("help")
    await bot.add_cog(Help(bot))
