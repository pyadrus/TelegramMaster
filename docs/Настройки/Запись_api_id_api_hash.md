Для записи api_id, api_hash и возможности дальнейшего взаимодействия с аккаунтами Telegram выполните следующие действия:

1. Запустить TelegramMaster (см. [Запуск TelegramMaster](https://github.com/pyadrus/TelegramMaster/blob/be6a5227cc285e000763645563b2d21c600939f6/docs/%D0%9D%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B8_%D0%B8_%D0%BA%D0%BE%D0%BD%D1%84%D0%B8%D0%B3%D1%83%D1%80%D0%B0%D1%86%D0%B8%D1%8F/%D0%97%D0%B0%D0%BF%D1%83%D1%81%D0%BA_TelegramMaster.md)).
2. Перейти в раздел "[Настройки](Настройки.md)".
3. Запустить функцию "[Запись api_id, api_hash](Запись_api_id_api_hash.md)".
4. Ввести api_id
5. Ввести api_hash
6. После завершения этого процесса TelegramMaster перезапустится.

После выполнения указанных действий программа автоматически запишет введенные данные в файл `TelegramMaster/user_settings/config.ini`.

> **ПРИМЕЧАНИЕ**
> Убедитесь в правильности ввода api_id, api_hash, если поля ввода будут пустыми, то и в файл `TelegramMaster/user_settings/config.ini` запишутся пустые данные, что повлечет за собой ошибки TelegramMaster.