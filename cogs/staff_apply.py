import discord
from discord.ext import commands
import io

class StaffApplyModal(discord.ui.Modal, title="Moonlings Staff Application"):
    age = discord.ui.TextInput(
        label="Age",
        placeholder="Type your age here...",
        required=True,
        max_length=3
    )
    experience = discord.ui.TextInput(
        label="Experience",
        placeholder="Tell us about your previous staff experience...",
        style=discord.TextStyle.paragraph,
        required=True,
        max_length=500
    )
    why_you = discord.ui.TextInput(
        label="Why You?",
        placeholder="Why would you like to join our staff team?",
        style=discord.TextStyle.paragraph,
        required=True,
        max_length=500
    )

    async def on_submit(self, interaction: discord.Interaction):
        guild = interaction.guild
        user = interaction.user

        # Create a unique application channel name
        channel_name = f"apply-{user.name}-{user.id}".lower()
        channel_name = "".join(c for c in channel_name if c.isalnum() or c == "-")

        existing_channel = discord.utils.get(guild.text_channels, name=channel_name)
        if existing_channel:
            await interaction.response.send_message(f"You already have an open application channel: {existing_channel.mention}", ephemeral=True)
            return

        # Private channel permissions (hidden from regular members, visible to user and bot/staff with permissions)
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True)
        }

        channel = await guild.create_text_channel(name=channel_name, overwrites=overwrites)

        embed = discord.Embed(
            title=f"🌸 Staff Application: {user.name}",
            description=f"**Applicant:** {user.mention}\n\n**Age:** {self.age.value}\n\n**Experience:**\n{self.experience.value}\n\n**Why You:**\n{self.why_you.value}\n\n**Commands:**\n• `??applyclose` - Closes and generates a transcript for this application",
            color=discord.Color.from_rgb(230, 210, 240)
        )
        embed.set_footer(text="Moonlings Staff Applications 🌸")
        
        await channel.send(embed=embed)
        await interaction.response.send_message(f"Your application has been submitted! Channel created: {channel.mention}", ephemeral=True)

class StaffApplyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Apply for Staff 📝", style=discord.ButtonStyle.primary, custom_id="apply_staff_btn")
    async def apply_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(StaffApplyModal())

class StaffApply(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="staffapplypanel")
    @commands.has_permissions(administrator=True)
    async def staff_apply_panel(self, ctx):
        """Sends the staff application panel with a button."""
        await ctx.message.delete()
        embed = discord.Embed(
            title="✨ Moonlings Staff Applications",
            description="Want to join our amazing team? Click the button below to fill out an application! 🌸",
            color=discord.Color.from_rgb(230, 210, 240)
        )
        embed.set_footer(text="Moonlings Staff Applications 🌸")
        await ctx.send(embed=embed, view=StaffApplyView())

    @commands.command(name="applyclose")
    async def close_application(self, ctx):
        """Closes the active staff application channel and generates a transcript."""
        if not ctx.channel.name.startswith("apply-"):
            await ctx.send("❌ This command can only be used in application channels!", delete_after=5)
            return

        # Collect messages for the transcript file
        messages = []
        async for message in ctx.channel.history(limit=200, oldest_first=True):
            messages.append(f"[{message.created_at.strftime('%Y-%m-%d %H:%M:%S')}] {message.author}: {message.content}")
        
        transcript_content = "\n".join(messages)
        file = discord.File(io.BytesIO(transcript_content.encode('utf-8')), filename=f"{ctx.channel.name}-transcript.txt")

        embed = discord.Embed(
            title="🔒 Application Closed",
            description="Transcript generated below. This channel will be deleted in 5 seconds...",
            color=discord.Color.from_rgb(255, 182, 193)
        )
        embed.set_footer(text="Moonlings Staff Applications 🌸")
        
        await ctx.send(embed=embed, file=file)
        await ctx.channel.delete(delay=5)

async def setup(bot):
    await bot.add_cog(StaffApply(bot))
