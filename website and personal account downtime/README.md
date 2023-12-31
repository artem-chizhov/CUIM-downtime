## Данный скрипт призван облегчить подсчет простоя сайта и личного кабинета на основе данных zabbix.

### **Задачи:**

- Разделить необходимый временной диапазон на отрезки по 12 часов (внутренние особенности системы мониторинга).
- Забрать данные с zabbix.
- Сформировать выгрузку в TXT файлы (опционально).
- Вставить выгруженные данные в конкретные ячейки Excel файла (в котором согласно формулам и производится подсчет простоя).

### **Зависимости**

>Особенности реализации:
>
>*GUI реализация по средствам библиотеки tkinter*
>
>*"Компиляция" производилась по средствам библиотеки auto-py-to-exe (не включена в requirements.txt)*

**Установка:**

    1. pip install auto-py-to-exe
    2. выполнить команду auto-py-to-exe
    3. в открывшемся окне выбираем script location -> файл main.py
    4. выбираем "Onefile"
    5. выбираем Window
    6. convert


*В корневой директории скрипт ожидает наличие файлов **.env**, **LK.xlsx**, **Site.xlsx***

>В файле переменных окружения (.env) хранятся данные следующего формата:
>
>       LOGIN_
>       PASSWORD_
>       IDX2_
>       URL_
>
>Эти данные необходимы для скраппинга данных из системы мониторинга, 
>      могут быть изменены по необходимости из GUI скрипта (вкладки - LOG/PASS и URL)



>Возможность редактирования имени файлов не реализовывалась.
>
>Скрипту нет дела до содержимого файлов(excel). Затирает определенные ячейки и вставляет данные, на этом его работа закончена.
