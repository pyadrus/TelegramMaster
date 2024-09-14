import flet as ft

line_width = 580  # Ширина окна и ширина строки


async def settings_menu(page):
    """Меню настройки"""
    page.views.append(
        ft.View("/settings",
                [ft.AppBar(title=ft.Text("Главное меню"),
                           bgcolor=ft.colors.SURFACE_VARIANT),
                 ft.Column([  # Добавляет все чекбоксы и кнопку на страницу (page) в виде колонок.
                     ft.Row([ft.ElevatedButton(width=270, height=30, text="Выбор реакций",
                                               on_click=lambda _: page.go("/choice_of_reactions")),
                             ft.ElevatedButton(width=270, height=30, text="Запись proxy",
                                               on_click=lambda _: page.go("/proxy_entry"))]),
                     ft.Row([ft.ElevatedButton(width=270, height=30, text="Смена аккаунтов",
                                               on_click=lambda _: page.go("/changing_accounts")),
                             ft.ElevatedButton(width=270, height=30, text="Запись api_id, api_hash",
                                               on_click=lambda _: page.go("/recording_api_id_api_hash"))]),
                     ft.Row([ft.ElevatedButton(width=270, height=30, text="Запись времени",
                                               on_click=lambda _: page.go("/time_between_subscriptions")),
                             ft.ElevatedButton(width=270, height=30, text="Запись сообщений",
                                               on_click=lambda _: page.go("/message_recording"))]),
                     ft.Row([ft.ElevatedButton(width=270, height=30, text="Запись ссылки для инвайтинга",
                                               on_click=lambda _: page.go("/link_entry")),
                             ft.ElevatedButton(width=270, height=30, text="Лимиты на аккаунт",
                                               on_click=lambda _: page.go("/account_limits"))]),
                     ft.Row([ft.ElevatedButton(width=270, height=30, text="Лимиты на сообщения",
                                               on_click=lambda _: page.go("/message_limits")),
                             ft.ElevatedButton(width=270, height=30, text="Время между подпиской",
                                               on_click=lambda _: page.go("/time_between_subscriptionss")), ]),
                     ft.ElevatedButton(width=line_width, height=30, text="Формирование списка username",
                                       on_click=lambda _: page.go("/creating_username_list")),
                     ft.ElevatedButton(width=line_width, height=30, text="Запись времени между сообщениями",
                                       on_click=lambda _: page.go("/recording_the_time_between_messages")),
                     ft.ElevatedButton(width=line_width, height=30,
                                       text="Время между инвайтингом, рассылка сообщений",
                                       on_click=lambda _: page.go("/time_between_invites_sending_messages")),
                     ft.ElevatedButton(width=line_width, height=30, text="Запись ссылки для реакций",
                                       on_click=lambda _: page.go("/recording_reaction_link")),
                     ft.ElevatedButton(width=line_width, height=30, text="Формирование списка чатов / каналов",
                                       on_click=lambda _: page.go("/forming_list_of_chats_channels")),
                 ])]))


async def bio_editing_menu(page):
    """Меню редактирование БИО"""
    page.views.append(
        ft.View("/bio_editing",
                [ft.AppBar(title=ft.Text("Главное меню"),
                           bgcolor=ft.colors.SURFACE_VARIANT),
                 ft.Column([  # Добавляет все чекбоксы и кнопку на страницу (page) в виде колонок.
                     ft.ElevatedButton(width=line_width, height=30, text="Изменение username",
                                       on_click=lambda _: page.go("/changing_username")),
                     ft.ElevatedButton(width=line_width, height=30, text="Изменение фото",
                                       on_click=lambda _: page.go("/edit_photo")),
                     ft.ElevatedButton(width=line_width, height=30, text="Изменение описания",
                                       on_click=lambda _: page.go("/edit_description")),
                     ft.ElevatedButton(width=line_width, height=30, text="Изменение имени",
                                       on_click=lambda _: page.go("/name_change")),
                     ft.ElevatedButton(width=line_width, height=30, text="Изменение фамилии",
                                       on_click=lambda _: page.go("/change_surname")),
                 ])]))


async def inviting_menu(page):
    """Меню инвайтинг"""
    page.views.append(
        ft.View("/inviting",
                [ft.AppBar(title=ft.Text("Главное меню"),
                           bgcolor=ft.colors.SURFACE_VARIANT),
                 ft.Column([  # Добавляет все чекбоксы и кнопку на страницу (page) в виде колонок.
                     ft.ElevatedButton(width=line_width, height=30, text="Инвайтинг",
                                       on_click=lambda _: page.go("/inviting_without_limits")),
                     ft.ElevatedButton(width=line_width, height=30, text="Инвайтинг 1 раз в час",
                                       on_click=lambda _: page.go("/inviting_1_time_per_hour")),
                     ft.ElevatedButton(width=line_width, height=30, text="Инвайтинг в определенное время",
                                       on_click=lambda _: page.go("/inviting_certain_time")),
                     ft.ElevatedButton(width=line_width, height=30, text="Инвайтинг каждый день",
                                       on_click=lambda _: page.go("/inviting_every_day")),
                 ])]))


async def message_distribution_menu(page):
    """Меню рассылка сообщений"""
    page.views.append(
        ft.View("/sending_messages",
                [ft.AppBar(title=ft.Text("Главное меню"),
                           bgcolor=ft.colors.SURFACE_VARIANT),
                 ft.Column([  # Добавляет все чекбоксы и кнопку на страницу (page) в виде колонок.
                     ft.ElevatedButton(width=line_width, height=30, text="Отправка сообщений в личку",
                                       on_click=lambda _: page.go("/sending_messages_personal_account")),
                     ft.ElevatedButton(width=line_width, height=30, text="Отправка файлов в личку",
                                       on_click=lambda _: page.go("/sending_files_personal_account")),
                     ft.ElevatedButton(width=line_width, height=30, text="Рассылка сообщений по чатам",
                                       on_click=lambda _: page.go("/sending_messages_via_chats")),
                     ft.ElevatedButton(width=line_width, height=30,
                                       text="Рассылка сообщений по чатам с автоответчиком",
                                       on_click=lambda _: page.go(
                                           "/sending_messages_via_chats_with_answering_machine")),
                     ft.ElevatedButton(width=line_width, height=30, text="Рассылка файлов по чатам",
                                       on_click=lambda _: page.go("/sending_files_via_chats")),
                     ft.ElevatedButton(width=line_width, height=30, text="Рассылка сообщений + файлов по чатам",
                                       on_click=lambda _: page.go("/sending_messages_files_via_chats")),
                     ft.ElevatedButton(width=line_width, height=30,
                                       text="Отправка сообщений в личку (с лимитами)",
                                       on_click=lambda _: page.go("/sending_personal_messages_with_limits")),
                     ft.ElevatedButton(width=line_width, height=30, text="Отправка файлов в личку (с лимитами)",
                                       on_click=lambda _: page.go(
                                           "/sending_files_to_personal_account_with_limits")),
                 ])]))


async def working_with_contacts_menu(page):
    """Меню работа с контактами"""
    page.views.append(
        ft.View("/working_with_contacts",
                [ft.AppBar(title=ft.Text("Главное меню"),
                           bgcolor=ft.colors.SURFACE_VARIANT),
                 ft.Column([  # Добавляет все чекбоксы и кнопку на страницу (page) в виде колонок.
                     ft.ElevatedButton(width=line_width, height=30, text="Формирование списка контактов",
                                       on_click=lambda _: page.go("/creating_contact_list")),
                     ft.ElevatedButton(width=line_width, height=30, text="Показать список контактов",
                                       on_click=lambda _: page.go("/show_list_contacts")),
                     ft.ElevatedButton(width=line_width, height=30, text="Удаление контактов",
                                       on_click=lambda _: page.go("/deleting_contacts")),
                     ft.ElevatedButton(width=line_width, height=30, text="Добавление контактов",
                                       on_click=lambda _: page.go("/adding_contacts")),
                 ])]))


async def menu_parsing(page):
    """Парсинг меню"""
    page.views.append(
        ft.View("/parsing",
                [ft.AppBar(title=ft.Text("Главное меню"),
                           bgcolor=ft.colors.SURFACE_VARIANT),
                 ft.Column([  # Добавляет все чекбоксы и кнопку на страницу (page) в виде колонок.
                     ft.ElevatedButton(width=line_width, height=30,
                                       text="Парсинг одной группы / групп",
                                       on_click=lambda _: page.go("/parsing_single_groups")),
                     ft.ElevatedButton(width=line_width, height=30,
                                       text="Парсинг выбранной группы из подписанных пользователем",
                                       on_click=lambda _: page.go("/parsing_selected_group_user_subscribed")),
                     ft.ElevatedButton(width=line_width, height=30,
                                       text="Парсинг активных участников группы",
                                       on_click=lambda _: page.go("/parsing_active_group_members")),
                     ft.ElevatedButton(width=line_width, height=30,
                                       text="Парсинг групп / каналов на которые подписан аккаунт",
                                       on_click=lambda _: page.go(
                                           "/parsing_groups_channels_account_subscribed")),
                     ft.ElevatedButton(width=line_width, height=30,
                                       text="Очистка списка от ранее спарсенных данных",
                                       on_click=lambda _: page.go("/clearing_list_previously_saved_data")),
                 ])]))


async def reactions_menu(page):
    """Меню работа с реакциями"""
    page.views.append(
        ft.View("/working_with_reactions",
                [ft.AppBar(title=ft.Text("Главное меню"),
                           bgcolor=ft.colors.SURFACE_VARIANT),
                 ft.Column([  # Добавляет все чекбоксы и кнопку на страницу (page) в виде колонок.
                     ft.ElevatedButton(width=line_width, height=30, text="Ставим реакции",
                                       on_click=lambda _: page.go("/setting_reactions")),
                     ft.ElevatedButton(width=line_width, height=30, text="Накручиваем просмотры постов",
                                       on_click=lambda _: page.go("/we_are_winding_up_post_views")),
                     ft.ElevatedButton(width=line_width, height=30, text="Автоматическое выставление реакций",
                                       on_click=lambda _: page.go("/automatic_setting_of_reactions")),
                 ])]))


async def subscribe_and_unsubscribe_menu(page):
    """Меню подписка и отписка"""
    page.views.append(
        ft.View("/subscribe_unsubscribe",
                [ft.AppBar(title=ft.Text("Главное меню"),
                           bgcolor=ft.colors.SURFACE_VARIANT),
                 ft.Column([  # Добавляет все чекбоксы и кнопку на страницу (page) в виде колонок.
                     ft.ElevatedButton(width=line_width, height=30, text="Подписка",
                                       on_click=lambda _: page.go("/subscription_all")),
                     ft.ElevatedButton(width=line_width, height=30, text="Отписываемся",
                                       on_click=lambda _: page.go("/unsubscribe_all")),
                 ])]))
