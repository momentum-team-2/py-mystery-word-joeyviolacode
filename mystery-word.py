file_name = "words.txt"

words_file = open(file_name)
MASTER_WORD_LIST = words_file.readlines()

#explore mapping 1 and 0 to letters of words in subset:






def handle_family_selection(list_of_words, letter_to_check):
    """Uses a collection of helper functions(below) to take in the current list of words and select a subset of that list based on
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


if __name__ == "__main__":
    test_words = ["teeth", "clear", "tooth", "beech", "beach", "teach", "peach", "place", "mango"]
    print(test_words)
    new_family = handle_family_selection(test_words, "a")
    print(new_family)
    newer_family = handle_family_selection(new_family, "p")
    print(newer_family)
