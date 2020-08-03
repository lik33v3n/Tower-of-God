from contextlib import suppress
from datetime import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import (MessageNotModified,
                                      MessageToDeleteNotFound)
from aiogram.utils.markdown import quote_html

from ..__main__ import bot
from ..database.base import Item, Shop, User
from ..helpers.dev_text import gear_info_text
from ..helpers.keyboards import (IDLE_Kb, SHOP_Kb, SHOP_LOT_Kb, SHOP_MY_Kb,
                                 SHOP_MY_LOT_Kb)
from ..utils.states import MainStates

GLOBAL_LOTS = '~  ~  ~  🛒  <b>Торговая площадка</b>:  ~  ~  ~'
MY_LOTS = '~  ~  ~ 👤  <b>Мои лоты на продажу</b>:  ~  ~  ~'


async def buy_heal_potion(c: CallbackQuery, user: User):
    if user.balance - (user.lvl * 10) // 4 >= 0:
        await user.update(heal_potions=user.heal_potions+1, balance=user.balance - (user.lvl * 10) // 4).apply()
        with suppress(MessageToDeleteNotFound):
            await c.message.delete()
        await c.message.answer(f'❕ Вы преобрели 1 лечебное зельё, с вашего баланса списано {(user.lvl * 10) // 4} монет.', reply_markup=IDLE_Kb())
    else:
        with suppress(MessageToDeleteNotFound):
            await c.message.delete()
        await c.message.answer('❗ У вас недостаточно монет', reply_markup=IDLE_Kb())


async def shop_all(m: Message, state: FSMContext, user: User, enter=True):
    if enter: await MainStates.shopping.set()
    async with state.proxy() as data:
        data['shop'] = [await Shop.query.where(Shop.user_id != user.id).gino.all(), 0]
        data['keyboards'] = [SHOP_Kb(data['shop'][0], data['shop'][1])]
        if enter: 
            data['msg'] = await m.answer(text=GLOBAL_LOTS, reply_markup=data['keyboards'][0])
        else:
            data['msg'] = await data['msg'].edit_text(text=GLOBAL_LOTS, reply_markup=data['keyboards'][0])



async def shop_query_my(c: CallbackQuery, state: FSMContext, user: User):
    lots = await Shop.query.where(Shop.user_id == user.id).gino.all()
    if lots:
        async with state.proxy() as data:
            data['shop'] = [lots, 0]
            data['keyboards'] = [SHOP_MY_Kb(lots, data['shop'][1])]
            data['msg'] = await data['msg'].edit_text(text=MY_LOTS, reply_markup=data['keyboards'][0])
    else:
        await c.answer('❗ У вас нет предметов, выставленных на продажу. Вы можете продать предметы из инвентаря.', show_alert=True)


async def shop_query_refresh(c: CallbackQuery, state: FSMContext, user: User):
    try:
        if c.data == 'shop_refresh':
            await shop_all(c.message, state, user, False)
        elif c.data == 'shop_refresh_my':
            await shop_query_my(c, state, user)
    except MessageNotModified:
        await c.answer('❕ Already up to date.') 


async def shop_query_scroll(c: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if c.data == 'shop_forward' or c.data == 'shop_my_forward':
            max_pages = len(data['shop'][0])//5+1 if len(data['shop'][0])%5>0 else len(data['shop'][0])//5
            if max_pages > data['shop'][1]+1:
                data['shop'][1] += 1
                data['keyboards'].append(SHOP_Kb(data['shop'][0], data['shop'][1]) if c.data == 'shop_forward' else SHOP_MY_Kb(data['shop'][0], data['shop'][1]))
                data['msg'] = await data['msg'].edit_text(text=GLOBAL_LOTS, reply_markup=data['keyboards'][data['shop'][1]])
            else:
                await c.answer('❕ Максимальная страница')
        elif c.data == 'shop_back' or c.data == 'shop_my_back':
            if data['shop'][1] - 1 >= 0:
                data['shop'][1] -= 1
                data['msg'] = await data['msg'].edit_text(text=GLOBAL_LOTS, reply_markup=data['keyboards'][data['shop'][1]])
            else:
                await c.answer('❕ Вы на первой странице.')   
        

async def shop_query_get(c: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if c.data[:12] == 'shop_get_my_' or c.data[:9] == 'shop_get_':
            boolean = True if c.data[:12] == 'shop_get_my_' else False
            lot = await Shop.get(int(c.data[12 if boolean else 9:]))
            if lot:
                item = await Item.get(lot.item_id)
                if item:
                    data['msg'] = await data['msg'].edit_text(text=f'❕ Лот №{lot.id}:\n\n{gear_info_text(item)}\n\n💸 Цена: {lot.price}', 
                                                              reply_markup=SHOP_MY_LOT_Kb(lot.id) if boolean else SHOP_LOT_Kb(lot.id))
                else:
                    with suppress(MessageToDeleteNotFound):
                        await c.message.delete()
                    await c.message.answer('<b>Error:</b> Broken item (Свяжитесь с администрацией)', reply_markup=IDLE_Kb())
                    raise NameError("Broken item")
            else:
                await c.answer('❗ Лот больше не существует, обновите страницу.', show_alert=True)   


async def shop_query_delete(c: CallbackQuery, state: FSMContext, user: User):
    async with state.proxy() as data:
        lot = await Shop.get(int(c.data[16:]))
        if user.id == lot.user_id:
            user.inventory.append(lot.item_id)
            await user.update(inventory=user.inventory).apply()
            await Shop.delete.where(Shop.id == lot.id).gino.first()

            data['msg'] = await data['msg'].edit_text(text=MY_LOTS, reply_markup=data['keyboards'][0])
            await c.answer(f'❕ Лот №{lot.id} был удалён.\n\nПредмет \"{lot.item}\" возвращен в инвентарь.', show_alert=True)


async def shop_query_buy(c: CallbackQuery, state: FSMContext, user: User):
    lot = await Shop.get(int(c.data[13:]))
    if lot:
        if user.balance >= lot.price:
            receiver = await User.get(lot.user_id)
            if receiver:
                # chating with receiver:
                time = datetime.now().strftime('%d.%m.%y - %H:%M:%S')
                await bot.send_message(chat_id=receiver.id, 
                                       text=f'💰 Ваш лот <b>№{lot.id}</b> был успешно продан:\n\n<b>{lot.item}</b>: /{lot.item_id}\n🏆 Ранг предмета: {lot.rank}\n'
                                            f'👤 Покупатель: <a href="tg://user?id={user.id}">{user.username}</a>\n👤 Продавец: <a href="tg://user?id={receiver.id}">{receiver.username}</a>\n'
                                            f'🕓 Тайм код: {time}\n💸 Вам засчитано <b>+{lot.price}</b>.\n\n<i>В случае любых несостыковок это сообщение считается за доказательство</i>')
                await receiver.update(balance=receiver.balance+lot.price).apply()
                await Shop.delete.where(Shop.id == lot.id).gino.first()

                # working with customer:
                user.inventory.append(lot.item_id)
                user.balance = user.balance-lot.price
                await user.update(inventory=user.inventory, balance=user.balance).apply()
                with suppress(MessageToDeleteNotFound):
                        await c.message.delete()
                await c.message.answer(f'📦 Лот №{lot.id} был успешно продан.\n\n<b>{lot.item}</b>: /{lot.item_id}\n🏆 Ранг предмета: {lot.rank}\n'
                                       f'👤 Покупатель: <a href="tg://user?id={user.id}">{user.username}</a>\n👤 Продавец: <a href="tg://user?id={receiver.id}">{receiver.username}</a>\n'
                                       f'🕓 Тайм код: {time}\n💸 С вашего счета списано <b>-{lot.price}</b>.\n\n<i>В случае любых несостыковок это сообщение считается за доказательство</i>')
                await state.reset_data()
                await state.reset_state()
            else:
                await c.answer(f'❗ Мы не можем достучаться к {lot.user_id}. Пожалуйста сообщите администрации.', show_alert=True)  
        else:
            await c.answer('❗ У вас недостаточно средств на балансе.', show_alert=True)  
    else:
        await c.answer('❗ Лот больше не существует, обновите страницу.', show_alert=True)  
