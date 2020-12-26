# Name          : Oleksandr Shysh
# Collaborators : -
# Time spent    : Four days(18 hours)

# Imports modules.
import math
import random
import re

# Declares constants.
VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7
WILDCARD = '*'
STOP_SYMBOL = '!!'

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1,
    'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """

    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """

    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x, 0) + 1
    return freq


def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

    The score for a word is the product of two components:

    The first component is the sum of the points for letters in the word.
    The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

    Letters are scored as in Scrabble; A is worth 1, B is
    worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """

    first_component = 0
    hand_length = len(word)  # The length of the word.

    # Calculates the sum of the points for letters in the word.
    for letter in word.lower():
        if letter != WILDCARD:
            first_component += SCRABBLE_LETTER_VALUES[letter]

    # Calculates the second component.
    second_component = HAND_SIZE * hand_length - 3 * (n - hand_length)
    # If it is less than one, the second component becomes one.
    if second_component < 1:
        second_component = 1

    # Calculates the final score.
    final_score = first_component * second_component

    return final_score


def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """

    print('Current hand: ', end='')
    for letter in hand.keys():
        for _ in range(hand[letter]):
            print(letter, end=' ')  # print all on the same line
    print()  # print an empty line


def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """

    hand = {}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels - 1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1

    hand[WILDCARD] = 1

    for i in range(num_vowels, n):
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1

    return hand


def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """

    # Creates a new dictionary.
    new_hand = dict()
    # Converts the word to dictionary(string -> int), same as hand.
    word_frequency_dict = get_frequency_dict(word.lower())
    # Makes the number of occurrences of letters, that was used in the word, equal to zero.
    for letter in hand:
        new_hand[letter] = hand[letter] - word_frequency_dict.get(letter, 0)
        # If a letter is not in a hand but was used, makes it equal to zero.
        if new_hand[letter] < 0:
            new_hand[letter] = 0

    # Returns the new hand.
    return new_hand


def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """

    if not is_match(word, word_list):
        return False

    # Converts the word to dictionary(string -> int), same as hand.
    word_frequency_dict = get_frequency_dict(word.lower())

    # If the number of occurrences of a letter more than the number in the hand, returns False.
    for key in word_frequency_dict:
        if word_frequency_dict[key] > hand.get(key, 0):
            return False

    # Otherwise, returns True.
    return True


def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """

    # Counts the number of occurrences of each letter in the word and adds together.
    length = sum(hand.values())

    return length


def is_match(word, word_list):
    """
    Returns True, if a match is found(the wildcard is replaced by a vowel gives a valid word).
    Otherwise, returns False.

    word: string
    word_list: list of lowercase strings
    returns: boolean
    """

    # Creates a pattern to find match.
    pattern = re.compile(word.replace(WILDCARD, f'[{VOWELS}]'))
    # Checks if a word can be match.
    for w in word_list:
        match = pattern.fullmatch(w)
        # If a match is found, aborts the search and returns True.
        if match:
            return True

    # If no matches found, returns False.
    return False


def ask_user(prompt, **kwargs):
    """
    Asks user for entering the corresponding values and checks the inputs depending on the parameters.
    Returns the correct input user entered.

    prompt: string, helpful input message.
    type: string, the input format(int, float, single(only one character)), default - str.
    bool: bool, indicates if the input should be only 'Yes' or 'No', default - False.
    returns: string.
    """

    # Allows to enter value until it gets the right one.
    while True:
        answer = input(prompt)

        # If the function calls with validator or values parameter, checks the input.
        if (('validator' in kwargs and not kwargs['validator'](answer)) or
                ('values' in kwargs and answer not in kwargs['values'])):
            # If an error happens, shows a warning message.
            if 'warn_msg' in kwargs:  # If a warning message is described in the function calling, prints it.
                print(kwargs['warn_msg'])
            # Otherwise, prints usual warnings message.
            else:
                print("That is not valid value")

        # If there is no problems, interrupts the loop.
        else:
            break

    return answer


def calc_word_score(hand, word, total_score):
    """
    Calculates the word score after a word entered dependent on a word is valid or not.

    hand: dictionary (string-> int).
    word: string, a word user entered.
    total_score: integer, the word score after a word entered.

    Returns: total_score - integer.
    """

    # If the word is valid:
    if is_valid_word(word, hand, word_list):
        # Tells the user how many points the word earned, and the updated total score.
        total_score += get_word_score(word, calculate_handlen(hand))
        print(f'"{word}" earned {get_word_score(word, calculate_handlen(hand))} points. '
              f'Total: {total_score} points')
        print()
    # Otherwise (the word is not valid):
    else:
        # Rejects invalid word (prints a message).
        print("This is not a valid word. Please choose another word.")
        print()

    return total_score


def print_score(hand, total_score):
    """
    Prints the word score after each hand played.

    hand: dictionary (string-> int).
    total_score: integer, the word score after a hand played.

    Returns: nothing.
    """

    if calculate_handlen(hand) == 0:
        print("Ran out of letters.")
    # so tell user the total score
    print(f"Total score for this hand: {total_score}")
    print("--------")


def input_substitute(hand, ask_substitute):
    """
    Asks if a user wants to substitute a letter and which one. If a user agreed, substitutes the letter.

    hand: dictionary (string-> int).
    ask_substitute: bool, denotes if the substitute was already used.

    Returns: hand - dictionary and ask_substitute - bool.
    """

    to_substitute = ask_user("Would you like to substitute a letter? ",
                             values=('yes', 'no'),
                             warn_msg='You need to enter "yes" or "no"')

    # If a user agreed, asks which letter to replace.
    if to_substitute == 'yes':
        letter = ask_user('Which letter would you like to replace: ',
                          validator=lambda ans: (ans.lower() in CONSONANTS or ans.lower() in VOWELS) and len(ans) == 1,
                          warn_msg="You need to enter a single Latin letter")
        # Substitutes the letter.
        hand = substitute_hand(hand, letter.lower())
        # Does not allow to do it again(does not ask it again).
        ask_substitute = False

    return hand, ask_substitute


def input_replay(hand, ask_substitute, ask_replay):
    """
    Asks if a user wants to replay last hand. If a user agrees.

    hand: dictionary (string-> int).
    ask_substitute: bool, denotes if the substitute was already used.
    ask_replay: bool, denotes if the replay was already used.

    Returns: ask_replay - bool.
    """

    to_replay = ask_user("Would you like to replay the hand? ",
                         values=('yes', 'no'),
                         warn_msg='You need to enter "yes" or "no"')

    if to_replay == 'yes':
        # Does not allow to do it again(does not ask it again).
        ask_replay = False
        # Displays the hand, if the substitute was not used.
        if ask_substitute:
            display_hand(hand)

    return ask_replay


def add_guessed_word(hand, ask_replay, total_list, replayed):
    """
    Calculates the word score after a word entered dependent on a word is valid or not. Adds it to the list.
    If a hand was replayed, adds to the list of guessed words the biggest of two scores.

    ask_replay: bool, denotes if the program should ask user for replaying or not.
    total_list: list, a list of scores.
    replayed: bool, denotes if the replay was already used.

    Returns: total_list: list, replayed: bool.
    """

    if ask_replay:
        # Play each hand separately and adds the received points to the total.
        total_list.append(play_hand(hand, word_list))
    # If a hand is replayed, adds to the total list the biggest of two scores.
    elif not ask_replay and replayed:
        total_list[-1] = max(total_list[-1], play_hand(hand, word_list))
        # Takes into account that user can replay only once.
        replayed = False
    # If a user already replayed hand, plays new hand and adds the received points to the total.
    else:
        total_list.append(play_hand(hand, word_list))

    return total_list, replayed


def sum_total_score(total_list, total):
    """
    Sums all hand scores and returns total score.

    total_list: list, a list of scores.
    total: integer, the sum of all scores.

    Returns total: integer.
    """

    # Adds each score from the list to the total.
    for score in total_list:
        total += score
    # Prints the total score.
    print(f"Total score over all hands: {total}")
    return total


def deal_new_hand(hand, hands, ask_substitute):
    """
    Deals new hand, subtracts a hand from remaining hands.

    hand: dictionary (string -> int)
    hands: integer, the number of remaining hands to play.
    ask_substitute: bool, denotes if the substitute was already used.

    Returns hand: dictionary (string -> int), hands: integer.
    """

    # Creates a new hand.
    hand = deal_hand(HAND_SIZE)
    # Subtracts a hand after it was played.
    hands -= 1
    # Prints a new hand.
    if hands > 0 and ask_substitute:
        display_hand(hand)

    return hand, hands


def play_hand(hand, word_list):
    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputting two
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
    """

    # Keeps track of the total score.
    total_score = 0
    # As long as there are still letters left in the hand:
    while calculate_handlen(hand) > 0:
        # Displays the hand.
        display_hand(hand)
        # Asks user for input.
        word = ask_user("Enter word, or “!!” to indicate that you are finished: ")
        # If the input is two exclamation points:
        if word == STOP_SYMBOL:
            break  # Ends the game (breaks out of the loop)

        # Otherwise (the input is not two exclamation points).
        total_score = calc_word_score(hand, word, total_score)
        # Updates the user's hand by removing the letters of their inputted word.
        hand = update_hand(hand, word)

    # Game is over (user entered '!!' or ran out of letters),
    print_score(hand, total_score)
    # Returns the total score as result of function.
    return total_score


def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """

    # If the letter user wants to replace is in the hand, substitutes it with a random unused letter.
    if letter in hand.keys():
        # Copies the hand to not mutate it.
        new_hand = hand.copy()
        # Creates a set of letters in the hand.
        existed_hand = set(hand.keys())
        # Creates a set of all alphabetic letters.
        all_letters = set(CONSONANTS + VOWELS)
        # Creates a list of the not used letters.
        not_used_letters = [item for item in all_letters if item not in existed_hand]

        # Chooses random letter.
        new_letter = random.choice(not_used_letters)
        # Substitutes the letter.
        new_hand[new_letter] = new_hand[letter]
        # Removes the substituted letter.
        new_hand.pop(letter)

    return new_hand


def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitute option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand. This can only be done once
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """

    # Creates a hand.
    hand = deal_hand(HAND_SIZE)
    # Allows to substitute a letter or replay a hand.
    ask_substitute, ask_replay, replayed = True, True, True
    # A list of guessed letters.
    total_list = []

    # Asks for entering the number of hands.
    hands = int(ask_user("Enter total number of hands: ", validator=lambda ans: ans.isdigit() and int(ans) > 0,
                         warn_msg="You should enter a positive integer"))
    # Shows a hand at the start of the game.
    display_hand(hand)

    # The game continues until all hands have been played.
    while hands > 0:
        # Asks a user for a substitute.
        if ask_substitute:
            hand, ask_substitute = input_substitute(hand, ask_substitute)
            print()
        # Plays a hand and adds a word score to the total list.
        total_list, replayed = add_guessed_word(hand, ask_replay, total_list, replayed)

        if ask_replay:
            # Asks a user for replaying.
            ask_replay = input_replay(hand, ask_substitute, ask_replay)
            if not ask_replay:
                continue
        # Deals new hand, subtracts a hand from remaining hands.
        hand, hands = deal_new_hand(hand, hands, ask_substitute)

    # Adds each score from the list to the total.
    total = sum_total_score(total_list, 0)
    return total


# Launches the game.
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
