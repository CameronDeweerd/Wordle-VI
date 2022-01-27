import os
import pathlib
import pytest
import guess_manager
import app

TEST_PATH = pathlib.Path(__file__).parent


@pytest.fixture
def word_list_small():
    return app.import_word_list(TEST_PATH / "answer_list_for_test.txt")


def test_ensure_solution_picked(word_list_small):
    GMX = guess_manager.GuessManager(word_list_small, word_list_small)
    GM1a = guess_manager.GuessManager(word_list_small, word_list_small, 1)
    GM1b = guess_manager.GuessManager(word_list_small, word_list_small, 1)
    GM2 = guess_manager.GuessManager(word_list_small, word_list_small, 3)
    assert GMX.solution in word_list_small
    assert GMX.solution_length == len(word_list_small[0])
    assert GM1a.solution in word_list_small
    assert GM1a.solution_length == len(word_list_small[0])
    assert GM1a.solution == GM1b.solution
    assert GM1a.solution != GM2.solution


def test_check_guesses():
    GM1 = guess_manager.GuessManager(['ABCDE'], ['ABCDE'])
    assert GM1.solution == 'ABCDE'
    assert GM1.check_guess('ABCDE') == ['O', 'O', 'O', 'O', 'O']
    assert GM1.check_guess('abcde') == ['O', 'O', 'O', 'O', 'O']
    assert GM1.check_guess('AFFFF') == ['O', 'X', 'X', 'X', 'X']
    assert GM1.check_guess('FFFFF') == ['X', 'X', 'X', 'X', 'X']
    assert GM1.check_guess('FAFFF') == ['X', '?', 'X', 'X', 'X']
    assert GM1.check_guess('AAFFF') == ['O', 'X', 'X', 'X', 'X']
    assert GM1.check_guess('BCDEA') == ['?', '?', '?', '?', '?']

    GM2 = guess_manager.GuessManager(['ABBBA'], ['ABBBA'])
    assert GM2.solution == 'ABBBA'
    assert GM2.check_guess('FAFFF') == ['X', '?', 'X', 'X', 'X']
    assert GM2.check_guess('AAFFF') == ['O', '?', 'X', 'X', 'X']

    GM3 = guess_manager.GuessManager(['SQUALL'], ['SQUALL'])
    assert GM3.solution == 'SQUALL'
    assert GM3.check_guess('LLAMAS') == ['?', '?', '?', 'X', 'X', '?']


def test_history_update():
    GM1 = guess_manager.GuessManager(['ABCDE'], ['ABCDE'])
    assert GM1.guesses_history == []
    GM1.update_history('abbbc', GM1.check_guess('abbbc'))
    assert GM1.guesses_history == [(['A', 'B', 'B', 'B', 'C'], ['O', 'O', 'X', 'X', '?'])]
    assert GM1.letter_status['A'] == 'O'
    assert GM1.letter_status['C'] == '?'
    GM1.update_history('FFFFF', GM1.check_guess('FFFFF'))
    assert GM1.guesses_history == [(['A', 'B', 'B', 'B', 'C'], ['O', 'O', 'X', 'X', '?']),
                                   (['F', 'F', 'F', 'F', 'F'], ['X', 'X', 'X', 'X', 'X'])]
    assert GM1.letter_status['A'] == 'O'
    assert GM1.letter_status['F'] == 'X'
    GM1.update_history('FACFF', GM1.check_guess('FACFF'))
    assert GM1.guesses_history == [(['A', 'B', 'B', 'B', 'C'], ['O', 'O', 'X', 'X', '?']),
                                   (['F', 'F', 'F', 'F', 'F'], ['X', 'X', 'X', 'X', 'X']),
                                   (['F', 'A', 'C', 'F', 'F'], ['X', '?', 'O', 'X', 'X'])]
    assert GM1.letter_status['A'] == 'O'
    assert GM1.letter_status['C'] == 'O'
    assert GM1.letter_status['F'] == 'X'
