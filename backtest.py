import pandas as pd
import pickle
import matplotlib.pyplot as plt
import numpy as np
import ta
import matplotlib.dates as mdates

class Backtester:
    def __init__(self, symbol, candles, initial_cash, commission):
        self.symbol = symbol
        self.candles = candles
        self.trades = pd.DataFrame(columns=['timestamp', 'type', 'price', 'quantity'])
        self.pnl = pd.DataFrame(columns=['timestamp', 'pnl'])
        self.cash = initial_cash
        self.commission = commission
        self.mid_prices = []
        self.close_prices = []
        self.timestamps = []

    def load_model(self, model_file):
        with open(model_file, 'rb') as file:
            self.model = pickle.load(file)

    def strategy(self, candle):
        open_price = candle.open
        high_price = candle.high
        low_price = candle.low
        close_price = candle.close

        input_data = {
            'open': open_price,
            'high': high_price,
            'low': low_price,
            'close': close_price
        }
        predicted_close_price = self.model.predict(pd.DataFrame([input_data]))
        if predicted_close_price > close_price:
            return 'buy'
        elif predicted_close_price < close_price:
            return 'sell'
        else:
            return 'hold'

    def sma_crossover_strategy(self, candles):
        sma_short = ta.trend.sma_indicator(candles['close'], window=5)
        sma_long = ta.trend.sma_indicator(candles['close'], window=10)
        if sma_short.iloc[-1] > sma_long.iloc[-1] and sma_short.iloc[-2] < sma_long.iloc[-2]:
            return 'buy'
        elif sma_short.iloc[-1] < sma_long.iloc[-1] and sma_short.iloc[-2] > sma_long.iloc[-2]:
            return 'sell'
        else:
            return 'hold'

    def rsi_strategy(self, candles):
        rsi = ta.momentum.rsi_indicator(candles['close'], window=14)
        if rsi.iloc[-1] < 30:
            return 'buy'
        elif rsi.iloc[-1] > 70:
            return 'sell'
        else:
            return 'hold'

    def macd_strategy(self, candles):
        macd = ta.trend.macd_diff(candles['close'])
        if macd.iloc[-1] > 0 and macd.iloc[-2] < 0:
            return 'buy'
        elif macd.iloc[-1] < 0 and macd.iloc[-2] > 0:
            return 'sell'
        else:
            return 'hold'

    def bollinger_bands_strategy(self, candles):
        upper_band, _, lower_band = ta.volatility.bollinger_hband_indicator(candles['close'])
        if candles['close'].iloc[-1] > upper_band.iloc[-1]:
            return 'sell'
        elif candles['close'].iloc[-1] < lower_band.iloc[-1]:
            return 'buy'
        else:
            return 'hold'

    def run_backtest(self, strategy_name, risk_pct):
        position = 0  # Current position: 0 - no position, 1 - long position, -1 - short position
        entry_price = 0  # Entry price
        size = 1
        for i in range(1, len(self.candles)):
            prev_candle = self.candles.iloc[i-1]
            candle = self.candles.iloc[i]
            timestamp = candle.timestamp
            open_price = candle.open
            high_price = candle.high
            low_price = candle.low
            close_price = candle.close
            mid_price = (high_price + low_price) / 2  # Calculate midprice
            self.mid_prices.append(mid_price)
            self.close_prices.append(close_price)
            self.timestamps.append(timestamp)

            # Determine the trading signal
            if strategy_name== "ML":
                signal = self.strategy(candle)
            elif strategy_name == "SMA":
                signal = self.sma_crossover_strategy(self.candles.iloc[:i+1])
            elif strategy_name == "RSI":
                signal = self.rsi_strategy(self.candles.iloc[:i+1])
            elif strategy_name == "MACD":
                signal = self.macd_strategy(self.candles.iloc[:i+1])
            elif strategy_name == "BB":
                signal = self.bollinger_bands_strategy(self.candles.iloc[:i+1])

            if signal == 'buy':
                if position != 1 and self.calculate_risk(risk_pct, size):
                    # Entry to a long position
                    position = 1
                    entry_price = close_price * (1 + self.commission)  # consider commission
                    self.record_trade(timestamp, 'buy', entry_price)

            elif signal == 'sell':
                if position == 1:
                    # Exit from a long position
                    position = 0
                    exit_price = close_price * (1 - self.commission)  # consider commission
                    self.record_trade(timestamp, 'sell', exit_price)
                    self.calculate_pnl(timestamp, entry_price, exit_price, risk_pct)

            elif signal == 'hold':
                continue

        self.save_results()
        self.plot_pnl()
        self.plot_trades()

    def record_trade(self, timestamp, trade_type, price):
        trade = {'timestamp': timestamp, 'type': trade_type, 'price': price, 'quantity': 1}
        self.trades = self.trades.append(trade, ignore_index=True)

    def calculate_pnl(self, timestamp, entry_price, exit_price, risk_pct):
        pnl = (exit_price - entry_price) / entry_price * risk_pct
        pnl_entry = {'timestamp': timestamp, 'pnl': pnl}
        self.pnl = self.pnl.append(pnl_entry, ignore_index=True)

    def save_results(self):
        self.trades.to_csv(f'{self.symbol}_trades.csv', index=False)
        self.pnl.to_csv(f'{self.symbol}_pnl.csv', index=False)

    def calculate_risk(self, risk_pct, size):
        max_risk = self.cash * (risk_pct / 100)
        # The trade size should be less than or equal to max_risk
        if size <= max_risk:
            return True
        else:
            return False

    def plot_pnl(self):
        plt.figure(figsize=(12, 6))
        plt.plot_date(self.pnl['timestamp'], self.pnl['pnl'], '-')
        plt.xlabel('Timestamp')
        plt.ylabel('PnL')
        plt.title('PnL')
        plt.grid(True)
        plt.gca().xaxis.set_major_formatter(plt.NullFormatter())
        plt.show()

    def plot_trades(self):
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot_date(self.timestamps, self.mid_prices, '-', label='Mid Price', color='blue')
        buy_signals = self.trades[self.trades['type'] == 'buy']
        sell_signals = self.trades[self.trades['type'] == 'sell']
        plt.plot_date(buy_signals['timestamp'], buy_signals['price'], '^', markersize=10, color='g', label='buy')
        plt.plot_date(sell_signals['timestamp'], sell_signals['price'], 'v', markersize=10, color='r', label='sell')
        plt.xlabel('Timestamp')
        plt.ylabel('Price')
        plt.title('Trades')
        plt.grid(True)
        plt.legend()
        plt.gca().xaxis.set_major_formatter(plt.NullFormatter())
        plt.show()





