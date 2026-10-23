import discord
from discord.ext import commands

class Security(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.antinuke_enabled = True
        self.antiraid_enabled = True
        self.whitelisted_users = []  # Lista whitelisted-käyttäjien ID:istä

    # 1. ANTINUKE TOGGLE
    @commands.command(name="antinuke")
    @commands.has_permissions(administrator=True)
    async def antinuke_command(self, ctx, status: str = None):
        """Enables or disables Anti-Nuke protection."""
        await ctx.message.delete()
        if status and status.lower() == "off":
            self.antinuke_enabled = False
            state_text = "disabled ❌"
            color = discord.Color.from_rgb(255, 182, 193)
        else:
            self.antinuke_enabled = True
            state_text = "enabled & protecting our galaxy! 🛡️✨"
            color = discord.Color.from_rgb(152, 251, 152)

        embed = discord.Embed(
            title="🚀 ∙ Anti-Nuke System",
            description=f"Anti-Nuke protection is now **{state_text}**",
            color=color
        )
        embed.set_footer(text="Moonlings Security Suite 🌸")
        await ctx.send(embed=embed)

    # 2. ANTIRAID TOGGLE
    @commands.command(name="antiraid")
    @commands.has_permissions(administrator=True)
    async def antiraid_command(self, ctx, status: str = None):
        """Enables or disables Anti-Raid protection."""
        await ctx.message.delete()
        if status and status.lower() == "off":
            self.antiraid_enabled = False
            state_text = "disabled ❌"
            color = discord.Color.from_rgb(255, 182, 193)
        else:
            self.antiraid_enabled = True
            state_text = "enabled & monitoring joins! 🛸✨"
            color = discord.Color.from_rgb(152, 251, 152)

        embed = discord.Embed(
            title="🛸 ∙ Anti-Raid System",
            description=f"Anti-Raid protection is now **{state_text}**",
            color=color
        )
        embed.set_footer(text="Moonlings Security Suite 🌸")
        await ctx.send(embed=embed)

    # 3. WHITELIST GROUP & COMMANDS
    @commands.group(name="whitelist", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def whitelist_group(self, ctx):
        """Manage the Anti-Nuke whitelist."""
        await ctx.message.delete()
        embed = discord.Embed(
            title="🛡️ ∙ Whitelist Management",
            description="Use `??whitelist add [@user]` or `??whitelist remove [@user]`.",
            color=discord.Color.from_rgb(255, 182, 193)
        )
        await ctx.send(embed=embed, delete_after=10)

    @whitelist_group.command(name="add")
    @commands.has_permissions(administrator=True)
    async def whitelist_add(self, ctx, member: discord.Member):
        """Adds a trusted staff member to the whitelist."""
        await ctx.message.delete()
        if member.id not in self.whitelisted_users:
            self.whitelisted_users.append(member.id)
            embed = discord.Embed(
                title="✨ ∙ Member Whitelisted",
                description=f"{member.mention} has been added to the Anti-Nuke whitelist.",
                color=discord.Color.from_rgb(152, 251, 152)
            )
        else:
            embed = discord.Embed(
                title="⚠️ ∙ Already Whitelisted",
                description=f"{member.mention} is already in the whitelist.",
                color=discord.Color.from_rgb(255, 182, 193)
            )
        embed.set_footer(text="Moonlings Security Suite 🌸")
        await ctx.send(embed=embed, delete_after=10)

    @whitelist_group.command(name="remove")
    @commands.has_permissions(administrator=True)
    async def whitelist_remove(self, ctx, member: discord.Member):
        """Removes a staff member from the whitelist."""
        await ctx.message.delete()
        if member.id in self.whitelisted_users:
            self.whitelisted_users.remove(member.id)
            embed = discord.Embed(
                title="🛡️ ∙ Whitelist Removed",
                description=f"{member.mention} has been removed from the Anti-Nuke whitelist.",
                color=discord.Color.from_rgb(255, 182, 193)
            )
        else:
            embed = discord.Embed(
                title="❌ ∙ Not Found",
                description=f"{member.mention} is not in the whitelist.",
                color=discord.Color.from_rgb(255, 182, 193)
            )
        embed.set_footer(text="Moonlings Security Suite 🌸")
        await ctx.send(embed=embed, delete_after=10)

    @commands.command(name="whitelisted")
    @commands.has_permissions(administrator=True)
    async def show_whitelisted(self, ctx):
        """Shows the list of trusted staff members bypassed by Anti-Nuke."""
        await ctx.message.delete()
        if not self.whitelisted_users:
            description = "No members currently whitelisted."
        else:
            description = "\n".join([f"• <@{uid}> (`{uid}`)" for uid in self.whitelisted_users])

        embed = discord.Embed(
            title="🛡️ ∙ Anti-Nuke Whitelisted Staff",
            description=description,
            color=discord.Color.from_rgb(152, 251, 152)
        )
        embed.set_footer(text="Moonlings Security Suite 🌸")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Security(bot))
