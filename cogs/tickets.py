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

        channel_name = f"ticket-{user.name}".lower()
        # Siivotaan erikoismerkit kanavan nimestä, ettei tule virheitä
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
            description=f"Hei {user.mention}! Ylläpito vastaa sinulle pian.\n\n**Komennot:**\n• `??close` - Sulkee tiketin ja luo transcriptin\n• `??add @käyttäjä` - Lisää käyttäjän\n• `??remove @käyttäjä` - Poistaa käyttäjän\n• `??block @käyttäjä` - Estää pääsyn",
            color=discord.Color.purple()
        )
        await channel.send(embed=embed)
        await interaction.response.send_message(f"Tiketti luotu: {channel.mention}", ephemeral=True)
