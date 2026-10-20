import discord
from discord.ext import commands
from discord.ui import Select, View

class HelpSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Moderation & Security",
                description="Keep our cosmic ocean safe and cozy~ 🛡️",
                emoji="🛸",
                value="moderation"
            ),
            discord.SelectOption(
                label="Tickets & Support",
                description="Need help? Drop into a cozy starlight bubble 💌",
                emoji="🫧",
                value="tickets"
            ),
            discord.SelectOption(
                label="Community & Games",
                description="Counting, partnerships, & star-fishing! 🎮",
                emoji="⭐",
                value="community"
            ),
            discord.SelectOption(
                label="Utility & Tools",
                description="AFK bubbles, galaxy stats & moon tools ☁️",
                emoji="🌙",
                value="utility"
            ),
        ]
        super().__init__(placeholder="dive into the galaxy, cutie~ 🪐", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "moderation":
            embed = discord.Embed(
                title="🛸 ∙ Cosmic Moderation & Security",
                description="Gentle star-tools to keep our ocean peaceful and bright~ 🌊✨",
                color=discord.Color.from_rgb(135, 206, 250) # Light Sky Blue
            )
            embed.add_field(name="Commands", value=(
                "`??kick @user [reason]` - Guide a troublemaker back to shore\n"
                "`??ban @user [reason]` - Send a mischievous soul to deep space\n"
                "`??mute @user [minutes]` - Give a quiet underwater timeout\n"
                "`??lock / ??unlock` - Lock or unlock starry channels\n"
                "`??purge [amount]` - Sweep away stardust and messy messages\n"
                "`??antinuke / ??antiraid` - Shield our galaxy from meteors"
            ), inline=False)
            embed.set_footer(text="Moonlings Space Protection 🌌", icon_url=interaction.client.user.display_avatar.url)
            await interaction.response.edit_message(embed=embed)

        elif self.values[0] == "tickets":
            embed = discord.Embed(
                title="🫧 ∙ Starlight Tickets & Support",
                description="Floating in a sea of questions? Open a ticket in our cozy bubbles! 💌",
                color=discord.Color.from_rgb(175, 238, 238) # Pale Turquoise
            )
            embed.add_field(name="Commands", value=(
                "`??setup` - Spawn the interactive ocean support menu\n"
                "`??close` - Pop the ticket bubble and save a star-transcript"
            ), inline=False)
            embed.set_footer(text="Moonlings Deep Sea Support 🌊", icon_url=interaction.client.user.display_avatar.url)
            await interaction.response.edit_message(embed=embed)

        elif self.values[0] == "community":
            embed = discord.Embed(
                title="⭐ ∙ Galaxy Community & Games",
                description="Let's swim together through constellations and fun! 🐳✨",
                color=discord.Color.from_rgb(221, 160, 221) # Plum / Soft Purple
            )
            embed.add_field(name="Commands", value=(
                "`??partner @user [details]` - Share a glowing constellation partnership\n"
                "`??setcounting` - Swim along with our endless star-counting game\n"
                "`??tod` - Play cosmic Truth or Dare with glowing buttons\n"
                "`??truth` / `??dare` - Spin a random star question"
            ), inline=False)
            embed.set_footer(text="Moonlings Starry Sea 🌟", icon_url=interaction.client.user.display_avatar.url)
            await interaction.response.edit_message(embed=embed)

        elif self.values[0] == "utility":
            embed = discord.Embed(
                title="🌙 ∙ Moonlit Utility & Tools",
                description="Little shooting stars and deep sea gadgets for your journey~ 🪐",
                color=discord.Color.from_rgb(255, 182, 193) # Light Pink
            )
            embed.add_field(name="Commands", value=(
                "`??afk [reason]` - Float away to sleep with an [AFK] moon tag\n"
                "`??top daily/weekly/all` - Check our glowing activity comets\n"
                "`??vctop` - See who spends the most time in coral voice chats\n"
                "`??tz set [zone]` / `??tz @user` - Check star-times across the world\n"
                "`??steal [emoji]` - Catch a stray emoji from another nebula\n"
                "`??clone` - Duplicate a cozy channel layout"
            ), inline=False)
            embed.set_footer(text="Moonlings Cosmic Tools 🚀", icon_url=interaction.client.user.display_avatar.url)
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
            title="🪐 ∙ Moonlings Cosmic Help Menu",
            description="Welcome to our dreamy space ocean! 🌊🌙 Please pick a constellation from the dropdown menu below to explore~ ✨",
            color=discord.Color.from_rgb(176, 224, 230)
        )
        embed.set_footer(text="Floating through space & sea with Moonlings 🐳", icon_url=ctx.bot.user.display_avatar.url)
        
        await ctx.send(embed=embed, view=HelpView())

async def setup(bot):
    await bot.add_cog(HelpMenu(bot))

