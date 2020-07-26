# pylint: skip-file

import asyncio
from gino import Gino
from sqlalchemy import ARRAY

db = Gino()

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


async def main():
    await db.set_bind('postgresql://lkeeve:5759@localhost:5432/tower')
    await db.gino.create_all()

    # further code goes here
    item1 = await Item.create(id=12, name='(Обычное) Разбитая бутылка', 
                             attack_boost=5, 
                             defence_boost=0,
                             rank='F', 
                             quality='Common', 
                             item_class='weapon', 
                             price=0)

    item2 = await Item.create(id=13, name='(Редкое) Разбитая бутылка', 
                            attack_boost=7, 
                            defence_boost=0,
                            rank='F', 
                            quality='Rare', 
                            item_class='weapon', 
                            price=0)

    item3 = await Item.create(id=14, name='(Эпическое) Разбитая бутылка', 
                            attack_boost=8, 
                            defence_boost=1,
                            rank='F', 
                            quality='Epic', 
                            item_class='weapon', 
                            price=0)

    item4 = await Item.create(id=15, name='(Легендарное) Разбитая бутылка', 
                            attack_boost=10, 
                            defence_boost=2,
                            rank='F', 
                            quality='Legendary', 
                            item_class='weapon', 
                            price=0)                           

    await db.pop_bind().close()


asyncio.get_event_loop().run_until_complete(main())

