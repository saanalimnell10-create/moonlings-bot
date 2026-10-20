import discord
from discord.ext import commands
from discord.ui import Select, View

class HelpSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Moderation & Security",
                description="View ban, kick, mute, lock, and anti-nuke commands.",
                emoji="🛡️",
                value="moderation"
            ),
            discord.SelectOption(
                label="Tickets & Setup",
                description="View ticket creation, setup, and close commands.",
                emoji="🎫",
                value="tickets"
            ),
            discord.SelectOption(
                label="Community & Games",
                description="View counting, partnership, and Truth or Dare commands.",
                emoji="🎮",
                value="community"
            ),
            discord.SelectOption(
                label="Utility & Tools",
                description="View stats, AFK, timezone, and clone tools.",
                emoji="🛠️",
                value="utility"
            ),
        ]
        super().__init__(placeholder="Select a help category...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "moderation":
            embed = discord.Embed(
                title="🛡️ Moderation & Security Commands",
                description="Here are your moderation and security tools:",
                color=discord.Color.red()
            )
            embed.add_field(name="Commands", value=(
                "`??kick @user [reason]` - Kick a member\n"
                "`??ban @user [reason]` - Ban a member\n"
                "`??mute @user [minutes]` - Timeout a member\n"
                "`??lock / ??unlock` - Lock or unlock channels\n"
                "`??purge [amount]` - Mass delete messages\n"
                "`??antinuke / ??antiraid` - Security toggles"
            ), inline=False)
            await interaction.response.edit_message(embed=embed)

        elif self.values[0] == "tickets":
            embed = discord.Embed(
                title="🎫 Ticket System Commands",
                description="Manage your support and application tickets:",
                color=discord.Color.blue()
            )
            embed.add_field(name="Commands", value=(
                "`??setup` - Send the interactive support ticket dropdown menu\n"
                "`??close` - Close an active ticket and generate a transcript"
            ), inline=False)
            await interaction.response.edit_message(embed=embed)

        elif self.values[0] == "community":
            embed = discord.Embed(
                title="🎮 Community & Games",
                description="Fun and interactive community features:",
                color=discord.Color.green()
            )
            embed.add_field(name="Commands", value=(
                "`??partner @user [details]` - Post a partnership announcement\n"
                "`??setcounting` - Set up the chill counting channel\n"
                "`??tod` - Play Truth or Dare with buttons\n"
                "`??truth` / `??dare` - Random truth or dare questions"
            ), inline=False)
            await interaction.response.edit_message(embed=embed)

        elif self.values[0] == "utility":
            embed = discord.Embed(
                title="🛠️ Utility & Server Tools",
                description="General server and personal tools:",
                color=discord.Color.purple()
            )
            embed.add_field(name="Commands", value=(
                "`??afk [reason]` - Set AFK status & auto-nickname tag\n"
                "`??top daily/weekly/all` - View chat leaderboards\n"
                "`??vctop` - View voice channel activity\n"
                "`??tz set [zone]` / `??tz @user` - Timezone tools\n"
                "`??steal [emoji]` - Steal an emoji\n"
                "`??clone` - Clone a channel"
            ), inline=False)
            await interaction.response.edit_message(embed=embed)

class HelpView(View):
    def __init__(self):
        super().__init__(timeout=180)
        self.add_item(HelpSelect())

class HelpMenu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx):
        embed = discord.Embed(
            title="🌙 Moonlings Bot Help Menu",
            description="Welcome to **Moonlings Bot**! Please choose a category from the dropdown menu below to view its commands.",
            color=discord.Color.from_rgb(43, 45, 49)
        )
        embed.set_footer(text="Moonlings Automation & Moderation", icon_url=ctx.bot.user.display_avatar.url)
        
        await ctx.send(embed=embed, view=HelpView())

async def setup(bot):
    await bot.add_cog(HelpMenu(bot))
