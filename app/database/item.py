# pylint: skip-file

from .db import db


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True, index=True, unique=True, comment='Уникальный ID')
    name = db.Column(db.String, nullable=False, comment='Название предмета')
    attack_boost = db.Column(db.Integer, nullable=False, comment='Повышение урона')
    defence_boost = db.Column(db.Integer, nullable=False, comment='Повышение защиты')
    rank = db.Column(db.String, nullable=False, comment='Ранг для получения')
    quality = db.Column(db.String, nullable=False, comment='Качество')
    item_class = db.Column(db.String, nullable=False, comment='Оружие или броня')
    price = db.Column(db.Integer, nullable=False, default='1', comment='Стоимость предмета')