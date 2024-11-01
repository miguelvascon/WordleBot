import re
import random

def load_words(file_path="../data/words.txt"):
    with open(file_path, "r") as open_file:
        words = [line.strip() for line in open_file.readlines()]
    return words

'''
Build a regular expression to be used by filter_words() to determine next guess

NOTE: There may be an edge case where the regex fails when a word contains multiple instances
of a character. The function tries to account for this, just keep an eye out when testing
performance to make sure nothing slips by
'''
def build_pattern(feedback, contains_letters, exclude_letters):
    pattern = ["." for _ in range(5)]

    for index, (letter, status) in enumerate(feedback):
        if status == "correct":
            pattern[index] = letter
        elif status == "misplaced":
            pattern[index] = f"[^{letter}]"
            contains_letters.add(letter)
        elif status == "incorrect" and letter not in contains_letters:
            exclude_letters.add(letter)

    contains_pattern = "".join(f"(?=.*{letter})" for letter in contains_letters)
    pattern_str = f"^(?!.*[{''.join(exclude_letters)}]){contains_pattern}{''.join(pattern)}$"
    return pattern_str

def filter_words(possible_words, pattern):
    regex = re.compile(pattern);
    return [word for word in possible_words if regex.match(word)]

def pick_guess(filtered_words):
    return random.choice(filtered_words)
