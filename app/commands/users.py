import discord

def setup(bot):
    @bot.tree.command(name="userinfo", description="Показать информацию о пользователе")
    async def userinfo(
        interaction: discord.Interaction,
        пользователь: discord.Member = None
    ):
        member = пользователь or interaction.user

        roles = [role.mention for role in getattr(member, "roles", [])[1:]] if isinstance(member, discord.Member) else []
        is_owner = getattr(interaction.guild, "owner_id", None) == member.id if hasattr(interaction, "guild") else False

        embed = discord.Embed(
            title="👤 Информация о пользователе",
            color=member.color if isinstance(member, discord.Member) else discord.Color.blurple()
        )
        embed.set_thumbnail(url=member.display_avatar.url)

        embed.add_field(name="Имя пользователя", value=f"**{member.name}**", inline=False)
        embed.add_field(name="Отображаемое имя", value=f"{member.display_name}", inline=False)
        embed.add_field(
            name="Тип",
            value=f"Пользователь{' (Владелец сервера)' if is_owner else ''}",
            inline=False
        )
        if isinstance(member, discord.Member):
            embed.add_field(name="Участник сервера", value="Да", inline=False)
            embed.add_field(name="Серверный никнейм", value=member.nick or member.display_name, inline=False)
            embed.add_field(name="Присоединился", value=member.joined_at.strftime('%d %B %Y г. %H:%M'), inline=False)
        else:
            embed.add_field(name="Участник сервера", value="Нет", inline=False)
        embed.add_field(name="ID пользователя", value=f"{member.id}", inline=False)
        embed.add_field(name="Аватар", value=f"[Открыть]({member.display_avatar.url})", inline=False)
        embed.add_field(
            name="Дата создания аккаунта",
            value=member.created_at.strftime('%d %B %Y г. %H:%M'),
            inline=False
        )
        if roles:
            embed.add_field(name="Роли", value=" ".join(roles), inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=False)