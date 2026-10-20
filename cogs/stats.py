import discord
from discord.ext import commands
import time

class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Viestit ja tilastot
        self.messages_all = {}
        self.messages_daily = {}
        self.messages_weekly = {}
        
        # VC Timing
        self.vc_join_times = {}
        self.vc_total_time = {}

    # ==================== 1. LISTENERIT (Viestit & VC) ====================
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        user_id = message.author.id

        # Päivitetään viestimäärät
        self.messages_all[user_id] = self.messages_all.get(user_id, 0) + 1
        self.messages_daily[user_id] = self.messages_daily.get(user_id, 0) + 1
        self.messages_weekly[user_id] = self.messages_weekly.get(user_id, 0) + 1

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return

        user_id = member.id
        now = time.time()

        if before.channel is None and after.channel is not None:
            self.vc_join_times[user_id] = now

        elif before.channel is not None and after.channel is None:
            if user_id in self.vc_join_times:
                time_spent = int(now - self.vc_join_times.pop(user_id))
                self.vc_total_time[user_id] = self.vc_total_time.get(user_id, 0) + time_spent

    # ==================== 2. STATS & LEADERBOARD KOMENNOT ====================
    @commands.command(name="top")
    async def top_messages(self, ctx, timeframe: str = "all"):
        await ctx.message.delete()
        timeframe = timeframe.lower()

        if timeframe == "daily":
            data = self.messages_daily
            title_text = "Daily Active Stars ☀️"
        elif timeframe == "weekly":
            data = self.messages_weekly
            title_text = "Weekly Active Stars 🌸"
        else:
            data = self.messages_all
            title_text = "All-Time Active Stars 🌌"

        if not data:
            embed = discord.Embed(
                title=f"📊 ∙ {title_text}",
                description="No message statistics available yet~ 🫧",
                color=discord.Color.from_rgb(230, 230, 250)
            )
            await ctx.send(embed=embed)
            return

        sorted_users = sorted(data.items(), key=lambda x: x[1], reverse=True)[:10]

        leaderboard_lines = []
        for index, (u_id, count) in enumerate(sorted_users, 1):
            user = ctx.guild.get_member(u_id)
            name = user.display_name if user else f"User ({u_id})"
            leaderboard_lines.append(f"**{index}.** `{name}` — **{count}** messages")

        embed = discord.Embed(
            title=f"📊 ∙ {title_text}",
            description="\n".join(leaderboard_lines),
            color=discord.Color.from_rgb(255, 192, 203)
        )
        embed.set_footer(text="Moonlings Activity Tracking ✨", icon_url=self.bot.user.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.command(name="messages")
    async def check_messages(self, ctx, member: discord.Member = None):
        await ctx.message.delete()
        target = member or ctx.author
        count = self.messages_all.get(target.id, 0)

        embed = discord.Embed(
            title="💬 ∙ Message Count",
            description=f"**{target.display_name}** has sent **{count}** messages in total~ 🌸✨",
            color=discord.Color.from_rgb(175, 238, 238)
        )
        await ctx.send(embed=embed)

    @commands.command(name="vctop")
    async def vc_top(self, ctx):
        await ctx.message.delete()

        if not self.vc_total_time:
            embed = discord.Embed(
                title="🎙️ ∙ Voice Channel Activity",
                description="No voice activity recorded yet~ 🫧",
                color=discord.Color.from_rgb(230, 230, 250)
            )
            await ctx.send(embed=embed)
            return

        sorted_users = sorted(self.vc_total_time.items(), key=lambda x: x[1], reverse=True)[:10]

        leaderboard_lines = []
        for index, (u_id, total_seconds) in enumerate(sorted_users, 1):
            user = ctx.guild.get_member(u_id)
            name = user.display_name if user else f"User ({u_id})"

            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60

            time_str = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"
            leaderboard_lines.append(f"**{index}.** `{name}` — **{time_str}** in VC")

        embed = discord.Embed(
            title="🎙️ ∙ Top Voice Activity Stars",
            description="\n".join(leaderboard_lines),
            color=discord.Color.from_rgb(176, 224, 230)
        )
        embed.set_footer(text="Moonlings VC Tracking 🌙", icon_url=self.bot.user.display_avatar.url)
        await ctx.send(embed=embed)

    # ==================== 3. RESET STATS KOMENNOT ====================
    @commands.command(name="resetstats")
    @commands.has_permissions(administrator=True)
    async def reset_stats(self, ctx, category: str, member: discord.Member = None):
        await ctx.message.delete()
        category = category.lower()

        if category == "daily":
            self.messages_daily.clear()
            msg = "Reset all **daily** message stats~ ☀️"
        elif category == "weekly":
            self.messages_weekly.clear()
            msg = "Reset all **weekly** message stats~ 🌸"
        elif category == "all":
            self.messages_all.clear()
            msg = "Reset all **all-time** message stats~ 🌌"
        elif category == "messages" and member:
            self.messages_all.pop(member.id, None)
            self.messages_daily.pop(member.id, None)
            self.messages_weekly.pop(member.id, None)
            msg = f"Reset message stats for **{member.display_name}**~ 💬"
        elif category == "vc" and member:
            self.vc_total_time.pop(member.id, None)
            msg = f"Reset VC activity time for **{member.display_name}**~ 🎙️"
        else:
            await ctx.send("❌ Usage: `??resetstats [daily/weekly/all/messages @user/vc @user]`", delete_after=5)
            return

        embed = discord.Embed(
            title="✨ ∙ Statistics Reset",
            description=msg,
            color=discord.Color.from_rgb(255, 182, 193)
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Stats(bot))
