import sqlite3
from datetime import datetime, timedelta

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create the users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uuid TEXT NOT NULL UNIQUE,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    device_fingerprint TEXT NOT NULL,
    subscription_type TEXT CHECK(subscription_type IN ('daily', 'weekly', 'monthly', 'yearly')) NOT NULL,
    expiration_date TEXT NOT NULL,
    FOREIGN KEY (uuid) REFERENCES subscription_uuids(uuid)
)
''')

# Create the subscription_uuids table
cursor.execute('''
CREATE TABLE IF NOT EXISTS subscription_uuids (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uuid TEXT NOT NULL UNIQUE,
    tier TEXT CHECK(tier IN ('daily', 'weekly', 'monthly', 'yearly')) NOT NULL,
    issued BOOLEAN NOT NULL DEFAULT 0,
    expiration_date TEXT NOT NULL  -- Add expiration_date column
)
''')

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database setup complete. 'users.db' with 'users' table created successfully.")
