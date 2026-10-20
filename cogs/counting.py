import discord
from discord.ext import commands

class Counting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.counting_channel_id = None
        self.current_count = 0
        self.last_user_id = None

    # 1. SETCOUNTING COMMAND (Aseta laskentakanava)
    @commands.command(name="setcounting")
    @commands.has_permissions(administrator=True)
    async def set_counting(self, ctx):
        await ctx.message.delete()
        self.counting_channel_id = ctx.channel.id
        self.current_count = 0
        self.last_user_id = None
        
        embed = discord.Embed(
            title="🔢 ∙ Chill Counting Channel Set!",
            description="This channel is now configured for starry counting! 🌟\nStart counting from **1**~ 🌸✨\n\n*(Don't worry, mistakes won't reset the score!)*",
            color=discord.Color.from_rgb(175, 238, 238)
        )
        embed.set_footer(text="Moonlings Chill Counting ☁️", icon_url=self.bot.user.display_avatar.url)
        await ctx.send(embed=embed)

    # 2. MESSAGE LISTENER (Tarkkailee laskentakanavan viestejä)
    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignorataan botit
        if message.author.bot:
            return

        # Tarkistetaan onko viesti laskentakanavalla
        if self.counting_channel_id and message.channel.id == self.counting_channel_id:
            # Jos viesti on pelkkä numero
            if message.content.isdigit():
                user_number = int(message.content)

                # Eihän sama käyttäjä laske kahdesti peräkkäin
                if message.author.id == self.last_user_id:
                    await message.add_reaction("❌")
                    await message.channel.send(
                        f"⚠️ {message.author.mention}, you can't count twice in a row, cutie! The next number is still **{self.current_count + 1}**~ 🌸"
                    )
                    return

                # Tarkistetaan onko numero oikein
                if user_number == self.current_count + 1:
                    self.current_count += 1
                    self.last_user_id = message.author.id
                    await message.add_reaction("✅")
                else:
                    await message.add_reaction("❌")
                    await message.channel.send(
                        f"❌ Oopsie {message.author.mention}! That's the wrong number, but we don't reset here~ The next number is **{self.current_count + 1}**! ✨"
                    )

async def setup(bot):
    await bot.add_cog(Counting(bot))
