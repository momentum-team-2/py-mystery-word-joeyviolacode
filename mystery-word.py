import random

file_name = "words.txt"

words_file = open(file_name)
complete_words_list = words_file.readlines()
words_file.close()
MASTER_WORD_LIST = [word.replace("\n", "").upper() for word in complete_words_list]
TRIES_ALLOWED = 8


def start_game():
    print()
    difficulty = get_difficulty()
    length = get_length()
    word_list = get_words_of_length(length)
    if difficulty == "E":
        run_game_e(get_word(word_list))
    else:
        run_game_s(word_list)

def run_game_e(word):
    guessed_letters = []
    wrong_tries = 0
    while True:
        display_word = get_display_str(word, guessed_letters)
        if no_blanks(display_word):
            print("You win!!!  I didn't think you could do it.  Surprises all around.  Your word was: " + word + "\n\n")
            play_again()
        guess = get_guess(display_word, wrong_tries, guessed_letters)
        guessed_letters.append(guess)
        if guess in word:
            print("\nGood guess!  That's in the word!")
        else:
            print("\nSorry.  That's not a letter in the word you're trying to guess.")
            wrong_tries += 1
        if wrong_tries == TRIES_ALLOWED:
            print("You've taken too many guesses.  Unfortunately, you have not won the day.\n")
            print("The word that you were trying to figure out was: " + word)
            print("It's kind of obvious now that you see it, isn't it?")
            play_again()


def run_game_s(word_list):
    print("The word list currently contains " + str(len(word_list)) + " words.")
    guessed_letters = []
    wrong_tries = 0
    while True:
        display_word = get_display_str(word_list, guessed_letters)
        if no_blanks(display_word):
            print("You win!!!  I didn't think you could do it.  Surprises all around.  Your word was: " 
                    + word_list[random.randint(0, len(word_list) - 1)] + "\n\n")
            play_again()
        guess = get_guess(display_word, wrong_tries, guessed_letters)
        guessed_letters.append(guess)
        word_list = handle_family_selection(word_list, guess)
        print("The word list currently contains " + str(len(word_list)) + " words.")
        if guess in word_list[0]:
            print("\nGood guess!  That's in the word!")
        else:
            print("\nSorry.  That's not a letter in the word you're trying to guess.")
            wrong_tries += 1
        if wrong_tries == TRIES_ALLOWED:
            print("You've taken too many guesses.  Unfortunately, you have not won the day.\n")
            print("The word that you were trying to figure out was: " + word_list[random.randint(0, len(word_list) - 1)])
            print("It's kind of obvious now that you see it, isn't it?")
            play_again()

def play_again():
    print()
    print("That was...exciting?  Please don't feel like you have to, but do you want to play again?")
    print("Don't feel like you have to just to make me feel better.\nI'm completely happy to free up some memory and just catch some sleep.")
    print("Anyway, let's make this easy on all of us.  Press Y for (Y)es if you want to play again.")
    again = input("If you don't want to play again, press anything at all other than Y.   ").upper()
    if again == "Y":
        print("Starting")
        start_game()
    else:
        print("exiting")
        exit()

def no_blanks(display_word):
    return "_" not in display_word


def get_guess(display_word, wrong_tries, guessed_letters):
    """This function takes in a word (or list of words in Sinister), displays the information known so far about the guesses that have
        been made and then prompts the user for a letter.  I makes sure that it receives a letter, and if so, returns a capitalized
        version of that letter to the caller"""
    print()
    print(f"You're allowed only {TRIES_ALLOWED - wrong_tries} more wrong guesses.  Be very careful.")
    print("Here's what you know so far about the word you're trying to guess:\n")
    print(display_word + "\n\n")
    guess = ""
    if len(guessed_letters) == 0:
        guess = input("Make your first guess.  In case it helps, this should be a letter, one of the ones in the alphabet: ")
    else: 
        print("You have already used: " + ", ".join(guessed_letters))
        guess = input("Time to make another guess: ")
    while not ("A" <= guess <= "z") or guess.upper() in guessed_letters:
        print("\nUm...I'm afraid that isn't a letter.  Or you've already picked that one.  I don't know.")
        print("You'll find letters kind of in the big middle part of your keyboard.\n")
        guess = input("Try again: ")
    return guess.upper()


def get_difficulty():
    difficulty = input("Welcome to Mystery Word!  Would you like to play the (E)asy or (S)inister version?\nOr would you just like to (Q)uit while you're ahead? ")
    while difficulty is not "E" and difficulty is not "S" and difficulty is not "Q":
        print("\nWell, that isn't an E or an S.  You know that this IS a spelling game, right?  Do you know your lettters?\nWait!  Do you know what letters ARE?")
        print("Please try again, but just...be better this time.")
        difficulty = input("\nWould you like to play the (E)asy or (S)inister version?  Or, you know, you can just give me a 'Q'.\nWhich is it? ")
    if difficulty is "E":
        print("\nOkay, but that seems a bit tame.\n")
    elif difficulty is "S":
        print("\nIt's your funeral.\n")
    else:
        print("\nThat's probably for the best, isn't it?\nIt'll certainly save us all a lot of trouble.\nStudy up and come back later.\nOr don't.  I don't really care.")
        exit(1)
    return difficulty

def get_length():
    length = int(input("Please let me know what length of word you'd like to try to solve.\nThis number should be between 3 and 24, inclusive: "))
    while length < 3 or length > 24:
        print("\n**SIGH**   Are you the same person who was having trouble with letters a few minutes back?")
        print("No, no.  Don't answer.  I don't want to know.  Can you please just try again?")
        length = input("But please do really, really try to give me a number between 3 and 24: ")
    return length

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
#by the game.....the commented pairs of variables and print provide testing options for seeing what happens at each stage 
# of the process.

# test_words = ["teeth", "clear", "tooth", "beech", "beach", "teach", "peach", "place", "mango"]
# print(test_words)

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

# test_words_keyed = map_key_to_word(test_words, "a")
# print(test_words_keyed)

def collect_keys(words_key):
    """This function sifts the given list of tuples for all the unique keys, passing them all
        back in a list to be used for sorting"""
    list_of_keys = []
    for item in words_key:
        if item[1] not in list_of_keys:
            list_of_keys.append(item[1])
    return list_of_keys

# list_of_keys = collect_keys(test_words_keyed)
# print(list_of_keys)

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

# word_families = sort_by_key(test_words_keyed, list_of_keys)
# print(word_families)

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

# selected_family = select_family(word_families)
# print(selected_family)



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


## Main function to start game logic
if __name__ == "__main__":
    start_game()
    #run_game_s(["TEETH", "CLEAR", "TOOTH", "BEECH", "BEACH", "TEACH", "PEACH", "PLACE", "MANGO"])
    #get_guess(get_display_str("PASTE", ["P", "S"]), 3, ["P", "S"])
    #print(no_blanks("P E A R T"))
    #start_game()
    # test_words = ["teeth", "clear", "tooth", "beech", "beach", "teach", "peach", "place", "mango"]
    # print(test_words)
    # new_family = handle_family_selection(test_words, "a")
    # print(new_family)
    # newer_family = handle_family_selection(new_family, "p")
    # print(newer_family)









### Obsolete function...added list-check to make a single function that performs this operation
# def get_display_str_s(word_list):
# """Returns a string representation of guessed letters and blanks for unguessed letters to show the player for the chosen word family"""
# str = ""
# word = word_list[0]
# for letter in word:
#     if letter in guessed_letters:
#         str += letter + " "
#     else:
#         str += "_ "
# return str