from random import randint

from app.utils.game_logic import get_xp
from math import sqrt

u_attack = 2
u_health = 4
u_defence = 4


def enemy_calc(u_attack, u_health, u_defence, lvl):
    enemy, result = [], {}
    for multiplier in range(5, 13):
        for stat in (u_attack, u_health, u_defence):
            enemy.append(int(stat*(multiplier*0.1)))

        e_power = enemy[0]*(enemy[1]+enemy[2])
        result[f"{multiplier}0%"] = [e_power, int((e_power/randint(5,10))*(10+randint(lvl-1, lvl+2)+lvl)/(5+lvl)//(sqrt(lvl)))]
        enemy = []
    return result


for i in range(1, 101):
    total_xp = get_xp(i)
    need_xp = get_xp(i+1)-total_xp
    if i < 15:
        u_attack += 1
        u_health += 1
        u_defence += 1
    else:
        u_attack += 2
        u_health += 2
        u_defence += 2

    u_power = u_attack*(u_health + u_defence)
    results = enemy_calc(u_attack, u_health, u_defence, i)

    print(f"\n({i}) lvl -- {total_xp}XP | {need_xp}XP t.n | {u_power} u.pw.")
    for key, value in results.items():
        print(f'• {key}  -  {value[0]} m.pw. | {value[1]} g.xp')
