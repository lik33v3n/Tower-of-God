"""first migration

Revision ID: bd2a265a2642
Revises: 
Create Date: 2021-10-06 20:13:24.708778

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd2a265a2642'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('abilities',
    sa.Column('id', sa.Integer(), nullable=False, comment='Уникальный ID'),
    sa.Column('name', sa.String(), nullable=False, comment='Название способности'),
    sa.Column('func', sa.String(), nullable=False, comment='Функция'),
    sa.Column('rank', sa.String(length=1), nullable=False, comment='Ранг для получения'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_abilities_id'), 'abilities', ['id'], unique=True)
    op.create_table('items',
    sa.Column('id', sa.Integer(), nullable=False, comment='Уникальный ID'),
    sa.Column('name', sa.String(), nullable=False, comment='Название предмета'),
    sa.Column('attack_boost', sa.Integer(), nullable=False, comment='Повышение урона'),
    sa.Column('defence_boost', sa.Integer(), nullable=False, comment='Повышение защиты'),
    sa.Column('rank', sa.String(), nullable=False, comment='Ранг для получения'),
    sa.Column('quality', sa.String(), nullable=False, comment='Качество'),
    sa.Column('item_class', sa.String(), nullable=False, comment='Оружие или броня'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_items_id'), 'items', ['id'], unique=True)
    op.create_table('shop',
    sa.Column('id', sa.Integer(), nullable=False, comment='Уникальный ид операции'),
    sa.Column('item_id', sa.Integer(), nullable=False, comment='Ид продаваемого предмета'),
    sa.Column('item', sa.String(), nullable=False, comment='Продаваемый предмет'),
    sa.Column('rank', sa.String(length=1), nullable=False, comment='Ранг'),
    sa.Column('price', sa.Integer(), nullable=False, comment='Цена предмета'),
    sa.Column('user_id', sa.Integer(), nullable=False, comment='ИД продавца'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False, comment='Уникальный ID'),
    sa.Column('username', sa.String(), server_default='noname', nullable=False, comment='Имя'),
    sa.Column('rank', sa.String(length=1), server_default='-', nullable=False, comment='Ранг'),
    sa.Column('lvl', sa.Integer(), server_default='1', nullable=False, comment='Уровень'),
    sa.Column('xp', sa.Integer(), server_default='0', nullable=False, comment='Опыт'),
    sa.Column('damage', sa.Integer(), server_default='3', nullable=False, comment='Наносимый урон'),
    sa.Column('weapon', sa.Integer(), nullable=True, comment='Оружие'),
    sa.Column('health', sa.Integer(), server_default='5', nullable=False, comment='Здоровье'),
    sa.Column('max_health', sa.Integer(), server_default='5', nullable=False, comment='Макс. Здоровье'),
    sa.Column('defence', sa.Integer(), server_default='5', nullable=False, comment='Защита'),
    sa.Column('max_defence', sa.Integer(), server_default='5', nullable=False, comment='Макс. Защита'),
    sa.Column('armor', sa.Integer(), nullable=True, comment='Броня'),
    sa.Column('level_points', sa.Integer(), server_default='0', nullable=False, comment='Очки повышения'),
    sa.Column('inventory', sa.ARRAY(sa.Integer()), server_default='{}', nullable=False, comment='Инвентарь'),
    sa.Column('balance', sa.Integer(), server_default='0', nullable=False, comment='Баланс'),
    sa.Column('heal_potions', sa.Integer(), server_default='1', nullable=False, comment='Лечебное зелье'),
    sa.Column('abilities', sa.ARRAY(sa.Integer()), server_default='{}', nullable=False, comment='Способности'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    op.drop_table('shop')
    op.drop_index(op.f('ix_items_id'), table_name='items')
    op.drop_table('items')
    op.drop_index(op.f('ix_abilities_id'), table_name='abilities')
    op.drop_table('abilities')
    # ### end Alembic commands ###
