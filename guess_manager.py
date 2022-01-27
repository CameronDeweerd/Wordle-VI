import random
import datetime


class GuessManager:
    def __init__(self, answer_words, legal_words, seed=None):
        self.legal_words = set(legal_words + answer_words)
        self.answer_words = answer_words.copy()
        self.solution = None
        self.solution_length = len(answer_words[0])
        self.guesses_history = []
        self.letter_status = {'A': 'X', 'B': 'X', 'C': 'X', 'D': 'X', 'E': 'X', 'F': 'X', 'G': 'X', 'H': 'X', 'I': 'X',
                              'J': 'X', 'K': 'X', 'L': 'X', 'M': 'X', 'N': 'X', 'O': 'X', 'P': 'X', 'Q': 'X', 'R': 'X',
                              'S': 'X', 'T': 'X', 'U': 'X', 'V': 'X', 'W': 'X', 'X': 'X', 'Y': 'X', 'Z': 'X'}
        self.select_solution(seed)

    def select_solution(self, seed=None):
        if seed:
            random.seed(seed)
        random.shuffle(self.answer_words)
        day_offset = (datetime.datetime.today() - datetime.datetime.utcfromtimestamp(0)).days % len(self.answer_words)
        self.solution = self.answer_words[0 + day_offset]

    def submit_guess(self, guess: str) -> ([str], {str: str}):
        guess = guess.upper()
        if self.verify_word(guess):
            checked_list = self.check_guess(guess)
            self.update_history(guess, checked_list)
        return self.guesses_history, self.letter_status

    def verify_word(self, word: str) -> bool:
        if word in self.legal_words and len(word) == self.solution_length:
            return True
        else:
            return False

    def check_guess(self, guess: str) -> [str]:
        solution_character_list = list(self.solution)
        guess_character_list = list(guess.upper())
        checked_list = ['X'] * len(solution_character_list)

        for index, character in enumerate(guess_character_list):
            if character == solution_character_list[index]:
                checked_list[index] = 'O'
                solution_character_list[index] = ''
        for index, character in enumerate(guess_character_list):
            if character in solution_character_list and checked_list[index] == 'X':
                checked_list[index] = '?'
                solution_character_list.remove(character)
        return checked_list

    def update_history(self, guess, checked_list):
        guess = guess.upper()
        self.guesses_history.append((list(guess), checked_list))
        for index, character in enumerate(list(guess)):
            if checked_list[index] == 'O':
                self.letter_status[character] = 'O'
            if checked_list[index] == '?' and self.letter_status[character] == 'X':
                self.letter_status[character] = '?'
