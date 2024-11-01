import json
import sqlite3

def create_connection(db_file="../db/wordle_game.db"):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Connection to database established")
    except sqlite3.Error as e:
        print(e)
    return conn

def init_db(conn, schema_file="../db/prod_schema.sql"):
    with conn:
        with open(schema_file, "r") as open_file:
            conn.executescript(open_file.read())

# Function returns the game_id
def insert_game(conn, date):
    sql = ''' INSERT OR IGNORE INTO Game(date)
              VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, (date,))
    conn.commit()
    return cur.lastrowid

# Function returns most recent guess_number, update guess number externally
def insert_guess(conn, game_id, guess, guess_number=1):
    sql = ''' INSERT INTO Guesses(game_id, guess_number, guess)
              VALUES(?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, (game_id, guess_number, guess))
    conn.commit()
    return guess_number

# Function returns guess if guess at guess_number exists, else returns None
def get_guess(conn, game_id, guess_number):
    sql = ''' SELECT guess FROM Guesses
              WHERE game_id = ? AND guess_number = ? '''
    cur = conn.cursor()
    cur.execute(sql, (game_id, guess_number))
    result = cur.fetchone()
    return result[0] if result else None

def update_feedback(conn, game_id, guess_number, feedback):
    feedback_str = json.dumps(feedback)
    sql = ''' UPDATE Guesses
              SET feedback = ?
              WHERE game_id = ? AND guess_number = ? '''
    cur = conn.cursor()
    cur.execute(sql, (feedback_str, game_id, guess_number))
    conn.commit()

# Function returns tuple for most recent feedback
def get_feedback(conn, game_id, guess_number):
    sql = ''' SELECT feedback FROM Guesses
              WHERE game_id = ? AND guess_number = ? '''
    cur = conn.cursor()
    cur.execute(sql, (game_id, guess_number))
    result = cur.fetchone()
    return json.loads(result[0]) if result else None

# Function returns string for most recent guess
def update_game(conn, game_id, result):
    sql = ''' UPDATE Game
              SET result = ?
              WHERE game_id = ? '''
    cur = conn.cursor()
    cur.execute(sql, (result, game_id))
    conn.commit()