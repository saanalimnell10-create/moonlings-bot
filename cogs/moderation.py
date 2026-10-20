import discord
from discord.ext import commands
from discord.ui import Select, View

class HelpSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Moderation & Security",
                description="Keep our cozy space station safe and sound~ 🛡️",
                emoji="🚀",
                value="moderation"
            ),
            discord.SelectOption(
                label="Tickets & Support",
                description="Need help? Float into a cozy starlight bubble 💌",
                emoji="🪐",
                value="tickets"
            ),
            discord.SelectOption(
                label="Community & Games",
                description="Counting, cute partnerships & star-fishing! 🎮",
                emoji="⭐",
                value="community"
            ),
            discord.SelectOption(
                label="Utility & Tools",
                description="AFK moon tags, sweet stats & star tools ☁️",
                emoji="🌙",
                value="utility"
            ),
        ]
        super().__init__(placeholder="make a selection under the stars, cutie~ ✨", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "moderation":
            embed = discord.Embed(
                title="🚀 ∙ Cozy Space Moderation",
                description="Soft star-tools to keep our galaxy peaceful and lovely~ 🌌✨",
                color=discord.Color.from_rgb(135, 206, 250)
            )
            embed.add_field(name="Commands", value=(
                "`??kick @user [reason]` - Gently guide a member back to Earth\n"
                "`??ban @user [reason]` - Send a mischievous soul to deep space\n"
                "`??mute @user [minutes]` - Give a quiet zero-gravity timeout\n"
                "`??warn @user [reason]` - Give a soft warning\n"
                "`??unwarn @user` - Remove a member's warning\n"
                "`??warnings [@user]` - Check active warnings\n"
                "`??warnexpiry [days/off]` - Set warning expiration time\n"
                "`??lock / ??unlock` - Lock or unlock sleepy starlight channels\n"
                "`??purge [amount]` - Sweep away cosmic dust\n"
                "`??antinuke / ??antiraid` - Keep our sweet space home safe"
            ), inline=False)
            embed.set_footer(text="Moonlings Starlight Protection 🌠", icon_url=interaction.client.user.display_avatar.url)
            await interaction.response.edit_message(embed=embed)

        elif self.values[0] == "tickets":
            embed = discord.Embed(
                title="🪐 ∙ Starlight Support & Tickets",
                description="Got a question or want to join the crew? Open a sweet ticket! 💌",
                color=discord.Color.from_rgb(230, 230, 250)
            )
            embed.add_field(name="Commands", value=(
                "`??setup` - Spawn the interactive space support menu\n"
                "`??close` - Close the ticket bubble and save a cute transcript"
            ), inline=False)
            embed.set_footer(text="Moonlings Space Café 🌙", icon_url=interaction.client.user.display_avatar.url)
            await interaction.response.edit_message(embed=embed)

        elif self.values[0] == "community":
            embed = discord.Embed(
                title="⭐ ∙ Galaxy Community & Games",
                description="Let's giggle, count shooting stars, and play together! ☁️✨",
                color=discord.Color.from_rgb(221, 160, 221)
            )
            embed.add_field(name="Commands", value=(
                "`??partner @user [details]` - Share a sweet constellation partnership\n"
                "`??setcounting` - Start our endless chill star-counting game\n"
                "`??tod` - Play Truth or Dare with cute glowing buttons\n"
                "`??truth` / `??dare` - Draw a fun random space question"
            ), inline=False)
            embed.set_footer(text="Moonlings Cosmic Garden 🌠", icon_url=interaction.client.user.display_avatar.url)
            await interaction.response.edit_message(embed=embed)

        elif self.values[0] == "utility":
            embed = discord.Embed(
                title="🌙 ∙ Moonlit Utility & Star Tools",
                description="Little ribbons and magical gadgets for your cosmic adventures~ 🧸",
                color=discord.Color.from_rgb(255, 182, 193)
            )
            embed.add_field(name="Commands", value=(
                "`??afk [reason]` - Float away to sleep with a cute [AFK] moon tag\n"
                "`??top daily/weekly/all` - Check our active chat comets\n"
                "`??vctop` - See who hangs out the most in nebula voice chats\n"
                "`??tz set [zone]` / `??tz @user` - Check friend timezones across galaxies\n"
                "`??steal [emoji]` - Collect a stray cute starlight emoji\n"
                "`??clone` - Duplicate a cozy channel layout"
            ), inline=False)
            embed.set_footer(text="Moonlings Magical Galaxy ✨", icon_url=interaction.client.user.display_avatar.url)
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
            title="🌙 ∙ Moonlings Cosmic Help Menu",
            description="Welcome to **Moonlings**! Please pick a cozy star category from the dropdown menu below~ 🌸✨",
            color=discord.Color.from_rgb(255, 192, 203)
        )
        embed.set_footer(text="Made with love under the stars 🚀", icon_url=ctx.bot.user.display_avatar.url)
        
        await ctx.send(embed=embed, view=HelpView())

async def setup(bot):
    await bot.add_cog(HelpMenu(bot))
