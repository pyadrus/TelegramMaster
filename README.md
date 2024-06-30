# TelegramMaster 🚀
Проект TelegramMaster создан на основе библиотеки Telethon и активно развивается с 29.01.2022 года.

>  [!info]
> ⚠️ Этот проект представляет собой личный (открытый) репозиторий, созданный для разработки новых версий программы. Полнофункциональную 
версию можно найти на канале https://t.me/master_tg_d.

<hr align="center"/>

Основные функции:

- [Инвайтинг](docs/Инвайтинг/Инвайтинг.md)
  - [✔️ Инвайтинг без лимитов](docs/Инвайтинг/Инвайтинг_без_лимитов.md)
  - [✔️ Инвайтинг с лимитами](docs/Инвайтинг/Инвайтинг_с_лимитами.md)
  - [✔️ Инвайтинг 1 раз в час](docs/Инвайтинг/Инвайтинг_1_раз_в_час.md)
  - [✔️ Инвайтинг в определенное время](docs/Инвайтинг/Инвайтинг_в_определенное_время.md)
  - [✔️ Инвайтинг каждый день](docs/Инвайтинг/Инвайтинг_каждый_день.md)
- [Парсинг](docs/Парсинг/Парсинг.md)
  - [✔️ Парсинг одной группы - групп](docs/Парсинг/Парсинг_одной_группы_групп.md)
  - [✔️ Парсинг выбранной группы из подписанных пользователем](docs/Парсинг/Парсинг_выбранной_группы_из_подписанных_пользователем.md)
  - [✔️ Парсинг активных участников группы](docs/Парсинг/Парсинг_активных_участников_группы.md)
  - [✔️ Парсинг групп - каналов на которые подписан аккаунт](docs/Парсинг/Парсинг_групп_каналов_на_которые_подписан_аккаунт.md)
  - [✔️ Очистка списка от ранее спарсенных данных](docs/Парсинг/Очистка_списка_от_ранее_спарсенных_данных.md)
- [Работа с контактами]()
  - [Формирование списка контактов]()
  - [Показ списка контактов]()
  - [Удаление контактов]()
  - [Добавление контактов]()
- [Подписка, отписка]()
  - [Подписка]()
  - [Отписка]()
- [Подключение аккаунтов]()
- [Рассылка сообщений]()
  - [Отправка сообщений в личку]()
  - [Отправка файлов в личку]()
  - [Рассылка сообщений по чатам]()
  - [Рассылка сообщений по чатам с автоответчиком]()
  - [Рассылка файлов по чатам]()
  - [Рассылка сообщений + файлов по чатам]()
  - [Отправка сообщений в личку (с лимитами)]()
  - [Отправка файлов в личку (с лимитами)]()
- [Работа с реакциями]()
  - [Ставим реакцию на 1 пост]()
  - [Накручиваем просмотры постов]()
  - [Автоматическое выставление реакций]()
- [Проверка аккаунтов]()
- [Создание групп (чатов)]()
- [Редактирование BIO]()
  - [Изменение username]()
  - [Изменение фото]()
  - [Изменение описания]()
  - [Изменение имени]()
  - [Изменение фамилии]()
- [Настройка]()
  - [Запись ссылки]()
  - [Запись api_id, api_hash]()
  - [Время между Inviting, рассылка сообщений]()
  - [Смена аккаунтов]()
  - [Время между подпиской]()
  - [Запись proxy]()
  - [Лимиты на аккаунт]()
  - [Смена типа устройства]()
  - [Запись времени (для инвайтинга 1 раз в сутки)]()
  - [Лимиты на сообщения]()
  - [Выбор реакций]()
  - [Запись ссылки для реакций]()
  - [Запись количества аккаунтов для реакций]()
  - [Запись сообщений]()
  - [Запись времени между сообщениями]()
  - [Формирование списка чатов - каналов]()
  - [Запись имени аккаунта]()
  - [Формирование списка username]()

<hr align="center"/>

## Установка
Для установки необходимых библиотек используйте команду:

```python setup.py```

На Linux или Mac OS используйте:

```python3 setup.py```

<a name="Запуск">Запуск программы</a>

Используйте <b>Запуск.bat</b> или следующую команду для запуска:

```python main.py```

На Linux или Mac OS используйте:

```python3 main.py```

<hr align="center"/>

## Обратная связь

Telegram: https://t.me/PyAdminRU

VK: https://vk.com/zh.vitaliy

## Дополнительная информация

Telegram: https://t.me/master_tg_d

VK: https://vk.com/tg_smm2

📣 Не забудьте поделиться своим опытом и отзывами!

🚀 Приятного использования! 🚀

<hr align="center"/>

# Документация по работе с TelegramMaster 🚀

**Рассылка сообщений по чатам**

Порядок действий:

1. <a href="#Запуск">Запустить программу _«TelegramMaster»_ 🚀</a>.
2. В настройках программы пропишите сообщения, которые будут рассылаться. Эти сообщения должны храниться по пути 
**user_settings/message** в формате **JSON**. При рассылке сообщений по группам (чатам) программа будет выбирать случайное 
сообщение из папки **user_settings/message**. Обратите внимание, что для более стабильной работы программы может 
потребоваться её перезагрузка.
3. Установите интервал времени, через который минуты будет отправляться сообщение в группе / группы.
4. Создайте список чатов в настройках программы в пункте меню _«Рассылка сообщений»_. Обратите внимание, что для более 
стабильной работы программы может потребоваться её перезагрузка.
5. Пропишите название аккаунта из папки с аккаунтами **user_settings/accounts**.
6. Запустите процесс рассылки сообщений по группам (чатам).
Программа будет брать случайное сообщение для отправки из папки **user_settings/message**.

**Автоответчик на сообщения**

Во время рассылки программа имеет функцию автоответчика. Сообщение для автоответа берется из <b>user_settings/answering_machine</b>.

<hr align="center"/>

#### Работа с BIO

1. Перед началом работы убедитесь, что ознакомились с лимитами Telegram. ([[Лимиты Telegram]])
2. Расположите файл сессии аккаунта в папке `TelegramMaster/user_settings/accounts/bio_accounts`. 

> [!warning] 
> ⚠️ Обратите внимание, что в папке должен быть только один файл сессии

3. Фото профиля должно быть размещено в папке `user_settings/bio`. Формат изображения должен быть JPG. Рекомендуемый 
минимальный размер изображения - **300 x 300** пикселей.
4. Вы можете изменить следующие параметры BIO аккаунта:\
   4.1. Username (не более 32 символов)\
   4.2.  Фото профиля (рекомендуемый минимальный размер - 300 x 300 пикселей)\
   4.3. Описание профиля (не более 70 символов)\
   4.4. Имя профиля (не более 64 символов)\
   4.5. Фамилия профиля (не более 64 символов)