import string
import pathlib
from guess_manager import GuessManager


class WordleVIManager():
    def __init__(self, solution_words_location, legal_words_location, seed=None):
        self.running = False
        self.guess_manager = None
        self.solution_words = self.import_word_list(solution_words_location)
        self.legal_words = self.import_word_list(legal_words_location)
        if self.verify_legal_word_list(self.solution_words) and self.verify_legal_word_list(self.legal_words):
            self.setup_game(seed)

    def setup_game(self, seed=None):
        self.running = True
        self.guess_manager = GuessManager(self.solution_words, self.legal_words, seed)

    @staticmethod
    def import_word_list(word_list_location: pathlib.Path) -> list[str]:
        return word_list_location.read_text().strip().upper().splitlines()

    @staticmethod
    def verify_legal_word_list(word_list: list[str]) -> bool:
        try:
            num_words = len(word_list)
            if num_words == 0:
                raise ImportError('Word list does not exist')
            if not num_words == len(set(word_list)):
                raise ImportError('Duplicates exist within the word list')

            word_size = len(word_list[0])
            for word in word_list:
                if not len(word) == word_size:
                    raise ImportError('Word list not of uniform length')
                if not word.isalpha():
                    raise ImportError('Word list contains non-alphabetical characters')

            return True
        except ImportError as err:
            print(err)
            return False

    def display(self):
        spaces = ' ' * (23 - self.guess_manager.solution_length)
        print('*******************************************************')
        print('-------------------------------------------------------')
        for guess in self.guess_manager.guesses_history:
            print('***', spaces, *guess[0], spaces, '***')
            print('***', spaces, *guess[1], spaces, '***')
            print('-------------------------------------------------------')

        print('*******************************************************')
        print('*', *self.guess_manager.letter_status.keys(), '*')
        print('*', *self.guess_manager.letter_status.values(), '*')
        print('*******************************************************')

    def victory_sequence(self):
        self.running = False
        response = ''
        print(f'You got it in {len(self.guess_manager.guesses_history)} guesses:')
        for guess in self.guess_manager.guesses_history:
            print(*guess[1])
        while not response.lower() in ('y', 'n'):
            print('\nPlay again with a random word? (Y/N)', end='')
            response = input().lower()
        if response == 'y':
            self.setup_game()
            print('\n\n\n*******************************************************')
            print('*******************************************************')
            print('*** New Game Begun ***\n')

    def check_victory(self):
        if self.guess_manager.guesses_history:
            if list(self.guess_manager.solution) == self.guess_manager.guesses_history[-1][0]:
                self.running = False
                self.victory_sequence()
                return True
        return False


def main(solution_words_location, legal_words_location):
    print('*** Welcome to Wordle VI ***\n')
    controller = WordleVIManager(solution_words_location, legal_words_location, 1)
    while controller.running:
        print(f'Please guess a {controller.guess_manager.solution_length} letter word: ', end='')
        guess = input()
        if guess == '':
            print('Closing Down')
            return
        if controller.guess_manager.submit_guess(guess):
            controller.display()
            controller.check_victory()
        else:
            print(f'Invalid Word --> ', end='')


'''
Application is booted up
    - answer_list.txt is verified
    - legal_words.txt is verified
    - Guess Manager(GM) instance is created.
        - GM uses a seed to choose a word from the answer_list.txt
        - GM creates guessed letters array
        - GM creates guessed answers array
User is prompted to make a selection
    - verify guess
    - update guessed letters array
    - update guessed answers list
    - print array of solutions
'''

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    FILEPATH = pathlib.Path(__file__).parent

    main((FILEPATH / "answer_list.txt"), (FILEPATH / "legal_words.txt"))
