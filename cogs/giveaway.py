import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import random
import re

def convert_time(time_str):
    match = re.match(r"^(\d+)([smhd])$", time_str.lower())
    if not match:
        return None
    amount, unit = int(match.group(1)), match.group(2)
    if unit == "s":
        return amount
    elif unit == "m":
        return amount * 60
    elif unit == "h":
        return amount * 3600
    elif unit == "d":
        return amount * 86400
    return None

class GiveawayJoinButton(discord.ui.View):
    def __init__(self, prize, winners_count, required_roles):
        super().__init__(timeout=None)
        self.prize = prize
        self.winners_count = winners_count
        self.required_roles = required_roles
        self.participants = set()

    @discord.ui.button(label="Join Giveaway 🎉", style=discord.ButtonStyle.success, custom_id="advanced_giveaway_join")
    async def join_giveaway(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.required_roles:
            user_role_ids = [r.id for r in interaction.user.roles]
            has_role = any(r_id in user_role_ids for r_id in self.required_roles)
            if not has_role:
                await interaction.response.send_message("❌ You do not have the required role to participate in this giveaway!", ephemeral=True)
                return

        if interaction.user.id in self.participants:
            self.participants.remove(interaction.user.id)
            await interaction.response.send_message("🌸 You have left the giveaway!", ephemeral=True)
        else:
            self.participants.add(interaction.user.id)
            await interaction.response.send_message("🌸 You are now participating in the giveaway! Good luck! ✨", ephemeral=True)
        
        button.label = f"Join Giveaway 🎉 ({len(self.participants)})"
        await interaction.message.edit(view=self)

class TicketCloseView(discord.ui.View):
    def __init__(self, prize):
        super().__init__(timeout=None)
        self.prize = prize

    @discord.ui.button(label="Vouch & Close Ticket 🌸", style=discord.ButtonStyle.danger, custom_id="vouch_and_close_ticket")
    async def vouch_and_close(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("💖 Thank you for the vouch! Your prize has been delivered and this ticket will close in 5 seconds...", ephemeral=False)
        
        await asyncio.sleep(5)
        try:
            await interaction.channel.delete(reason=f"Giveaway prize claimed and vouched by {interaction.user}")
        except discord.HTTPException:
            pass

class InitialClaimView(discord.ui.View):
    def __init__(self, winners, prize):
        super().__init__(timeout=None)
        self.winners = set(winners)
        self.claimed = set()
        self.prize = prize

    @discord.ui.button(label="Claim Prize 🎫", style=discord.ButtonStyle.primary, custom_id="claim_giveaway_prize_ticket")
    async def claim_prize(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id not in self.winners:
            await interaction.response.send_message("❌ You are not a winner of this giveaway!", ephemeral=True)
            return

        if interaction.user.id in self.claimed:
            await interaction.response.send_message("🌸 You have already claimed your prize and your ticket has been created!", ephemeral=True)
            return

        self.claimed.add(interaction.user.id)
        
        guild = interaction.guild
        member = interaction.user
        
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        clean_name = "".join(c for c in member.name.lower() if c.isalnum() or c == "-") or "winner"
        ticket_channel = await guild.create_text_channel(
            name=f"ticket-{clean_name}",
            overwrites=overwrites,
            reason=f"Giveaway prize claim ticket for {member}"
        )

        ticket_embed = discord.Embed(
            title="🌸 Giveaway Prize Ticket",
            description=(
                f"Hello {member.mention}! Congratulations on winning!\n\n"
                f"🎁 **Prize:** {self.prize}\n\n"
                f"**Step by step instructions:**\n"
                f"1. Wait for staff to deliver your prize in this channel.\n"
                f"2. Once received, click **'Vouch & Close Ticket 🌸'** below to confirm. The ticket will close automatically! ✨"
            ),
            color=discord.Color.from_rgb(230, 210, 240)
        )
        ticket_embed.set_footer(text="Moonlings Ticket System 🌸")

        ticket_view = TicketCloseView(self.prize)
        await ticket_channel.send(content=f"{member.mention}", embed=ticket_embed, view=ticket_view)

        await interaction.response.send_message(f"🎉 Prize successfully registered! Your ticket was created here: {ticket_channel.mention} 🌸✨", ephemeral=True)
        
        button.label = f"Claimed ({len(self.claimed)}/{len(self.winners)})"
        await interaction.message.edit(view=self)

class Giveaway(commands.GroupCog, name="giveaway"):
    def __init__(self, bot):
        self.bot = bot
        self.active_giveaways = {}
        super().__init__()

    @app_commands.command(name="create", description="Create an interactive giveaway step-by-step with skip options.")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def create(self, interaction: discord.Interaction):
        await interaction.response.send_message("🌸 **Giveaway Setup Wizard** started! What is the **prize** for this giveaway?", ephemeral=True)
        
        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            # 1. Prize
            msg = await self.bot.wait_for("message", timeout=45.0, check=check)
            prize = msg.content
            await msg.delete()

            # 2. Duration
            await interaction.edit_original_response(content="⏱️ How long should the giveaway last? (e.g. `30s`, `10m`, `2h`, `1d`) [Type `skip` for default 1h]")
            msg = await self.bot.wait_for("message", timeout=45.0, check=check)
            duration = "1h" if msg.content.lower() == "skip" else msg.content
            await msg.delete()

            # 3. Winners count
            await interaction.edit_original_response(content="🏆 How many winners? [Type `skip` for default 1]")
            msg = await self.bot.wait_for("message", timeout=45.0, check=check)
            winners = 1 if msg.content.lower() == "skip" else int(msg.content)
            await msg.delete()

            # 4. Claim Time
            await interaction.edit_original_response(content="⏳ Time for winners to claim before auto-reroll? (e.g. `1h`, `24h`) [Type `skip` for default 24h]")
            msg = await self.bot.wait_for("message", timeout=45.0, check=check)
            claim_time = "24h" if msg.content.lower() == "skip" else msg.content
            await msg.delete()

            # 5. Channel
            await interaction.edit_original_response(content="📢 Tag the channel where to post this giveaway (e.g. `#giveaways`) [Type `skip` for current channel]")
            msg = await self.bot.wait_for("message", timeout=45.0, check=check)
            if msg.content.lower() == "skip" or not msg.channel_mentions:
                target_channel = interaction.channel
            else:
                target_channel = msg.channel_mentions[0]
            await msg.delete()

        except asyncio.TimeoutError:
            await interaction.edit_original_response(content="❌ Giveaway setup timed out. Please try again.")
            return
        except ValueError:
            await interaction.edit_original_response(content="❌ Invalid number provided. Setup cancelled.")
            return

        seconds = convert_time(duration)
        claim_seconds = convert_time(claim_time)
        if not seconds:
            seconds = 3600
        if not claim_seconds:
            claim_seconds = 86400

        embed_color = discord.Color.from_rgb(230, 210, 240)
        embed = discord.Embed(
            title="🎁 **GIVEAWAY TIME!** 🎁",
            description=(
                f"**Prize:** {prize}\n"
                f"**Winner(s):** {winners}\n"
                f"**Claim Time:** {claim_time}\n"
                f"**Hosted by:** {interaction.user.mention}\n\n"
                f"✨ Click the button below to join the giveaway!"
            ),
            color=embed_color
        )
        embed.set_footer(text="Moonlings Advanced Giveaway 🌸")

        view = GiveawayJoinButton(prize, winners, [])
        message = await target_channel.send(embed=embed, view=view)

        self.active_giveaways[message.id] = {
            "view": view,
            "prize": prize,
            "winners_count": winners,
            "claim_time": claim_time,
            "claim_seconds": claim_seconds,
            "embed_color": embed_color,
            "channel": target_channel,
            "message": message
        }

        await interaction.edit_original_response(content=f"✅ Giveaway successfully created in {target_channel.mention}! 🎉✨")

        await asyncio.sleep(seconds)

        if message.id not in self.active_giveaways:
            return

        view.stop()
        participants_list = list(view.participants)
        
        if not participants_list:
            ended_embed = discord.Embed(
                title="🎁 **Giveaway Ended**",
                description=f"**Prize:** {prize}\n\n❌ Not enough participants to pick a winner.",
                color=embed_color
            )
            for item in view.children:
                item.disabled = True
            await message.edit(embed=ended_embed, view=view)
            self.active_giveaways.pop(message.id, None)
            return

        actual_winners_count = min(winners, len(participants_list))
        initial_winners = random.sample(participants_list, actual_winners_count)
        winner_mentions = ", ".join([f"<@{w}>" for w in initial_winners])

        for w_id in initial_winners:
            winner_user = target_channel.guild.get_member(w_id)
            if winner_user:
                try:
                    await winner_user.send(
                        f"🎉 **Congratulations!** You won a giveaway in **{target_channel.guild.name}**!\n"
                        f"🎁 **Prize:** {prize}\n"
                        f"🎫 Head back to the server and click the **'Claim Prize 🎫'** button on the giveaway message within **{claim_time}**! 🌸✨"
                    )
                except discord.Forbidden:
                    pass

        claim_view = InitialClaimView(initial_winners, prize)
        
        ended_embed = discord.Embed(
            title="🎁 **Giveaway Ended - Claiming Phase**",
            description=(
                f"**Prize:** {prize}\n"
                f"**Winner(s):** {winner_mentions}\n"
                f"**Claim Deadline:** {claim_time}\n\n"
                f"✨ Winners have been DMed! They must click the **'Claim Prize 🎫'** button to automatically create their ticket."
            ),
            color=embed_color
        )
        ended_embed.set_footer(text="Moonlings Giveaway Claim System 🌸")
        await message.edit(embed=ended_embed, view=claim_view)
        announcement = await message.reply(f"🎉 Congratulations to the winners: {winner_mentions}! Check your DMs and click the button above within **{claim_time}**! 🌸✨")

        await asyncio.sleep(claim_seconds)

        unclaimed = [w for w in initial_winners if w not in claim_view.claimed]
        if unclaimed:
            eligible_for_reroll = [p for p in participants_list if p not in claim_view.claimed and p not in initial_winners]
            if eligible_for_reroll:
                new_winner = random.choice(eligible_for_reroll)
                new_winner_user = target_channel.guild.get_member(new_winner)
                if new_winner_user:
                    try:
                        await new_winner_user.send(f"🎉 **Giveaway Reroll Win!** You won the reroll for **{prize}** in **{target_channel.guild.name}**! 🌸✨")
                    except discord.Forbidden:
                        pass
                await announcement.reply(f"⏰ Time is up! An unclaimed prize resulted in a new winner: <@{new_winner}>! 🌸✨")
            else:
                await announcement.reply(f"⏰ Time is up, and no new participants were found for a reroll.")
        else:
            await announcement.reply(f"✨ All winners claimed their prizes on time! Amazing! 🌸💖")

        self.active_giveaways.pop(message.id, None)

    @app_commands.command(name="end", description="End a giveaway early using the giveaway message ID[cite: 3].")
    @app_commands.describe(message_id="The message ID of the giveaway[cite: 3]")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def end(self, interaction: discord.Interaction, message_id: str):
        try:
            m_id = int(message_id)
        except ValueError:
            await interaction.response.send_message("❌ Invalid Message ID format!", ephemeral=True)
            return

        if m_id in self.active_giveaways:
            data = self.active_giveaways.pop(m_id)
            try:
                await data["message"].delete()
            except discord.HTTPException:
                pass
            await interaction.response.send_message(f"✅ Successfully ended and removed the giveaway (ID: {m_id}) early!", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Could not find an active giveaway with that Message ID.", ephemeral=True)

    @app_commands.command(name="delete", description="Delete a giveaway message and cancel its active state[cite: 3].")
    @app_commands.describe(message_id="The message ID of the giveaway to delete[cite: 3]")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def delete(self, interaction: discord.Interaction, message_id: str):
        try:
            m_id = int(message_id)
        except ValueError:
            await interaction.response.send_message("❌ Invalid Message ID format!", ephemeral=True)
            return

        if m_id in self.active_giveaways:
            data = self.active_giveaways.pop(m_id)
            try:
                await data["message"].delete()
            except discord.HTTPException:
                pass
            await interaction.response.send_message(f"🗑️ Giveaway (ID: {m_id}) has been successfully deleted[cite: 3]!", ephemeral=True)
        else:
            try:
                found = False
                for channel in interaction.guild.text_channels:
                    try:
                        msg = await channel.fetch_message(m_id)
                        await msg.delete()
                        found = True
                        break
                    except discord.NotFound:
                        continue
                if found:
                    await interaction.response.send_message(f"🗑️ Giveaway message (ID: {m_id}) found and deleted[cite: 3]!", ephemeral=True)
                else:
                    await interaction.response.send_message("❌ Could not find a giveaway message with that ID[cite: 3].", ephemeral=True)
            except Exception:
                await interaction.response.send_message("❌ Failed to delete the giveaway message.", ephemeral=True)

    @app_commands.command(name="fix", description="Fix or force-end a giveaway if it fails to end properly[cite: 4].")
    @app_commands.describe(message_id="The message ID of the stuck giveaway[cite: 4]")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def fix(self, interaction: discord.Interaction, message_id: str):
        try:
            m_id = int(message_id)
        except ValueError:
            await interaction.response.send_message("❌ Invalid Message ID format!", ephemeral=True)
            return

        if m_id in self.active_giveaways:
            self.active_giveaways.pop(m_id)
            await interaction.response.send_message(f"🛠️ Giveaway (ID: {m_id}) has been force-fixed and cleared from active states[cite: 4]!", ephemeral=True)
        else:
            await interaction.response.send_message("❌ No active giveaway state found for this ID to fix[cite: 4].", ephemeral=True)

    @app_commands.command(name="participants", description="View the users that have participated in a giveaway[cite: 4].")
    @app_commands.describe(message_id="The message ID of the giveaway[cite: 4]")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def participants(self, interaction: discord.Interaction, message_id: str):
        try:
            m_id = int(message_id)
        except ValueError:
            await interaction.response.send_message("❌ Invalid Message ID format!", ephemeral=True)
            return

        if m_id in self.active_giveaways:
            view = self.active_giveaways[m_id]["view"]
            count = len(view.participants)
            users_str = ", ".join([f"<@{uid}>" for uid in view.participants]) if view.participants else "No participants yet."
            
            embed = discord.Embed(
                title="🎁 Giveaway Participants",
                description=f"**Total Participants:** {count}\n\n**Users:** {users_str}",
                color=discord.Color.from_rgb(230, 210, 240)
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message("❌ Could not find active participants list for this giveaway ID.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Giveaway(bot))
