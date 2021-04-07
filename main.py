import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import sqlite3

db = 'db/database.db'
con = sqlite3.connect(db)
cur = con.cursor()
vk_session = vk_api.VkApi(
    token='TOKEN')
vk = vk_session.get_api()


def get_msg_info(event):
    user_id = event.obj.message['from_id']
    user = vk.users.get(user_id=user_id)
    print()
    print('*Новое сообщение')
    print(f'Пользователь: {user["first_name"]} {user["first_name"]}')
    print(f'Написал сообщение: {event.obj.message["text"]}')


def get_money(user, event):
    query = f"FROM user_info SELECT money WHERE id = {user['id']}"
    res = cur.execute(query).fetchall()
    send(f'Сейчас у вас: {res[0]} копеек', event)


def get_businesses(user, event):
    query = f"FROM businesses SELECT * WHERE id = {user['id']}"
    res = cur.execute(query).fetchall()
    send('unifinished', event)


def send(msg, event):
    vk.messages.send(user_id=event.obj.message['from_id'],
                     message=msg,
                     random_id=random.randint(0, 2 ** 64))


def start_game(user, event):
    user_name = f'{user["first_name"]} {user["last_name"]}'
    print()
    print(f'Пользователь {user_name} Начал играть!')
    send(f'Привет,{user_name}, давай начнем игру!', event)
    query = f"INSERT INTO user_info(id, username, money) VALUES({user['id']}," \
            f" '{user_name}', 100)"
    res = cur.execute(query).fetchall()
    get_money(user, event)
    get_businesses(user, event)
    send('список команд: старт, деньги, бизнесы, купить (название), '
                             'продать (название)', event)


def main():
    longpoll = VkBotLongPoll(vk_session, 'id_сообщества')

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            msg = event.obj.message['from_id']
            user_id = event.obj.message['from_id']
            user = vk.users.get(user_id=user_id)
            get_msg_info(event)
            send("Бот пока в стадии разработки, но я обязательно доделаю его!", event)
            if msg.lower() == 'старт':
                start_game(user, event)


if __name__ == '__main__':
    main()
