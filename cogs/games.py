import discord
from discord.ext import commands

class HelpDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Moderation", description="Keep the server safe and cozy! 🛡️", emoji="🛡️", value="moderation"
            ),
            discord.SelectOption(
                label="Channel Management", description="Lock, unlock and purge channels 🔒", emoji="🔒", value="channels"
            ),
            discord.SelectOption(
                label="Tickets", description="Support and help ticket system 🎫", emoji="🎫", value="tickets"
            ),
            discord.SelectOption(
                label="Community & Games", description="Counting, stats, games and fun! 🌸", emoji="✨", value="community"
            ),
            discord.SelectOption(
                label="Utility & Bump", description="AFK, Star Bumps and tools ☁️", emoji="🛠️", value="utility"
            )
        ]
        super().__init__(placeholder="Select a category to explore~ 🫧", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        selected = self.values[0]

        if selected == "moderation":
            embed = discord.Embed(
                title="🛡️ ∙ Moderation Commands",
                description="Keep Moonlings safe and cozy with these administrative tools~",
                color=discord.Color.from_rgb(255, 182, 193)
            )
            embed.add_field(name="`??kick [@user] [reason]`", value="Kicks a member from the server.", inline=False)
            embed.add_field(name="`??ban [@user] [reason]`", value="Bans a user from the galaxy.", inline=False)
            embed.add_field(name="`??mute [@user] [minutes] [reason]`", value="Timeouts a member to chill out.", inline=False)
            embed.add_field(name="`??warn [@user] [reason]`", value="Issues a gentle warning to a user.", inline=False)
            embed.add_field(name="`??unwarn [@user]`", value="Removes the latest warning from a user.", inline=False)
            embed.add_field(name="`??warnings [@user]`", value="Checks a user's warning history.", inline=False)

        elif selected == "channels":
            embed = discord.Embed(
                title="🔒 ∙ Channel Management Commands",
                description="Keep channels neat, tidy, and cozy~",
                color=discord.Color.from_rgb(255, 218, 185)
            )
            embed.add_field(name="`??purge [amount]`", value="Cleans up recent messages in the channel.", inline=False)
            embed.add_field(name="`??lock`", value="Locks the current channel for a cozy break.", inline=False)
            embed.add_field(name="`??unlock`", value="Unlocks the channel for chatting.", inline=False)

        elif selected == "tickets":
            embed = discord.Embed(
                title="🎫 ∙ Ticket System Commands",
                description="Manage support channels and inquiries easily~",
                color=discord.Color.from_rgb(175, 238, 238)
            )
            embed.add_field(name="`??setup`", value="Deploys the interactive ticket panel.", inline=False)
            embed.add_field(name="`??close`", value="Closes an active ticket and logs the transcript.", inline=False)

        elif selected == "community":
            embed = discord.Embed(
                title="✨ ∙ Community & Fun Commands",
                description="Games, stats, counting, and socializing stars!",
                color=discord.Color.from_rgb(230, 230, 250)
            )
            embed.add_field(name="`??setcounting`", value="Sets up the chill counting game channel.", inline=False)
            embed.add_field(name="`??resetcount`", value="Resets the counting score back to 0.", inline=False)
            embed.add_field(name="`??top [daily/weekly/all]`", value="Shows active message leaderboards.", inline=False)
            embed.add_field(name="`??messages [@user]`", value="Checks total message counts.", inline=False)
            embed.add_field(name="`??vctop`", value="Shows top voice channel activity stars.", inline=False)
            embed.add_field(name="`??resetstats`", value="Resets message or VC statistics.", inline=False)
            embed.add_field(name="`??truth`", value="Asks a cozy truth question.", inline=False)
            embed.add_field(name="`??dare`", value="Gives a cute and fun dare challenge.", inline=False)
            embed.add_field(name="`??tod`", value="Randomly picks either truth or dare for you!", inline=False)

        elif selected == "utility":
            embed = discord.Embed(
                title="🛠️ ∙ Utility & Tools",
                description="Handy tools and helpers for everyone in the cosmos~",
                color=discord.Color.from_rgb(176, 224, 230)
            )
            embed.add_field(name="`??afk [reason]`", value="Sets your status to AFK with [AFK] tag and ping memory.", inline=False)
            embed.add_field(name="`??bump`", value="Logs a Disboard bump and starts the 2-hour Star Bump timer! 🌌", inline=False)
            embed.add_field(name="`??bumptime`", value="Checks how much time is left until the next bump.", inline=False)
            embed.add_field(name="`??setbumpchannel`", value="Configures the channel for Star Bump reminders.", inline=False)

        embed.set_footer(text="Moonlings Help Menu 🌙", icon_url=interaction.client.user.display_avatar.url)
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
        await ctx.message.delete()
        
        embed = discord.Embed(
            title="🌸 ∙ Welcome to Moonlings Help Menu",
            description="Hello traveler! ✨ Use the dropdown menu below to explore categories and discover all the cozy features of our server~ ☁️",
            color=discord.Color.from_rgb(255, 192, 203)
        )
        embed.set_footer(text="Moonlings Bot 🌙", icon_url=self.bot.user.display_avatar.url)
        
        view = HelpView()
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(HelpMenu(bot))
