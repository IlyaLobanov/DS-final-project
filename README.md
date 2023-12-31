Документация проекта DS-final-project
Обзор
DS-final-project представляет собой проект по созданию системы для бэктестирования торговых стратегий. Основной код находится в файле backtest.py, который содержит класс Backtester для проведения бэктестирования.

Зависимости
Проект использует следующие библиотеки Python:

pandas
pickle
matplotlib
numpy
ta
matplotlib.dates
Класс Backtester
Основным компонентом проекта является класс Backtester. Он принимает следующие параметры при инициализации:

symbol: символ акции для тестирования
candles: исторические данные о ценах
initial_cash: начальный баланс для тестирования
commission: комиссия за сделку
Методы класса Backtester
load_model(self, model_file)
Загружает модель из файла pickle. 

strategy(self, candle)
Определяет базовую торговую стратегию, предсказывая цену закрытия и возвращая 'buy' если предсказанная цена выше текущей цены закрытия, 'sell' если ниже, и 'hold' в противном случае.

sma_crossover_strategy(self, candles)
Определяет торговую стратегию на основе пересечения скользящих средних (SMA). Возвращает 'buy' при восходящем пересечении и 'sell' при нисходящем пересечении.

rsi_strategy(self, candles)
Определяет торговую стратегию на основе индикатора относительной силы (RSI). Возвращает 'buy' если RSI меньше 30 (оверсолд), 'sell' если RSI больше 70 (овербот), и 'hold' в противном случае.

macd_strategy(self, candles)
Определяет торговую стратегию на основе индикатора MACD. Возвращает 'buy' при восходящем пересечении и 'sell' при нисходящем пересечении.

bollinger_bands_strategy(self, candles)
Определяет торговую стратегию на основе полос Боллинджера. Возвращает 'buy' если цена закрытия ниже нижней полосы(оверсолд), 'sell' если цена закрытия выше верхней полосы (овербот), и 'hold' в противном случае.

run_backtest(self, strategy_name, risk_pct)
Запускает бэктестирование с указанной стратегией и процентом риска. Стратегии включают "ML" (вероятно, основан на загруженной модели), "SMA" (пересечение скользящих средних), "RSI" (индикатор относительной силы), и "MACD" (индикатор MACD.

Другие файлы
В проекте также есть файлы data.py и model.py 

Заключение
DS-final-project представляет собой интересный проект, ориентированный на бэктестирование различных торговых стратегий с использованием исторических данных о ценах. Основной файл backtest.py содержит ряд стратегий, которые могут быть тестированы, а также возможность загрузить и использовать обученную модель для предсказания цены закрытия
