
Единая API для `set/get_file_*_time`: выровнять поведение/исключения и документацию у связанных функций (set_file_write_time, возможно get_file_create_time) под текущие правила.

`set_file_create_time` Тесты: добавить кейсы для tz-aware/naive, даты до 1601-01-01 (Windows), поведение на не‑Windows (skip/исключение), и явные проверки исключений для каталога/несуществующего файла.



**`os-sys`** — сторонний пакет в PyPI, который добавляет декоративные элементы (прогресс-бары, спиннеры в терминале) для консольных скриптов.

----------------

- [ ] os_script: реализовать поддержку получения списка физических дисков через `wmic diskdrive` (Windows):
      - вот тут готовый код:
        `D:\heXor\App\heX\autorun_hex\disk_list.py`
        `os_script\todo\disk_list.py`
      - Написать функцию парсинга сырых данных команды  
        `wmic diskdrive get deviceid, model, size, serialnumber /format:value`
        в структуру `list[dict]` с полями `DeviceID`, `Model`, `SerialNumber`, `Size`,
        а также рассчитанными `SizeGB` и `SizeStrGB`.
      - Написать функцию верхнего уровня `get_physical_disks_wmic()`, которая вызывает `run_command`,
        парсит вывод с помощью функции выше и возвращает список дисков.

