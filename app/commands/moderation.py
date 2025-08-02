import discord
from datetime import timedelta
import re

def parse_time(time_str):
    if not time_str:
        return None
    match = re.match(r"^(\d+)([smhd])$", time_str)
    if not match:
        return None
    value, unit = match.groups()
    value = int(value)
    if unit == "s":
        return timedelta(seconds=value)
    if unit == "m":
        return timedelta(minutes=value)
    if unit == "h":
        return timedelta(hours=value)
    if unit == "d":
        return timedelta(days=value)
    return None

def is_protected(target: discord.Member, actor: discord.Member):
    # Нельзя модератить админов и тех, у кого роль выше или равна
    return (
        target.guild_permissions.administrator or
        target.top_role >= actor.top_role
    )

def setup(bot):
    @bot.tree.command(name="kick", description="Кикнуть участника")
    async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "Без причины"):
        if not interaction.user.guild_permissions.kick_members:
            await interaction.response.send_message("❌ У тебя нет прав на кик участников.", ephemeral=True)
            return
        if is_protected(member, interaction.user):
            await interaction.response.send_message(
                "❌ Нельзя кикать других администраторов или участников с равными/более высокими правами.",
                ephemeral=True
            )
            return
        await member.kick(reason=reason)
        await interaction.response.send_message(f"👢 {member.mention} был кикнут. Причина: {reason}")

    @bot.tree.command(name="ban", description="Забанить участника")
    async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "Без причины"):
        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message("❌ У тебя нет прав на бан участников.", ephemeral=True)
            return
        if is_protected(member, interaction.user):
            await interaction.response.send_message(
                "❌ Нельзя банить других администраторов или участников с равными/более высокими правами.",
                ephemeral=True
            )
            return
        await member.ban(reason=reason)
        await interaction.response.send_message(f"🔨 {member.mention} был забанен. Причина: {reason}")

    @bot.tree.command(name="unban", description="Разбанить пользователя по ID")
    async def unban(interaction: discord.Interaction, user_id: str):
        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message("❌ У тебя нет прав на разбан участников.", ephemeral=True)
            return
        try:
            user = await bot.fetch_user(int(user_id))
            await interaction.guild.unban(user)
            await interaction.response.send_message(f"✅ Пользователь {user} был разбанен.")
        except Exception as e:
            await interaction.response.send_message(f"⚠️ Не удалось разбанить: {e}", ephemeral=True)

    @bot.tree.command(name="clear", description="Очистить сообщения")
    async def clear(interaction: discord.Interaction, amount: int = 10):
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message("❌ У тебя нет прав на удаление сообщений.", ephemeral=True)
            return
        deleted = await interaction.channel.purge(limit=amount)
        await interaction.response.send_message(f"🧹 Удалено {len(deleted)} сообщений.", ephemeral=True)

    @bot.tree.command(name="mute", description="Выдать мут участнику (timeout)")
    async def mute(
        interaction: discord.Interaction,
        member: discord.Member,
        time: str = None,
        reason: str = "Без причины"
    ):
        if not interaction.user.guild_permissions.moderate_members:
            await interaction.response.send_message("❌ У тебя нет прав на мут участников.", ephemeral=True)
            return
        if is_protected(member, interaction.user):
            await interaction.response.send_message(
                "❌ Нельзя мутить других администраторов или участников с равными/более высокими правами.",
                ephemeral=True
            )
            return
        duration = parse_time(time)
        try:
            if duration:
                until = discord.utils.utcnow() + duration
                await member.edit(timed_out_until=until, reason=reason)
                await interaction.response.send_message(
                    f"🔇 {member.mention} был замьючен на {time}. Причина: {reason}"
                )
            else:
                until = discord.utils.utcnow() + timedelta(days=28)
                await member.edit(timed_out_until=until, reason=reason)
                await interaction.response.send_message(
                    f"🔇 {member.mention} был замьючен навсегда (максимум 28 дней). Причина: {reason}"
                )
        except Exception as e:
            await interaction.response.send_message(f"⚠️ Не удалось выдать мут: {e}", ephemeral=True)

    @bot.tree.command(name="unmute", description="Снять мут с участника")
    async def unmute(interaction: discord.Interaction, member: discord.Member):
        if not interaction.user.guild_permissions.moderate_members:
            await interaction.response.send_message("❌ У тебя нет прав на снятие мута.", ephemeral=True)
            return
        if is_protected(member, interaction.user):
            await interaction.response.send_message(
                "❌ Нельзя снимать мут с других администраторов или участников с равными/более высокими правами.",
                ephemeral=True
            )
            return
        try:
            await member.edit(timed_out_until=None, reason="Мут снят через /unmute")
            await interaction.response.send_message(f"🔊 {member.mention} теперь может писать сообщения.")
        except Exception as e:
            await interaction.response.send_message(f"⚠️ Не удалось снять мут: {e}", ephemeral=True)
