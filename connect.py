import psycopg2

# Подключение к базе данных
conn = psycopg2.connect(
    host='localhost',
    database='market-data',
    user='ilya',
    password=''
)

# Создание курсора для выполнения SQL-запросов
cur = conn.cursor()

# Создание таблицы
create_table_query = """
CREATE TABLE crypto_data (
    symbol TEXT NOT NULL,
    timestamp TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    open NUMERIC NOT NULL,
    high NUMERIC NOT NULL,
    low NUMERIC NOT NULL,
    close NUMERIC NOT NULL,
    volume NUMERIC NOT NULL
);
"""

cur.execute(create_table_query)

# Сохранение изменений
conn.commit()

# Закрытие соединения
cur.close()
conn.close()


