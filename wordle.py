from random import choice
import os
import wordle_dictionary
from colorama import Back, Style


def find_all_indexes(string, char):
    indexes = []
    try:
        index = string.index(char)
        while True:
            indexes.append(index)
            index = string.index(char, index + 1)
    except ValueError:
        pass
    return indexes

#clears terminal to make game clearer
def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

#The game function
def play_wordle():
    #Give the player 6 lives or guesses
    lives = 6
    #win is returned to the main() to keep track of the overall wins or losses.
    win = False
    #Message that stores info to display from previous guess (such as incorrect input)
    message = ''
    error = ''
    #List of previous guesses used to stop user repeating the same guess
    previous_guesses = []

    prompt_add_word = ''


    #Chooses a random word from the list
    wordle_word = choice(wordle_dictionary.words)
    wordle_word = wordle_word.upper()

    
    while lives > 0:
        #Clears terminal to improve readability. Previous guesses are stored and redisplayed.
        clear()

        print(error)
        
        print(f'Guesses remaining: {lives}')
        print(message)
    
        player_word_input = input("\nGuess a five letter word\n")
        player_word = player_word_input.strip().upper()

        if len(player_word) != 5:
            error = '\nYour guess must be a FIVE-letter word. Please guess again.\n'
            continue
        #elif player_word.lower() not in wordle_dictionary.words:
        #    error = '\nYour guess is not in our dictionary. Please guess again.\n'
        #    prompt_add_word = f'Should the {player_word} be added to the dictionary? Y ? N'
        #    continue
        elif player_word in previous_guesses:
            error = f'\nYou have already guessed {player_word.upper()}. Please guess again.\n'
            continue
        
        previous_guesses.append(player_word)
        

        prompt_add_word = ''
        coloured_output = '    '

        matching_swapped_player_word = player_word

        matching_swapped_wordle_word = wordle_word
        correct_letter_index = []
        for index, char in enumerate(wordle_word):
            if char == player_word[index]:
                correct_letter_index.append(index)
                matching_swapped_player_word = matching_swapped_player_word[:index] + '£' + matching_swapped_player_word[index+1:]
                #matching_swapped_wordle_word = matching_swapped_wordle_word[:index] + '$' + matching_swapped_wordle_word[index+1:]
        
        #print('===========================================')
        #print(f'Edited Wordle Word:{matching_swapped_wordle_word}')
        #print(f'Edited Player Word:{matching_swapped_player_word}')
        #print(f'Correct letter index:{correct_letter_index}')
        #print('===========================================')

        wordle_set = set(matching_swapped_wordle_word)
        player_set = set(matching_swapped_player_word)

        common_set = wordle_set & player_set
        common_dictionary_wordle_count = {}
        common_dictionary_player_count = {}

        if len(common_set) != 0:
            for letter in common_set:
                common_dictionary_wordle_count[letter] = matching_swapped_wordle_word.count(letter)
                common_dictionary_player_count[letter] = matching_swapped_player_word.count(letter)

            commons_letter_index = []
            ##commons_letter_wordle_index = []
            #for each common in the player word, if the count in player word is smaller or equal to count in wordle word
            #    swap all letters,
            for key in common_dictionary_player_count.keys():
                if common_dictionary_player_count[key] <= common_dictionary_wordle_count[key]:
                    #print('CDPC LESS than or EQUAL to CDWC')
                    commons_letter_index = commons_letter_index + find_all_indexes(matching_swapped_player_word,key)
                #if count in player word is greater than count in wordle word
                else:
                    #print('CDPC GREATER than to CDWC')
                    commons_letter_index = commons_letter_index + find_all_indexes(matching_swapped_player_word,key)
                    #len(find_all_indexes(matching_swapped_wordle_word,key))
                    while len(commons_letter_index) > common_dictionary_wordle_count[key]:
                        commons_letter_index.pop()
            
            for index in commons_letter_index:
                matching_swapped_player_word = matching_swapped_player_word[:index] + '@' + matching_swapped_player_word[index+1:]
                    
        for i in range(len(wordle_word)):
            if matching_swapped_player_word[i] == '£':
                coloured_output += Back.LIGHTGREEN_EX + player_word[i] + Back.RESET
            elif matching_swapped_player_word[i] == '@':
                coloured_output += Back.LIGHTYELLOW_EX + player_word[i] + Back.RESET
            else:
                coloured_output += Back.LIGHTRED_EX + player_word[i] + Back.RESET

        message += '\n' + coloured_output + '\n'
        print(matching_swapped_player_word)
        if matching_swapped_player_word == '£££££':
            clear()
            print(message)
            win = True
            print('WINNER!!!\n')
            print(f'You guessed {Back.LIGHTGREEN_EX}{wordle_word.upper()}{Back.RESET} correctly!!!')        
            break

        #print('===========================================')
        #print(f'Matching with commons Wordle Word:{matching_swapped_wordle_word}')
        #print(f'Matching with commons Player Word:{matching_swapped_player_word}')
        #print(f'Common letter index:{commons_letter_index}')
        #print(f'Common letter wordle index:{commons_letter_wordle_index}')
        #print('===========================================')
                                   



                    
                
        
        #print(f'Wordle Set:{wordle_set}')
        #print(f'Player Set:{player_set}')
        #print(f'Common Set:{common_set}')
        #print(f'Dictionary Wordle:{common_dictionary_wordle_count}')
        #print(f'Dictionary Player:{common_dictionary_player_count}')
        lives -= 1







            
    #Executes when game is lost after the life loop has been exited, but only is the game is lost.
    if lives == 0:
        clear()
        print(message)
        print(f'\nYou failed to guess {Back.LIGHTRED_EX}{wordle_word.upper()}{Back.RESET} and have lost this round of Wordle!!!\n')
        win = False
    
    #win or loss return bool to main to keep track of score
    return win
    



#Loop that manages whether to initialise the game or not based on the players input
def main():
    #scores[0] is overall wins and scores[1] is overall loses
    scores = [0,0]

    #clear terminal
    clear()

    #Welcome message
    print(f'\nWelcome to a {Back.GREEN}W{Back.YELLOW}o{Back.RED}r{Back.GREEN}d{Back.YELLOW}l{Back.RED}e{Style.RESET_ALL} clone!\n')
    print('The aim of the game is too guess the five letter word by entering\nfive letter words of your own.')

    #Play again loop
    while True:
        #show overall scores if not the first game
        if sum(scores) > 0:
            print(f'The current score is {scores[0]} wins and {scores[1]} losses.')
    
        
        #ask play if they would like to play again and    
        input_play_again = input('\nWould you like to play Wordle? Y or N  ')
        input_play_again_clean = input_play_again.strip().lower()

        #Player would like to play again
        if input_play_again_clean == 'y' or input_play_again_clean == 'yes':
            
            #Run game function
            last_game = play_wordle()

            #keep track of overall score
            if last_game == True: 
                scores[0] += 1 #win
            else: 
                scores[1] += 1 #loss
            continue

                #Player does not want to play again
        elif input_play_again_clean == 'n' or input_play_again_clean == 'no':
            print('\nThank you for playing\n Goodbye!')
            break

        #incorrect input, ask again
        else:
            clear()
            print('\nPlease enter Y(es) or N(o)')
            continue

#Runs the game
if __name__ == '__main__':
    main()