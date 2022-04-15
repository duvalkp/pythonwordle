import os
import random
import pickle
from termcolor import colored

os.system('color')

def load_words():
    words = []
    with open("fivewordslist.txt", "r") as file:
        for line in file:
            words.append(line.strip())
    return words

class game_class:
    def __init__(self, current_word = "", words = load_words(), tries_left = 6, guesses = []):
        self.current_word = current_word
        self.words = words
        self.tries_left = tries_left
        self.guesses = guesses

    def newWord(self):
        self.current_word = random.choice(self.words)

    def expend_try(self):
        self.tries_left -= 1

    def reset_tries(self):
        self.tries_left = 6

    def add_guess(self, guess):
        self.guesses.append(guess)

    def clear_guesses(self):
        self.guesses = []

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def start_new_game():
    clear()
    game.newWord()
    game.reset_tries()
    game.clear_guesses()
    print(f"{game.tries_left} attempts remaining")
    user_in = input("Enter your first guess: ")
    word_guess(user_in.lower())

def word_guess(guess):
    clear()
    if len(guess) != 5:
        print("Your guess must be five letters")
        print(f"{game.tries_left} attempts remaining")
        print_all_guesses()
        user_in = input("")
        word_guess(user_in.lower())
    
    if guess not in game.words:
        print("Guess not in word list")
        print(f"{game.tries_left} attempts remaining")
        print_all_guesses()
        user_in = input()
        word_guess(user_in.lower())

    # game.expend_try()
    # print(f"{game.tries_left} attempts remaining")

    game.add_guess(guess)
    # print_all_guesses()
    print("") #space so the prompt looks better
    if guess.strip() == game.current_word.strip():
        save_stats()
        win()
    else:
        game.expend_try()
        if game.tries_left == 0:
            save_stats()
            lose()
        else:
            print(f"{game.tries_left} attempts remaining")
            print_all_guesses()
            user_in = input("")
            word_guess(user_in)

def win():
    print(f"Correct! The word was {game.current_word}")
    user_in = input("Play another game? (Y/N) ")
    if user_in == "y":
        start_new_game()
    else:
        main_menu()

def lose():
    print(f"No tries left, the word was {game.current_word}")
    user_in = input("Play again? (Y/N)")
    if user_in.lower() == 'y':
        start_new_game()
    else:
        main_menu()

def write_guess_colored(guess):
    pos = 0
    for letter in guess:
        if letter in game.current_word:
            if letter == game.current_word[pos]:
                print(colored(letter.upper(), 'green'), end=" ")
            else:
                print(colored(letter.upper(), 'yellow'), end=" ")
        else:
            print(colored(letter.upper(), 'red'), end=" ")
        pos += 1
    print() #newline

def print_all_guesses():
    # print(f"{game.tries_left - 1} attempts remaining")
    for guess in game.guesses:
        write_guess_colored(guess)

def save_stats():
    with open('player_stats.pkl', 'rb') as f:
        stats = pickle.load(f)

    stats["times_played"] += 1
    if game.tries_left == 6:
        stats["won_on_guesses"]['one'] += 1
    elif game.tries_left == 5:
        stats["won_on_guesses"]['two'] += 1
    elif game.tries_left == 4:
        stats["won_on_guesses"]['three'] += 1
    elif game.tries_left == 3:
        stats["won_on_guesses"]['four'] += 1
    elif game.tries_left == 2:
        stats["won_on_guesses"]['five'] += 1
    elif game.tries_left == 1:
        stats["won_on_guesses"]['six'] += 1

    with open('player_stats.pkl', 'wb') as f:
        pickle.dump(stats, f)

def reset_stats():

    t = input('Are you sure you want to reset your stats? (Y/N)')
    if t.lower() == 'y':
        stats = {
            'times_played' : 0,
            'won_on_guesses' : {
                'one' : 0,
                'two' : 0,
                'three' : 0,
                'four' : 0,
                'five' : 0,
                'six' : 0
            }
        }

        with open('player_stats.pkl', 'wb') as f:
            pickle.dump(stats, f)

        main_menu()

    else:
        main_menu()

def show_stats():
    clear()
    with open('player_stats.pkl', 'rb') as f:
        stats = pickle.load(f)

    wins_totaled = 0
    for x in stats["won_on_guesses"]:
        wins_totaled += stats["won_on_guesses"][x]

    print('Your stats')
    print('')
    print(f'Games played: {stats["times_played"]}')
    if stats['times_played'] == 0:
        print('Win percentage: 0%')
    else:
        print(f'Win percentage: {int((wins_totaled / stats["times_played"]) * 100)}%')
    print('Number of guesses needed:')
    print(f'1 : {stats["won_on_guesses"]["one"]}')
    print(f'2 : {stats["won_on_guesses"]["two"]}')
    print(f'3 : {stats["won_on_guesses"]["three"]}')
    print(f'4 : {stats["won_on_guesses"]["four"]}')
    print(f'5 : {stats["won_on_guesses"]["five"]}')
    print(f'6 : {stats["won_on_guesses"]["six"]}')
    print('Press enter to return to the main menu')
    input()
    main_menu()

def instructions():
    clear()
    print("How to play")
    print("-----------")
    print()
    print("Each time you play, a random five letter word will be generated")
    print()
    print("You have six attempts to guess this word")
    print()
    print("Your guesses have to be real words")
    print()
    print("For each letter in your guess, they will be either red, yellow, or green")
    print()
    print("Red letters mean that the letter is not in the secret word at all")
    print()
    print("Yellow letters mean that the letter is in the word, but it isn't in the right place")
    print()
    print("Green letters mean that the letter is in the word and in the right place")
    print()
    print("Press enter to return to the main menu")
    input()
    main_menu()

def main_menu():
    clear()
    print("Command Line wordle")
    print("-------------------")
    print("Type N to start a new game")
    print("Type H to learn how to play")
    print("Type S for your stats")
    print("Type R to reset your stats")
    print("Type X to exit")
    user_in = input().lower()
    if user_in == 'n':
        start_new_game()
    elif user_in == 'h':
        instructions()
    elif user_in == 's':
        show_stats()
    elif user_in == 'r':
        reset_stats()
    elif user_in == 'x':
        clear()
        exit()
    else:
        main_menu()

game = game_class()

main_menu()