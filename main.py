import os
import asyncio
from datetime import timedelta
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# Flask server to keep Render web service happy
app = Flask('')

@app.route('/')
def home():
    return "Bot is online!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="??", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("Moonlings bot is online and ready!")
    await bot.change_presence(activity=discord.Game(name="??help | Moonlings"))

# ----------------- CUSTOM EMBED HELP COMMAND -----------------
@bot.command(name="help")
async def custom_help(ctx):
    embed = discord.Embed(
        title="🌙 Moonlings Bot Commands",
        description="Here is the list of available commands for **Moonlings Bot**!",
        color=discord.Color.purple()
    )
    
    embed.add_field(
        name="🛠️ Moderation Commands",
        value=(
            "`??kick @user [reason]` - Kick a member from the server\n"
            "`??ban @user [reason]` - Ban a member from the server\n"
            "`??mute @user [minutes] [reason]` - Timeout/Mute a member"
        ),
        inline=False
    )
    
    embed.add_field(
        name="💬 Utility Commands",
        value=(
            "`??say [message]` - Bot repeats your message\n"
            "`??reply [message_id] [message]` - Bot replies to a specific message ID"
        ),
        inline=False
    )

    embed.add_field(
        name="🎫 Ticket System",
        value=(
            "`??ticket` - Creates a private support ticket channel\n"
            "`??close` - Closes/deletes the ticket channel (use inside ticket channel)"
        ),
        inline=False
    )
    
    embed.set_footer(text="Moonlings Automation & Moderation", icon_url=bot.user.display_avatar.url)
    
    await ctx.send(embed=embed)

# ----------------- TICKET SYSTEM -----------------
@bot.command(name="ticket")
async def create_ticket(ctx):
    guild = ctx.guild
    member = ctx.author
    
    category = discord.utils.get(guild.categories, name="Tickets")
    if not category:
        category = await guild.create_category("Tickets")
        
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        member: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
    }
    
    channel_name = f"ticket-{member.name}".lower().replace(" ", "-")
    ticket_channel = await guild.create_text_channel(name=channel_name, category=category, overwrites=overwrites)
    
    embed = discord.Embed(
        title="🎫 Ticket Opened",
        description=f"Hello {member.mention}, welcome to your support ticket!\nPlease state your issue and staff will assist you shortly.\n\nType `??close` to close this ticket.",
        color=discord.Color.blue()
    )
    await ticket_channel.send(embed=embed)
    await ctx.send(f"✅ Ticket created! Check {ticket_channel.mention}", delete_after=5)

@bot.command(name="close")
async def close_ticket(ctx):
    if "ticket-" in ctx.channel.name:
        await ctx.send("Closing ticket in 5 seconds...")
        await asyncio.sleep(5)
        await ctx.channel.delete()
    else:
        await ctx.send("❌ This command can only be used inside a ticket channel!")

# ----------------- OTHER COMMANDS -----------------
@bot.command(name="say")
async def say_command(ctx, *, message: str):
    await ctx.message.delete()
    await ctx.send(message)

@bot.command(name="reply")
async def reply_command(ctx, message_id: int, *, message: str):
    try:
        msg = await ctx.channel.fetch_message(message_id)
        await msg.reply(message)
        await ctx.message.delete()
    except discord.NotFound:
        await ctx.send("Message not found! Please check the ID.", delete_after=5)

@bot.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick_command(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"Done! {member.mention} has been kicked from the server.")

@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban_command(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"Done! {member.mention} has been banned from the server.")

@bot.command(name="mute")
@commands.has_permissions(moderate_members=True)
async def mute_command(ctx, member: discord.Member, minutes: int, *, reason=None):
    duration = timedelta(minutes=minutes)
    await member.timeout(duration, reason=reason)
    await ctx.send(f"Done! {member.mention} has been muted for {minutes} minutes.")

# Start server & bot
TOKEN = os.getenv("DISCORD_TOKEN")

if TOKEN:
    keep_alive()
    bot.run(TOKEN)
else:
    print("Error: DISCORD_TOKEN not found!")
