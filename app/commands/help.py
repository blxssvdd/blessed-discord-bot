import discord

def setup(bot):
    @bot.tree.command(name="help", description="Показать список доступных команд")
    async def help_command(interaction: discord.Interaction):
        embed = discord.Embed(
            title="Справка по командам",
            description="Вот список доступных команд по категориям:",
            color=discord.Color.blurple()
        )

        # 🎉 Развлекательные
        embed.add_field(name="🎉 Развлекательные", value=
            "/8ball [вопрос] — Магический шар предскажет судьбу\n"
            "/coinflip — Бросить монетку\n"
            "/joke — Случайная шутка\n"
            "/say [текст] — Пишет ваш текст от имени бота",
            inline=False
        )

        # 📅 Дни рождения
        embed.add_field(name="📅 Дни рождения", value=
            "/set_birthday [дата] — Установить свою дату рождения (ГГГГ-ММ-ДД)\n"
            "/birthday_countdown — Узнать, сколько осталось до дня рождения",
            inline=False
        )

        # 🛡️ Модерация
        embed.add_field(name="🛡️ Модерация", value=
            "/kick [участник] [причина] — Кикнуть участника\n"
            "/ban [участник] [причина] — Забанить участника\n"
            "/unban [user_id] — Разбанить пользователя по ID\n"
            "/mute [участник] [время] [причина] — Выдать мут (timeout)\n"
            "/unmute [участник] — Снять мут\n"
            "/clear [кол-во] — Очистить сообщения",
            inline=False
        )

        # ℹ️ Прочее
        embed.add_field(name="ℹ️ Прочее", value=
            "/help — Показать это сообщение\n"
            "/about — О боте\n"
            "/userinfo [пользователь] — Показать информацию о пользователе",
            inline=False
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @bot.tree.command(name="about", description="Информация о боте")
    async def about_command(interaction: discord.Interaction):
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
        await interaction.response.send_message(embed=embed, ephemeral=True)