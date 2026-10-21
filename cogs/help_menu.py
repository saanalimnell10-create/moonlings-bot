import discord
from discord.ext import commands
import io

class TicketDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Staff Complaint", description="Report an issue regarding a staff member", emoji="🛡️", value="staff_complaint"),
            discord.SelectOption(label="Promo & Sponsorship", description="Inquire about partnerships and promos", emoji="✨", value="promo"),
            discord.SelectOption(label="Giveaway Claim", description="Claim a giveaway reward you won", emoji="🎁", value="giveaway"),
            discord.SelectOption(label="Staff Applications", description="Apply to join our cozy team", emoji="📝", value="application"),
        ]
        super().__init__(placeholder="Select a category to open a ticket~ 🎫", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        user = interaction.user
        category_name = self.values[0].replace("_", " ").title()

        # Etsitään tai luodaan Tickets-kategoria
        category = discord.utils.get(guild.categories, name="Tickets")
        if not category:
            category = await guild.create_category("Tickets")

        # Tarkistetaan onko käyttäjällä jo auki oleva tiketti
        channel_name = f"ticket-{user.name.lower().replace(' ', '-')}"
        existing_channel = discord.utils.get(guild.text_channels, name=channel_name)

        if existing_channel:
            await interaction.response.send_message(f"❌ You already have an open ticket here: {existing_channel.mention}~", ephemeral=True)
            return

        # Oikeudet: Vain käyttäjä ja ylläpito näkevät kanavan
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True)
        }

        ticket_channel = await guild.create_text_channel(name=channel_name, category=category, overwrites=overwrites)

        embed = discord.Embed(
            title=f"🎫 ∙ Ticket: {category_name}",
            description=f"Welcome {user.mention}! ✨\nOur staff team will be with you shortly. Please explain your issue or request in detail below~ 🌸",
            color=discord.Color.from_rgb(175, 238, 238)
        )
        embed.set_footer(text="Type ??close to close this ticket 🌙", icon_url=user.display_avatar.url)

        await ticket_channel.send(embed=embed)
        await interaction.response.send_message(f"✨ Ticket created! Head over to {ticket_channel.mention}~", ephemeral=True)

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketDropdown())

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setup")
    @commands.has_permissions(administrator=True)
    async def setup_tickets(self, ctx):
        await ctx.message.delete()

        embed = discord.Embed(
            title="🎫 ∙ Moonlings Support Center",
            description="Need help, want to apply, or claim a giveaway reward? ✨\nSelect the appropriate category from the dropdown menu below to open a private ticket channel~ 🌸",
            color=discord.Color.from_rgb(255, 192, 203)
        )
        embed.set_footer(text="Moonlings Support System 🌙", icon_url=self.bot.user.display_avatar.url)

        view = TicketView()
        await ctx.send(embed=embed, view=view)

    @commands.command(name="close")
    async def close_ticket(self, ctx):
        if not ctx.channel.name.startswith("ticket-"):
            await ctx.send("❌ This command can only be used inside a ticket channel~", delete_after=5)
            return

        await ctx.send("🔒 Closing ticket and generating transcript in 5 seconds...")

        # Kerätään viestit transkriptia varten
        messages = []
        async for msg in ctx.channel.history(limit=500, oldest_first=True):
            messages.append(f"[{msg.created_at.strftime('%Y-%m-%d %H:%M')}] {msg.author}: {msg.content}")

        transcript_text = "\n".join(messages)
        file_data = io.BytesIO(transcript_text.encode("utf-8"))
        transcript_file = discord.File(file_data, filename=f"{ctx.channel.name}-transcript.txt")

        # Etsitään #ticket-logs kanava
        log_channel = discord.utils.get(ctx.guild.text_channels, name="ticket-logs")
        if log_channel:
            log_embed = discord.Embed(
                title="📜 ∙ Ticket Closed Transcript",
                description=f"Ticket **#{ctx.channel.name}** was closed by {ctx.author.mention}~ 🌸",
                color=discord.Color.from_rgb(230, 230, 250)
            )
            await log_channel.send(embed=log_embed, file=transcript_file)

        await ctx.channel.delete()

async def setup(bot):
    await bot.add_cog(Tickets(bot))
