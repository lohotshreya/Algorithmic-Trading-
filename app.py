import os
from flask import Flask, render_template, request
# Import the backtesting function from your backtester.py file
from backtester import backtest_ma_crossover

# --- Folder setup ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_FOLDER = os.path.join(BASE_DIR, 'static')
TEMPLATES_FOLDER = os.path.join(BASE_DIR, 'templates')

os.makedirs(STATIC_FOLDER, exist_ok=True)

app = Flask(__name__, static_folder='static', template_folder='templates')

# --- Routes ---
@app.route('/', methods=['GET', 'POST'])
def index():
    cumulative_chart_file = None
    price_chart_file = None
    metrics = None
    error = None
    ticker_input = "AAPL" # Default values for input fields
    short_ma_input = "20"
    long_ma_input = "50"
    start_date_input = "2020-01-01"
    end_date_input = "2023-01-01"

    if request.method == 'POST':
        ticker_input = request.form['ticker'].upper()
        short_ma_input = int(request.form['short_ma'])
        long_ma_input = int(request.form['long_ma'])
        start_date_input = request.form['start_date']
        end_date_input = request.form['end_date']

        # Call the backtesting function from backtester.py
        cumulative_chart_file, price_chart_file, metrics, error = backtest_ma_crossover(
            ticker_input, short_ma_input, long_ma_input, start_date_input, end_date_input, STATIC_FOLDER
        )
        # Ensure short_ma_input and long_ma_input are strings for the template value attribute
        short_ma_input = str(short_ma_input)
        long_ma_input = str(long_ma_input)

    return render_template('index.html',
                           cumulative_chart_file=cumulative_chart_file,
                           price_chart_file=price_chart_file,
                           metrics=metrics,
                           error=error,
                           # Pass back the input values to retain them in the form
                           ticker=ticker_input,
                           short_ma=short_ma_input,
                           long_ma=long_ma_input,
                           start_date=start_date_input,
                           end_date=end_date_input)

if __name__ == '__main__':
    # TRY A DIFFERENT PORT, e.g., 5001 or 8000
    app.run(debug=True, port=5001) # Changed port to 5001
