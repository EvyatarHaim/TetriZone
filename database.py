import sqlite3


connection = sqlite3.connect('TetrisGame.db')
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY, 
    user_name VARCHAR(255) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    age VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_online INTEGER NOT NULL DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS scores (
    placement INTEGER,
    user_name VARCHAR(255) NOT NULL PRIMARY KEY, 
    last_score INTEGER NOT NULL,  
    highest_score INTEGER NOT NULL,
    FOREIGN KEY (user_name)
    REFERENCES users (user_name)
)
""")

# Create a temporary table with ranks based on 'highest_score' by DESC order
cursor.execute("""
CREATE TEMP TABLE ranked_scores AS SELECT 
    user_name,
    RANK() OVER (ORDER BY highest_score DESC) AS placement
    FROM scores
""")

# Update the 'scores' table with the calculated placements
cursor.execute("""
UPDATE scores SET placement = ( SELECT placement FROM ranked_scores WHERE scores.user_name = ranked_scores.user_name
)""")

# cursor.execute("ALTER TABLE users ADD COLUMN is_online INTEGER NOT NULL DEFAULT 0")

connection.commit()
connection.close()

print("Scores table have been updated and the placement column is now based on the highest_score.")
