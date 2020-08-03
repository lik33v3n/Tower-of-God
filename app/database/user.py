# pylint: skip-file

from sqlalchemy import ARRAY
from .db import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, index=True, unique=True, comment='Уникальный ID')
    username = db.Column(db.String, nullable=False, default='noname', comment='Имя')
    rank = db.Column(db.String(1), nullable=False, default='-', comment='Ранг')
    lvl = db.Column(db.Integer, nullable=False, default=1, comment='Уровень')
    xp = db.Column(db.Integer, nullable=False, default=0, comment='Опыт')
    damage = db.Column(db.Integer, nullable=False, default=3, comment='Наносимый урон')
    weapon = db.Column(db.Integer, nullable=True, default=None, comment='Оружие')
    health = db.Column(db.Integer, nullable=False, default=5, comment='Здоровье')
    max_health = db.Column(db.Integer, nullable=False, default=5, comment='Макс. Здоровье')
    defence = db.Column(db.Integer, nullable=False, default=5, comment='Защита')
    max_defence = db.Column(db.Integer, nullable=False, default=5, comment='Макс. Защита')
    armor = db.Column(db.Integer, nullable=True, default=None, comment='Броня')
    level_points = db.Column(db.Integer, nullable=False, default=0, comment='Очки повышения')
    inventory = db.Column(ARRAY(db.Integer), nullable=False, default=[], comment='Инвентарь')
    balance = db.Column(db.Integer, nullable=False, default=0, comment='Баланс')
    heal_potions = db.Column(db.Integer, nullable=False, default=1, comment='Лечебное зелье')