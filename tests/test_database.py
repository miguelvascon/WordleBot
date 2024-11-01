import json
from database import create_connection, init_db, insert_game, insert_guess, get_feedback, get_guess, update_game

def test_database():
    # Create a connection to the database
    conn = create_connection("db/wordle_game.db")
    init_db(conn, "db/schema.sql")

    # Insert a new game with a date
    game_id = insert_game(conn, "2024-11-01")
    print(f"Inserted Game ID: {game_id}")

    # Insert a guess with feedback as a list of tuples
    guess = "CRANE"
    feedback = [('C', 'correct'), ('R', 'incorrect'), ('A', 'misplaced'), ('N', 'incorrect'), ('E', 'misplaced')]
    feedback_str = json.dumps(feedback)

    guess_id = insert_guess(conn, game_id, guess, feedback_str)
    print(f"Inserted Guess ID: {guess_id} with Guess: {guess} and Feedback: {feedback}")

    # Retrieve the most recent guess
    recent_guess = get_guess(conn, game_id)
    print(f"Most Recent Guess: {recent_guess}")

    # Retrieve and parse feedback for the most recent guess
    retrieved_feedback = get_feedback(conn, guess_id)
    print(f"Retrieved Feedback: {retrieved_feedback}")

    # Update game result
    update_game(conn, game_id, "Success")
    print(f"Updated Game ID {game_id} with Result: Success")

    # Verify the update by checking the Game table directly
    cur = conn.cursor()
    cur.execute("SELECT * FROM Game WHERE game_id = ?", (game_id,))
    game_data = cur.fetchone()
    print(f"Game Data after Update: {game_data}")

    conn.close()

if __name__ == "__main__":
    test_database()
