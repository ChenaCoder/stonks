
import yfinance as yf
import json
import pandas as pd
import mysql.connector

data = yf.download("AAPL")


# Sample DataFrame for demonstration


df = pd.DataFrame(data)
df=df.reset_index()
print(df)
ticker = 'AAPL'  # Replace with your actual ticker symbol

# MySQL database connection
connection = mysql.connector.connect(
    user='root',
    password='********',
    host='localhost',
    database='stonks',
    ssl_disabled=False
)

# Create a cursor for database interaction
cursor = connection.cursor()

# Ensure the "data" table exists with the appropriate columns
insert_ticker_query = f"INSERT INTO tickers (ticker) VALUES ('{ticker}')"
cursor.execute(insert_ticker_query)
connection.commit()

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
connection.commit()



# Insert the DataFrame into the database
for index, row in df.iterrows():
    insert_query = f'''
    INSERT INTO `{ticker}` (date, open, high, low, close, volume)
    VALUES (%s, %s, %s, %s, %s, %s);
    '''
    values = (row['Date'].date(), row['Open'], row['High'], row['Low'], row['Close'], row['Volume'])
    cursor.execute(insert_query, values)

# Commit changes and close the connection
connection.commit()
connection.close()