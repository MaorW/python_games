from random import randint
from os.path import exists
import csv

"""
### The "find the treasure" game ###

Code instructions:
Step1:
1. Create a new file or overwrite an existing file
2. The program will create a sequence of [1-20] random numbers between 0 and 9 in ascending order
3. After the last digit (The digit 9), Print the word 'TREASURE'
4. Then, The program will create a sequence of [1-20] random numbers between 0 and 9 in descending order order

Step2:
1. Open that file with ReadOnly permissions and take the cursor to the first character of the file
2. Let the user decide what direction to go  [1- forward 2-backward]
3. Then, the user must decide how many steps to move
4. If the user hits one of the characters 'TREASURE',  print to the user how many times it took to get there
    If not, send a msg to the user that the game continues until the cursor hits one of the 'TREASURE' characters

"""


def create_new_game_files():
    # Create a sequence of [1-20] random numbers between 0 and 9 in ascending order
    the_game_file = open("find_the_treasure_file.txt", 'w')
    for new_chr in range(10):
        for i in range(randint(1, 20)):
            the_game_file.write(str(new_chr))

    the_game_file.write('TREASURE')

    # Create a sequence of [1-20] random numbers between 0 and 9 in descending order
    for new_chr in range(9, 0, -1):
        for i in range(randint(1, 20)):
            the_game_file.write(str(new_chr))
    the_game_file.close()

    # Score csv file - If the file does not exist - Create it
    if not exists('score_file.csv'):
        score_file = open('score_file.csv', 'w', newline='')
        writer = csv.writer(score_file)
        writer.writerow(['Player_name', ' Score'])
        score_file.close()


def get_position(number_of_steps, characters_length):
    if 0 < number_of_steps < characters_length:
        return number_of_steps

    if number_of_steps > characters_length:
        return number_of_steps - characters_length

    if number_of_steps < 0:
        return number_of_steps + characters_length

    if number_of_steps == 0:
        # The first position
        return 1


# The challenge
# If the player guessed under ten guesses, record the name and the score to a CSV file
def challenge(num_of_steps_to_win, total_score_rows):
    # For space
    print()
    player_name = input('Congratulation! You\'ve won the game! \nWhat is your name?  ')
    # Append the new player_name and score values
    with open('score_file.csv', 'a', newline='') as players_file:
        write_payer = csv.writer(players_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        write_payer.writerow([player_name, num_of_steps_to_win])

    # Creating new_scores_table by list
    score_file = open('score_file.csv', 'r+')
    score_list = list(csv.reader(score_file))

    # Sorting the rows by the 'steps_to_win score'
    score_list.sort(key=lambda x: x[1])

    # If there are more than 10 scores - Delete the last row, which is the lower score
    if total_score_rows > 10:
        score_list.pop()
    score_file.close()

    # write the new_scores_table into the score file
    new_scores_table = open('score_file.csv', 'w', newline='')
    with new_scores_table:
        score = csv.writer(new_scores_table)
        score.writerows(score_list)
    new_scores_table.close()


def get_score_file_parameters():
    score_file = open('score_file.csv')
    score_list = list(csv.reader(score_file))
    # First row doesn't count as a score.
    number_of_scores = len(score_list) - 1
    if number_of_scores > 0:
        the_lower_score = score_list[-1]
        highest_steps = int(the_lower_score[1])
    else:
        # If the CSV is empty
        highest_steps = 0
    score_file.close()

    return number_of_scores, highest_steps


# Global env
steps_to_win = 0
position = 0
length_of_characters = 0

print('Welcome to the "find the treasure" game ')
# Step1
create_new_game_files()
num_of_scores, lower_score = get_score_file_parameters()

# Step2
with open("find_the_treasure_file.txt", 'r') as game_file:
    while True:
        direction = input("Where do you want to move? [1- forward 2-backwards] ")

        # If the user didn't use '1' or '2', ask an input again...
        if direction not in '12':
            print("again...")
            continue

        try:
            num_of_steps = int(input("How many characters? "))
        except ValueError:
            # For characters which are not numbers
            print("again...")
            continue

        # For efficiency, if the length is not equal to zero, the variable has been calculated
        if length_of_characters == 0:
            data = game_file.read()
            length_of_characters = len(data)

        if not num_of_steps >= 0:
            print("Pls Write a positive number for the characters' steps")
            continue

        if direction == '1':
            position = get_position(num_of_steps + position, length_of_characters)

        else:  # direction == '2'
            position = get_position((num_of_steps * -1) + position, length_of_characters)

        steps_to_win += 1
        game_file.seek(position)
        current_chr = game_file.readline(1)

        print(f'You hit the character “{current_chr}”. ')
        if current_chr in 'TREASURE':
            break
        else:
            print('… again … until hit one of the “TREASURE” letters…')

print(f'It took you {steps_to_win} steps to get there')

if steps_to_win <= lower_score or num_of_scores <= 10:
    num_of_scores += 1
    challenge(steps_to_win, num_of_scores)

print('Thank you for playing!')
