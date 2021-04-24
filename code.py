from time import sleep

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import vk_api.keyboard
import random
import sqlite3
import datetime

db = 'db/database.db'
con = sqlite3.connect(db)
cur = con.cursor()
vk_session = vk_api.VkApi(
    token='4ebc1ec9ad7258c37d00147cb33ff562caab9ce16593a9df22e294538feb86c1d043b6dd24ce7951a64ec')
vk = vk_session.get_api()


def get_msg_info(user, event):
    print()
    print('*Новое сообщение')
    print(f'Пользователь: {user["first_name"]} {user["last_name"]}')
    print(f'Написал сообщение: {event.obj.message["text"]}')


def get_money(user, event):
    query = f"SELECT money FROM user_info WHERE id = {user['id']}"
    res = cur.execute(query).fetchall()
    kb_send(f'Сейчас у вас: {res[0][0]} копеек', event, main_menu_keyboard())


def get_businesses(user, event):
    query = f"SELECT * FROM businesses WHERE user_id = {user['id']}"
    res = cur.execute(query).fetchall()
    kb_send(f'киоск (1). У вас -  {res[0][1]}\n штук.\nСтоит - 100 копеек\n Приносит -  1 коп/мин\n\n'
         f'магазин (2). У вас -  {res[0][2]}\n штук.\nСтоит - 950 копеек\n Приносит -  11 коп/мин\n\n'
         f'кинотеатр (3). У вас -  {res[0][3]}\n штук.\nСтоит - 9.000 копеек\n Приносит -  120 коп/мин\n\n'
         f'малый торговый центр (4). У вас -  {res[0][4]}\n штук.\nСтоит - 85.000 копеек\n Приносит -  1.300 коп/мин\n\n'
         f'сеть магазинов (5). У вас -  {res[0][5]}\n штук.\nСтоит - 800.000 копеек\n Приносит -  14.000 коп/мин\n\n'
         f'популярная игра (6). У вас -  {res[0][6]}\n штук.\nСтоит - 7.500.000 копеек\n Приносит -  150.000 коп/мин\n\n'
         f'завод (7). У вас -  {res[0][7]}\n штук.\nСтоит - 70.000.000 копеек\n Приносит -  1.600.000 коп/мин\n\n'
         f'гиганский торговый центр (8). У вас -  {res[0][8]}\n штук.\nСтоит - 650.000.000 копеек\n Приносит -  17.000.000 коп/мин\n\n'
         f'сеть заводов (9). У вас -  {res[0][9]}\n штук.\nСтоит - 6.000.000.000 копеек\n Приносит -  180.000.000 коп/мин\n\n'
         f'Прошел игру. Стоит - 100.000.000.000 копеек\n Приносит -  бесконечность коп/мин\n\n'
         f'ваш заработок: {res[0][-1]}', event, main_menu_keyboard())


def business_buying_keyboard():
    keyboard = vk_api.keyboard.VkKeyboard(one_time=True)

    keyboard.add_button("купить 1", color=vk_api.keyboard.VkKeyboardColor.SECONDARY)
    keyboard.add_button("купить 2", color=vk_api.keyboard.VkKeyboardColor.SECONDARY)
    keyboard.add_button("купить 3", color=vk_api.keyboard.VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button("купить 4", color=vk_api.keyboard.VkKeyboardColor.SECONDARY)
    keyboard.add_button("купить 5", color=vk_api.keyboard.VkKeyboardColor.SECONDARY)
    keyboard.add_button("купить 6", color=vk_api.keyboard.VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button("купить 7", color=vk_api.keyboard.VkKeyboardColor.SECONDARY)
    keyboard.add_button("купить 8", color=vk_api.keyboard.VkKeyboardColor.SECONDARY)
    keyboard.add_button("купить 9", color=vk_api.keyboard.VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button("прошел игру", color=vk_api.keyboard.VkKeyboardColor.SECONDARY)

    return keyboard.get_keyboard()


def main_menu_keyboard():
    keyboard = vk_api.keyboard.VkKeyboard(one_time=True)

    keyboard.add_button("деньги", color=vk_api.keyboard.VkKeyboardColor.SECONDARY)
    keyboard.add_button("бизнесы", color=vk_api.keyboard.VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button("купить", color=vk_api.keyboard.VkKeyboardColor.POSITIVE)
    keyboard.add_button("продать", color=vk_api.keyboard.VkKeyboardColor.NEGATIVE)

    return keyboard.get_keyboard()


def empty_keyboard():
    keyboard = vk_api.keyboard.VkKeyboard.get_empty_keyboard()

    return keyboard


def kb_send(msg, event, kb):
    vk.messages.send(user_id=event.obj.message['from_id'],
                     message=msg,
                     keyboard=kb,
                     random_id=random.randint(0, 2 ** 64))


def send(msg, event):
    vk.messages.send(user_id=event.obj.message['from_id'],
                     message=msg,
                     random_id=random.randint(0, 2 ** 64))


def start_game(user, event):
    user_name = f'{user["first_name"]} {user["last_name"]}'
    print()
    print(f'Пользователь {user_name} Начал играть!')
    send(f'Привет,{user_name}, давай начнем игру!', event)
    query = f"INSERT INTO user_info(id, username, money, businesses_id) VALUES({user['id']}," \
            f" '{user_name}', 100, {user['id']})"
    cur.execute(query).fetchall()
    query = f"INSERT INTO businesses(user_id, lvl1, lvl2, lvl3, lvl4, lvl5," \
            f" lvl6, lvl7, lvl8, lvl9, game_finished, profit)" \
            f" VALUES({user['id']}, 0, 0, 0, 0, 0, 0, 0, 0, 0, False, 0)"
    cur.execute(query).fetchall()
    con.commit()
    get_money(user, event)
    get_businesses(user, event)
    kb_send('список команд: старт, деньги, бизнесы, купить (название), '
         'продать (название).', event, main_menu_keyboard())


def business_buy(business, user, event):
    query = f"SELECT money FROM user_info WHERE id={user['id']}"
    res = cur.execute(query).fetchall()
    try:
        business = int(business)
    except ValueError:
        send('что-то пошло не так попробуй еще раз!', event)
    if business == 1:
        if res[0][0] >= 100:
            query = f"UPDATE user_info SET money = money - 100 WHERE id={user['id']}"
            cur.execute(query)
            kb_send('Спасибо за покупку!', event, main_menu_keyboard())
            query = f"UPDATE businesses SET lvl1 = lvl1 + 1" \
                    f" WHERE user_id={user['id']}"
            cur.execute(query)
            query = f"UPDATE businesses SET profit = profit + 1" \
                    f" WHERE user_id={user['id']}"
            cur.execute(query)
            get_businesses(user, event)
        else:
            send('Сожалею, но у вас не хватает денег(', event)
    elif business == 2:
        if res[0][0] >= 950:
            query = f"UPDATE user_info SET money = money - 950 WHERE id={user['id']}"
            cur.execute(query)
            kb_send('Спасибо за покупку!', event, main_menu_keyboard())
            query = f"UPDATE businesses SET lvl2 = lvl2 + 1" \
                    f" WHERE user_id={user['id']}"
            cur.execute(query)
            query = f"UPDATE businesses SET profit = profit + 11" \
                    f" WHERE user_id={user['id']}"
            cur.execute(query)
            get_businesses(user, event)
        else:
            send('Сожалею, но у вас не хватает денег(', event)
    elif business == 3:
        if res[0][0] >= 9000:
            query = f"UPDATE user_info SET money = money - 9000 WHERE id={user['id']}"
            cur.execute(query)
            kb_send('Спасибо за покупку!', event, main_menu_keyboard())
            query = f"UPDATE businesses SET lvl3 = lvl3 + 1" \
                    f" WHERE user_id={user['id']}"
            cur.execute(query)
            query = f"UPDATE businesses SET profit = profit + 120" \
                    f" WHERE user_id={user['id']}"
            cur.execute(query)
            get_businesses(user, event)
        else:
            send('Сожалею, но у вас не хватает денег(', event)
    elif business == 4:
        if res[0][0] >= 85000:
            query = f"UPDATE user_info SET money = money - 85000 WHERE id={user['id']}"
            cur.execute(query)
            kb_send('Спасибо за покупку!', event, main_menu_keyboard())
            query = f"UPDATE businesses SET lvl4 = lvl4 + 1" \
                    f" WHERE user_id={user['id']}"
            cur.execute(query)
            query = f"UPDATE businesses SET profit = profit + 1300" \
                    f" WHERE user_id={user['id']}"
            cur.execute(query)
            get_businesses(user, event)
        else:
            send('Сожалею, но у вас не хватает денег(', event)
    elif business == 5:
        if res[0][0] >= 800000:
            query = f"UPDATE user_info SET money = money - 800000 WHERE id={user['id']}"
            cur.execute(query)
            kb_send('Спасибо за покупку!', event, main_menu_keyboard())
            query = f"UPDATE businesses SET lvl5 = lvl5 + 1" \
                    f" WHERE user_id={user['id']}"
            cur.execute(query)
            query = f"UPDATE businesses SET profit = profit + 14000" \
                    f" WHERE user_id={user['id']}"
            cur.execute(query)
            get_businesses(user, event)
        else:
            send('Сожалею, но у вас не хватает денег(', event)
    elif business == 6:
        if res[0][0] >= 7500000:
            query = f"UPDATE user_info SET money = money - 7500000 WHERE id={user['id']}"
            cur.execute(query)
            kb_send('Спасибо за покупку!', event, main_menu_keyboard())
            query = f"UPDATE businesses SET lvl6 = lvl6 + 1" \
                    f" WHERE user_id={user['id']}"
            cur.execute(query)
            query = f"UPDATE businesses SET profit = profit + 150000" \
                    f" WHERE user_id={user['id']}"
            cur.execute(query)
            get_businesses(user, event)
        else:
            send('Сожалею, но у вас не хватает денег(', event)
    elif business == 7:
        if res[0][0] >= 70000000:
            query = f"UPDATE user_info SET money = money - 70000000 WHERE id={user['id']}"
            cur.execute(query)
            kb_send('Спасибо за покупку!', event, main_menu_keyboard())
            query = f"UPDATE businesses SET lvl7 = lvl7 + 1" \
                    f" WHERE user_id={user['id']}"
            cur.execute(query)
            query = f"UPDATE businesses SET profit = profit + 1600000" \
                    f" WHERE user_id={user['id']}"
            cur.execute(query)
            get_businesses(user, event)
        else:
            send('Сожалею, но у вас не хватает денег(', event)
    elif business == 8:
        if res[0][0] >= 650000000:
            query = f"UPDATE user_info SET money = money - 650000000 WHERE id={user['id']}"
            cur.execute(query)
            kb_send('Спасибо за покупку!', event, main_menu_keyboard())
            query = f"UPDATE businesses SET lvl8 = lvl8 + 1" \
                    f" WHERE user_id={user['id']}"
            cur.execute(query)
            query = f"UPDATE businesses SET profit = profit + 17000000" \
                    f" WHERE user_id={user['id']}"
            cur.execute(query)
            get_businesses(user, event)
        else:
            send('Сожалею, но у вас не хватает денег(', event)
    elif business == 8:
        if res[0][0] >= 6000000000:
            query = f"UPDATE user_info SET money = money - 6000000000 WHERE id={user['id']}"
            cur.execute(query)
            kb_send('Спасибо за покупку!', event, main_menu_keyboard())
            query = f"UPDATE businesses SET lvl9 = lvl9 + 1" \
                    f" WHERE user_id={user['id']}"
            cur.execute(query)
            query = f"UPDATE businesses SET profit = profit + 180000000" \
                    f" WHERE user_id={user['id']}"
            cur.execute(query)
            get_businesses(user, event)
        else:
            send('Сожалею, но у вас не хватает денег(', event)
    con.commit()


def main():
    longpoll = VkBotLongPoll(vk_session, 204038222)

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            msg = event.obj.message
            user_id = event.obj.message['from_id']
            user = vk.users.get(user_id=user_id)[0]
            get_msg_info(user, event)
            send("Бот пока в стадии разработки, но я обязательно доделаю его!", event)
            if msg['text'].lower() == 'старт':
                start_game(user, event)
            if msg['text'].lower() == 'деньги':
                get_money(user, event)
            if msg['text'].lower() == 'бизнесы':
                get_businesses(user, event)
            if 'купить' in msg['text'].lower():
                if len(msg['text'].lower().split()) < 2:
                    get_businesses(user, event)
                    kb_send('укажите номер бизнеса! (он указан в скобках)', event, business_buying_keyboard())
                else:
                    business_buy(msg['text'].lower().split()[1], user, event)


if __name__ == '__main__':
    main()
