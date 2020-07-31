import random
import json
import math


AVAILABLE_COMMANDS = ("👤 Профиль", "⚔️ Бой", "💉 Лечение", "🧪 Лечебные зелья", "📯 Повышение ранга",
                      "💊 Лазарет", "💼 Инвентарь", "📤 Снять экипировку", "🥋 Экипировка",
                      "⚖️ Повышение характеристик", "⚒ Крафт", "🔈 Помощь",
                      "🛒 Торговая площадка", '/help')

ADMIN_COMMANDS = ('lambda', 'info', 'log', 'get', 'deluser')


async def battle_attack(x, y, u, e, call):
    text = f"❕ Ты попал по \"{e.name}\"\n\nТы нанёс \"{e.name}\" {u.damage} урона.\n"
    if x == y:
        await call.answer("❗ Противник увернулся от удара", show_alert=True)
        return e.health, e.defence
    else:
        if e.defence <= 0:
            e.health -= u.damage
            await call.answer(text, show_alert=True)
            return e.health, e.defence
        else:
            if u.damage > e.defence:
                miss_dmg = u.damage - e.defence
                e.health -= miss_dmg
                await call.answer(text, show_alert=True)
                e.defence = 0
                return e.health, e.defence
            else:
                e.defence -= u.damage
                await call.answer(text, show_alert=True)
                return e.health, e.defence


async def battle_defence(x, y, u, e, call):
    text = f"❕ \"{e.name}\" попал по тебе\n\n\"{e.name}\" нанёс тебе {e.damage} урона.\n"
    if x == y:
        await call.answer("❗ Ты увернулся от удара", show_alert=True)
        return u.health, u.defence
    else:
        if u.defence <= 0:
            u.health -= e.damage
            await call.answer(text, show_alert=True)
            return u.health, u.defence
        else:
            if e.damage > u.defence:
                miss_dmg = e.damage - u.defence
                u.health -= miss_dmg
                await call.answer(f"{text}", show_alert=True)
                u.defence = 0
                return u.health, u.defence
            else:
                u.defence -= e.damage
                await call.answer(text, show_alert=True)
                return u.health, u.defence


def power(obj, maximal=False):
    if maximal is True:
        hp = obj.max_health + obj.max_defence
    else:
        hp = obj.health + obj.defence
    return hp * obj.damage


def exam_choose(user):
    from app.models.examinators import exams
    for i in range(len(exams)):
        if user.rank == '-':
            return exams[0]
        elif exams[i].rank == user.rank:
            try:
                return exams[i + 1]
            except IndexError:
                return 'Максимальный ранг!'


def set_difficulty(m, u):
    if m * 3 <= u:
        difficulty = 'Оч. легко'
    elif m * 2.5 <= u:
        difficulty = 'Легко'
    elif m * 2 < u:
        difficulty = 'Нормально'
    elif m * 1.5 < u:
        difficulty = 'Сложно'
    elif m < u:
        difficulty = 'Очень сложно'
    elif m > u * 3:
        difficulty = 'Верная смерть'
    elif m >= u:
        difficulty = 'Невозможно'
    else:
        return
    return difficulty


def get_xp(lvl):
    """
    Returns total XP according to gain level
    """
    if lvl != 1:
        math = (((lvl - 1) * 10) ** 1.2) * lvl
        total_xp = round(math / 10) * 10
    else:
        total_xp = 15
    return total_xp


# def json_inv(u):
#     """
#     Converts string from database to list

#     Example: '[3, 2]' => [3, 2]

#     :param u: User
#     :return: User's inventory as list
#     """
#     inventory = json.loads(u['inventory']) if u['inventory'] != '[]' else []
#     return inventory


def item_drop(chance):
    """
    :param chance: Mob's chance of drop
    :return: True/False
    """
    c = random.randint(1, 100)
    if c <= chance:
        return True
    return False


def round_down(n, decimals=0):
    """
    Rounds a number down to a specified number of digits.

    :param decimals: Specified number of digits
    :param n: Float
    """
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier


def enemy_calc(u_attack, u_health, u_defence, lvl):
    enemy, result = [], []
    multiplier = round_down(random.uniform(0.6, 1.2), 1)
    print(multiplier)
    for stat in (u_attack, u_health, u_defence):
        enemy.append(round(stat*multiplier) if stat != 0 else 0)
        
    e_power = enemy[0]*(enemy[1]+enemy[2])
    formulae = int((e_power/random.randint(5,10))*(10+random.randint(lvl-1, lvl+2)+lvl)/(5+lvl)//(math.sqrt(lvl)))
    result = [enemy, formulae if formulae > 1 else 2]
    
    return result
