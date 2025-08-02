import discord
import random

def setup(bot):
    @bot.tree.command(name="8ball", description="Магический шар предскажет судьбу")
    async def eight_ball(interaction: discord.Interaction, вопрос: str):
        ответы = [
            "Без сомнений!",
            "Вероятно да.",
            "Спроси позже...",
            "Не думаю.",
            "Определённо нет.",
            "Абсолютно точно!"
        ]
        await interaction.response.send_message(f"🎱 {random.choice(ответы)}")

    @bot.tree.command(name="coinflip", description="Бросить монетку")
    async def coinflip(interaction: discord.Interaction):
        результат = random.choice(["Орёл 🪙", "Решка 🪙"])
        await interaction.response.send_message(f"Монетка показывает: **{результат}**")

    @bot.tree.command(name="joke", description="Случайная шутка")
    async def joke(interaction: discord.Interaction):
        шутки = [
            "Почему Python не может танцевать? Потому что у него нет class!",
            "Я бы рассказал шутку про Java... но она слишком долго загружается.",
            "Бот завис. Перезагрузка чувства юмора..."
        ]
        await interaction.response.send_message(random.choice(шутки))

    @bot.tree.command(name="say", description="Пишет ваш текст от имени бота (анонимно)")
    async def say(interaction: discord.Interaction, text: str):
        await interaction.response.send_message("✅ Сообщение отправлено анонимно.", ephemeral=True)
        await interaction.channel.send(text)
