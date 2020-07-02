class Enemy:
    def __init__(self, name: str, damage: int, health: int, defence: int, drop_chance: int, bonus: int):
        self.name = name
        self.damage = damage
        self.health = health
        self.defence = defence
        self.drop_chance = drop_chance
        self.bonus = bonus
        