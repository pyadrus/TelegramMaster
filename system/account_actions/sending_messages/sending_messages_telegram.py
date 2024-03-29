import datetime
import sys
import time

from rich import print
from telethon.errors import *

from system.auxiliary_functions.auxiliary_functions import record_and_interrupt, record_inviting_results
from system.auxiliary_functions.global_variables import console, time_inviting_1
from system.menu.app_gui import program_window, done_button
from system.notification.notification import app_notifications
from system.telegram_actions.telegram_actions import telegram_connect_and_output_name


def we_send_a_message_by_members(limits, db_handler) -> None:
    """Рассылка сообщений по списку software_database.db"""
    # Предупреждаем пользователя о вводе ссылок в графическое окно программы
    print("[medium_purple3][+] Введите текст который будем рассылать в личку, для вставки в графическое окно готового "
          "текста используйте комбинацию клавиш Ctrl + V, обратите внимание что при использование комбинации язык "
          "должен быть переключен на английский")

    root, text = program_window()

    def output_values_from_the_input_field() -> None:
        """Выводим значения с поля ввода (то что ввел пользователь)"""
        message_text = text.get("1.0", 'end-1c')
        closing_the_input_field()
        we_send_a_message_from_all_accounts(message_text, limits, db_handler)

    def closing_the_input_field() -> None:
        """Закрываем программу"""
        root.destroy()

    done_button(root, output_values_from_the_input_field)  # Кнопка "Готово"
    root.mainloop()  # Запускаем программу


def send_files_to_personal_account(limits, db_handler) -> None:
    """Отправка файлов в личку"""
    # Просим пользователя ввести расширение сообщения
    link_to_the_file: str = console.input(
        "[medium_purple3][+] Введите название файла с папки user_settings/files_to_send: ")
    event: str = f"Отправляем сообщение"
    app_notifications(notification_text=event)  # Выводим уведомление
    # Открываем базу данных для работы с аккаунтами user_settings/software_database.db
    records: list = db_handler.open_and_read_data("config")
    for row in records:
        # Подключение к Telegram и вывод имя аккаунта в консоль / терминал
        client, phone = telegram_connect_and_output_name(row, db_handler)
        try:
            # Открываем parsing список user_settings/software_database.db для inviting в группу
            records: list = db_handler.open_the_db_and_read_the_data_lim("members", number_of_accounts=limits)
            # Количество аккаунтов на данный момент в работе
            print(f"[medium_purple3]Всего username: {len(records)}")
            for rows in records:
                username = rows[0] # Получаем имя аккаунта из базы данных user_settings/software_database.db
                print(f"[magenta][!] Отправляем сообщение: {username}")
                try:
                    user_to_add = client.get_input_entity(username)
                    client.send_file(user_to_add, f"user_settings/files_to_send/{link_to_the_file}")
                    # Записываем данные в базу данных, чистим список кого добавляли или писали сообщение
                    actions = "Сообщение отправлено"
                    record_inviting_results(username, phone, f"username : {username}", event, actions, db_handler)
                except FloodWaitError as e:
                    actions: str = f'Flood! wait for {str(datetime.timedelta(seconds=e.seconds))}'
                    record_and_interrupt(actions, phone, f"username : {username}", event, db_handler)
                    break  # Прерываем работу и меняем аккаунт
                except PeerFloodError:
                    actions = "Предупреждение о Flood от telegram."
                    record_and_interrupt(actions, phone, f"username : {username}", event, db_handler)
                    break  # Прерываем работу и меняем аккаунт
                except UserNotMutualContactError:
                    actions = "User не является взаимным контактом."
                    record_inviting_results(username, phone, f"username : {username}", event, actions, db_handler)
                except (UserIdInvalidError, UsernameNotOccupiedError, ValueError, UsernameInvalidError):
                    actions = "Не корректное имя user"
                    record_inviting_results(username, phone, f"username : {username}", event, actions, db_handler)
                except ChatWriteForbiddenError:
                    actions = "Вам запрещено писать в супергруппу / канал."
                    record_and_interrupt(actions, phone, f"username : {username}", event, db_handler)
                    break  # Прерываем работу и меняем аккаунт
                except (TypeError, UnboundLocalError):
                    continue  # Записываем ошибку в software_database.db и продолжаем работу
        except KeyError:
            sys.exit(1)
    app_notifications(notification_text="Работа окончена!")  # Выводим уведомление


def we_send_a_message_from_all_accounts(message_text, limits, db_handler) -> None:
    """
    Отправка (текстовых) сообщений в личку Telegram пользователям из базы данных.
    :arg message_text: (str) Текст сообщения, которое будет отправлено каждому пользователю.
    :arg limits: (int) количество аккаунтов, которые в данный момент находятся в работе.
    :arg db_handler: (db_handler) объект, который используется для работы с базой данных.
    """
    event: str = f"Отправляем сообщение в личку пользователям Telegram"
    app_notifications(notification_text=event)  # Выводим уведомление
    # Открываем базу данных для работы с аккаунтами user_settings/software_database.db
    records: list = db_handler.open_and_read_data("config")
    for row in records:
        # Подключение к Telegram и вывод имя аккаунта в консоль / терминал
        client, phone = telegram_connect_and_output_name(row, db_handler)
        try:
            records: list = db_handler.open_the_db_and_read_the_data_lim("members", number_of_accounts=limits)
            # Количество аккаунтов на данный момент в работе
            print(f"[medium_purple3]Всего username: {len(records)}")
            for rows in records:
                username = rows[0]  # Имя аккаунта пользователя в базе данных user_settings/software_database.db
                print(f"[magenta][!] Отправляем сообщение: {username}")
                try:
                    user_to_add = client.get_input_entity(username)
                    client.send_message(user_to_add, message_text.format(username))
                    # Записываем данные в log файл, чистим список кого добавляли или писали сообщение
                    time.sleep(time_inviting_1)
                    actions = "Сообщение отправлено"
                    record_inviting_results(username, phone, f"username : {username}", event, actions, db_handler)
                except FloodWaitError as e:
                    # account_actions: str = f'Flood! wait for {str(datetime.timedelta(seconds=e.seconds))}'
                    record_and_interrupt(f'Flood! wait for {str(datetime.timedelta(seconds=e.seconds))}', phone,
                                         f"username : {username}", event, db_handler)
                    break  # Прерываем работу и меняем аккаунт
                except PeerFloodError:
                    actions = "Предупреждение о Flood от telegram."
                    record_and_interrupt(actions, phone, f"username : {username}", event, db_handler)
                    break  # Прерываем работу и меняем аккаунт
                except UserNotMutualContactError:
                    actions = "User не является взаимным контактом."
                    record_inviting_results(username, phone, f"username : {username}", event, actions, db_handler)
                except (UserIdInvalidError, UsernameNotOccupiedError, ValueError, UsernameInvalidError):
                    actions = "Не корректное имя user"
                    record_inviting_results(username, phone, f"username : {username}", event, actions, db_handler)
                except ChatWriteForbiddenError:
                    actions = "Вам запрещено писать в супергруппу / канал."
                    record_and_interrupt(actions, phone, f"username : {username}", event, db_handler)
                    break  # Прерываем работу и меняем аккаунт
                except (TypeError, UnboundLocalError):
                    continue  # Записываем ошибку в software_database.db и продолжаем работу
        except KeyError:  # В случае отсутствия ключа в базе данных (нет аккаунтов в базе данных).
            sys.exit(1)
    app_notifications(notification_text="Работа окончена!")  # Выводим уведомление
