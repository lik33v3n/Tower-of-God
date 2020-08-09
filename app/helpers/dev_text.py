from app.utils.game_logic import power, get_xp
from .scenario import ABILITIES


def user_text(user, username, boost, equipment):
    return (f"Игрок: {username} ({user.xp}/{get_xp(user.lvl)})\n"
            f"🎖 Уровень: {user.lvl} ({user.level_points})\n"
            f"💉 Лечебные зелья: {user.heal_potions}\n\n"
            f"🗡 Урон: {user.damage} "
            f"(+{boost[0] + boost[2] if boost is not None else 0})\n"
            f"♥ Здоровье: <b>{user.health}</b>/{user.max_health}\n"
            f"🛡️ Защита: <b>{user.defence}</b>/{user.max_defence} "
            f"(+{boost[1] + boost[3] if boost is not None else 0})\n\n"
            f"🔪 Оружие: {'-' if user.weapon is None else ' /'.join((equipment[0].split(' ', 1)[1], str(user.weapon)))}\n"
            f"🥋 Броня: {'-' if user.armor is None else ' /'.join((equipment[1].split(' ', 1)[1], str(user.armor)))}\n"
            f"💼 Инвентарь: {len(user.inventory) if user.inventory else 0}\n\n"
            f"⚜ Сила: <b>{power(user)}</b>/{power(user, maximal=True)}\n"
            f"💰 Баланс: {user.balance}\n"
            f"🏆 Ранг: {user.rank}")


def meet_enemy_text(enemy, difficulty):
    return (f"Ты встретил <b>{enemy.name}</b>:\n\n"
            f"⭐ Опыт за убийство: {enemy.bonus}\n"   
            f"💰 Деньги за убийство: {enemy.bonus//2}\n\n"
            f"🗡 Урон: {enemy.damage}\n"
            f"♥ Здоровье: {enemy.health}\n"
            f"🛡 Защита: {enemy.defence}\n\n"
            f"🎲 Шанс дропа: {enemy.drop_chance}%\n"
            f"‼ Cложность: <b>{difficulty}</b> (⚜️<b>{power(enemy)}</b>)")


def rankup_text(enemy, user, difficulty):
    return (f"<b>Ваш текущий ранг: \"{user.rank}\":</b>\n"
            f"Твой экзаменатор: <b>{enemy.name}</b>:\n\n"
            f"🗡 Урон: {enemy.damage}\n"
            f"♥ Здоровье: {enemy.health}\n"
            f"🛡 Защита: {enemy.defence}\n\n"
            f"🏆 Ранг: {enemy.rank}\n"
            f"‼ Cложность: {difficulty} (<b>{enemy.power}</b>)")


def gear_info_text(gear):
    return (f"{gear.name}:\n"
            f"+🗡 Повышение атаки: {gear.attack_boost}\n"
            f"+🛡 Повышение защиты: {gear.defence_boost}\n"
            f"🏆 Ранг предмета: {gear.rank}\n"
            f"🎗 Назначение: {'Оружие' if gear.item_class == 'weapon' else 'Броня'}\n"
            f"💠 Качество: {gear.quality}")


def ability_info_text(ability):
    return (f"🎲 <b>{ability.name}</b>:\n\n"
            f"❔ <i>\"{ABILITIES.get(ability.id)}\"</i>\n\n"
            f"🏆 Ранг способности: {ability.rank}\n")


def lvl_up_text(bonus, points):
    return (f"🎊 Вы получили +{bonus}<i>XP</i>, и ваш уровень повышен! "
            f"В связи с чем перешли на следующий этаж!!\n"
            f"<i>Вам засчитано ({points}) очки повышения.</i>")
