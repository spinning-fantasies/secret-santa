import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect("secretsanta.db")
cursor = conn.cursor()

# Create a table to store participant information
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS participants (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        assigned_recipient INTEGER DEFAULT 0
    )
"""
)

# Commit changes and close connection
conn.commit()
conn.close()
