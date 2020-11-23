# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"

# Initial variables
guesses_remaining = 6
warnings_remaining = 3
vowels = set('aeiou')
letters_guessed = []


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("{}".format(len(wordlist)), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    """
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    """
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    for letter in list(secret_word):
        if letter not in letters_guessed:
            return False

    return True


def get_guessed_word(secret_word, letters_guessed):
    """
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    """
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    not_guessed_letters = len(secret_word)
    encrypted_word_list = ('_ ,' * (not_guessed_letters)).split(',')
    encrypted_word = ''

    for letter in list(secret_word):
        if letter in letters_guessed:
            indices = [index for index, element in enumerate(secret_word) if element == letter]
            for i in range(len(indices)):
                encrypted_word_list[indices[i]] = letter

    for char in encrypted_word_list:
        encrypted_word += char

    return encrypted_word


def get_available_letters(letters_guessed):
    """
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    """
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    alphabet = string.ascii_lowercase
    for letter in letters_guessed:
        if letter in alphabet:
            alphabet = alphabet.replace(letter, '')

    return alphabet


def delimiter():
    """
    prints the dividing line
    """
    print('-------------------------------')


def welcome_msg(secret_word):
    """
    secret_word: string, the word the user is guessing; assumes all letters are lowercase
    Prints welcome-message
    """

    print(f"Welcome to the game Hangman! \nI am thinking of a word that"
          f" is {len(secret_word)} letters long.")
    print(f'You have {warnings_remaining} warnings left.')


def guesses_msg(guesses_remaining, letters_guessed):
    """
    guesses_remaining: integer, number of remaining guesses
    letters_guessed: list (of letters), which letters have been guessed so far
    Prints remaining guesses and available letters
    """

    delimiter()
    print(f'You have {guesses_remaining} guesses left.')
    print(f'Available letters: {get_available_letters(letters_guessed)}')


def reduce_warnings(guesses_remaining, warnings_remaining):
    """
    guesses_remaining: integer, number of remaining guesses
    warnings_remaining: integer, number of remaining warnings

    Takes away a warning or a guess if there are no warnings left
    Returns remaining guesses and warnings
    """

    if warnings_remaining <= 0:
        warnings_remaining -= 1
        guesses_remaining -= 1
        return (guesses_remaining, warnings_remaining)
    else:
        warnings_remaining -= 1
    return (guesses_remaining, warnings_remaining)


def check_letter(letter, guesses_remaining, warnings_remaining, letters_guessed):
    """
    letter: string, letter to check
    guesses_remaining: integer, remaining guesses
    warnings_remaining: integer, remaining warnings
    letters_guessed: list (of letters), which letters have been guessed so far

    Checks if letter is valid
    Returns a tuple with the following values: boolean True if the letter is valid, False otherwise,
    remaining guesses and warnings, message - one of 4 messages depending on the situation
    """

    not_valid_msg = "Oops! That is not a valid letter. You have {warnings_remaining} warnings left: {secret_word}"
    repeat_msg = "Oops! You've already guessed that letter. You have {warnings_remaining} warnings left: {secret_word}"
    no_warns_not_valid_msg = "Oops! That is not a valid letter. You have no warnings left" \
                             " so you lose one guess: {secret_word}"
    no_warns_repeated_msg = "Oops! You've already guessed that letter. You have no warnings left" \
                            " so you lose one guess: {secret_word}"

    if not letter.isascii() or len(letter) != 1:
        guesses_remaining, warnings_remaining = reduce_warnings(guesses_remaining, warnings_remaining)

        if warnings_remaining < 0:
            not_valid_msg = no_warns_not_valid_msg

        return False, guesses_remaining, warnings_remaining, not_valid_msg

    elif letter in letters_guessed:
        guesses_remaining, warnings_remaining = reduce_warnings(guesses_remaining, warnings_remaining)

        if warnings_remaining < 0:
            repeat_msg = no_warns_repeated_msg

        return False, guesses_remaining, warnings_remaining, repeat_msg

    else:
        return True, guesses_remaining, warnings_remaining, None


def is_in_word(letter, secret_word, guesses_remaining):
    """
    letter: string, letter to check
    secret_word: string
    guesses_remaining: integer, number of remaining guesses

    Prints whether there is the letter in the secret word and takes away guesses if the letter is not in the secret word
    Returns remaining guesses
    """

    if letter in list(secret_word):
        print("Good guess: ", end='')

    else:
        print("Oops! That letter is not in my word: ", end='')
        if letter in vowels:
            guesses_remaining -= 2
        else:
            guesses_remaining -= 1

    return guesses_remaining


def calc_score(secret_word, guesses_remaining):
    """
    secret_word: string, the word the user is guessing; assumes all letters are lowercase
    guesses_remaining: integer, number of remaining guesses

    Returns the score which is equal to the number of remaining guesses multiplied
     by the number of unique letters in the secret word
    """

    score = guesses_remaining * len(set(secret_word))
    return score


def win_or_lose(secret_word, letters_guessed, guesses_remaining):
    """
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    guesses_remaining: integer, number of remaining guesses

    Prints congratulation-message and the score if a user won and sorry-message if a user lost
    """

    if is_word_guessed(secret_word, letters_guessed):
        print(f'Congratulations, you won! Your total score for this game '
              f'is: {calc_score(secret_word, guesses_remaining)}')

    else:
        print(f'Sorry, you ran out of guesses. The word was {secret_word}')


def hangman(secret_word, hints_on=False, guesses_remaining=6, warnings_remaining=3):
    """
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    Follows the other limitations detailed in the problem write-up.
    """
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    welcome_msg(secret_word)

    while not is_word_guessed(secret_word, letters_guessed) and guesses_remaining > 0:
        guesses_msg(guesses_remaining, letters_guessed)

        while True:
            letter = input('Please guess a letter: ').lower()

            # activating hints
            if hints_on and letter == "*":
                show_possible_matches(get_guessed_word(secret_word, letters_guessed))
                guesses_msg(guesses_remaining, letters_guessed)
                continue

            is_letter_correct, guesses_remaining, warnings_remaining, msg = check_letter(letter,
                                                                                         guesses_remaining,
                                                                                         warnings_remaining,
                                                                                         letters_guessed)

            if is_letter_correct:
                break
            else:
                print(msg.format(warnings_remaining=warnings_remaining,
                                 secret_word=get_guessed_word(secret_word, letters_guessed)))
                if guesses_remaining == 0:
                    break
                guesses_msg(guesses_remaining, letters_guessed)

        if guesses_remaining == 0:
            break

        letters_guessed.append(letter)

        guesses_remaining = is_in_word(letter, secret_word, guesses_remaining)
        print(get_guessed_word(secret_word, letters_guessed))

    delimiter()
    win_or_lose(secret_word, letters_guessed, guesses_remaining)


# -----------------------------------


def match_with_gaps(my_word, other_word):
    """
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise:
    """
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    my_word = my_word.replace(" ", "")

    if len(my_word) != len(other_word):
        return False

    else:
        for i in range(len(my_word)):

            if my_word[i] != "_" and my_word[i] != other_word[i]:
                return False

        return True


def show_possible_matches(my_word):
    """
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    """
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    possible_matches_list = []

    for word in wordlist:
        if match_with_gaps(my_word, word):
            possible_matches_list.append(word)

    if len(possible_matches_list) == 0:
        print('No matches found')
    else:
        print("Possible word matches are: ", end="")
        print(*possible_matches_list)


def hangman_with_hints(secret_word):
    """
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word.

    Follows the other limitations detailed in the problem write-up.
    """
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    hangman(secret_word, hints_on=True)


# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.

    # secret_word = choose_word(wordlist)
    # hangman(secret_word)

###############

# To test part 3 re-comment out the above lines and
# uncomment the following two lines.

    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
