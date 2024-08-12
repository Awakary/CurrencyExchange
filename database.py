import sqlite3

connection = sqlite3.connect('DB.sqlite')

cursor = connection.cursor()

cursor.executescript("""
CREATE TABLE IF NOT EXISTS Currencies 
(id INTEGER PRIMARY KEY,
code VARCHAR NOT NULL UNIQUE,
name VARCHAR NOT NULL,
sign VARCHAR NOT NULL);

CREATE TABLE IF NOT EXISTS ExchangeRates 
(id INTEGER PRIMARY KEY,
base_currency INTEGER REFERENCES Currencies,
target_currency INTEGER REFERENCES Currencies,
rate DECIMAL(6) NOT NULL);

CREATE UNIQUE INDEX IF NOT EXISTS Pare ON ExchangeRates (base_currency, target_currency)
""")
connection.close()