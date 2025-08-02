import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

from app.commands import birthday, fun, moderation, help, users, hello

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Бот вошёл как {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Синхронизировано {len(synced)} слэш-команд")
    except Exception as e:
        print(f"Ошибка синхронизации: {e}")


birthday.setup(bot)
fun.setup(bot)
moderation.setup(bot)
help.setup(bot)
users.setup(bot)
hello.setup(bot)

bot.run(DISCORD_TOKEN)