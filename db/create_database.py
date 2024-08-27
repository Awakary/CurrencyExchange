import os
import sqlite3
import sys

sys.path.append(os.getcwd())
from settings import database

connection = sqlite3.connect(database)

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

CREATE UNIQUE INDEX IF NOT EXISTS Pare ON ExchangeRates (base_currency, target_currency);

INSERT OR IGNORE INTO Currencies (name, code, sign)
VALUES  ('Австралийский доллар', 'AUD', '$'),
('Гуарани', 'PYG', '₲'),
('Иена', 'JPY', '¥');

INSERT OR IGNORE INTO ExchangeRates (base_currency, target_currency, rate)
VALUES ((SELECT id FROM Currencies WHERE code = 'AUD'), 
(SELECT id FROM Currencies WHERE code = 'PYG'), 
5109.08),
((SELECT id FROM Currencies WHERE code = 'AUD'), 
(SELECT id FROM Currencies WHERE code = 'JPY'), 
98.24),
((SELECT id FROM Currencies WHERE code = 'PYG'), 
(SELECT id FROM Currencies WHERE code = 'JPY'),
0.019)
""")
connection.close()
print('База создана')
