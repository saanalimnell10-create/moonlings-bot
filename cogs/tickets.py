import discord
from discord.ext import commands

class TicketSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Partnership", description="Kysy kumppanuudesta", emoji="🤝"),
            discord.SelectOption(label="Promo Server", description="Palvelimen mainostamiseen liittyvät asiat", emoji="📢"),
            discord.SelectOption(label="GW Claim", description="Lunasta giveaway-palkinto", emoji="🎉"),
            discord.SelectOption(label="GW Host", description="Järjestä giveaway yhteistyössä", emoji="✨"),
            discord.SelectOption(label="Staff Complaint", description="Valita ylläpitäjän toiminnasta", emoji="⚠️"),
            discord.SelectOption(label="Report User", description="Ilmoita sääntörikkomuksesta", emoji="🚨"),
            discord.SelectOption(label="Ban Appeal", description="Ano bännejä pois", emoji="🔓"),
            discord.SelectOption(label="General Support", description="Yleiset kysymykset ja apu", emoji="💬"),
        ]
        super().__init__(placeholder="Valitse tiketin aihe...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        user = interaction.user
        category_name = self.values[0]

        # Luodaan uniikki kanavanimi käyttäjän nimen ja ID:n perusteella
        channel_name = f"ticket-{user.name}-{user.id}".lower()
        channel_name = "".join(c for c in channel_name if c.isalnum() or c == "-")
        
        existing_channel = discord.utils.get(guild.text_channels, name=channel_name)
        if existing_channel:
            await interaction.response.send_message(f"Sinulla on jo auki oleva tiketti: {existing_channel.mention}", ephemeral=True)
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True)
        }

        channel = await guild.create_text_channel(name=channel_name, overwrites=overwrites)
        
        embed = discord.Embed(
            title=f"🎫 Tiketti: {category_name}",
            description=f"Hei {user.mention}! Ylläpito vastaa sinulle pian.\n\n**Komennot:**\n• `??close` - Sulkee tiketin\n• `??add @käyttäjä` - Lisää käyttäjän\n• `??remove @käyttäjä` - Poistaa käyttäjän\n• `??block @käyttäjä` - Estää pääsyn",
            color=discord.Color.from_rgb(230, 210, 240)
        )
        embed.set_footer(text="Moonlings Ticket System 🌸")
        await channel.send(embed=embed)
        await interaction.response.send_message(f"Tiketti luotu: {channel.mention}", ephemeral=True)

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ticketpanel")
    @commands.has_permissions(administrator=True)
    async def ticket_panel(self, ctx):
        """Sends the support ticket panel with a drop-down menu."""
        await ctx.message.delete()
        embed = discord.Embed(
            title="🎫 Moonlings Support & Tickets",
            description="Tarvitsetko apua, haluatko tehdä kumppanuuden tai ilmoittaa jostain? Valitse alta sopiva aihe avataksesi tiketin! 🌸",
            color=discord.Color.from_rgb(230, 210, 240)
        )
        embed.set_footer(text="Moonlings Ticket System 🌸")
        await ctx.send(embed=embed, view=TicketView())

    @commands.command(name="close")
    async def close_ticket(self, ctx):
        """Closes the active ticket channel."""
        if not ctx.channel.name.startswith("ticket-"):
            await ctx.send("❌ Tätä komentoa voi käyttää vain tikettikanavilla!", delete_after=5)
            return

        embed = discord.Embed(
            title="🔒 Tiketti suljetaan",
            description="Tämä kanava poistetaan 5 sekunnin kuluttua...",
            color=discord.Color.from_rgb(255, 182, 193)
        )
        embed.set_footer(text="Moonlings Ticket System 🌸")
        await ctx.send(embed=embed)
        await ctx.channel.delete(delay=5)

    @commands.command(name="add")
    @commands.has_permissions(manage_channels=True)
    async def add_user(self, ctx, member: discord.Member):
        """Adds a user to the active ticket channel."""
        await ctx.message.delete()
        if not ctx.channel.name.startswith("ticket-"):
            await ctx.send("❌ Tätä komentoa voi käyttää vain tikettikanavilla!", delete_after=5)
            return
        await ctx.channel.set_permissions(member, read_messages=True, send_messages=True)
        await ctx.send(f"✨ {member.mention} on lisätty tikettiin.")

    @commands.command(name="remove")
    @commands.has_permissions(manage_channels=True)
    async def remove_user(self, ctx, member: discord.Member):
        """Removes a user from the active ticket channel."""
        await ctx.message.delete()
        if not ctx.channel.name.startswith("ticket-"):
            await ctx.send("❌ Tätä komentoa voi käyttää vain tikettikanavilla!", delete_after=5)
            return
        await ctx.channel.set_permissions(member, overwrite=None)
        await ctx.send(f"🛡️ {member.mention} on poistettu tiketistä.")

    @commands.command(name="block")
    @commands.has_permissions(manage_channels=True)
    async def block_user(self, ctx, member: discord.Member):
        """Blocks a user from viewing the ticket channel."""
        await ctx.message.delete()
        if not ctx.channel.name.startswith("ticket-"):
            await ctx.send("❌ Tätä komentoa voi käyttää vain tikettikanavilla!", delete_after=5)
            return
        await ctx.channel.set_permissions(member, read_messages=False)
        await ctx.send(f"🚫 {member.mention} on estetty tässä tiketissä.")

async def setup(bot):
    await bot.add_cog(Tickets(bot))
