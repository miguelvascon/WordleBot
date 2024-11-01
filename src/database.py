import json
import sqlite3
from datetime import datetime

def create_connection(db_file="../db/wordle_game.db"):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Connection to database established")
    except sqlite3.Error as e:
        print(e)
    return conn

def init_db(conn, schema_file="../db/schema.sql"):
    with conn:
        with open(schema_file, "r") as open_file:
            conn.executescript(open_file.read())

# Function returns the game_id
def insert_game(conn, date):
    sql = ''' INSERT OR IGNORE INTO Game(date, result)
              VALUES(?, NULL) '''
    cur = conn.cursor()
    cur.execute(sql, (date,))
    conn.commit()
    return cur.lastrowid

# Function returns the guess_id
def insert_guess(conn, game_id, guess, feedback):
    feedback_str = json.dumps(feedback)
    timestamp = datetime.now().isoformat()
    sql = ''' INSERT INTO Guesses(game_id, guess, feedback, timestamp)
              VALUES(?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, (game_id, guess, feedback_str, timestamp))
    conn.commit()
    return cur.lastrowid

# Function returns tuple for most recent feedback
def get_feedback(conn, guess_id):
    sql = ''' SELECT feedback FROM Guesses WHERE guess_id = ? '''
    cur = conn.cursor()
    cur.execute(sql, (guess_id,))
    feedback_str = cur.fetchone()[0]
    feedback = json.loads(feedback_str)
    return feedback

# Function returns string for most recent guess
def get_guess(conn, game_id):
    sql = ''' SELECT guess FROM Guesses
              WHERE game_id = ?
              ORDER BY guess_id DESC
              LIMIT 1 '''
    cur = conn.cursor()
    cur.execute(sql, (game_id,))
    return cur.fetchone()

def update_game(conn, game_id, result):
    sql = ''' UPDATE Game
              SET result = ?
              WHERE game_id = ? '''
    cur = conn.cursor()
    cur.execute(sql, (result, game_id))
    conn.commit()