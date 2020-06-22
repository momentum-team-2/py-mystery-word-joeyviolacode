


test_words = ["TEETH", "TOOTH", "BOOKS", "BOOTH", "MANGO", "PEACH", "BEACH", "TENTH", "PLACE", "CLEAR", "BONGO", "TOMES", "OTHER"]

def handle_family_selection(list_of_words, letter_to_check):
    """Uses a collection of functions(below) to take in the current list of words and select a subset of that list based on
    criteria set in the select_family() function.  This is used to dodge the players guesses by (at this time) selecting the largest
    list of words that somehow contains the letter checked in some pattern"""
    print("\n\nOur starter list on this step of filtration is:\n")
    print(list_of_words)
    print("\nWe are filtering it by the letter: " + letter_to_check + "\n")
    print("_________________________________________________________________________")
    words_keyed = map_key_to_word(list_of_words, letter_to_check)
    print("\nHere is the list of words with their accompanying keys, with a 1 appearing where the letter appears in the word and a 0 when other letters show up:\n")
    print(words_keyed)
    print("_________________________________________________________________________")
    keys = collect_keys(words_keyed)
    print("\nThe next step is to collect a list of all the unique keys in the dictionary.\n")
    print(keys)
    print("_________________________________________________________________________")
    sorted_words = sort_by_key(words_keyed, keys)
    print("\nWe then sort the words into lists of words that share the same key, e.g., containing our checked letter in the same places for every word in the list:\n")
    print(sorted_words)
    print("_________________________________________________________________________")
    family = select_family(sorted_words)
    print("\nFinally, in this simple implementation, we choose the family with the most members as the one to continue using in the game:\n")
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

while True:
    print("************************************************************************************")
    print("The current list of words is: " + ", ".join(test_words))
    letter = input("Enter a letter to use for sifting: ")
    test_words = handle_family_selection(test_words, letter)