import datetime
import time

import schedule
from rich import print
from telethon.errors import *

from system.account_actions.sending_messages.telegram_chat_dialog import connecting_tg_account_creating_list_groups
from system.account_actions.subscription.subscription import subscribe_to_the_group_and_send_the_link
from system.auxiliary_functions.auxiliary_functions import record_and_interrupt
from system.error.telegram_errors import record_account_actions, delete_files
from system.menu.app_gui import program_window, done_button

creating_a_table = """SELECT * from writing_group_links"""
writing_data_to_a_table = """DELETE from writing_group_links where writing_group_links = ?"""
event: str = f"Рассылаем сообщение по чатам Telegram"


def send_mess(db_handler) -> None:
    with open("user_settings/message_text.csv", 'r') as chats:
        cursor_members = chats.read()
    sending_messages_via_chats_time(cursor_members, db_handler)


def sending_messages_via_chats_time(message_text, db_handler) -> None:
    """Массовая рассылка в чаты"""
    client, phone, records = connecting_tg_account_creating_list_groups(db_handler)
    for groups in records:
        groups_wr = subscribe_to_the_group_and_send_the_link(client, groups, phone, db_handler)
        description_action = f"Sending messages to a group: {groups_wr}"
        try:
            # Рассылаем сообщение по чатам
            client.send_message(entity=groups_wr, message=message_text)
            # Работу записываем в лог файл, для удобства слежения, за изменениями
            actions: str = f"[medium_purple3]Сообщение в группу {groups_wr} написано!"
            record_account_actions(phone, description_action, event, actions, db_handler)
        except ChannelPrivateError:
            actions: str = "Указанный канал является приватным, или вам запретили подписываться."
            record_account_actions(phone, description_action, event, actions, db_handler)
            db_handler.write_data_to_db(creating_a_table, writing_data_to_a_table, groups_wr)
        except PeerFloodError:
            actions: str = "Предупреждение о Flood от Telegram."
            record_and_interrupt(actions, phone, description_action, event, db_handler)
            break  # Прерываем работу и меняем аккаунт
        except FloodWaitError as e:
            actions: str = f'Flood! wait for {str(datetime.timedelta(seconds=e.seconds))}'
            record_account_actions(phone, description_action, event, actions, db_handler)
            print(f'Спим {e.seconds} секунд')
            time.sleep(e.seconds)
        except UserBannedInChannelError:
            actions: str = "Вам запрещено отправлять сообщения в супергруппу."
            record_and_interrupt(actions, phone, description_action, event, db_handler)
            break  # Прерываем работу и меняем аккаунт
        except ChatWriteForbiddenError:
            actions = "Вам запрещено писать в супергруппу / канал."
            record_and_interrupt(actions, phone, description_action, event, db_handler)
            break  # Прерываем работу и меняем аккаунт
        except (TypeError, UnboundLocalError):
            continue  # Записываем ошибку в software_database.db и продолжаем работу
    client.disconnect()  # Разрываем соединение Telegram


def message_time() -> None:
    """
    Пишем сообщения от 1 до 5 раз в ча
    Метод every() модуля schedule, чтобы указать, что задача должна выполняться каждый день
    Метод at() для указания времени выполнения задачи, используя текущий час и значение минут, указанные пользователем
    Метод do() для указания функции, которую нужно вызвать в указанное время
    """
    print("[magenta]Сколько сообщений в час, мы будем отправлять\n",
          "[magenta][1[magenta]] - 1 сообщение в час\n",
          "[magenta][2[magenta]] - 2 сообщение в час\n",
          "[magenta][3[magenta]] - 3 сообщение в час\n",
          "[magenta][4[magenta]] - 4 сообщение в час\n",
          "[magenta][5[magenta]] - 5 сообщение в час\n", )
    user_input_mes_hour: str = input("[+] Введите от 1 до 5: ")
    if user_input_mes_hour == "1":  # Пишем сообщения 1 раз в час
        # Выводим на экран сообщение о том, что сообщения будут публиковаться раз в час
        print("[medium_purple3]Пишем сообщения 1 раз в час")
        # Получаем от пользователя значение минут для публикации сообщений
        user_input_minute_1 = input("[+] Введите минуты, публикации: ")
        # Создаем расписание на каждый час с помощью цикла for
        for hour in range(24):
            schedule.every().day.at(f"{hour:02d}:{user_input_minute_1}").do(send_mess)
    elif user_input_mes_hour == "2":  # Пишем сообщения 2 раза в час
        print("[medium_purple3]Пишем сообщения 2 раза в час")
        user_input_minute_1 = input("[+] Введите минуты, публикации: ")
        user_input_minute_2 = input("[+] Введите минуты, публикации: ")
        for hour in range(24):  # Перебираем часы от 0 до 23
            schedule.every().day.at(f"{hour:02d}:{user_input_minute_1}").do(send_mess)
            schedule.every().day.at(f"{hour:02d}:{user_input_minute_2}").do(send_mess)
    elif user_input_mes_hour == "3":  # Пишем сообщения 3 раза в час
        print("[medium_purple3]Пишем сообщения 3 раза в час")
        # Вводим часы и минуты, повторяем до тех пор, пока не будет нужное количество
        user_input_minute_1: str = input("[+] Введите минуты, публикации: ")
        user_input_minute_2: str = input("[+] Введите минуты, публикации: ")
        user_input_minute_3: str = input("[+] Введите минуты, публикации: ")
        for hour in range(24):  # Перебираем часы от 0 до 23
            schedule.every().day.at(f"{hour:02d}:{user_input_minute_1}").do(send_mess)
            schedule.every().day.at(f"{hour:02d}:{user_input_minute_2}").do(send_mess)
            schedule.every().day.at(f"{hour:02d}:{user_input_minute_3}").do(send_mess)
    elif user_input_mes_hour == "4":  # Пишем сообщения 4 раза в час
        print("[medium_purple3]Пишем сообщения 4 раза в час")
        # Вводим часы и минуты, повторяем до тех пор, пока не будет нужное количество
        user_input_minute_1: str = input("[+] Введите минуты, публикации: ")
        user_input_minute_2: str = input("[+] Введите минуты, публикации: ")
        user_input_minute_3: str = input("[+] Введите минуты, публикации: ")
        user_input_minute_4: str = input("[+] Введите минуты, публикации: ")
        for hour in range(24):  # Перебираем часы от 0 до 23
            schedule.every().day.at(f"{hour:02d}:{user_input_minute_1}").do(send_mess)
            schedule.every().day.at(f"{hour:02d}:{user_input_minute_2}").do(send_mess)
            schedule.every().day.at(f"{hour:02d}:{user_input_minute_3}").do(send_mess)
            schedule.every().day.at(f"{hour:02d}:{user_input_minute_4}").do(send_mess)
    elif user_input_mes_hour == "5":  # Пишем сообщения 5 раз в час
        print("[medium_purple3]Пишем сообщения 5 раза в час")
        # Вводим часы и минуты, повторяем до тех пор, пока не будет нужное количество
        user_input_minute_1: str = input("[+] Введите минуты, публикации: ")
        user_input_minute_2: str = input("[+] Введите минуты, публикации: ")
        user_input_minute_3: str = input("[+] Введите минуты, публикации: ")
        user_input_minute_4: str = input("[+] Введите минуты, публикации: ")
        user_input_minute_5: str = input("[+] Введите минуты, публикации: ")
        for hour in range(24):  # Перебираем часы от 0 до 23
            schedule.every().day.at(f"{hour:02d}:{user_input_minute_1}").do(send_mess)
            schedule.every().day.at(f"{hour:02d}:{user_input_minute_2}").do(send_mess)
            schedule.every().day.at(f"{hour:02d}:{user_input_minute_3}").do(send_mess)
            schedule.every().day.at(f"{hour:02d}:{user_input_minute_4}").do(send_mess)
            schedule.every().day.at(f"{hour:02d}:{user_input_minute_5}").do(send_mess)
    else:
        print("Ошибка выбора!")
    while True:
        schedule.run_pending()
        time.sleep(1)


def message_entry_window_time() -> None:
    """Выводим поле ввода для ввода текста сообщения"""
    # Предупреждаем пользователя о вводе ссылок в графическое окно программы
    print("[medium_purple3][+] Введите текст который будем рассылать по чатам, для вставки в графическое окно готового "
          "текста используйте комбинацию клавиш Ctrl + V, обратите внимание что при использование комбинации язык "
          "должен быть переключен на английский")

    root, text = program_window()

    def output_values_from_the_input_field() -> None:
        """Выводим значения с поля ввода (то что ввел пользователь)"""
        message_text = text.get("1.0", 'end-1c')
        closing_the_input_field()
        delete_files(file=f"user_settings/message_text.csv")
        with open(f'user_settings/message_text.csv', "w") as res_as:
            res_as.write(message_text)

    def closing_the_input_field() -> None:
        """Закрываем программу"""
        root.destroy()

    done_button(root, output_values_from_the_input_field)  # Кнопка "Готово"
    root.mainloop()  # Запускаем программу


if __name__ == "__main__":
    message_entry_window_time()
