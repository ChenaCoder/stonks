import os
import pandas as pd
import yfinance as yf
import mysql.connector



# MySQL database connection

connection = mysql.connector.connect(
    user='root',
    password='********',
    host='localhost',
    database='stonks',
    ssl_disabled=False
)
cursor = connection.cursor()

def read_tickers(csv_file):
     try:
          df = pd.read_csv(csv_file)
          print("DataFrame contents:")
          print(df)

          if df.empty:
               raise ValueError(f"The CSV file {csv_file} is empty.")

          tickers = df.iloc[:, 0].tolist()

          return tickers
     except pd.errors.EmptyDataError:
          raise ValueError(f"The CSV file {csv_file} is empty.")
     except Exception as e:
          raise ValueError(f"Error reading tickers from {csv_file}: {e}")

def download_ticker_data(tickers):
     bad_tickers = []
     for ticker in tickers:
          try:
               data = yf.download(ticker)
               df = pd.DataFrame(data)
               df=df.reset_index()
               if not data.empty:
                    try:
                         insert_ticker_query = f"INSERT INTO tickers (ticker) VALUES ('{ticker}')"
                         cursor.execute(insert_ticker_query)
                         create_table_query = f"""
                         CREATE TABLE `{ticker}` (
                              `date` DATE NOT NULL,
                              `open` DOUBLE NULL,
                              `high` DOUBLE NULL,
                              `low` DOUBLE NULL,
                              `close` DOUBLE NULL,
                              `volume` DOUBLE NULL,
                              PRIMARY KEY (`date`)
                         );
                         """
                         cursor.execute(create_table_query)
                         for index, row in df.iterrows():
                              insert_query = f'''
                              INSERT INTO `{ticker}` (date, open, high, low, close, volume)
                              VALUES (%s, %s, %s, %s, %s, %s);
                              '''
                              values = (row['Date'].date(), row['Open'], row['High'], row['Low'], row['Close'], row['Volume'])
                              cursor.execute(insert_query, values)
                              # Commit changes and close the connection
                         print(f"Downloaded data for {ticker} and saved")
                    except Exception as e:
                         print("already exists")
               else:
                    bad_tickers.append(ticker)
               connection.commit()
          except yf.TickerError as e:
               print(f"Error downloading data for {ticker}: {e}")
               bad_tickers.append(ticker)
     
     
     return bad_tickers

nasdaq_csv = '/tickers/nasdaq.csv'
nyse_csv = '/tickers/nyse.csv'


nasdaq_tickers = read_tickers(nasdaq_csv)
nyse_tickers = read_tickers(nyse_csv)

all_tickers = nasdaq_tickers + nyse_tickers

bad_tickers = download_ticker_data(all_tickers)
connection.close()
if not bad_tickers == []:
     print("\nHere are the invalid tickers: ")
     for ticker in bad_tickers:
          print(ticker)