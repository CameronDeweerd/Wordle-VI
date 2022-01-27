import os
import pathlib
import pytest
import app

TEST_PATH = pathlib.Path(__file__).parent


@pytest.fixture
def random_seed():
    return 1


@pytest.fixture
def word_list_small():
    return app.import_word_list(TEST_PATH / "answer_list_for_test.txt")


def test_list_imported(word_list_small):
    assert word_list_small == [
        "SHOULD",
        "PEOPLE",
        "BEFORE",
        "LITTLE",
        "WITHIN",
        "DURING",
        "NUMBER",
        "SYSTEM",
        "SOCIAL",
        "STATES"]


def test_verify_legal_word_lists_false():
    assert app.verify_legal_word_list([]) is False  # empty list
    assert app.verify_legal_word_list(['abc', 'abc']) is False  # duplicates
    assert app.verify_legal_word_list(['abc', 'abcd']) is False  # incorrect sizes
    assert app.verify_legal_word_list(['aaaa', 'bbb', 'ccc']) is False  # incorrect sizes
    assert app.verify_legal_word_list(['']) is False  # empty value in list
    assert app.verify_legal_word_list(['', 'bbb', 'ccc']) is False  # empty value in list
    assert app.verify_legal_word_list(['aaa', 'bbb', '   ']) is False  # invalid character: space
    assert app.verify_legal_word_list(['aaa', 'b1b', 'ccc']) is False  # invalid character: number
    assert app.verify_legal_word_list(['aaa', 'b*b', 'ccc']) is False  # invalid character: special char
    assert app.verify_legal_word_list(['aaa', 'bbb', 'c"c']) is False  # invalid character: apostrophe
    assert app.verify_legal_word_list(["aaa", "bbb", "c'c"]) is False  # invalid character: apostrophe


def test_verify_legal_word_lists_true(word_list_small):
    assert app.verify_legal_word_list(['aaa']) is True  # one entry
    assert app.verify_legal_word_list(['aaa', 'bbb', 'ccc']) is True  # lowercase
    assert app.verify_legal_word_list(['AAA', 'BBB', 'CCC']) is True  # capital
    assert app.verify_legal_word_list(['a', 'b', 'c']) is True  # length 1
    assert app.verify_legal_word_list(['aAa', 'Bbb', 'ccc']) is True  # mix case
    assert app.verify_legal_word_list(word_list_small) is True  # word list for future testing
