import discord
from discord.ext import commands
from datetime import timedelta
import json
import random
from config import PREFIX, STAFF_ROLE_ID
import os

TOKEN = os.getenv("TOKEN")

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

# ================= ERROR HANDLER =================

@bot.event
async def on_command_error(ctx, error):

    if isinstance(error, commands.MissingRequiredArgument):

        await ctx.send(
            "❌ Missing required arguments."
        )

    elif isinstance(error, commands.CommandNotFound):

        return

    elif isinstance(error, commands.MissingPermissions):

        await ctx.send(
            "❌ You don't have permission."
        )

    else:
        print(error)

# =========================================================
# PING
# =========================================================

@bot.command()
async def ping(ctx):

    latency = round(bot.latency * 1000)

    await ctx.send(f"🏓 Pong! {latency}ms")

@bot.slash_command(
    name="ping",
    description="Check bot ping"
)
async def slash_ping(ctx):

    latency = round(bot.latency * 1000)

    await ctx.respond(
        f"🏓 Pong! {latency}ms"
    )

# =========================================================
# BAN
# =========================================================

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason"):

    await member.ban(reason=reason)

    embed = discord.Embed(
        title="🔨 User Banned",
        color=discord.Color.red()
    )

    embed.add_field(
        name="User",
        value=member.mention
    )

    embed.add_field(
        name="Moderator",
        value=ctx.author.mention
    )

    embed.add_field(
        name="Reason",
        value=reason
    )

    await ctx.send(embed=embed)

@bot.slash_command(
    name="ban",
    description="Ban a member"
)
@commands.has_permissions(ban_members=True)
async def slash_ban(
    ctx,
    member: discord.Member,
    reason: str = "No reason"
):

    await member.ban(reason=reason)

    embed = discord.Embed(
        title="🔨 User Banned",
        color=discord.Color.red()
    )

    embed.add_field(
        name="User",
        value=member.mention
    )

    embed.add_field(
        name="Moderator",
        value=ctx.author.mention
    )

    embed.add_field(
        name="Reason",
        value=reason
    )

    await ctx.respond(embed=embed)

# =========================================================
# UNBAN
# =========================================================

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id: int):

    user = await bot.fetch_user(user_id)

    await ctx.guild.unban(user)

    await ctx.send(
        f"✅ Unbanned {user}"
    )

@bot.slash_command(
    name="unban",
    description="Unban a member"
)
@commands.has_permissions(ban_members=True)
async def slash_unban(
    ctx,
    user_id: str
):

    user = await bot.fetch_user(
        int(user_id)
    )

    await ctx.guild.unban(user)

    await ctx.respond(
        f"✅ Unbanned {user}"
    )

# =========================================================
# TIMEOUT
# =========================================================

@bot.command()
@commands.has_permissions(moderate_members=True)
async def timeout(
    ctx,
    member: discord.Member,
    minutes: int
):

    duration = timedelta(
        minutes=minutes
    )

    await member.timeout(duration)

    await ctx.send(
        f"⏳ Timed out {member.mention} for {minutes} minutes"
    )

@bot.slash_command(
    name="timeout",
    description="Timeout a member"
)
@commands.has_permissions(moderate_members=True)
async def slash_timeout(
    ctx,
    member: discord.Member,
    minutes: int
):

    duration = timedelta(
        minutes=minutes
    )

    await member.timeout(duration)

    await ctx.respond(
        f"⏳ Timed out {member.mention} for {minutes} minutes"
    )

# =========================================================
# REMOVE TIMEOUT
# =========================================================

@bot.command()
@commands.has_permissions(moderate_members=True)
async def removetimeout(
    ctx,
    member: discord.Member
):

    await member.timeout(None)

    await ctx.send(
        f"✅ Removed timeout from {member.mention}"
    )

@bot.slash_command(
    name="removetimeout",
    description="Remove timeout"
)
@commands.has_permissions(moderate_members=True)
async def slash_removetimeout(
    ctx,
    member: discord.Member
):

    await member.timeout(None)

    await ctx.respond(
        f"✅ Removed timeout from {member.mention}"
    )

# =========================================================
# KICK
# =========================================================

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(
    ctx,
    member: discord.Member
):

    await member.kick()

    await ctx.send(
        f"👢 Kicked {member.mention}"
    )

@bot.slash_command(
    name="kick",
    description="Kick a member"
)
@commands.has_permissions(kick_members=True)
async def slash_kick(
    ctx,
    member: discord.Member
):

    await member.kick()

    await ctx.respond(
        f"👢 Kicked {member.mention}"
    )

# =========================================================
# PURGE
# =========================================================

@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(
    ctx,
    amount: int
):

    await ctx.channel.purge(
        limit=amount + 1
    )

    msg = await ctx.send(
        f"🗑 Deleted {amount} messages"
    )

    await msg.delete(delay=3)

@bot.slash_command(
    name="purge",
    description="Delete messages"
)
@commands.has_permissions(manage_messages=True)
async def slash_purge(
    ctx,
    amount: int
):

    await ctx.channel.purge(
        limit=amount
    )

    await ctx.respond(
        f"🗑 Deleted {amount} messages",
        delete_after=3
    )

# =========================================================
# BALANCE
# =========================================================

@bot.command()
async def balance(ctx):

    user_id = str(ctx.author.id)

    if user_id not in credits:
        credits[user_id] = 0
        save_credits()

    await ctx.send(
        f"💰 Balance: {credits[user_id]}"
    )

@bot.slash_command(
    name="balance",
    description="Check balance"
)
async def slash_balance(ctx):

    user_id = str(ctx.author.id)

    if user_id not in credits:
        credits[user_id] = 0
        save_credits()

    await ctx.respond(
        f"💰 Balance: {credits[user_id]}"
    )

# =========================================================
# ADD CREDITS
# =========================================================

@bot.command()
async def addcredits(
    ctx,
    member: discord.Member,
    amount: int
):

    if not has_staff_role(ctx.author):
        return await ctx.send(
            "❌ No permission"
        )

    user_id = str(member.id)

    if user_id not in credits:
        credits[user_id] = 0

    credits[user_id] += amount

    save_credits()

    await ctx.send(
        f"✅ Added {amount} credits to {member.mention}"
    )

@bot.slash_command(
    name="addcredits",
    description="Add credits"
)
async def slash_addcredits(
    ctx,
    member: discord.Member,
    amount: int
):

    if not has_staff_role(ctx.author):
        return await ctx.respond(
            "❌ No permission"
        )

    user_id = str(member.id)

    if user_id not in credits:
        credits[user_id] = 0

    credits[user_id] += amount

    save_credits()

    await ctx.respond(
        f"✅ Added {amount} credits to {member.mention}"
    )

# =========================================================
# RIG ROCKET
# =========================================================

@bot.command()
async def rigrocket(ctx):

    if not has_staff_role(ctx.author):
        return await ctx.send(
            "❌ No permission"
        )

    game_settings["rocket_rigged"] = True

    save_settings()

    await ctx.send(
        "🚀 Rocket rig enabled"
    )

@bot.slash_command(
    name="rigrocket",
    description="Rig rocket"
)
async def slash_rigrocket(ctx):

    if not has_staff_role(ctx.author):
        return await ctx.respond(
            "❌ No permission"
        )

    game_settings["rocket_rigged"] = True

    save_settings()

    await ctx.respond(
        "🚀 Rocket rig enabled"
    )

# =========================================================
# UNRIG ROCKET
# =========================================================

@bot.command()
async def unrigrocket(ctx):

    if not has_staff_role(ctx.author):
        return await ctx.send(
            "❌ No permission"
        )

    game_settings["rocket_rigged"] = False

    save_settings()

    await ctx.send(
        "✅ Rocket rig disabled"
    )

@bot.slash_command(
    name="unrigrocket",
    description="Unrig rocket"
)
async def slash_unrigrocket(ctx):

    if not has_staff_role(ctx.author):
        return await ctx.respond(
            "❌ No permission"
        )

    game_settings["rocket_rigged"] = False

    save_settings()

    await ctx.respond(
        "✅ Rocket rig disabled"
    )

# =========================================================
# PLINKO
# =========================================================

@bot.command()
async def plinko(
    ctx,
    bet: int
):

    user_id = str(ctx.author.id)

    if user_id not in credits:
        credits[user_id] = 0

    if credits[user_id] < bet:
        return await ctx.send(
            "❌ Not enough credits"
        )

    credits[user_id] -= bet

    multiplier = random.choice([
        0.5,
        1,
        2,
        5
    ])

    winnings = int(
        bet * multiplier
    )

    credits[user_id] += winnings

    save_credits()

    embed = discord.Embed(
        title="🎯 Plinko",
        description=(
            f"Multiplier: {multiplier}x\n"
            f"Won: {winnings}"
        ),
        color=discord.Color.blurple()
    )

    await ctx.send(embed=embed)

@bot.slash_command(
    name="plinko",
    description="Play plinko"
)
async def slash_plinko(
    ctx,
    bet: int
):

    user_id = str(ctx.author.id)

    if user_id not in credits:
        credits[user_id] = 0

    if credits[user_id] < bet:
        return await ctx.respond(
            "❌ Not enough credits"
        )

    credits[user_id] -= bet

    multiplier = random.choice([
        0.5,
        1,
        2,
        5
    ])

    winnings = int(
        bet * multiplier
    )

    credits[user_id] += winnings

    save_credits()

    embed = discord.Embed(
        title="🎯 Plinko",
        description=(
            f"Multiplier: {multiplier}x\n"
            f"Won: {winnings}"
        ),
        color=discord.Color.blurple()
    )

    await ctx.respond(embed=embed)

# =========================================================
# TICKET SYSTEM
# =========================================================

SUPPORT_ROLE_ID = 1505989423760937040

GENERAL_SUPPORT_CATEGORY = 1506203152108621874
PLUGIN_BUY_CATEGORY = 1506203245540806686
BUG_REPORT_CATEGORY = 1506203360343363674
CUSTOM_BOT_CATEGORY = 1506203448880660560
BOT_SUPPORT_CATEGORY = 1506203521031077898
BOT_BUY_CATEGORY = 1506203613108768879

# =========================================================
# CLOSE / CLAIM / TRANSCRIPT VIEW
# =========================================================

class TicketControls(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    # ================= CLAIM =================

    @discord.ui.button(
        label="Claim",
        style=discord.ButtonStyle.green
    )
    async def claim_ticket(
        self,
        button,
        interaction
    ):

        role = interaction.guild.get_role(
            SUPPORT_ROLE_ID
        )

        if role not in interaction.user.roles:
            return await interaction.response.send_message(
                "❌ No permission",
                ephemeral=True
            )

        embed = discord.Embed(
            title="✅ Ticket Claimed",
            description=(
                f"{interaction.user.mention} "
                f"claimed this ticket."
            ),
            color=discord.Color.green()
        )

        await interaction.channel.send(
            embed=embed
        )

        await interaction.response.defer()

    # ================= TRANSCRIPT =================

    @discord.ui.button(
        label="Transcript",
        style=discord.ButtonStyle.blurple
    )
    async def transcript_ticket(
        self,
        button,
        interaction
    ):

        messages = []

        async for msg in interaction.channel.history(
            limit=None,
            oldest_first=True
        ):

            messages.append(
                f"{msg.author}: {msg.content}"
            )

        transcript = "\n".join(messages)

        with open(
            "transcript.txt",
            "w",
            encoding="utf-8"
        ) as f:

            f.write(transcript)

        await interaction.user.send(
            file=discord.File(
                "transcript.txt"
            )
        )

        await interaction.response.send_message(
            "📄 Transcript sent in DM.",
            ephemeral=True
        )

    # ================= CLOSE =================

    @discord.ui.button(
        label="Close",
        style=discord.ButtonStyle.red
    )
    async def close_ticket(
        self,
        button,
        interaction
    ):

        role = interaction.guild.get_role(
            SUPPORT_ROLE_ID
        )

        if role not in interaction.user.roles:
            return await interaction.response.send_message(
                "❌ No permission",
                ephemeral=True
            )

        await interaction.response.send_message(
            "🔒 Closing ticket..."
        )

        await interaction.channel.delete()

# =========================================================
# CREATE TICKET VIEW
# =========================================================

class TicketPanel(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    # =====================================================
    # GENERAL SUPPORT
    # =====================================================

    @discord.ui.button(
        label="General Support",
        style=discord.ButtonStyle.blurple
    )
    async def general_support(
        self,
        button,
        interaction
    ):

        await create_ticket(
            interaction,
            GENERAL_SUPPORT_CATEGORY,
            "general"
        )

    # =====================================================
    # PLUGIN BUY
    # =====================================================

    @discord.ui.button(
        label="Plugin Buy",
        style=discord.ButtonStyle.green
    )
    async def plugin_buy(
        self,
        button,
        interaction
    ):

        await create_ticket(
            interaction,
            PLUGIN_BUY_CATEGORY,
            "plugin"
        )

    # =====================================================
    # BUG REPORT
    # =====================================================

    @discord.ui.button(
        label="Bug Report",
        style=discord.ButtonStyle.red
    )
    async def bug_report(
        self,
        button,
        interaction
    ):

        await create_ticket(
            interaction,
            BUG_REPORT_CATEGORY,
            "bug"
        )

    # =====================================================
    # CUSTOM BOT
    # =====================================================

    @discord.ui.button(
        label="Custom Bot Order",
        style=discord.ButtonStyle.gray
    )
    async def custom_bot(
        self,
        button,
        interaction
    ):

        await create_ticket(
            interaction,
            CUSTOM_BOT_CATEGORY,
            "custom-bot"
        )

    # =====================================================
    # BOT SUPPORT
    # =====================================================

    @discord.ui.button(
        label="Discord Bot Problem",
        style=discord.ButtonStyle.red
    )
    async def bot_problem(
        self,
        button,
        interaction
    ):

        await create_ticket(
            interaction,
            BOT_SUPPORT_CATEGORY,
            "bot-support"
        )

    # =====================================================
    # BOT BUY
    # =====================================================

    @discord.ui.button(
        label="Discord Bot Buy",
        style=discord.ButtonStyle.green
    )
    async def bot_buy(
        self,
        button,
        interaction
    ):

        await create_ticket(
            interaction,
            BOT_BUY_CATEGORY,
            "bot-buy"
        )

# =========================================================
# CREATE TICKET FUNCTION
# =========================================================

async def create_ticket(
    interaction,
    category_id,
    ticket_type
):

    guild = interaction.guild

    category = guild.get_channel(
        category_id
    )

    role = guild.get_role(
        SUPPORT_ROLE_ID
    )

    overwrites = {

        guild.default_role:
        discord.PermissionOverwrite(
            view_channel=False
        ),

        interaction.user:
        discord.PermissionOverwrite(
            view_channel=True,
            send_messages=True
        ),

        role:
        discord.PermissionOverwrite(
            view_channel=True,
            send_messages=True
        )
    }

    channel = await guild.create_text_channel(

        name=f"{ticket_type}-{interaction.user.name}",

        category=category,

        overwrites=overwrites
    )

    embed = discord.Embed(
        title="🎫 Support Ticket",
        description=(
            f"{interaction.user.mention}\n\n"
            "Please explain your issue.\n"
            "Staff will assist you soon."
        ),
        color=discord.Color.blurple()
    )

    await channel.send(
        f"{interaction.user.mention} "
        f"<@&{SUPPORT_ROLE_ID}>",
        embed=embed,
        view=TicketControls()
    )

    await interaction.response.send_message(
        f"✅ Ticket created: {channel.mention}",
        ephemeral=True
    )

# =========================================================
# SEND PANEL COMMAND
# =========================================================

@bot.command()
async def sendpanel(ctx):

    if not has_staff_role(ctx.author):
        return await ctx.send(
            "❌ No permission"
        )

    embed = discord.Embed(
        title="🎫 Evonix Support Panel",
        description=(
            "Choose a category below "
            "to create a ticket."
        ),
        color=discord.Color.purple()
    )

    embed.add_field(
        name="General Support",
        value="General help & support",
        inline=False
    )

    embed.add_field(
        name="Plugin Buy",
        value="Purchase plugins",
        inline=False
    )

    embed.add_field(
        name="Bug Report",
        value="Report bugs/issues",
        inline=False
    )

    embed.add_field(
        name="Custom Bot Order",
        value="Order custom bots",
        inline=False
    )

    embed.add_field(
        name="Discord Bot Problem",
        value="Bot support/issues",
        inline=False
    )

    embed.add_field(
        name="Discord Bot Buy",
        value="Purchase Discord bots",
        inline=False
    )

    await ctx.send(
        embed=embed,
        view=TicketPanel()
    )



# =========================================================
# RUN
# =========================================================

bot.run(TOKEN)
