import discord
from discord.ext import commands
import os
import asyncio
from utils.database import init_db

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot inicializado com sucesso como {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Sincronizado {len(synced)} comandos")
    except Exception as e:
        print(e)

async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"Carregado: {filename}")

async def main():
    init_db()
    await load_cogs()
    token = os.getenv("DISCORD_TOKEN")
    await bot.start(token)

asyncio.run(main())
