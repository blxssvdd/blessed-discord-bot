import discord
from datetime import datetime
import json
import os

BIRTHDAY_FILE = "birthdays.json"

def load_birthdays():
    if not os.path.exists(BIRTHDAY_FILE):
        return {}
    with open(BIRTHDAY_FILE, "r") as file:
        return json.load(file)

def save_birthdays(data):
    with open(BIRTHDAY_FILE, "w") as file:
        json.dump(data, file, indent=4)

def setup(bot):
    @bot.tree.command(name="set_birthday", description="Установить свою дату рождения (ГГГГ-ММ-ДД)")
    async def set_birthday(interaction: discord.Interaction, date: str):
        try:
            datetime.strptime(date, "%Y-%m-%d")
            data = load_birthdays()
            data[str(interaction.user.id)] = date
            save_birthdays(data)
            await interaction.response.send_message(f"✅ Твоя дата рождения сохранена: **{date}**")
        except ValueError:
            await interaction.response.send_message("❌ Неверный формат! Используй `ГГГГ-ММ-ДД`.", ephemeral=True)

    @bot.tree.command(name="birthday_countdown", description="Узнать, сколько осталось до дня рождения")
    async def birthday_countdown(interaction: discord.Interaction):
        data = load_birthdays()
        user_id = str(interaction.user.id)

        if user_id not in data:
            await interaction.response.send_message("📅 Ты ещё не установил дату рождения. Используй `/set_birthday`.", ephemeral=True)
            return

        try:
            birthdate = datetime.strptime(data[user_id], "%Y-%m-%d")
            now = datetime.now()
            next_birthday = birthdate.replace(year=now.year)

            if next_birthday < now:
                next_birthday = next_birthday.replace(year=now.year + 1)

            days_left = (next_birthday - now).days

            if days_left == 0:
                await interaction.response.send_message("🎉 Сегодня твой день рождения! С праздником! 🥳")
            else:
                await interaction.response.send_message(f"⏳ До твоего дня рождения осталось **{days_left}** дней.")
        except Exception as e:
            await interaction.response.send_message(f"⚠️ Ошибка при подсчёте: {e}", ephemeral=True)
