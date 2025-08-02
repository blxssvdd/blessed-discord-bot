import discord

def setup(bot):
    @bot.event
    async def on_guild_join(guild):
        # Попытка найти системный канал для приветствий
        channel = guild.system_channel

        # Если системный канал не задан, ищем первый доступный текстовый канал
        if channel is None:
            for ch in guild.text_channels:
                if ch.permissions_for(guild.me).send_messages:
                    channel = ch
                    break

        if channel is None:
            return

        embed = discord.Embed(
            title="🤖 Sukuna Discord Bot",
            description=(
                "Добро пожаловать в **Sukuna Discord Bot**!\n\n"
                "Этот бот создан для того, чтобы сделать ваш сервер уютнее, веселее и безопаснее.\n"
                "Он сочетает в себе развлечения, напоминания о днях рождения и удобные инструменты для модерации.\n\n"
                "✨ **Возможности:**\n"
                "• Развлекательные команды (шар 8, монетка, шутки, анонимные сообщения)\n"
                "• Система дней рождения с напоминаниями\n"
                "• Мощные инструменты модерации (мут, бан, кик, очистка чата)\n\n"
                "🔗 [GitHub автора](https://github.com/blxssvdd)  |  🛠️ Автор: *blessed/blxssvd*\n"
                "Спасибо, что используете Sukuna! В будущем будет больше новых команд. Если есть вопросы или предложения — пишите автору. (blxssvd)"
            ),
            color=discord.Color.gold()
        )
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/4712/4712035.png")
        await channel.send(embed=embed)