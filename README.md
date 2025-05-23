# Algorithmic Trading Backtester: Simple Moving Average Crossover

## Project Overview

This project presents a web-based algorithmic trading backtester designed to evaluate the performance of a Simple Moving Average (SMA) Crossover trading strategy using historical stock data. It provides a user-friendly interface to input trading parameters and visualize the strategy's hypothetical performance, including key financial metrics and comparative charts.

### Why a Backtester? (From Real-time to Simulation)

Initially, the ambition for this project was to develop a real-time algorithmic trading model capable of automated market monitoring and trade execution. However, during the development process, I gained a deeper understanding of the significant complexities and resource demands inherent in real-time trading systems. These include:

* **Reliable Data Feeds:** Requiring fast, consistent, and often costly data streams.
* **Broker API Integration:** Complexities in connecting directly to brokerage platforms for trade execution, managing latency, and ensuring correct order fulfillment.
* **Infrastructure & Compliance:** The need for robust server infrastructure, stringent security protocols, continuous monitoring, and adherence to regulatory requirements.
* **Capital Risk:** The inherent financial risk involved in deploying a live trading strategy with real capital.

Recognizing these challenges, I made a strategic decision to pivot and focus on building a robust **algorithmic trading backtester**. This was not a compromise, but a crucial and foundational step. A backtester allows for:

* **Risk-Free Experimentation:** Simulate strategies on historical data without risking actual capital.
* **Strategy Validation & Optimization:** Rigorously test a strategy's potential profitability and optimize its parameters (e.g., ideal moving average windows) before any real-world deployment.
* **Understanding Strategy Behavior:** Analyze performance metrics and visualize trade signals to gain insights into how the strategy behaves under various market conditions.
* **Learning & Iteration:** Master the core logic of algorithmic trading (data acquisition, signal generation, trade simulation, performance analysis) in a controlled environment.

## The Simple Moving Average (SMA) Crossover Strategy

This backtester evaluates one of the most fundamental trend-following strategies: the Simple Moving Average (SMA) Crossover.

### How it Works:

1.  **Two Moving Averages:** The strategy uses two Simple Moving Averages:
    * **Short MA:** A faster-reacting average (e.g., 20 days) that tracks recent price movements.
    * **Long MA:** A slower-reacting average (e.g., 50 days) that indicates the broader trend.
2.  **Buy Signal (Golden Cross):** When the **Short MA crosses *above*** the Long MA, it generates a buy signal, indicating potential upward momentum.
3.  **Sell Signal (Death Cross):** When the **Short MA crosses *below*** the Long MA, it generates a sell signal, indicating potential downward momentum.

### Features

* **Web-based User Interface:** A clean, dark-themed interface built with Flask for easy input of parameters.
* **Customizable Parameters:** Users can specify:
    * **Ticker Symbol:** (e.g., AAPL, MSFT, GOOGL)
    * **Short MA Window:** Number of days for the shorter moving average.
    * **Long MA Window:** Number of days for the longer moving average.
    * **Start Date & End Date:** The historical period for backtesting.
* **Performance Metrics:** Calculates and displays key metrics:
    * **Total Return:** Overall percentage profit or loss.
    * **Sharpe Ratio:** Risk-adjusted return (higher is better).
    * **Max Drawdown:** The largest percentage loss from a peak to a
