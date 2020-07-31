# pylint: skip-file

from .db import db


class Shop(db.Model):
    __tablename__ = 'shop'

    id = db.Column(db.Integer, primary_key=True, comment='Уникальный ид операции')
    item_id = db.Column(db.Integer, nullable=False, comment='Ид продаваемого предмета')
    item = db.Column(db.String, nullable=False, comment='Продаваемый предмет')
    rank = db.Column(db.String(1), nullable=False, comment='Ранг')
    price = db.Column(db.Integer, nullable=False, comment='Цена предмета')
    user_id = db.Column(db.Integer, nullable=False, comment='ИД продавца')