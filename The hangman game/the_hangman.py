import sys # For input's exception

def get_hangman_mode_photos():
    """
    The func returns a dict with all of the game modes photos
    Every key describe the number of tries that the user has been guessed wrong

    :return: A dict which conatins the game modes' images. keys(Num_of_tries), Value(Images to output)
    :rtype: dictionary
    """
    game_mode_images = {}
    game_mode_images[0] = """
    x-------x
        """

    game_mode_images[1] = """
    x-------x
    |
    |
    |
    |
    |
        """

    game_mode_images[2] = """
    x-------x
    |       |
    |       0
    |
    |
    |
        """

    game_mode_images[3] = """
    x-------x
    |       |
    |       0
    |       |
    |
    |
        """

    game_mode_images[4] = """
    x-------x
    |       |
    |       0
    |      /|\\
    |
    |
        """

    game_mode_images[5] = """
    x-------x
    |       |
    |       0
    |      /|\\
    |      /
    |
        """

    game_mode_images[6] = """
    x-------x
    |       |
    |       0
    |      /|\\
    |      / \\
    |
        """

    return game_mode_images

def welcome_screen(max_tries):
    """
    The func gets the max_tries variable as a parameter and returns the "the Welcome Screen" as string
    The "welcome screen" Looks like this:
     _    _                                         
    | |  | |                                        
    | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __  
    |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
    | |  | | (_| | | | | (_| | | | | | | (_| | | | |
    |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                         __/ |                      
                        |___/
    6(max_tries_variable)

    :param max_tries: The maximum tries that the user may guess wrong
    :type max_tries: int
    :return: The "Welcome Screen" of the game
    :rtype: string
    """

    HANGMAN_ASCII_ART = """
    Welcome to the game Hangman\n 
     _    _                                         
    | |  | |                                        
    | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __  
    |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
    | |  | | (_| | | | | (_| | | | | | | (_| | | | |
    |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                         __/ |                      
                        |___/
    \n
    """
    HANGMAN_ASCII_ART += str(max_tries)
    HANGMAN_ASCII_ART += '\n'

    return HANGMAN_ASCII_ART

def get_index_Value():
    """
    This func gets from the user an input and validates that it's a positive number
    Else, it will ask again for an input (A loop)
    
    :return: The index value
    :rtype: int
    """
    int_condition = False
    index = input("Enter index: ")

    while not int_condition:
        int_condition = True
        if index == '0': # Not positive
            int_condition = False

        if not index.isnumeric():
            int_condition = False

        if not int_condition:
            index = input("Enter index (A positive number): ")
    return int(index)

def show_fail_status(status_image):
    """
    This func gets the game mode image from the "HANGMAN_PHOTOS" dict and prints it to the user

    :param status_image: The game's mode image
    :type status_image: string
    """
    print(":(")
    print(status_image)

def choose_word(file_path, index):
    """
    The func gets the file path and index number to receive the secret word of tehe game

    :param file_path: The path of the input's file
    :param index: An index numbers which point to the secret word from the input's file
    :type file_path: String
    :type index: int
    :return: The secret word of the game
    :rtype: string
    """
    secret_word = '' # Initiate the return variable
    try:
        # Open the user's file
        file = open(file_path, 'r')
    except OSError as e:
        print(f"\nError message: {e}", file=sys.stderr)
        return ''
    else:
        # Ignrore the '\n' and get the value of the list as string 
        read_file = file.read().split("\n")[0]
        
        # Convert the string into a list
        words_list = read_file.split()
        
        # Get the secret word by the index
        # If index exceed the lenght, reset the index value
        while index > len(words_list):
            index -= len(words_list) 
        secret_word = words_list[index - 1]
        # Close the user's file
        file.close()
        return secret_word

def check_win(secret_word, old_letters_guessed):
    """
    The func checks if the user has won this game by guessing all of the letters

    :param secret_word: The secret_word value
    :param old_letters_guessed: A list that conatins all the of the user's guesses
    :type secret_word: string
    :type old_letters_guessed: list
    :return: True if all of the secret word's letters are in the "old_letters_guessed" list. Else, return False
    :rtype: boolean
    """
    if len(secret_word) == 0:
        return True
    elif len(secret_word) == 1 and secret_word in old_letters_guessed:
        return True
    elif len(secret_word) == 1 and secret_word not in old_letters_guessed:
        return False
    else:
        condition = True
        for word in secret_word:
            if word not in old_letters_guessed:
                condition = False
                break
        return condition

def show_hidden_word(secret_word, old_letters_guessed):
    """
    The func gets a secret word from the user and returns a string that contains all of the words
    If there are words which have not guessed, they will be shown as Underscore character

    :param secret_word: The secret_word value
    :param old_letters_guessed: A list that conatins all the of the user's guesses
    :type secret_word: string
    :type old_letters_guessed: list
    :return:
        A string of words and bottom lines
        All of the guessed words will be displayed on the right place
        All of the unguessed words will be displaty as underscore on the right place 
    :rtype: string
    """
    output = ""
    if len(secret_word) == 0:
        return output
    elif len(secret_word) == 1 and secret_word in old_letters_guessed:
        output += secret_word
    elif len(secret_word) == 1 and secret_word not in old_letters_guessed:
        output += '_'
    else:
        for word in secret_word[0:-1]:
            if word in old_letters_guessed:
                output += word.lower() + ' '
            else:
                output += '_ '
        # Avoid appending space after the last character
        if secret_word[-1] in old_letters_guessed:
            output += secret_word[-1] 
        else:
            output += '_'
    return output

def check_valid_input(letter_guessed, old_letters_guessed):
    """
    The func returns true if the letter_guessed string consists of only one character 
    which is an English letter (and not another character), and if it's not in the 
    old_letters_guessed list (i.e. we have not guessed this character before).

    :param letter_guessed: The letter_guessed value
    :param old_letters_guessed: A list that conatins all the of the user's guesses
    :type letter_guessed: string
    :type old_letters_guessed: list
    :return: 
        False in the following cases:
        If the letter_guessed string contains two or more characters
        If the string letter_guessed contains a non-English letter (like: &, *)
        If the letter_guessed is not in the old_letters_guessed list (hasn't been geussed before)
        Else, return True
    :rtype: boolean
    """
    return len(letter_guessed) == 1 and letter_guessed.isalpha() and letter_guessed.lower() not in old_letters_guessed

def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    """
    The func appends a valid guessed letter to the old_letters_guessed list
    If the guessed letter isn't valid, an output will be shown to the user

    :param letter_guessed: The letter_guessed value
    :param old_letters_guessed: A list that conatins all the of the user's guesses
    :type letter_guessed: string
    :type old_letters_guessed: list
    :return: True if the guess letter has been appened to the "old_letters_guessed" list or False
    :rtype: boolean
    """
    if check_valid_input(letter_guessed, old_letters_guessed): # If the guessed letter is valid and hasn't been geussed before
        old_letters_guessed.append(letter_guessed.lower())
        return True
    else:
        print('X')
        """
        If the old_letters_guessed list is not empty:
        Print all of the old guessed words with a sorted manner 
        Separate them with the "->" character
        """
        if old_letters_guessed:
            print(" -> ".join(sorted(old_letters_guessed, key=str.lower)))
        return False


def main():
    # Initiate the lists and variables
    old_letters_guessed = []
    HANGMAN_PHOTOS = get_hangman_mode_photos() # Contains the Hangman's images for every situation
    MAX_TRIES = 6       # Max guesses
    num_of_tries = 0    # Counts the failing guesses of the user
    is_win = False      # Condition if the user won or not
    
    # Print the Welcome Screen
    print(welcome_screen(MAX_TRIES))

    # Get the secret word
    file_path = input("Enter file path: ")
    index = get_index_Value()

    secret_word = choose_word(file_path, index)
    if secret_word == '': # If there's an issue wth the user's file path input
        print("Game is over. Please enter an existing's files path next time\n")
        sys.exit()

    # Print the opening mode to the user
    print(r"Let's start!")
    print(HANGMAN_PHOTOS[num_of_tries])

    # Print the word's underscores to the user
    print(show_hidden_word(secret_word, old_letters_guessed))

    while num_of_tries < MAX_TRIES:
        letter_guessed = input("Guess a letter: ")
        is_right = try_update_letter_guessed(letter_guessed, old_letters_guessed)

        # If the input is valid, print the status of the game
        if(is_right):
            if letter_guessed.lower() not in secret_word:
                num_of_tries += 1
                # Show the status image when not guessing
                show_fail_status(HANGMAN_PHOTOS[num_of_tries]) 
            
            # Show the secret word guess status
            print(show_hidden_word(secret_word, old_letters_guessed)) 
        
            if check_win(secret_word, old_letters_guessed):
                is_win = True
                num_of_tries = MAX_TRIES # To break the while condition
    
    # Output to the user if he won or not
    if is_win:
        print("WIN")
    else:
        print("LOSE")


if __name__ == "__main__":
    main()