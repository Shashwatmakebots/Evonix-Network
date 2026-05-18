import discord
from discord.ext import commands
from datetime import timedelta
import json
import random
from config import TOKEN, PREFIX, STAFF_ROLE_ID

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix=PREFIX,
    intents=intents,
    help_command=None
)

# ================= LOAD FILES =================

try:
    with open("credits.json", "r") as f:
        credits = json.load(f)
except:
    credits = {}

try:
    with open("game_settings.json", "r") as f:
        game_settings = json.load(f)
except:
    game_settings = {
        "rocket_rigged": False
    }

# ================= SAVE =================

def save_credits():
    with open("credits.json", "w") as f:
        json.dump(credits, f, indent=4)

def save_settings():
    with open("game_settings.json", "w") as f:
        json.dump(game_settings, f, indent=4)

# ================= ROLE CHECK =================

def has_staff_role(member):
    return any(role.id == STAFF_ROLE_ID for role in member.roles)

# ================= READY =================

@bot.event
async def on_ready():

    print(f"Logged in as {bot.user}")

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash commands")
    except Exception as e:
        print(e)

# ================= PING =================

@bot.command()
async def ping(ctx):

    latency = round(bot.latency * 1000)

    await ctx.send(f"🏓 Pong! {latency}ms")

# ================= BAN =================

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason"):

    await member.ban(reason=reason)

    embed = discord.Embed(
        title="🔨 User Banned",
        color=discord.Color.red()
    )

    embed.add_field(name="User", value=member.mention)
    embed.add_field(name="Moderator", value=ctx.author.mention)
    embed.add_field(name="Reason", value=reason)

    await ctx.send(embed=embed)

# ================= UNBAN =================

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id: int):

    user = await bot.fetch_user(user_id)

    await ctx.guild.unban(user)

    await ctx.send(f"✅ Unbanned {user}")

# ================= TIMEOUT =================

@bot.command()
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, member: discord.Member, minutes: int):

    duration = timedelta(minutes=minutes)

    await member.timeout(duration)

    await ctx.send(
        f"⏳ Timed out {member.mention} for {minutes} minutes"
    )

# ================= REMOVE TIMEOUT =================

@bot.command()
@commands.has_permissions(moderate_members=True)
async def removetimeout(ctx, member: discord.Member):

    await member.timeout(None)

    await ctx.send(
        f"✅ Removed timeout from {member.mention}"
    )

# ================= KICK =================

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member):

    await member.kick()

    await ctx.send(f"👢 Kicked {member.mention}")

# ================= PURGE =================

@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int):

    await ctx.channel.purge(limit=amount + 1)

    msg = await ctx.send(
        f"🗑 Deleted {amount} messages"
    )

    await msg.delete(delay=3)

# ================= BALANCE =================

@bot.command()
async def balance(ctx):

    user_id = str(ctx.author.id)

    if user_id not in credits:
        credits[user_id] = 0
        save_credits()

    await ctx.send(
        f"💰 Balance: {credits[user_id]}"
    )

# ================= ADD CREDITS =================

@bot.command()
async def addcredits(ctx, member: discord.Member, amount: int):

    if not has_staff_role(ctx.author):
        return await ctx.send("❌ No permission")

    user_id = str(member.id)

    if user_id not in credits:
        credits[user_id] = 0

    credits[user_id] += amount

    save_credits()

    await ctx.send(
        f"✅ Added {amount} credits to {member.mention}"
    )

# ================= RIG ROCKET =================

@bot.command()
async def rigrocket(ctx):

    if not has_staff_role(ctx.author):
        return await ctx.send("❌ No permission")

    game_settings["rocket_rigged"] = True

    save_settings()

    await ctx.send("🚀 Rocket rig enabled")

# ================= UNRIG ROCKET =================

@bot.command()
async def unrigrocket(ctx):

    if not has_staff_role(ctx.author):
        return await ctx.send("❌ No permission")

    game_settings["rocket_rigged"] = False

    save_settings()

    await ctx.send("✅ Rocket rig disabled")

# ================= PLINKO =================

@bot.command()
async def plinko(ctx, bet: int):

    user_id = str(ctx.author.id)

    if user_id not in credits:
        credits[user_id] = 0

    if credits[user_id] < bet:
        return await ctx.send("❌ Not enough credits")

    credits[user_id] -= bet

    multiplier = random.choice([
        0.5,
        1,
        2,
        5
    ])

    winnings = int(bet * multiplier)

    credits[user_id] += winnings

    save_credits()

    embed = discord.Embed(
        title="🎯 Plinko",
        description=f"Multiplier: {multiplier}x\nWon: {winnings}",
        color=discord.Color.blurple()
    )

    await ctx.send(embed=embed)

# ================= RUN =================

bot.run(TOKEN)