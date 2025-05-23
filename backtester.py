import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Define STATIC_FOLDER here if this file is responsible for saving charts,
# or make sure the calling function passes the path.
# For now, let's assume app.py will pass the STATIC_FOLDER path.

def backtest_ma_crossover(ticker, short_window, long_window, start_date, end_date, static_folder_path):
    """
    Backtests a moving average crossover strategy for a given ticker,
    calculates performance metrics, and generates charts.
    """
    try:
        print(f"Fetching data for {ticker} from {start_date} to {end_date}...")
        data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True)

        if data.empty:
            return None, None, None, "No data available for the selected ticker and date range."

        data.reset_index(inplace=True)

        # Calculate moving averages
        data[f'{short_window}_day_ma'] = data['Close'].rolling(window=short_window).mean()
        data[f'{long_window}_day_ma'] = data['Close'].rolling(window=long_window).mean()

        # Generate trading signals
        # Signal: 1 for Buy, -1 for Sell
        data['Signal'] = 0
        # Gold cross: Short MA > Long MA -> Buy (Signal 1)
        data.loc[data[f'{short_window}_day_ma'] > data[f'{long_window}_day_ma'], 'Signal'] = 1
        # Death cross: Short MA < Long MA -> Sell (Signal -1)
        data.loc[data[f'{short_window}_day_ma'] < data[f'{long_window}_day_ma'], 'Signal'] = -1


        # Calculate returns
        data['Daily_Return'] = data['Close'].pct_change()
        # Shift the signal to avoid look-ahead bias: position taken on next day's open or current day's close for next day's return
        data['Strategy_Return'] = data['Signal'].shift(1) * data['Daily_Return']

        # Calculate cumulative returns
        # Handle potential NaNs at the beginning of Strategy_Return due to shifting/rolling
        data['Cumulative_Strategy_Return'] = (1 + data['Strategy_Return'].fillna(0)).cumprod()
        data['Cumulative_Market_Return'] = (1 + data['Daily_Return'].fillna(0)).cumprod()

        # Calculate performance metrics
        # Filter out NaN values from Strategy_Return before calculating total_return
        filtered_strategy_returns = data['Cumulative_Strategy_Return'].dropna()
        if not filtered_strategy_returns.empty:
            total_return = (filtered_strategy_returns.iloc[-1] - 1) * 100
        else:
            total_return = 0

        # Basic Sharpe Ratio (assuming risk-free rate is 0)
        strategy_daily_returns_for_sharpe = data['Strategy_Return'].dropna()
        if not strategy_daily_returns_for_sharpe.empty and strategy_daily_returns_for_sharpe.std() != 0:
            sharpe_ratio = strategy_daily_returns_for_sharpe.mean() / strategy_daily_returns_for_sharpe.std() * np.sqrt(252) # Assuming 252 trading days
        else:
            sharpe_ratio = 0

        # Maximum Drawdown
        cumulative_returns_for_drawdown = data['Cumulative_Strategy_Return'].dropna()
        if not cumulative_returns_for_drawdown.empty:
            peak = cumulative_returns_for_drawdown.expanding(min_periods=1).max()
            drawdown = (cumulative_returns_for_drawdown / peak) - 1
            max_drawdown = drawdown.min() * 100 if not drawdown.empty else 0
        else:
            max_drawdown = 0

        performance_metrics = {
            'total_return': f"{total_return:.2f}%",
            'sharpe_ratio': f"{sharpe_ratio:.2f}",
            'max_drawdown': f"{max_drawdown:.2f}%"
        }

        # --- Plotting Cumulative Returns ---
        plt.figure(figsize=(12, 6))
        plt.plot(data['Date'], data['Cumulative_Strategy_Return'], label='Strategy Cumulative Return', color='purple')
        plt.plot(data['Date'], data['Cumulative_Market_Return'], label='Market Cumulative Return', color='grey', alpha=0.7)
        plt.title(f'{ticker} Cumulative Returns: SMA Crossover ({short_window}/{long_window})')
        plt.xlabel('Date')
        plt.ylabel('Cumulative Return')
        plt.legend()
        plt.grid(True)
        cumulative_chart_filename = f"{ticker}_cumulative_returns.png"
        cumulative_chart_path = os.path.join(static_folder_path, cumulative_chart_filename)
        plt.savefig(cumulative_chart_path)
        plt.close()

        # --- Plotting Price with MA and Signals ---
        plt.figure(figsize=(12, 6))
        plt.plot(data['Date'], data['Close'], label='Close Price', color='blue', alpha=0.7)
        plt.plot(data['Date'], data[f'{short_window}_day_ma'], label=f'{short_window}-day MA', linestyle='--', color='orange')
        plt.plot(data['Date'], data[f'{long_window}_day_ma'], label=f'{long_window}-day MA', linestyle='--', color='green')

        # Buy signals (when Signal changes from -1 or 0 to 1)
        buy_signals_indices = data[(data['Signal'].shift(1) <= 0) & (data['Signal'] == 1)].index
        plt.plot(data.loc[buy_signals_indices, 'Date'], data.loc[buy_signals_indices, 'Close'], '^', markersize=10, color='green', lw=0, label='Buy Signal')

        # Sell signals (when Signal changes from 1 or 0 to -1)
        sell_signals_indices = data[(data['Signal'].shift(1) >= 0) & (data['Signal'] == -1)].index
        plt.plot(data.loc[sell_signals_indices, 'Date'], data.loc[sell_signals_indices, 'Close'], 'v', markersize=10, color='red', lw=0, label='Sell Signal')

        plt.title(f'{ticker} Price, MAs, and Signals: SMA Crossover ({short_window}/{long_window})')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.grid(True)
        price_chart_filename = f"{ticker}_price_signals.png"
        price_chart_path = os.path.join(static_folder_path, price_chart_filename)
        plt.savefig(price_chart_path)
        plt.close()

        return cumulative_chart_filename, price_chart_filename, performance_metrics, None # Return both chart filenames and metrics

    except Exception as e:
        print(f"Error during backtesting for {ticker}: {e}")
        return None, None, None, f"An error occurred during backtesting: {e}"

# No __main__ block here, as app.py will import and call this function.
