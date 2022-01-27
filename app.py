import string
from pathlib import Path


def import_word_list(word_list_location: Path) -> list[str]:
    return word_list_location.read_text().strip().upper().splitlines()


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


def display():
    print('Welcome to Wordle VI')
    print('A 6 letter word has been chosen!')
    print('Make a Guess')


def main():
    pass


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
    main()
