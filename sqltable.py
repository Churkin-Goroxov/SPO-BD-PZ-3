import re

import mysql.connector


class SQLTable:
    def __init__(self, db_config, table_name):
        """
        Initialize with database configuration and table name.

        :param db_config: Dictionary with keys 'user', 'password', 'host', 'database'.
        :param table_name: Name of the table in the database.
        """
        self.db_config = db_config
        self._validate_name(table_name)
        self.table_name = table_name
        self.connection = mysql.connector.connect(**db_config)
        self.cursor = self.connection.cursor()
        self.columns = []

    def _validate_name(self, name):
        """валдация значений, для защиты от инъекций
        Разрешено:
        - буквы
        - цифры
        - _
        - имя не может начинаться с цифры
        """
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name):
            raise ValueError(f"недопустимое имя: {name}")

    def create_table(self, columns: list, primary_key=None, existence=False):
        """
        создание таблицы

        columns: список словарей
        приемер:
        [
            {"name": "id", "type": "INT", "nullable": False, "auto_increment": True},
            { ... }
        ]
        """
        parts = []

        auto_incr = None

        for column in columns:
            name = column["name"]
            col_type = column["type"]

            self._validate_name(name)

            col_def = f"`{name}` {col_type}"

            if not column.get("nullable", True):
                col_def += " NOT NULL"

            if column.get("auto_increment", False):
                col_def += " AUTO_INCREMENT"
                auto_incr = name

            if column.get("unique", False):
                col_def += " UNIQUE"

            if "default" in column:
                col_def += f" DEFAULT {column['default']}"

            parts.append(col_def)

        if auto_incr:
            parts.append(f"PRIMARY KEY (`{auto_incr}`)")
        elif primary_key:
            self._validate_name(primary_key)
            parts.append(f"PRIMARY_REY (`{primary_key}`)")

        body = ",\n ".join(parts)
        exist = "IF NOT EXISTS " if not existence else ""

        query = f"""
        CREATE TABLE {exist}`{self.table_name}` (
        {body}
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """

        self.cursor.execute(query)
        self.connection.commit()

    def add_column(self, name, col_type, nullable=True):
        """добавление столбца"""
        self._validate_name(name)

        col_def = f"`{name}` {col_type}"

        if not nullable:
            col_def += " NOT NULL"

        query = f"""
        ALTER TABLE `{self.table_name}`
        ADD COLUMN {col_def}
        """

        self.cursor.execute(query)
        self.connection.commit()

    def get_all(self):
        """получение всех записей таблицы"""
        query = f"SELECT * FROM `{self.table_name}`"
        self.cursor.execute(query)

    def get_id(self, ness_id):
        """получение записи по id"""
        query = f"SELECT * FROM `{self.table_name}` WHERE id = %s"
        self.cursor.execute(query, (ness_id, ))

    def insert(self, data: dict):
        """добавление значений посторочно"""

        for key in data.keys():
            self._validate_name(key)

        columns = ", ".join(f"`{key}`" for key in data.keys())
        filler = ", ".join(["%s"] * len(data))
        values = tuple(data.values())

        query = f"""
        INSERT INTO `{self.table_name}`
        ({columns})
        VALUES ({filler})
        """

        self.cursor.execute(query, values)
        self.connection.commit()

    def update(self, ness_id, data: dict):
        """обнавление значений"""

        for key in data.keys():
            if key == "id":
                continue
            self._validate_name(key)

        # set_values = ", ".join([f"`{key}`=%s" for key in data.keys() if key != "id"])
        # values = tuple(value for key, value in data.items() if key != "id") + (ness_id, )

        set_values = ", ".join([f"`{key}`=%s" for key in data.keys()])
        values = tuple(data.values()) + (ness_id, )

        query = f"""
        UPDATE `{self.table_name}`
        SET {set_values}
        WHERE id = %s
        """

        self.cursor.execute(query, values)
        self.connection.commit()

    def delete_id(self, ness_id):
        """удаление по id"""
        query = f"DELETE FROM `{self.table_name}` WHERE id = %s"
        self.cursor.execute(query, (ness_id, ))
        self.connection.commit()

    def delete_tab(self):
        """удаление таблицы"""
        query = f"DROP TABLE `{self.table_name}`"
        self.cursor.execute(query)
        self.connection.commit()

    def close(self):
        """закрытие соединения с БД"""
        self.cursor.close()
        self.connection.close()


db_config = {
    "host": "srv221-h-st.jino.ru",
    "user": "j30084097_137",
    "password": "Gruppa137",
    "database": "j30084097_137",
    "use_pure": True
}
