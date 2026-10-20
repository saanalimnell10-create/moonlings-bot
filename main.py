import os
from datetime import timedelta
import discord
from discord.ext import commands

# Set up bot intents
intents = discord.Intents.default()
intents.message_content = True

# Initialize bot with prefix '!'
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("Moonlings bot is online and ready!")

# 1. SAY COMMAND - Bot repeats your message and deletes original
@bot.command(name="say")
async def say_command(ctx, *, message: str):
    await ctx.message.delete()
    await ctx.send(message)

# 2. REPLY COMMAND - Bot replies to a specific message ID
@bot.command(name="reply")
async def reply_command(ctx, message_id: int, *, message: str):
    try:
        msg = await ctx.channel.fetch_message(message_id)
        await msg.reply(message)
        await ctx.message.delete()
    except discord.NotFound:
        await ctx.send("Message not found! Please check the ID.", delete_after=5)

# 3. KICK COMMAND
@bot.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick_command(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"Done! {member.mention} has been kicked from the server.")

@kick_command.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to kick members!")

# 4. BAN COMMAND
@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban_command(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"Done! {member.mention} has been banned from the server.")

@ban_command.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to ban members!")

# 5. MUTE / TIMEOUT COMMAND
@bot.command(name="mute")
@commands.has_permissions(moderate_members=True)
async def mute_command(ctx, member: discord.Member, minutes: int, *, reason=None):
    duration = timedelta(minutes=minutes)
    await member.timeout(duration, reason=reason)
    await ctx.send(f"Done! {member.mention} has been muted for {minutes} minutes.")

@mute_command.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to mute members!")

# Get secret token from environment variables
TOKEN = os.getenv("DISCORD_TOKEN")

if TOKEN:
    bot.run(TOKEN)
else:
    print("Error: DISCORD_TOKEN not found! Please check environment variables.")
