import discord
from discord.ext import commands

class Reply(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="reply")
    @commands.has_permissions(manage_messages=True)
    async def reply_command(self, ctx, message_id: int, *, message_text: str):
        await ctx.message.delete()

        # Etsitään viesti kanavalta ID:n perusteella
        try:
            target_message = await ctx.channel.fetch_message(message_id)
        except discord.NotFound:
            await ctx.send("❌ Could not find a message with that ID in this channel, sweetie~", delete_after=5)
            return
        except discord.HTTPException:
            await ctx.send("❌ Failed to fetch the message. Please check the ID and try again~", delete_after=5)
            return

        # Vastataan suoraan tavallisella tekstiviestillä (Discord tekee siihen sen pienen vastausviivan)
        await target_message.reply(message_text)

    @reply_command.error
    async def reply_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ Usage: `??reply [message_id] [message_text]`~", delete_after=5)
        elif isinstance(error, commands.BadArgument):
            await ctx.send("❌ Please provide a valid numerical message ID~", delete_after=5)
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to use this command, cutie~", delete_after=5)

async def setup(bot):
    await bot.add_cog(Reply(bot))
