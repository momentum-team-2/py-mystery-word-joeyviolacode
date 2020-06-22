import random

import os
clear = lambda: os.system("clear")

file_name = "words.txt"
words_file = open(file_name)
complete_words_list = words_file.readlines()
words_file.close()
MASTER_WORD_LIST = [word.replace("\n", "").upper() for word in complete_words_list]
TRIES_ALLOWED = 10


def start_game():
    """Called by the main in order to initialize user options for the game and call the appropriate mode"""
    clear()
    difficulty = get_difficulty()
    length = get_length()
    word_list = get_words_of_length(length)
    if difficulty == "E":
        run_game_e(get_word(word_list))
    else:
        run_game_s(word_list)

def run_game_e(word):
    """Runs the easy version of the game logic"""
    guessed_letters = []
    wrong_tries = 0
    confirm_string = ""
    while True:
        clear()
        print(confirm_string)
        display_word = get_display_str(word, guessed_letters)
        if no_blanks(display_word):
            print("You win!!!  I didn't think you could do it.  Surprises all around.  Your word was: " + word + "\n\n")
            play_again()
        guess = get_guess(display_word, wrong_tries, guessed_letters)
        guessed_letters.append(guess)
        guessed_letters.sort()
        if guess in word:
            confirm_string = "\nGood guess!  That's in the word!"
        else:
            confirm_string = "\nSorry.  That's not a letter in the word you're trying to guess."
            wrong_tries += 1
        if wrong_tries == TRIES_ALLOWED:
            clear()
            game_over(word, guessed_letters)
            play_again()

def run_game_s(word_list):
    """Runs the hard version of the game logic"""
    guessed_letters = []
    wrong_tries = 0
    confirm_string = ""
    word_quantity_string = "The word list currently contains " + str(len(word_list)) + " words."
    while True:
        clear()
        print(confirm_string)
        print(word_quantity_string)
        display_word = get_display_str(word_list, guessed_letters)
        if no_blanks(display_word):
            print("You win!!!  I didn't think you could do it.  Surprises all around.  Your word was: " 
                    + word_list[random.randint(0, len(word_list) - 1)] + "\n\n")
            play_again()
        guess = get_guess(display_word, wrong_tries, guessed_letters)
        guessed_letters.append(guess)
        guessed_letters.sort()
        word_list = handle_family_selection(word_list, guess)
        word_quantity_string = "The word list currently contains " + str(len(word_list)) + " words."
        if guess in word_list[0]:
            confirm_string = "\nGood guess!  That's in the word!"
        else:
            confirm_string = "\nSorry.  That's not a letter in the word you're trying to guess."
            wrong_tries += 1
        if wrong_tries == TRIES_ALLOWED:
            game_over(word_list[random.randint(0, len(word_list) - 1)], guessed_letters)
            play_again()


def get_guess(display_word, wrong_tries, guessed_letters):
    """This function takes in a word (or list of words in Sinister), displays the information known so far about the guesses that have
        been made and then prompts the user for a letter.  I makes sure that it receives a letter, and if so, returns a capitalized
        version of that letter to the caller"""
    print()
    print(f"You have {TRIES_ALLOWED - wrong_tries} wrong guesses remaining.  Be very careful.")
    print("Here's what you know so far about the word you're trying to guess:\n\n")
    print(display_word + "\n\n")
    guess = ""
    if len(guessed_letters) == 0:
        guess = input("Make your first guess.  In case it helps, this should be a letter, one of the ones in the alphabet: ")
    else: 
        print("You have already used: " + ", ".join(guessed_letters))
        guess = input("Time to make another guess: ")
    while not ("A" <= guess <= "z") or guess.upper() in guessed_letters or len(guess) != 1:
        print("\nUm...I'm afraid that isn't a letter.  Or you've already picked that one.  I don't know.")
        print("You'll find letters kind of in the big middle part of your keyboard.\n")
        guess = input("Try again: ")
    return guess.upper()

def get_difficulty():
    """Prompts the user for a difficulty setting, checking for errors and reprompting (and mocking) if necessary before returning
        the selected difficulty"""
    difficulty = input("Welcome to Mystery Word!  Would you like to play the (E)asy or (S)inister version?\nOr would you just like to (Q)uit while you're ahead? ")
    difficulty = difficulty.upper()
    while difficulty != "E" and difficulty != "S" and difficulty != "Q":
        print("\nWell, that isn't an E or an S.  You know that this IS a spelling game, right?  Do you know your lettters?\nWait!  Do you know what letters ARE?")
        print("Please try again, but just...be better this time.")
        difficulty = input("\nWould you like to play the (E)asy or (S)inister version?  Or, you know, you can just give me a 'Q'.\nWhich is it? ").upper()
    if difficulty == "E":
        print("\nOkay, but that seems a bit tame.\n")
    elif difficulty == "S":
        print("\nIt's your funeral.\n")
    else:
        print("\nThat's probably for the best, isn't it?\nIt'll certainly save us all a lot of trouble.\nStudy up and come back later.\nOr don't.  I don't really care.")
        exit(1)
    return difficulty.upper()

def get_length():
    """Prompts the user for a length to their word, checking for errors and reprompting (and mocking) if necessary before returning
        the selected length"""
    length = input("Please let me know what length of word you'd like to try to solve.\nThis number should be between 3 and 24, inclusive: ")
    while length < "0" or length > "9" or int(length) < 3 or int(length) > 24:
        print("\n**SIGH**   Are you the same person who was having trouble with letters a few minutes back?")
        print("No, no.  Don't answer.  I don't want to know.  Can you please just try again?")
        length = input("But please do really, really try to give me a number between 3 and 24: ")
    return int(length)

def get_words_of_length(length):
    """Returns a list of words of a given length.  This will be the starting master family for Sinister and the pool from which 
        a word will be chosen for easy difficulty"""
    return [word for word in MASTER_WORD_LIST if len(word) == length]

def get_word(word_list):
    """Pulls a random word out of the word list.  This is used by the easy version to select a word at random for the player to 
        guess.  It is used by the Sinister version to select a display word at the end of the game when the player has failed to narrow
        the families of words down to a single word"""
    return word_list[random.randint(0, len(word_list) - 1)]

def get_display_str(word_or_list, guessed_letters):
    """Returns a string representation of guessed letters and blanks for unguessed letters to show the player for the chosen word"""
    if isinstance(word_or_list, list):
        word_or_list = word_or_list[0]
    str = ""
    for letter in word_or_list:
        if letter in guessed_letters:
            str += letter + " "
        else:
            str += "_ "
    return str

def game_over(word, guessed_letters):
    """Prints an end of game message to the user"""
    clear()
    print("You've taken too many guesses.  Unfortunately, you have not won the day.\n")
    print("The letters you used were: " + ", ".join(guessed_letters) + "\n")
    print("The word that you were trying to figure out was: " + word + "\n")
    print("It's kind of obvious now that you see it, isn't it?\n")
    input("Press RETURN to continue.")
    clear()


def play_again():
    """Prints a dialogue to the user asking if they would like to play again."""
    print("That was...exciting?  I'm not encouraging it, but do you want to play again?\n")
    print("Don't feel like you have to just to make me feel better.\nI'm completely happy to free up some memory and just catch some sleep.\n")
    print("Anyway, let's make this easy on all of us.  Press Y for (Y)es if you want to play again.")
    again = input("If you don't want to play again, press anything at all other than Y.   ").upper()
    if again == "Y":
        start_game()
    else:
        exit()

def no_blanks(display_word):
    """Helper function used to check if a word no longer has blanks in it and is therefore finished."""
    return "_" not in display_word


def handle_family_selection(list_of_words, letter_to_check):
    """Uses a collection of functions(below) to take in the current list of words and select a subset of that list based on
    criteria set in the select_family() function.  This is used to dodge the players guesses by (at this time) selecting the largest
    list of words that somehow contains the letter checked in some pattern"""
    words_keyed = map_key_to_word(list_of_words, letter_to_check)
    keys = collect_keys(words_keyed)
    sorted_words = sort_by_key(words_keyed, keys)
    family = select_family(sorted_words)
    return family

#The following are a set of functions called by handle_family_selection in order to select the next family of words to be used
#by the game.....

def map_key_to_word(list_of_words, letter_to_check):
    """This requires a list of candidate words and a letter to map onto keys and
    returns a set of tuples with the word and its corresponding key"""
    word_key_pairs = []
    for word in list_of_words:
        key = ""
        for letter in word:
            if letter == letter_to_check:
                key += "1"
            else:
                key += "0"
        word_key_pairs.append((word, key))
    return word_key_pairs

def collect_keys(words_key):
    """This function sifts the given list of tuples for all the unique keys, passing them all
        back in a list to be used for sorting."""
    list_of_keys = []
    for item in words_key:
        if item[1] not in list_of_keys:
            list_of_keys.append(item[1])
    return list_of_keys

def sort_by_key(words_with_keys, key_list):
    """This function requires a list of of tuples containing words and their keys and a list of keys.
        It returns a list of word families (each in a list of its own) that match each individual key"""
    word_list_sorted = []
    for key in key_list:
        word_list = []
        for word in words_with_keys:
            if word[1] == key:
                word_list.append(word[0])
        word_list_sorted.append(word_list)
    return word_list_sorted

def select_family(list_of_families):
    """This function takes in a list of word families and selects the one that will be used by the
        program from this point forward as the word list.
        
        For now, this only selects based on the size of the family.
        
        This is the function to change if a different or more complex selection algorithm is needed/wanted"""
    longest_family = []
    longest_family_length = 0
    for family in list_of_families:
        if len(family) > longest_family_length:
            longest_family_length = len(family)
            longest_family = family
    return longest_family

def welcome():
    """Prints a welcome message??? to the user when the program is fist run"""
    print("West of House")
    print("You are standing in an open field west of a white house, with a boarded front door.")
    input("There is a small mailbox here.")
    input("\n\nJust kidding.\nAlthough it may be better if you just go play Zork instead.")
    print("\n")

## Main function to start game logic
if __name__ == "__main__":
    clear()
    welcome()
    start_game()



#PRELIMINARY DICTIONARY EXPLORATION FUNCTIONS
def find_longest(words_list):
    longest = 0
    for word in words_list:
        if len(word) > longest:
            longest = len(word)
    print(longest)

def find_amount_per_length(words_list):
    for length in range(26):
        count = 0
        for word in words_list:
            if len(word) == length:
                count += 1
        print(str(length) + ": " + str(count))

def print_words_of_length(words_list, length):
    for word in words_list:
        if len(word) == length:
            print(word)




# Working function to combine both easy and sinister into one run_game function....it's possible, but 
# at this point there would be too many if blocks as I have it set up now, as I'm giving extra info in Sinister
# so that it's a little more transparent about how the word sifting is happening.
def run_game_both(word_or_list):
    if isinstance(word_or_list, list):
        print("The word list currently contains " + str(len(word_or_list)) + " words.")
    guessed_letters = []
    wrong_tries = 0
    while True:
        display_word = get_display_str(word_or_list, guessed_letters)
        if no_blanks(display_word):
            print("You win!!!  I didn't think you could do it.  Surprises all around.  Your word was: " 
                    + word_or_list[random.randint(0, len(word_or_list) - 1)] + "\n\n")
            play_again()
        guess = get_guess(display_word, wrong_tries, guessed_letters)
        guessed_letters.append(guess)
        word_list = handle_family_selection(word_or_list, guess)
        print("The word list currently contains " + str(len(word_list)) + " words.")
        if guess in word_or_list[0]:
            print("\nGood guess!  That's in the word!")
        else:
            print("\nSorry.  That's not a letter in the word you're trying to guess.")
            wrong_tries += 1
        if wrong_tries == TRIES_ALLOWED:
            print("You've taken too many guesses.  Unfortunately, you have not won the day.\n")
            print("The word that you were trying to figure out was: " + word_or_list[random.randint(0, len(word_or_list) - 1)])
            print("It's kind of obvious now that you see it, isn't it?")
            play_again()