# -*- coding: utf-8 -*-
import random
import time

from loguru import logger
from telethon import functions
from telethon import types
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.types import InputPeerEmpty
from telethon.tl.types import UserStatusEmpty
from telethon.tl.types import UserStatusLastMonth
from telethon.tl.types import UserStatusLastWeek
from telethon.tl.types import UserStatusOffline
from telethon.tl.types import UserStatusOnline
from telethon.tl.types import UserStatusRecently

from system.account_actions.TGConnect import TGConnect
from system.account_actions.subscription import subscribe_to_group_or_channel
from system.auxiliary_functions.auxiliary_functions import find_files
from system.auxiliary_functions.global_variables import ConfigReader
from system.sqlite_working_tools.sqlite_working_tools import DatabaseHandler


class ParsingGroupMembers:
    """Парсинг групп"""

    def __init__(self):
        self.db_handler = DatabaseHandler()
        self.tg_connect = TGConnect()
        self.config_reader = ConfigReader()

    async def connect_to_telegram(self, file):
        """Подключение к Telegram"""
        logger.info(f"{file[0]}")
        proxy = await self.tg_connect.reading_proxies_from_the_database()
        client = await self.tg_connect.connecting_to_telegram(file[0], proxy, "user_settings/accounts/parsing")
        await client.connect()
        return client

    async def process_telegram_groups(self) -> None:
        """Парсинг групп"""
        entities = find_files(directory_path="user_settings/accounts/parsing", extension='session')
        for file in entities:
            client = await self.connect_to_telegram(file)
            # Подключение к Telegram и вывод имя аккаунта в консоль / терминал
            # Открываем базу с группами для дальнейшего parsing
            records: list = await self.db_handler.open_and_read_data("writing_group_links")
            for groups in records:  # Поочередно выводим записанные группы
                logger.info(f'[+] Парсинг группы: {groups[0]}')
                await subscribe_to_group_or_channel(client, groups[0])
                await self.group_parsing(client, groups[0])  # Parsing групп
                await self.db_handler.delete_row_db(table="writing_group_links", column="writing_group_links",
                                                    value=groups)
            await self.db_handler.clean_no_username()  # Чистка списка parsing списка, если нет username
            await self.db_handler.delete_duplicates(table_name="members",
                                                    column_name="id")  # Чистка дублирующих username по столбцу id
            await client.disconnect()

    async def choosing_a_group_from_the_subscribed_ones_for_parsing(self) -> None:
        """Выбираем группу из подписанных для parsing"""
        entities = find_files(directory_path="user_settings/accounts/parsing", extension='session')
        for file in entities:
            client = await self.connect_to_telegram(file)
            tg_tar = await self.output_a_list_of_groups_new(client)
            all_participants_list = await self.parsing_of_users_from_the_selected_group(client, tg_tar)
            # Записываем parsing данные в файл user_settings/software_database.db
            entities: list = await self.all_participants_user(all_participants_list)
            await self.db_handler.write_parsed_chat_participants_to_db(entities)
            await self.db_handler.clean_no_username()  # Чистка списка parsing списка, если нет username
            await self.db_handler.delete_duplicates(table_name="members",
                                                    column_name="id")  # Чистка дублирующих username по столбцу id
            await client.disconnect()  # Разрываем соединение telegram

    async def parsing_of_active_participants(self, chat_input, limit_active_user) -> None:
        """
        Parsing участников, которые пишут в чат (активных участников)
        :param chat_input: ссылка на чат
        :param limit_active_user: лимит активных участников
        """
        entities = find_files(directory_path="user_settings/accounts/parsing", extension='session')
        for file in entities:
            client = await self.connect_to_telegram(file)
            await subscribe_to_group_or_channel(client, chat_input)
            time_activity_user_1, time_activity_user_2 = self.config_reader.get_time_activity_user()
            time.sleep(time_activity_user_2)
            await self.we_get_the_data_of_the_group_members_who_wrote_messages(client, chat_input, limit_active_user)
            await client.disconnect()  # Разрываем соединение telegram
        await self.db_handler.clean_no_username()  # Чистка списка parsing списка, если нет username
        await self.db_handler.delete_duplicates(table_name="members",
                                                column_name="id")  # Чистка дублирующих username по столбцу id

    async def group_parsing(self, client, groups_wr) -> None:
        """
        Эта функция выполняет парсинг групп, на которые пользователь подписался. Аргумент phone используется декоратором
        @handle_exceptions для отлавливания ошибок и записи их в базу данных user_settings/software_database.db.
        """
        all_participants: list = await self.parsing_of_users_from_the_selected_group(client, groups_wr)
        logger.info(f"[+] Спарсили данные с группы {groups_wr}")
        # Записываем parsing данные в файл user_settings/software_database.db
        entities: list = await self.all_participants_user(all_participants)
        await self.db_handler.write_parsed_chat_participants_to_db(entities)

    async def we_get_the_data_of_the_group_members_who_wrote_messages(self, client, chat, limit_active_user) -> None:
        """
        Получаем данные участников группы которые писали сообщения
        :param client: клиент Telegram
        :param chat: ссылка на чат
        :param limit_active_user: лимит активных участников
        """
        async for message in client.iter_messages(chat, limit=int(limit_active_user)):
            if message.from_id is not None and hasattr(message.from_id, 'user_id'):
                from_user = await client.get_entity(message.from_id.user_id)  # Получаем отправителя по ИД
                entities = await self.getting_active_user_data(from_user)
                logger.info(entities)
                await self.db_handler.write_parsed_chat_participants_to_db_active(entities)
            else:
                logger.warning(f"Message {message.id} does not have a valid from_id.")

    async def output_a_list_of_groups_new(self, client):
        """Выводим список групп, выбираем группу, которую будем parsing user с группы telegram
        :param client: объект клиента
        """
        chats: list = []
        last_date = None
        groups: list = []
        result = await client(GetDialogsRequest(offset_date=last_date, offset_id=0,
                                                offset_peer=InputPeerEmpty(), limit=200, hash=0))
        chats.extend(result.chats)
        for chat in chats:

            try:
                if chat.megagroup:
                    groups.append(chat)
            except AttributeError:
                continue  # Игнорируем объекты, у которых нет атрибута 'megagroup'

        i = 0
        for g in groups:
            logger.info(f"[{str(i)}] - {g.title}")
            i += 1
        logger.info("")

        logger.info("[+] Введите номер группы: ")

        g_index = input("")

        target_group = groups[int(g_index)]
        return target_group

    async def parsing_of_users_from_the_selected_group(self, client, target_group) -> list:
        """Собираем данные user и записываем в файл members.db (создание нового файла members.db)"""

        logger.info("[+] Ищем участников... Сохраняем в файл software_database.db...")

        all_participants: list = []
        while_condition = True
        my_filter = ChannelParticipantsSearch("")
        offset = 0
        while while_condition:
            try:
                participants = await client(
                    GetParticipantsRequest(channel=target_group, offset=offset, filter=my_filter,
                                           limit=200, hash=0))

                all_participants.extend(participants.users)
                offset += len(participants.users)
                if len(participants.users) < 1:
                    while_condition = False
            except TypeError:
                logger.info(
                    f'Ошибка parsing: не верное имя или cсылка {target_group} не является группой / каналом: {target_group}')
                time.sleep(2)
                break
        return all_participants

    async def all_participants_user(self, all_participants) -> list:
        """Формируем список user_settings/software_database.db"""
        entities: list = []  # Создаем словарь
        for user in all_participants:
            await self.getting_user_data(user, entities)
        return entities  # Возвращаем словарь пользователей

    async def getting_user_data(self, user, entities) -> None:
        """Получаем данные пользователя"""
        username = user.username if user.username else "NONE"
        user_phone = user.phone if user.phone else "Номер телефона скрыт"
        first_name = user.first_name if user.first_name else ""
        last_name = user.last_name if user.last_name else ""
        photos_id = (
            "Пользователь с фото" if isinstance(user.photo, types.UserProfilePhoto) else "Пользователь без фото")
        online_at = "Был(а) недавно"
        # Статусы пользователя https://core.telegram.org/type/UserStatus
        if isinstance(user.status, (
                UserStatusRecently, UserStatusOffline, UserStatusLastWeek, UserStatusLastMonth, UserStatusOnline,
                UserStatusEmpty)):
            if isinstance(user.status, UserStatusOffline):
                online_at = user.status.was_online
            if isinstance(user.status, UserStatusRecently):
                online_at = "Был(а) недавно"
            if isinstance(user.status, UserStatusLastWeek):
                online_at = "Был(а) на этой неделе"
            if isinstance(user.status, UserStatusLastMonth):
                online_at = "Был(а) в этом месяце"
            if isinstance(user.status, UserStatusOnline):
                online_at = user.status.expires
            if isinstance(user.status, UserStatusEmpty):
                online_at = "статус пользователя еще не определен"
        user_premium = "Пользователь с premium" if user.premium else ""

        entities.append(
            [username, user.id, user.access_hash, first_name, last_name, user_phone, online_at, photos_id,
             user_premium])

    async def getting_active_user_data(self, user):
        """Получаем данные пользователя"""
        username = user.username if user.username else "NONE"
        user_phone = user.phone if user.phone else "Номер телефона скрыт"
        first_name = user.first_name if user.first_name else ""
        last_name = user.last_name if user.last_name else ""
        photos_id = (
            "Пользователь с фото" if isinstance(user.photo, types.UserProfilePhoto) else "Пользователь без фото")
        online_at = "Был(а) недавно"
        # Статусы пользователя https://core.telegram.org/type/UserStatus
        if isinstance(user.status, (
                UserStatusRecently, UserStatusOffline, UserStatusLastWeek, UserStatusLastMonth, UserStatusOnline,
                UserStatusEmpty)):
            if isinstance(user.status, UserStatusOffline):
                online_at = user.status.was_online
            if isinstance(user.status, UserStatusRecently):
                online_at = "Был(а) недавно"
            if isinstance(user.status, UserStatusLastWeek):
                online_at = "Был(а) на этой неделе"
            if isinstance(user.status, UserStatusLastMonth):
                online_at = "Был(а) в этом месяце"
            if isinstance(user.status, UserStatusOnline):
                online_at = user.status.expires
            if isinstance(user.status, UserStatusEmpty):
                online_at = "статус пользователя еще не определен"
        user_premium = "Пользователь с premium" if user.premium else ""

        entity = (username, user.id, user.access_hash,
                  first_name, last_name, user_phone,
                  online_at, photos_id, user_premium)

        return entity

    """Parsing активных участников группы"""

    """Работа с номерами телефонов"""

    async def we_record_phone_numbers_in_the_db(self) -> None:
        """Записываем номера телефонов в базу данных"""
        logger.info("Контакты которые были добавлены в телефонную книгу, будем записывать с файл "
                    "software_database.db, в папке user_settings")
        # Вводим имя файла с которым будем работать
        file_name_input = input("[+] Введите имя файла с контактами, в папке contacts, имя вводим без txt: ")
        # Открываем файл с которым будем работать
        with open(f"user_settings/{file_name_input}.txt", "r") as file_contact:
            for line in file_contact.readlines():
                logger.info(line.strip())
                # strip() - удаляет с конца и начала строки лишние пробелы, в том числе символ окончания строки
                lines = line.strip()
                entities = [lines]
                await self.db_handler.write_data_to_db("CREATE TABLE IF NOT EXISTS contact(phone)",
                                                       "INSERT INTO contact(phone) VALUES (?)", entities)

    async def show_account_contact_list(self) -> None:
        """Показать список контактов аккаунтов и запись результатов в файл"""
        # Открываем базу данных для работы с аккаунтами user_settings/software_database.db
        records: list = await self.db_handler.open_and_read_data("config")
        for row in records:
            # Подключение к Telegram и вывод имя аккаунта в консоль / терминал
            # client, phone = telegram_connect_and_output_name(row, db_handler)
            await self.parsing_and_recording_contacts_in_the_database(client)
            client.disconnect()  # Разрываем соединение telegram

    async def parsing_and_recording_contacts_in_the_database(self, client) -> None:
        """Парсинг и запись контактов в базу данных"""
        entities: list = []  # Создаем список сущностей
        all_participants = self.get_and_parse_contacts(client)
        for contact in all_participants:  # Выводим результат parsing
            await self.getting_user_data(contact, entities)
        await self.db_handler.write_parsed_chat_participants_to_db(entities)

    async def we_get_the_account_id(self, client) -> None:
        """Получаем id аккаунта"""
        entities: list = []  # Создаем список сущностей
        all_participants = self.get_and_parse_contacts(client)
        for user in all_participants:  # Выводим результат parsing
            await self.getting_user_data(user, entities)
            await self.we_show_and_delete_the_contact_of_the_phone_book(client, user)
        await self.db_handler.write_parsed_chat_participants_to_db(entities)

    async def get_and_parse_contacts(self, client) -> list:
        all_participants: list = []
        result = client(functions.contacts.GetContactsRequest(hash=0))
        logger.info(result)  # Печатаем результат
        all_participants.extend(result.users)
        return all_participants

    async def we_show_and_delete_the_contact_of_the_phone_book(self, client, user) -> None:
        """Показываем и удаляем контакт телефонной книги"""
        client(functions.contacts.DeleteContactsRequest(id=[user.id]))
        logger.info("Подождите 2 - 4 секунды")
        time.sleep(random.randrange(2, 3, 4))  # Спим для избежания ошибки о flood

    async def delete_contact(self) -> None:
        """Удаляем контакты с аккаунтов"""
        records: list = await self.db_handler.open_and_read_data("config")
        for row in records:
            # Подключение к Telegram и вывод имя аккаунта в консоль / терминал
            # client, phone = await telegram_connect_and_output_name(row, db_handler)
            await self.we_get_the_account_id(client)
            client.disconnect()  # Разрываем соединение telegram

    async def inviting_contact(self) -> None:
        """Добавление данных в телефонную книгу с последующим формированием списка software_database.db, для inviting"""
        # Открываем базу данных для работы с аккаунтами user_settings/software_database.db
        records: list = await self.db_handler.open_and_read_data("config")
        logger.info(f"Всего accounts: {len(records)}")
        for row in records:
            # Подключение к Telegram и вывод имя аккаунта в консоль / терминал
            # client, phone = await telegram_connect_and_output_name(row, db_handler)
            await self.adding_a_contact_to_the_phone_book(client)

    async def adding_a_contact_to_the_phone_book(self, client) -> None:
        """Добавляем контакт в телефонную книгу"""
        records: list = await self.db_handler.open_and_read_data("contact")
        logger.info(f"Всего номеров: {len(records)}")
        entities: list = []  # Создаем список сущностей
        for rows in records:
            user = {"phone": rows[0]}
            phone = user["phone"]
            # Добавляем контакт в телефонную книгу
            client(functions.contacts.ImportContactsRequest(contacts=[types.InputPhoneContact(client_id=0,
                                                                                              phone=phone,
                                                                                              first_name="Номер",
                                                                                              last_name=phone)]))
            try:
                # Получаем данные номера телефона https://docs.telethon.dev/en/stable/concepts/entities.html
                contact = client.get_entity(phone)
                await self.getting_user_data(contact, entities)
                logger.info(f"[+] Контакт с добавлен в телефонную книгу!")
                time.sleep(4)
                # Запись результатов parsing в файл members_contacts.db, для дальнейшего inviting
                # После работы с номером телефона, программа удаляет номер со списка
                await self.db_handler.delete_row_db(table="contact", column="phone", value=user["phone"])
            except ValueError:
                logger.info(
                    f"[+] Контакт с номером {phone} не зарегистрирован или отсутствует возможность добавить в телефонную книгу!")
                # После работы с номером телефона, программа удаляет номер со списка
                await self.db_handler.delete_row_db(table="contact", column="phone", value=user["phone"])
        client.disconnect()  # Разрываем соединение telegram
        await self.db_handler.write_parsed_chat_participants_to_db(entities)
        await self.db_handler.clean_no_username()  # Чистка списка parsing списка, если нет username
