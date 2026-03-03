from sqltable import *

users = SQLTable(db_config, "users")

# создание таблицы
users.create_table(
    columns=[
        {"name": "id", "type": "INT", "nullable": False, "auto_increment": True},
        {"name": "name", "type": "VARCHAR(100)", "nullable": False},
        {"name": "email", "type": "VARCHAR(255)", "unique": True}
    ],
    primary_key="id"
)

# добавление столбца
users.add_column("age", "INT")

# добавление данных
users.insert({"name": "Alex", "email": "alex@gmail.com", "age": 25})
users.insert({"name": "Ivan", "email": "ivan@gmail.com", "age": 20})

# получение всех данных
print("-- получение всех записей --")
users.get_all()
for row in users.cursor.fetchall():
    print(row)

# получение данных по id
print("-- получение записи по id --")
users.get_id(1)
print(users.cursor.fetchone())

# обновление данных
print("-- обновление --")
users.update(1, {"name": "Lexa", "age": 26})
users.get_id(1)
print(users.cursor.fetchone())

# удаление данных по id
print("-- удаление по id --")
users.delete_id(1)
users.get_all()
for row in users.cursor.fetchall():
    print(row)

# удаление таблицы
users.delete_tab()

# завершение работы
users.close()