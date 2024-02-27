import yfinance as yf
from ta.trend import SMAIndicator 
from ta.volatility import BollingerBands
import matplotlib.pyplot as plt

# Function to calculate CCI manually
def calculate_cci(df, n=20):
    tp = (df['High'] + df['Low'] + df['Close']) / 3
    sma_tp = tp.rolling(window=n).mean()
    mean_deviation = (tp - sma_tp).abs().rolling(window=n).mean()
    cci = (tp - sma_tp) / (0.015 * mean_deviation)
    return cci

# Function to perform currency analysis
def perform_currency_analysis():
    # Scraping EUR/INR currency data from Yahoo Finance
    eur_inr = yf.download('EURINR=X', start='2023-01-01', end='2024-02-16')

    # Calculate Moving Average
    sma = SMAIndicator(eur_inr['Close'], window=20)
    eur_inr['SMA'] = sma.sma_indicator()

    # Calculate Bollinger Bands
    bb = BollingerBands(eur_inr['Close'], window=20, window_dev=2)
    eur_inr['BB_High'] = bb.bollinger_hband()
    eur_inr['BB_Low'] = bb.bollinger_lband()

    # Calculate Commodity Channel Index (CCI)
    eur_inr['CCI'] = calculate_cci(eur_inr)

    # Making trading decisions based on Moving Average and CCI
    eur_inr['Decision'] = 'NEUTRAL'
    eur_inr.loc[(eur_inr['Close'] > eur_inr['SMA']) & (eur_inr['CCI'] > 0), 'Decision'] = 'BUY'
    eur_inr.loc[(eur_inr['Close'] < eur_inr['SMA']) & (eur_inr['CCI'] < 0), 'Decision'] = 'SELL'

    return eur_inr

# Call the function and store the results
results = perform_currency_analysis()

# Print the results 
print(results)

# Save the results to a CSV file
results.to_csv('Harshada_Finance_Flash_Currency_Analysis.csv', index=False)

# it's visualize the data
plt.figure(figsize=(14, 7))
plt.plot(results['Close'], label='Close Price')
plt.plot(results['SMA'], label='SMA')
plt.plot(results['BB_High'], label='BB High')
plt.plot(results['BB_Low'], label='BB Low')
plt.title('EUR/INR Technical Analysis')
plt.legend()
plt.xlabel('Date')
plt.ylabel('Price')
plt.grid(True)
plt.savefig('Harshada_Finance_Flash_Currency_Analysis_Graph.png')
plt.show()

# Print the trading decisions
print("Trading Decisions:")
print(results['Decision'].value_counts())
