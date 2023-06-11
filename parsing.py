import requests
import json
import pandas as pd
import psycopg2
from datetime import datetime, timedelta
from binance import Client
import time
# from connector import conn


# Параметры подключения к базе данных PostgreSQL
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'market-data'
DB_USER = 'your_username'
DB_PASSWORD = 'your_password'

# Параметры Binance API
API_KEY = open('token.txt').readlines()[0].strip()
API_SECRET = open('token.txt').readlines()[1].strip()
BASE_URL = 'https://api.binance.com/api/v3'

# Функция для получения минутных свечей за последнюю неделю
client = Client(API_KEY, API_SECRET)
#cur = conn.cursor()
# Символы, для которых нужно получить минутные свечи
symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'ADAUSDT']

# Параметры времени
end_time = datetime.now()
start_time = end_time - timedelta(days=7)

# Получение и сохранение минутных свечей для каждого символа
for symbol in symbols:
    print(symbol)
    all_candles = []

    # Разделение периода на дни и делаем запросы для каждого дня
    current_time = start_time
    while current_time <= end_time:
        candles = client.futures_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE,
                                        limit=1440,  # Максимальное значение limit для интервала 1 минута
                                        startTime=int(current_time.timestamp() * 1000),
                                        endTime=int((current_time + timedelta(days=1)).timestamp() * 1000))
        all_candles.extend(candles)
        current_time += timedelta(days=1)
    
    # Сохранение данных в CSV файл
    df = pd.DataFrame(all_candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    filename = f"{symbol}_candles.csv"
    df.to_csv(filename, index=False)
    
    for candle in all_candles:
        timestamp = pd.Timestamp(candle[0], unit='ms')
        open_price = float(candle[1])
        high_price = float(candle[2])
        low_price = float(candle[3])
        close_price = float(candle[4])
        volume = float(candle[5])
        
        # Вставка данных в таблицу crypto_data
        insert_query = """
        INSERT INTO crypto_data (symbol, timestamp, open, high, low, close, volume)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (symbol, timestamp, open_price, high_price, low_price, close_price, volume)




        #cur.execute(insert_query, values)

# Сохранение изменений
#conn.commit()

# Закрытие соединения
#cur.close()
#conn.close()