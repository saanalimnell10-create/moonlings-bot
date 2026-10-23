import discord
from discord.ext import commands
import io

# --- MODAL: HAKEMUSLOMAKE ---
class StaffApplyModal(discord.ui.Modal, title="📝 Staff Application"):
    age = discord.ui.TextInput(
        label="Ikäsi / Age",
        placeholder="Esim. 16",
        required=True,
        max_length=3
    )
    
    experience = discord.ui.TextInput(
        label="Aiempi kokemus / Previous Experience",
        style=discord.TextStyle.paragraph,
        placeholder="Oletko toiminut aiemmin moderaattorina/ylläpitäjänä?",
        required=True,
        max_length=500
    )
    
    why_you = discord.ui.TextInput(
        label="Miksi juuri sinut pitäisi valita?",
        style=discord.TextStyle.paragraph,
        placeholder="Kerro hieman itsestäsi ja vahvuuksistasi...",
        required=True,
        max_length=1000
    )

    async def on_submit(self, interaction: discord.Interaction):
        guild = interaction.guild
        user = interaction.user

        # Tarkistetaan ettei hakijalla ole jo avointa hakemusta
        channel_name = f"apply-{user.name}".lower()
        channel_name = "".join(c for c in channel_name if c.isalnum() or c == "-")
        
        existing_channel = discord.utils.get(guild.text_channels, name=channel_name)
        if existing_channel:
            await interaction.response.send_message(f"Sinulla on jo auki oleva hakemus: {existing_channel.mention}", ephemeral=True)
            return

        # Kanavan oikeudet (vain hakija ja ylläpito näkevät)
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True)
        }

        channel = await guild.create_text_channel(name=channel_name, overwrites=overwrites)

        # Hakemuksen Embed-viesti luodulle kanavalle
        embed = discord.Embed(
            title=f"📝 Uusi Staff-hakemus: {user.name}",
            color=discord.Color.gold()
        )
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.add_field(name="Hakija", value=user.mention, inline=True)
        embed.add_field(name="Ikä", value=self.age.value, inline=True)
        embed.add_field(name="Aiempi kokemus", value=self.experience.value, inline=False)
        embed.add_field(name="Miksi valita tämä hakija", value=self.why_you.value, inline=False)
        embed.set_footer(text="Käytä '??close' sulkeaksesi hakemuksen ja luodaksesi transcriptin.")

        await channel.send(embed=embed)

        # Automaattinen ilmoitus ylläpidon logikanavaan (jos olemassa)
        log_channel = discord.utils.get(guild.text_channels, name="staff-logs")
        if log_channel:
            log_embed = discord.Embed(
                title=f"📥 Uusi hakemus: {user.name}",
                description=f"Hakemuskanava luotu: {channel.mention}",
                color=discord.Color.gold()
            )
            await log_channel.send(embed=log_embed)

        await interaction.response.send_message(f"Hakemuksesi on luotu: {channel.mention}", ephemeral=True)


# --- NAPPI JONKA PAINAMISESTA LOMAKE AUKEAA ---
class StaffApplyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Hae Staffiin / Apply Here", style=discord.ButtonStyle.success, emoji="📝", custom_id="staff_apply_btn")
    async def apply_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(StaffApplyModal())


# --- COG LUOKKA ---
class StaffApply(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="applypanel")
    @commands.has_permissions(administrator=True)
    async def applypanel(self, ctx):
        """Lähettää Staff Application -paneelin nappuloineen."""
        embed = discord.Embed(
            title="✨ Staff Applications",
            description="Haluatko liittyä osaksi Moonlings-tiimiä?\n\nPaina alla olevaa nappia ja täytä avautuva hakemuskenttä!",
            color=discord.Color.purple()
        )
        await ctx.send(embed=embed, view=StaffApplyView())

    # SULKEMINEN JA AUTOMAATTINEN TRANSCRIPT-KANAVAN LUOMINEN
    @commands.command(name="close")
    async def close_apply(self, ctx):
        """Sulkee hakemuskanavan ja lähettää transcriptin automaattisesti luotuun kanavaan."""
        if not ctx.channel.name.startswith("apply-"):
            return # Jättää tavalliset tiketit rauhaan

        await ctx.send("🔒 Luodaan transcriptiä ja suljetaan hakemusta...")

        messages = []
        async for message in ctx.channel.history(limit=500, oldest_first=True):
            messages.append(f"[{message.created_at.strftime('%Y-%m-%d %H:%M:%S')}] {message.author}: {message.content}")

        transcript_text = "\n".join(messages)
        file = discord.File(io.BytesIO(transcript_text.encode("utf-8")), filename=f"{ctx.channel.name}-transcript.txt")

        # Tarkistetaan onko transcript-kanavaa olemassa, luodaan tarvittaessa automaattisesti
        transcript_channel_name = "staff-apply-transcripts"
        transcript_channel = discord.utils.get(ctx.guild.text_channels, name=transcript_channel_name)
        
        if not transcript_channel:
            # Luodaan kanava automaattisesti (piilotettu jäseniltä, vain botille ja ylläpidolle)
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                ctx.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True)
            }
            transcript_channel = await ctx.guild.create_text_channel(transcript_channel_name, overwrites=overwrites)

        # Lähetetään tiedosto automaattisesti luotuun kanavaan
        await transcript_channel.send(content=f"📁 Suljetun hakemuksen `{ctx.channel.name}` transcript:", file=file)

        # Poistetaan alkuperäinen hakemuskanava
        await ctx.channel.delete()

async def setup(bot):
    await bot.add_cog(StaffApply(bot))
