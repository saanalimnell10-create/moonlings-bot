import discord
from discord.ext import commands
import json
import os

PERMS_FILE = "fake_permissions.json"

def load_fake_perms():
    if os.path.exists(PERMS_FILE):
        with open(PERMS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_fake_perms(data):
    with open(PERMS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

class FakePermissions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.fake_perms = load_fake_perms()

    def get_role_perms(self, guild_id, role_id):
        guild_str = str(guild_id)
        role_str = str(role_id)
        return self.fake_perms.get(guild_str, {}).get(role_str, [])

    # --- KOMENNOT ---

    @commands.group(name="fakepermissions", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def fake_permissions(self, ctx):
        """Näyttää ohjeen fake permissions -järjestelmän käyttöön."""
        embed = discord.Embed(
            title="🔒 Custom Fake Permissions System",
            description=(
                "Manage bot command permissions for roles safely without native Discord admin permissions.\n\n"
                "**Subcommands:**\n"
                "`??fakepermissions grant [@role] [permissions]` – Grants specific permissions.\n"
                "`??fakepermissions list [@role]` – Views permissions for a role.\n"
                "`??fakepermissions remove [@role] [permissions]` – Revokes permissions.\n"
                "`??fakepermissions reset [@role]` – Resets all fake permissions for a role."
            ),
            color=0xFFB6C1
        )
        embed.set_footer(text="Moonlings Security Suite 🌸")
        await ctx.send(embed=embed)

    @fake_permissions.command(name="grant")
    @commands.has_permissions(administrator=True)
    async def grant_perm(self, ctx, role: discord.Role, *, permissions: str):
        """Grants specific bot command permissions to a role."""
        guild_str = str(ctx.guild.id)
        role_str = str(role.id)

        # Pilkotaan annetut oikeudet pilkulla tai välilyönnillä
        perm_list = [p.strip().lower() for p in permissions.replace(",", " ").split() if p.strip()]

        if guild_str not in self.fake_perms:
            self.fake_perms[guild_str] = {}

        if role_str not in self.fake_perms[guild_str]:
            self.fake_perms[guild_str][role_str] = []

        added = []
        for perm in perm_list:
            if perm not in self.fake_perms[guild_str][role_str]:
                self.fake_perms[guild_str][role_str].append(perm)
                added.append(perm)

        save_fake_perms(self.fake_perms)

        embed = discord.Embed(
            title="🔒 Fake Permissions Granted",
            description=f"Granted permissions to {role.mention}:\n`" + "`, `".join(added) + "`",
            color=0xFFB6C1
        )
        await ctx.send(embed=embed)

    @fake_permissions.command(name="list")
    async def list_perms(self, ctx, role: discord.Role):
        """Views all fake permissions granted to a specific role."""
        perms = self.get_role_perms(ctx.guild.id, role.id)

        if not perms:
            embed = discord.Embed(
                title="🔒 Fake Permissions List",
                description=f"No fake permissions currently assigned to {role.mention}.",
                color=0xFFB6C1
            )
        else:
            embed = discord.Embed(
                title=f"🔒 Fake Permissions for {role.name}",
                description="`" + "`, `".join(perms) + "`",
                color=0xFFB6C1
            )
        await ctx.send(embed=embed)

    @fake_permissions.command(name="remove")
    @commands.has_permissions(administrator=True)
    async def remove_perm(self, ctx, role: discord.Role, *, permissions: str):
        """Revokes specific fake permissions from a role."""
        guild_str = str(ctx.guild.id)
        role_str = str(role.id)

        perm_list = [p.strip().lower() for p in permissions.replace(",", " ").split() if p.strip()]

        if guild_str in self.fake_perms and role_str in self.fake_perms[guild_str]:
            removed = []
            for perm in perm_list:
                if perm in self.fake_perms[guild_str][role_str]:
                    self.fake_perms[guild_str][role_str].remove(perm)
                    removed.append(perm)

            save_fake_perms(self.fake_perms)

            if removed:
                embed = discord.Embed(
                    title="🔒 Fake Permissions Revoked",
                    description=f"Removed permissions from {role.mention}:\n`" + "`, `".join(removed) + "`",
                    color=0xFFB6C1
                )
            else:
                embed = discord.Embed(
                    title="🔒 No Changes Made",
                    description=f"None of the specified permissions were found on {role.mention}.",
                    color=0xFFB6C1
                )
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"❌ Role {role.mention} has no active fake permissions.", delete_after=5)

    @fake_permissions.command(name="reset")
    @commands.has_permissions(administrator=True)
    async def reset_perms(self, ctx, role: discord.Role):
        """Resets all fake permissions for a role."""
        guild_str = str(ctx.guild.id)
        role_str = str(role.id)

        if guild_str in self.fake_perms and role_str in self.fake_perms[guild_str]:
            del self.fake_perms[guild_str][role_str]
            save_fake_perms(self.fake_perms)

            embed = discord.Embed(
                title="🔒 Fake Permissions Reset",
                description=f"Successfully cleared all fake permissions for {role.mention}.",
                color=0xFFB6C1
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"❌ Role {role.mention} has no active fake permissions.", delete_after=5)


async def setup(bot):
    await bot.add_cog(FakePermissions(bot))
