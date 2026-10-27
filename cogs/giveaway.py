import discord
from discord.ext import commands
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

    @commands.command(name="create", description="Create an advanced giveaway with custom options")
    @commands.has_permissions(manage_guild=True)
    async def create(
        self,
        ctx,
        duration: str,
        winners: int,
        *,
        prize: str
    ):
        target_channel = ctx.channel
        hosting_member = ctx.author
        claim_time = "24h"
        rerolls = 1
        required_roles = None
        color = "#FFB6C1"
        thumbnail = None
        image = None

        seconds = convert_time(duration)
        claim_seconds = convert_time(claim_time)

        if not seconds or not claim_seconds:
            await ctx.send("❌ Invalid time format! Use something like `30s`, `10m`, `2h`, or `1d`.")
            return

        embed_color = discord.Color.from_rgb(230, 210, 240)
        if color:
            try:
                clean_hex = color.lstrip('#')
                embed_color = discord.Color(int(clean_hex, 16))
            except ValueError:
                pass

        embed = discord.Embed(
            title="🎁 **GIVEAWAY TIME!** 🎁",
            description=(
                f"**Prize:** {prize}\n"
                f"**Winner(s):** {winners}\n"
                f"**Claim Time:** {claim_time}\n"
                f"**Max Rerolls:** {rerolls}\n"
                f"**Hosted by:** {hosting_member.mention}\n\n"
                f"✨ Click the button below to join the giveaway!"
            ),
            color=embed_color
        )
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)
        if image:
            embed.set_image(url=image)
        embed.set_footer(text="Moonlings Advanced Giveaway 🌸")

        role_ids = [required_roles.id] if required_roles else []
        view = GiveawayJoinButton(prize, winners, role_ids)

        message = await target_channel.send(embed=embed, view=view)
        await ctx.message.delete()

        self.active_giveaways[message.id] = {
            "view": view,
            "prize": prize,
            "winners_count": winners,
            "claim_time": claim_time,
            "claim_seconds": claim_seconds,
            "embed_color": embed_color,
            "thumbnail": thumbnail,
            "image": image,
            "channel": target_channel,
            "message": message
        }

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
                        f"🎟️ Head back to the server and click the **'Claim Prize 🎫'** button on the giveaway message to create your claim ticket within **{claim_time}**! 🌸✨"
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
        if thumbnail:
            ended_embed.set_thumbnail(url=thumbnail)
        if image:
            ended_embed.set_image(url=image)
        ended_embed.set_footer(text="Moonlings Giveaway Claim System 🌸")

        await message.edit(embed=ended_embed, view=claim_view)
        announcement = await message.reply(f"🎉 Congratulations to the winners: {winner_mentions}! Check your DMs and click the button above within **{claim_time}**! 🌸✨")

        await asyncio.sleep(claim_seconds)

        unclaimed = [w for w in initial_winners if w not in claim_view.claimed]

        if unclaimed:
            eligible_for_reroll = [p for p in participants_list if p not in claim_view.claimed and p not in initial_winners]
            reroll_count = min(len(unclaimed), len(eligible_for_reroll), rerolls)

            if reroll_count > 0:
                new_winners = random.sample(eligible_for_reroll, reroll_count)
                for nw_id in new_winners:
                    new_winner_user = target_channel.guild.get_member(nw_id)
                    if new_winner_user:
                        try:
                            await new_winner_user.send(
                                f"🎉 **Giveaway Reroll Win!** You got a second chance in **{target_channel.guild.name}**!\n"
                                f"🎁 **Prize:** {prize}\n"
                                f"🌸 Claim your prize right away! ✨"
                            )
                        except discord.Forbidden:
                            pass

                new_winner_mentions = ", ".join([f"<@{nw}>" for nw in new_winners])
                await announcement.reply(f"⏰ Time is up! Unclaimed prizes resulted in new rerolls: {new_winner_mentions}! 🌸✨")
            else:
                await announcement.reply(f"⏰ Time is up, and no new participants were found for a reroll.")
        else:
            await announcement.reply(f"✨ All winners claimed their prizes on time! Amazing! 🌸💕")

        self.active_giveaways.pop(message.id, None)

    @commands.command(name="end", description="End an active giveaway early using message ID")
    @commands.has_permissions(manage_guild=True)
    async def end(self, ctx, message_id: str):
        try:
            m_id = int(message_id)
        except ValueError:
            await ctx.send("❌ Invalid Message ID format!")
            return

        if m_id in self.active_giveaways:
            data = self.active_giveaways.pop(m_id)
            try:
                await data["message"].delete()
            except discord.HTTPException:
                pass
            await ctx.send(f"✅ Successfully ended and removed the giveaway (ID: {m_id}) early!")
        else:
            await ctx.send("❌ Could not find an active giveaway with that Message ID.")

    @commands.command(name="delete", description="Delete a giveaway message")
    @commands.has_permissions(manage_guild=True)
    async def delete(self, ctx, message_id: str):
        try:
            m_id = int(message_id)
        except ValueError:
            await ctx.send("❌ Invalid Message ID format!")
            return

        if m_id in self.active_giveaways:
            data = self.active_giveaways.pop(m_id)
            try:
                await data["message"].delete()
            except discord.HTTPException:
                pass
            await ctx.send(f"🗑️ Giveaway (ID: {m_id}) has been successfully deleted!")
        else:
            found = False
            for channel in ctx.guild.text_channels:
                try:
                    msg = await channel.fetch_message(m_id)
                    await msg.delete()
                    found = True
                    break
                except discord.NotFound:
                    continue
            if found:
                await ctx.send(f"🗑️ Giveaway message (ID: {m_id}) found and deleted from channel.")
            else:
                await ctx.send("❌ Could not find a giveaway message with that ID.")

    @commands.command(name="fix", description="Force-fix or clear a stuck giveaway state")
    @commands.has_permissions(manage_guild=True)
    async def fix(self, ctx, message_id: str):
        try:
            m_id = int(message_id)
        except ValueError:
            await ctx.send("❌ Invalid Message ID format!")
            return

        if m_id in self.active_giveaways:
            self.active_giveaways.pop(m_id)
            await ctx.send(f"🔧 Giveaway (ID: {m_id}) has been force-fixed and cleared from active states!")
        else:
            await ctx.send("❌ No active giveaway state found for this ID to fix.")

    @commands.command(name="participants", description="View all users who have participated")
    @commands.has_permissions(manage_guild=True)
    async def participants(self, ctx, message_id: str):
        try:
            m_id = int(message_id)
        except ValueError:
            await ctx.send("❌ Invalid Message ID format!")
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
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Could not find active participants list for this giveaway ID.")

async def setup(bot):
    await bot.add_cog(Giveaway(bot))

