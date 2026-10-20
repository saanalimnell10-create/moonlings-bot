import discord
from discord.ext import commands

class AFK(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.afk_users = {}  # Tallentaa {user_id: {"reason": syy, "pings": [viestit]}}

    # 1. AFK COMMAND (Aseta AFK-tila päälle)
    @commands.command(name="afk")
    async def afk_command(self, ctx, *, reason: str = "Taking a cozy little nap~ 🌙"):
        await ctx.message.delete()
        user = ctx.author
        
        # Tallennetaan käyttäjä AFK-listaan
        self.afk_users[user.id] = {
            "reason": reason,
            "pings": []
        }

        # Vaihdetaan nimimerkkiin [AFK]-tagi (jos botilla on oikeudet)
        try:
            original_nick = user.nick or user.name
            if not original_nick.startswith("[AFK]"):
                await user.edit(nick=f"[AFK] {original_nick}")
        except Exception:
            pass # Jos botilla ei ole oikeuksia vaihtaa nimeä, jatketaan silti normaalisti

        embed = discord.Embed(
            title="💤 ∙ AFK Mode Activated",
            description=f"Sweet dreams, **{user.mention}**! I've set your status to AFK~ ✨",
            color=discord.Color.from_rgb(176, 224, 230)
        )
        embed.add_field(name="Reason", value=f"```{reason}```", inline=False)
        embed.set_footer(text="Moonlings AFK System 🌙", icon_url=user.display_avatar.url)
        
        await ctx.send(embed=embed, delete_after=10)

    # 2. LISTENER (Tarkkailee viestejä: paluu & pingien tallennus)
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        user = message.author

        # TARKISTUS A: Jos AFK-käyttäjä kirjoittaa chättiin -> poistetaan AFK-tila
        if user.id in self.afk_users:
            afk_data = self.afk_users.pop(user.id)
            pings_received = afk_data["pings"]

            # Palautetaan alkuperäinen nimi
            try:
                current_nick = user.nick or user.name
                if current_nick.startswith("[AFK]"):
                    clean_nick = current_nick.replace("[AFK]", "").strip()
                    await user.edit(nick=clean_nick)
            except Exception:
                pass

            # Lähetetään tervetuloa takaisin -viesti ja lista pingeistä
            embed = discord.Embed(
                title="✨ ∙ Welcome Back!",
                description=f"Welcome back, **{user.mention}**! I've removed your [AFK] tag~ 🌸",
                color=discord.Color.from_rgb(255, 182, 193)
            )

            if pings_received:
                ping_summary = "\n".join(pings_received[:10]) # Näytetään enintään 10 uusinta pingiä
                embed.add_field(name="📬 Pings while you were away:", value=f"```{ping_summary}```", inline=False)
            else:
                embed.add_field(name="📬 Pings while you were away:", value="```No one pinged you! Such a peaceful nap~ ☁️```", inline=False)

            embed.set_footer(text="Moonlings AFK System 🌙", icon_url=user.display_avatar.url)
            await message.channel.send(embed=embed, delete_after=15)

        # TARKISTUS B: Jos joku mainitsee (pingaa) AFK-käyttäjän
        if message.mentions:
            for mentioned_user in message.mentions:
                if mentioned_user.id in self.afk_users:
                    reason = self.afk_users[mentioned_user.id]["reason"]
                    
                    # Tallennetaan ping muistiin
                    ping_msg = f"{message.author.display_name}: \"{message.content}\" (in #{message.channel.name})"
                    self.afk_users[mentioned_user.id]["pings"].append(ping_msg)

                    embed = discord.Embed(
                        title="💤 ∙ User is currently AFK",
                        description=f"**{mentioned_user.display_name}** is taking a break right now~ 🌸",
                        color=discord.Color.from_rgb(230, 230, 250)
                    )
                    embed.add_field(name="Reason", value=f"```{reason}```", inline=False)
                    embed.set_footer(text="They will see your ping when they return! ✨", icon_url=mentioned_user.display_avatar.url)
                    
                    await message.channel.send(embed=embed, delete_after=8)

async def setup(bot):
    async def setup(bot):
        await bot.add_cog(AFK(bot))
