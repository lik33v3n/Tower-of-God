# pylint: skip-file

from .db import db


class Ability(db.Model):
    __tablename__ = 'abilities'

    id = db.Column(db.Integer, primary_key=True, index=True, unique=True, comment='Уникальный ID')
    name = db.Column(db.String, nullable=False, comment='Название способности')
    func = db.Column(db.String, nullable=False, comment='Функция')
    rank = db.Column(db.String(1), nullable=False, comment='Ранг для получения')
