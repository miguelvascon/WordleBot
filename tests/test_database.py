from database import create_connection, init_db, insert_game, insert_guess, get_feedback, get_guess, update_feedback, update_game

def test_database():
    # Create a connection to the test database
    conn = create_connection("db/wordle_test.db")
    init_db(conn, "db/test_schema.sql")  # Initialize with the test schema

    # Insert a new game and get its ID
    game_id = insert_game(conn, "2024-11-01")
    print(f"Inserted Game ID: {game_id}")

    # Start with the first guess and set guess_number
    guess_number = insert_guess(conn, game_id, "crane")  # Default to guess_number=1
    print(f"Inserted Guess Number {guess_number} with Guess: 'crane'")

    # Mock feedback to update for the first guess
    feedback = [('c', 'correct'), ('r', 'incorrect'), ('a', 'misplaced'), ('n', 'incorrect'), ('e', 'misplaced')]
    update_feedback(conn, game_id, guess_number, feedback)
    print(f"Updated feedback for Guess Number {guess_number}: {feedback}")

    # Retrieve and print the most recent guess
    recent_guess = get_guess(conn, game_id, guess_number)
    print(f"Most Recent Guess: {recent_guess}")

    # Retrieve and print the feedback for the most recent guess
    retrieved_feedback = get_feedback(conn, game_id, guess_number)
    print(f"Retrieved Feedback for Guess Number {guess_number}: {retrieved_feedback}")

    # Update the game result after all guesses
    update_game(conn, game_id, True)
    print(f"Updated Game ID {game_id} with Result: True")

    # Verify the update by checking the Game table directly
    cur = conn.cursor()
    cur.execute("SELECT * FROM Game WHERE game_id = ?", (game_id,))
    game_data = cur.fetchone()
    print(f"Game Data after Update: {game_data}")

    # Close the connection
    conn.close()

if __name__ == "__main__":
    test_database()
