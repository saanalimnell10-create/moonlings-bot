import discord
from discord.ext import commands
import json
import os

FORCED_NAMES_FILE = "forced_names.json"

def load_forced_names():
    if os.path.exists(FORCED_NAMES_FILE):
        with open(FORCED_NAMES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_forced_names(data):
    with open(FORCED_NAMES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

class AdvancedMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.forced_names = load_forced_names()

    # --- ISOLATE & ENDBEEF ---

    @commands.command(name="isolate")
    @commands.has_permissions(manage_channels=True, manage_roles=True)
    async def isolate(self, ctx, user1: discord.Member, user2: discord.Member, *, reason: str = "Cooling down"):
        """Isolates arguing members into a temporary private channel."""
        guild = ctx.guild

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.author: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            user1: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            user2: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        # Luodaan puhdas ja turvallinen kanavaniimi
        clean_name1 = "".join(c for c in user1.name.lower() if c.isalnum() or c == "-") or "user1"
        clean_name2 = "".join(c for c in user2.name.lower() if c.isalnum() or c == "-") or "user2"
        channel_name = f"safe-space-{clean_name1}-{clean_name2}"

        isolation_channel = await guild.create_text_channel(
            name=channel_name,
            overwrites=overwrites,
            reason=f"Isolation by {ctx.author}: {reason}"
        )

        embed = discord.Embed(
            title="🛡️ Conflict Isolation Active",
            description=(
                f"**Isolating:** {user1.mention} & {user2.mention}\n"
                f"**Reason:** {reason}\n\n"
                f"Please take a deep breath and talk things out calmly here. "
                f"Staff member {ctx.author.mention} will assist when needed."
            ),
            color=0xFFB6C1
        )
        embed.set_footer(text="Moonlings Safety Suite 🌸")
        
        await isolation_channel.send(content=f"{user1.mention} {user2.mention}", embed=embed)

        success_embed = discord.Embed(
            title="🔒 Isolation Channel Created",
            description=f"Successfully isolated the users in {isolation_channel.mention}!",
            color=0xFFB6C1
        )
        await ctx.send(embed=success_embed)

    @commands.command(name="endbeef")
    @commands.has_permissions(manage_channels=True)
    async def end_beef(self, ctx, user1: discord.Member = None, user2: discord.Member = None):
        """Ends the isolation and deletes the temporary private channel."""
        # Jos käyttäjiä ei annettu, tarkistetaanko ollaanko suoraan konfliktikanavassa
        if not user1 and not user2:
            if "safe-space" in ctx.channel.name:
                await ctx.channel.delete(reason=f"Isolation ended by {ctx.author}")
                return
            else:
                await ctx.send("❌ Please specify the two users or run this command inside the isolation channel.", delete_after=5)
                return

        # Jos käyttäjät annettiin, etsitään kyseinen kanava niiden mukaan
        if user1 and user2:
            target_channel = None
            for channel in ctx.guild.text_channels:
                if "safe-space" in channel.name:
                    if user1 in channel.members and user2 in channel.members:
                        target_channel = channel
                        break
            
            if target_channel:
                await target_channel.delete(reason=f"Isolation ended by {ctx.author}")
                await ctx.send(embed=discord.Embed(
                    title="✨ Conflict Resolved",
                    description=f"The isolation channel for {user1.mention} and {user2.mention} has been closed.",
                    color=0xFFB6C1
                ))
            else:
                await ctx.send("❌ Could not find an active isolation channel for these users.", delete_after=5)
        else:
            await ctx.send("❌ Please specify both users or run the command inside the isolation channel.", delete_after=5)

    # --- FORCENAME ---

    @commands.command(name="forcename")
    @commands.has_permissions(manage_nicknames=True)
    async def force_name(self, ctx, member: discord.Member, *, nickname: str):
        """Forces a nickname on a member and automatically re-applies it if changed."""
        guild_id_str = str(ctx.guild.id)

        if nickname.lower() == "remove":
            if guild_id_str in self.forced_names and str(member.id) in self.forced_names[guild_id_str]:
                del self.forced_names[guild_id_str][str(member.id)]
                save_forced_names(self.forced_names)
                await member.edit(nick=None)
                await ctx.send(embed=discord.Embed(
                    title="🌸 Nickname Lock Removed",
                    description=f"Forced nickname lock removed for {member.mention}.",
                    color=0xFFB6C1
                ))
            else:
                await ctx.send(f"❌ {member.mention} does not have an active forced nickname.", delete_after=5)
            return

        try:
            await member.edit(nick=nickname, reason=f"Forced nickname by {ctx.author}")
            
            if guild_id_str not in self.forced_names:
                self.forced_names[guild_id_str] = {}
            
            self.forced_names[guild_id_str][str(member.id)] = nickname
            save_forced_names(self.forced_names)

            embed = discord.Embed(
                title="🔒 Nickname Locked",
                description=f"Successfully locked {member.mention}'s nickname to: **{nickname}**",
                color=0xFFB6C1
            )
            await ctx.send(embed=embed)

        except discord.Forbidden:
            await ctx.send("❌ I do not have permission to change this member's nickname (their role might be higher than mine).", delete_after=5)

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        """Automaattisesti palauttaa pakotetun lempinimen, jos käyttäjä yrittää vaihtaa sitä."""
        guild_id_str = str(after.guild.id)
        
        if guild_id_str in self.forced_names:
            forced_dict = self.forced_names[guild_id_str]
            user_id_str = str(after.id)
            
            if user_id_str in forced_dict:
                target_nick = forced_dict[user_id_str]
                if after.nick != target_nick:
                    try:
                        await after.edit(nick=target_nick, reason="Re-applying forced nickname lock.")
                    except discord.Forbidden:
                        pass

async def setup(bot):
    await bot.add_cog(AdvancedMod(bot))
