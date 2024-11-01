CREATE TABLE IF NOT EXISTS Game (
    game_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL UNIQUE,
    result BOOLEAN DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS Guesses (
    game_id INTEGER NOT NULL,
    guess_number INTEGER NOT NULL,
    guess TEXT NOT NULL,
    feedback TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (game_id, guess_number),
    FOREIGN KEY (game_id) REFERENCES Game(game_id)
);