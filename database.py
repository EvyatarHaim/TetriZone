import sqlite3


def reset_status():
    connection = sqlite3.connect('TetriZone.db')
    cursor = connection.cursor()

    cursor.execute("UPDATE users SET is_online = 0")
    print("Reset all the is_online values to 0")
    connection.commit()
    connection.close()


def handel_placement():
    connection = sqlite3.connect("TetriZone.db")
    cursor = connection.cursor()
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

    connection.commit()
    connection.close()


def create_db():
    connection = sqlite3.connect('TetriZone.db')
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_name VARCHAR(255) NOT NULL,
        first_name VARCHAR(255) NOT NULL,
        age VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        is_online INTEGER NOT NULL DEFAULT 0,
        creation_date DATE NOT NULL
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
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stats (
        user_name VARCHAR(255) NOT NULL PRIMARY KEY, 
        games_played INTEGER NOT NULL DEFAULT 0,
        played_time INTEGER NOT NULL DEFAULT 0,
        total_score INTEGER NOT NULL DEFAULT 0,
        lines INTEGER NOT NULL DEFAULT 0,  
        FOREIGN KEY (user_name)
        REFERENCES users (user_name)
    )
    """)

    print("Tables have created successfully")

    # cursor.execute("ALTER TABLE users ADD COLUMN is_online INTEGER NOT NULL DEFAULT 0")

    connection.commit()
    connection.close()


if __name__ == '__main__':
    # connection = sqlite3.connect('TetrisGame.db')
    # cursor = connection.cursor()
    # cursor.execute("UPDATE users SET creation_date = '2024-05-07' WHERE user_name=?", ("test9",))
    # connection.commit()
    # connection.close()

    # Connect to the SQLite database
    # Connect to the SQLite database

    reset_status()
