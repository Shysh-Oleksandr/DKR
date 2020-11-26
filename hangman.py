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

    # If at least one letter in secret word is not in guessed letters, returns False.
    for letter in list(secret_word):
        if letter not in letters_guessed:
            return False
    # Otherwise, returns True.
    return True


def get_guessed_word(secret_word, letters_guessed):
    """
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    """
    # Makes a list where each element is an encrypted letter.
    encrypted_word_list = ('_ ,' * (len(secret_word))).split(',')
    # Makes a blank string.
    encrypted_word = ''

    # If a letter of the secret word is guessed, replaces the underscore with a letter.
    for letter in list(secret_word):
        if letter in letters_guessed:
            indices = [index for index, element in enumerate(secret_word) if element == letter]
            for i in range(len(indices)):
                encrypted_word_list[indices[i]] = letter

    # Adds all elements of the list to one string.
    for char in encrypted_word_list:
        encrypted_word += char

    return encrypted_word


def get_available_letters(letters_guessed):
    """
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    """

    # All alphabet letters in one string.
    available_letters = string.ascii_lowercase

    # If the letter is guessed, removes it from the list of available letters.
    for letter in letters_guessed:
        if letter in available_letters:
            available_letters = available_letters.replace(letter, '')

    return available_letters


# Secondary functions
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


def subtract_warnings(guesses_remaining, warnings_remaining):
    """
    guesses_remaining: integer, number of remaining guesses
    warnings_remaining: integer, number of remaining warnings

    Subtracts a warning or a guess if there are no warnings left
    Returns remaining guesses and warnings
    """

    # If there are not warnings left, subtracts  one guess.
    if warnings_remaining <= 0:
        warnings_remaining -= 1
        guesses_remaining -= 1
        return guesses_remaining, warnings_remaining

    # Otherwise, subtracts one warning.
    else:
        warnings_remaining -= 1

    return guesses_remaining, warnings_remaining


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

    # Makes four messages: if the entered letter is not valid, is repeated,
    # the same two cases but there are no warnings left.
    not_valid_msg = "Oops! That is not a valid letter. You have {warnings_remaining} warnings left: {secret_word}"
    repeated_msg = "Oops! You've already guessed that letter. You have {warnings_remaining} warnings left: {secret_word}"
    no_warns_not_valid_msg = "Oops! That is not a valid letter. You have no warnings left" \
                             " so you lose one guess: {secret_word}"
    no_warns_repeated_msg = "Oops! You've already guessed that letter. You have no warnings left" \
                            " so you lose one guess: {secret_word}"

    # If the letter is not in alphabet or more than one letter is entered, subtracts warning.
    if not letter.isascii() or len(letter) != 1:
        guesses_remaining, warnings_remaining = subtract_warnings(guesses_remaining, warnings_remaining)

        if warnings_remaining < 0:
            not_valid_msg = no_warns_not_valid_msg

        return False, guesses_remaining, warnings_remaining, not_valid_msg

    # If the letter was already named, subtracts warning.
    elif letter in letters_guessed:
        guesses_remaining, warnings_remaining = subtract_warnings(guesses_remaining, warnings_remaining)

        if warnings_remaining < 0:
            repeated_msg = no_warns_repeated_msg

        return False, guesses_remaining, warnings_remaining, repeated_msg

    else:
        return True, guesses_remaining, warnings_remaining, None


def is_in_word(letter, secret_word, guesses_remaining):
    """
    letter: string, letter to check
    secret_word: string
    guesses_remaining: integer, number of remaining guesses

    Prints whether there is the letter in the secret word and subtracts guesses if the letter is not in the secret word
    Returns remaining guesses
    """

    # If the letter is in the secret word, prints positive message.
    if letter in list(secret_word):
        print("Good guess: ", end='')

    # Otherwise, prints negative message and subtracts guesses.
    else:
        print("Oops! That letter is not in my word: ", end='')
        # If the letter is a vowel, subtracting two guesses.
        if letter in vowels:
            guesses_remaining -= 2
        # Otherwise, subtracts one guess.
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

    # If the word is guessed, prints positive message and the score.
    if is_word_guessed(secret_word, letters_guessed):
        print(f'Congratulations, you won! Your total score for this game '
              f'is: {calc_score(secret_word, guesses_remaining)}')
    # Otherwise, prints negative message.
    else:
        print(f'Sorry, you ran out of guesses. The word was {secret_word}')


def hangman(secret_word, hints_on=False, guesses_remaining=6, warnings_remaining=3):
    """
    secret_word: string, the secret word to guess.
    hints_on: boolean. True, if you want to play with hints. Default = False
    guesses_remaining: integer, the number of guesses. Default = 6
    warnings_remaining: integer, the number of warnings. Default = 3

    Starts up an interactive game of Hangman.
    """

    # Prints welcome-message.
    welcome_msg(secret_word)

    # The game continues until the word is guessed or the guesses end.
    while not is_word_guessed(secret_word, letters_guessed) and guesses_remaining > 0:

        # Prints message about remaining guesses.
        guesses_msg(guesses_remaining, letters_guessed)

        while True:
            # Asks to enter new letter.
            letter = input('Please guess a letter: ').lower()

            # If hints is on and user entered asterisk(*), shows possible word variants.
            if hints_on and letter == "*":
                show_possible_matches(get_guessed_word(secret_word, letters_guessed))
                guesses_msg(guesses_remaining, letters_guessed)
                continue

            # Checks the letter for validity.
            is_letter_correct, guesses_remaining, warnings_remaining, msg = check_letter(letter,
                                                                                         guesses_remaining,
                                                                                         warnings_remaining,
                                                                                         letters_guessed)
            # If the letter is valid, exits the loop.
            if is_letter_correct:
                break
            # Otherwise, prints message with explanations for incorrect input.
            else:
                print(msg.format(warnings_remaining=warnings_remaining,
                                 secret_word=get_guessed_word(secret_word, letters_guessed)))

                # If there are no guesses left, exits the loop.
                if guesses_remaining == 0:
                    break
                # Otherwise, prints guesses left.
                else:
                    guesses_msg(guesses_remaining, letters_guessed)

        if guesses_remaining == 0:
            break

        # Appends letter to list of the guessed letters.
        letters_guessed.append(letter)

        # Updates remaining guesses.
        guesses_remaining = is_in_word(letter, secret_word, guesses_remaining)
        # Prints the encrypted secret word.
        print(get_guessed_word(secret_word, letters_guessed))

    delimiter()
    # Checks whether the word is guessed or not.
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
    # Removes all spaces.
    my_word = my_word.replace(" ", "")

    # If the length of my word is not equal to the length of another word, another word does not fit.
    if len(my_word) != len(other_word):
        return False

    else:
        for i in range(len(my_word)):
            # If there are not the same symbols in both words, other word does not fit.
            if my_word[i] != "_" and (my_word[i] != other_word[i] or
                                      my_word.count(my_word[i]) != other_word.count(my_word[i])):
                return False

        # Otherwise, It fits.
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

    # Creates blank list for possible matches.
    possible_matches_list = []

    # Adds to the list words that may be the same as my word.
    for word in wordlist:
        if match_with_gaps(my_word, word):
            possible_matches_list.append(word)

    # If there is no matches, prints negative message.
    if len(possible_matches_list) == 0:
        print('No matches found')

    # Otherwise, prints positive message and the list of matches.
    else:
        print("Possible word matches are: ", end="")
        print(*possible_matches_list)


def hangman_with_hints(secret_word):
    """
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.
    """

    # Launches the game with hints.
    hangman(secret_word, hints_on=True)


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
