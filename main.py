import os

import discord
from discord.ext import commands


# =========================================================
# ENVIRONMENT VARIABLES
# =========================================================

TOKEN = os.getenv("DISCORD_TOKEN")

print("========================================")
print("RAILWAY ENV DEBUG")
print("========================================")

print(
    "DISCORD_TOKEN existe:",
    TOKEN is not None
)

print(
    "DISCORD_TOKEN vazio:",
    not bool(TOKEN)
)

if TOKEN:
    print(
        "Token começa por:",
        TOKEN[:5]
    )

    print(
        "Token termina em:",
        TOKEN[-5:]
    )

print("========================================")


if not TOKEN:
    raise RuntimeError(
        "❌ DISCORD_TOKEN não chegou ao container da Railway."
    )


# =========================================================
# INTENTS
# =========================================================

intents = discord.Intents.default()

intents.guilds = True
intents.members = True


# =========================================================
# BOT
# =========================================================

bot = commands.Bot(
    command_prefix="/",
    intents=intents
)


# =========================================================
# LOAD COGS
# =========================================================

async def load_cogs():

    for filename in os.listdir("./cogs"):

        if filename.endswith(".py") and not filename.startswith("_"):

            try:

                await bot.load_extension(
                    f"cogs.{filename[:-3]}"
                )

                print(
                    f"✅ Loaded: {filename}"
                )

            except Exception as e:

                print(
                    f"❌ Erro ao carregar {filename}: {e}"
                )


# =========================================================
# SETUP HOOK
# =========================================================

@bot.event
async def setup_hook():

    print(
        "🔄 A carregar cogs..."
    )

    await load_cogs()

    print(
        "✅ Todos os cogs foram carregados."
    )


# =========================================================
# READY
# =========================================================

@bot.event
async def on_ready():

    print()

    print(
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )

    print(
        f"✅ Bot online: {bot.user}"
    )

    print(
        f"🆔 Bot ID: {bot.user.id}"
    )

    print(
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )

    try:

        synced = await bot.tree.sync()

        print(
            f"✅ {len(synced)} slash commands sincronizados."
        )

    except Exception as e:

        print(
            f"❌ Erro ao sincronizar comandos: {e}"
        )


# =========================================================
# START
# =========================================================

print(
    "🚀 A iniciar o Hustler Bot..."
)

bot.run(TOKEN)