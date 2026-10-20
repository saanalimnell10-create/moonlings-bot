import discord
from discord.ext import commands
from discord.ui import Select, View
import asyncio
import io

# ----------------- TICKET DROPDOWN -----------------
class TicketSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Staff Complaint",
                description="Report or complain about a staff member~ ⚖️",
                emoji="⚖️",
                value="staff_complaint"
            ),
            discord.SelectOption(
                label="Promo & Sponsorship",
                description="Inquiries for promotions or partnerships~ 🤝",
                emoji="🤝",
                value="promo_sponsorship"
            ),
            discord.SelectOption(
                label="Giveaway Claim",
                description="Claim your won giveaway prize~ 🎁",
                emoji="🎁",
                value="giveaway_claim"
            ),
            discord.SelectOption(
                label="Staff Applications",
                description="Apply to join our sweet staff team! 📝",
                emoji="📝",
                value="staff_applications"
            ),
        ]
        super().__init__(placeholder="pick a category to open a ticket, cutie~ 🫧", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        member = interaction.user
        
        # Luodaan Tickets-kategoria jos sitä ei ole
        category = discord.utils.get(guild.categories, name="Tickets")
        if not category:
            category = await guild.create_category("Tickets")
            
        # Oikeudet: Vain käyttäjä, bot ja modet/adminit näkevät
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        
        reason_map = {
            "staff_complaint": "complaint",
            "promo_sponsorship": "promo",
            "giveaway_claim": "giveaway",
            "staff_applications": "apply"
        }
        prefix = reason_map.get(self.values[0], "ticket")
        channel_name = f"{prefix}-{member.name}".lower().replace(" ", "-")
        
        ticket_channel = await guild.create_text_channel(name=channel_name, category=category, overwrites=overwrites)
        
        embed = discord.Embed(
            title="🪐 ∙ Starlight Ticket Opened",
            description=f"Hello **{member.mention}**! Welcome to your cozy support bubble~ 🫧\n\nSelected category: **{self.values[0].replace('_', ' ').title()}**\nPlease state your issue or application details, and staff will assist you shortly ✨\n\nType `??close` to pop this ticket channel!",
            color=discord.Color.from_rgb(175, 238, 238) # Pale Turquoise
        )
        embed.set_footer(text="Moonlings Space Support 🌙", icon_url=interaction.client.user.display_avatar.url)
        
        await ticket_channel.send(embed=embed)
        await interaction.response.send_message(f"✅ Ticket created! Check {ticket_channel.mention} ~ 🚀", ephemeral=True)

class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())

# ----------------- COG CLASS -----------------
class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 1. SETUP COMMAND (Lähettää tukivalikon kanavalle)
    @commands.command(name="setup")
    @commands.has_permissions(administrator=True)
    async def setup_ticket(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(
            title="🪐 ∙ Moonlings Support Center",
            description="Welcome to **Moonlings Support Center**! Please select the appropriate category from the dropdown menu below depending on what you need assistance with~ 🫧✨",
            color=discord.Color.from_rgb(230, 230, 250)
        )
        embed.set_footer(text="Floating through space & sea with Moonlings 🌸", icon_url=self.bot.user.display_avatar.url)
        await ctx.send(embed=embed, view=TicketView())

    # 2. CLOSE COMMAND (Sulkee ticketin & lähettää transcriptin lokikanavalle)
    @commands.command(name="close")
    async def close_ticket(self, ctx):
        if "-" in ctx.channel.name or "ticket" in ctx.channel.name:
            await ctx.send("Popping this ticket bubble in 5 seconds... 🫧✨")
            
            # Kerätään viestit transcriptiä varten
            messages = []
            async for msg in ctx.channel.history(limit=500, oldest_first=True):
                messages.append(f"[{msg.created_at.strftime('%Y-%m-%d %H:%M:%S')}] {msg.author.name}: {msg.content}")
            
            transcript_text = "\n".join(messages)
            
            # Etsitään tai luodaan ticket-logs -kanava transcriptille
            log_channel = discord.utils.get(ctx.guild.text_channels, name="ticket-logs")
            if not log_channel:
                log_channel = await ctx.guild.create_text_channel("ticket-logs")
            
            # Lähetetään transcript-tiedosto lokikanavalle
            file_data = io.BytesIO(transcript_text.encode('utf-8'))
            transcript_file = discord.File(file_data, filename=f"transcript-{ctx.channel.name}.txt")
            
            log_embed = discord.Embed(
                title="📜 ∙ Ticket Closed Transcript",
                description=f"Ticket **{ctx.channel.name}** was closed by {ctx.author.mention}~ ✨",
                color=discord.Color.from_rgb(255, 182, 193)
            )
            await log_channel.send(embed=log_embed, file=transcript_file)
            
            await asyncio.sleep(5)
            await ctx.channel.delete()
        else:
            await ctx.send("❌ This command can only be used inside a ticket channel!")

async def setup(bot):
    await bot.add_cog(Tickets(bot))
