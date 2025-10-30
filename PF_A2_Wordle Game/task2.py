#Wordle Game - 09/01/2025

##Modules##

import time
import random

##Own Files##

dictionary_file = open("dictionary.txt", "r")  #open and read the dictionary file
dictionary_file_lines = dictionary_file.readlines()

winners_file = open("winners.txt", "r")  #open and read the dictionary file
winners_file_lines = winners_file.readlines()

winners_append = open("winners.txt", "a")  #open to append the dictionary file

import howToPlay

##Game Variable Initalisation##

length_4_words = []
length_5_words = []
length_6_words = []

init__wordLength = 5
init__difficulty = "Normal  "
init__turns = 6
init__hints = 1
init__turnTime = 30

init__totalSolveTime = 0

blank_top = "╭╌╌╌╮"  #displays blank boxes by line based on the number of letters to guess
blank_mid = "┆ ? ┆"
blank_mid_left = "┆ "
blank_mid_right = " ┆"
blank_bot = "╰╌╌╌╯"
blank_bot_left = "╰ "
blank_bot_right = " ╯"

symbol_rightPos = "*"
symbol_wrongPos = "+"
symbol_notInWord = "−"



###UNIVERSAL - VALIDATIONS###

def validate_input(typeOfValidation, inputToValidate, optionScopeStart, optionScopeEnd):
    """
    > Based on the typeOfValidation passed, the function will return if the input provided is valid or invalid,
      providing an exception string with the error if there is one.
    """
    
    if typeOfValidation == "numOnly":  #checking if input is a whole number
        if inputToValidate.isnumeric(): #checks if the input by the player is a number and only a number
            if (int(inputToValidate) < optionScopeStart) or (int(inputToValidate) > optionScopeEnd): #if the input by the player greater than the option numbers
               
                return False, "Input must be one of the options provided."
            
            else:  #valid

                return True, ""

        else:
            
            return False, "Input must be one of the numerical options provided."
    
    elif typeOfValidation == "alnumOnly":  #checking if input is alphanumeric
        if inputToValidate.isnumeric():  #invalid - can't contain only numbers

            return False, "Input cannot solely contain numbers."
        
        elif inputToValidate.isalnum():  #valid
            if (len(inputToValidate) < optionScopeStart) or (len(inputToValidate) > optionScopeEnd):
                
                return False, ("Input must be between " + str(optionScopeStart) + " and " + str(optionScopeEnd) + " characters long.")
            
            else:
               
                return True, ""
        
        elif inputToValidate.isalpha():  #valid
            if (len(inputToValidate) < optionScopeStart) or (len(inputToValidate) > optionScopeEnd):
                
                return False, ("Input must be between " + str(optionScopeStart) + " and " + str(optionScopeEnd) + " characters long.")
            
            else:
                
                return True, ""
        
        else:

            return False, "Input must contain letters or a mix of letters and numbers."
    
    elif typeOfValidation == "alOnly":  #checking if input is alphabetical
        if inputToValidate.isnumeric():  #invalid - can't contain only numbers

            return False, "Input cannot contain numbers."
        
        elif inputToValidate.isalpha():  #valid
            if (len(inputToValidate) < optionScopeStart) or (len(inputToValidate) > optionScopeEnd):
                
                if optionScopeStart == optionScopeEnd:
                
                    return False, ("Input must be " + str(optionScopeStart) + " characters long.")

                else:

                    return False, ("Input must be between " + str(optionScopeStart) + " and " + str(optionScopeEnd) + " characters long.")
            
            else:
                
                return True, ""
        
        else:

            return False, "Input must only contain letters."
        
    else:

            return False, "Internal Error: validate_input() has not recieved a valid typeOfValidaton"


###UNIVERSAL - OPTION SELECT###

def option_select(optionScopeStart, optionScopeEnd):
    """
    > Takes input from the player, checks if it's a number and in the specified range.
        > If the input is valid then return with the input and no exception string.
    > If the input is not valid the return with the input and an exception string.
    """
    
    option_input = input("")

    if option_input.isnumeric(): #checks if the input by the player is a number and only a number
        if (int(option_input) < optionScopeStart) or (int(option_input) > optionScopeEnd): #if the input by the player greater than the option numbers
            
            return option_input, False, "Input must be one of the options provided."
        
        else:  #valid

            return option_input, True, ""

    else:
        
        return option_input, False, "Input must be one of the numerical options provided."



###DISPLAY GAME SCREEN###

def display_game(numOfLetters, selected_list, hiddenWord, difficultySet, turnsSet, hintsSet, turnTimerSet, totalSolveTimeSet):
    """
    > Initialise lists that will be accessed throughout this particular game.
        > Append correctLetters and lettersNotFound with each letter from the hiddenWord

    Next main fn > refresh()
    """
    
    correctLetters = []
    incorrectLetters = []

    lettersNotFound = []
    lettersFound = []

    hintLetters = []

    for i in hiddenWord:
        if not i.upper() in correctLetters:
            correctLetters.append(i.upper())
            lettersNotFound.append(i.upper())
    
    #print(lettersNotFound, correctLetters)
    
    startGameTimer = time.monotonic()  #get the value of the monotonic clock at the start of the game

    def end_game(won, wonButOutOfTurns, endGameTimer, gaveUp, quitToMenu):
        """
        > Calculate the total time in minutes and seconds the player took to win
        > If the player won.
            > If the player did not run out of turns.
                > If player is not in god mode and their alias is in the winners.txt file, append their name and time if its better than last time.
            > Otherwise tell them they won but took too long.
            > Call wonOptions()
        > Otherwise if they gave up call givenUp_options()
        > Otherwise they must have run out of turns so call end_game() again with specific parameters so only wonOptions() is called.

        Next main fn > choose_word() or main_menu()
        """
        
        totTime = endGameTimer - startGameTimer
        totTime_mins = format(totTime//60, ".0f")
        totTime_seconds = format(totTime%60, '.0f')
        
        if won:
            if not wonButOutOfTurns:
                if not difficultySet == "God Mode":
                    aliasExists = None
                    aliasLine = 0
                    lastWin = ""

                    count = 0

                    for i in open("winners.txt", "r").readlines():
                        if i[:str.rfind(i, " ")] == alias:  #alias exists in the winners.txt file
                            aliasExists = True
                            aliasLine = count
                            lastWin = i[str.find(i, " "):-1].strip("s").strip()  #find the time of their best win
                            
                            break

                        count += 1
                    
                    totTimeRounded = format(totTime, ".0f")
                    #print(int(lastWin), totTimeRounded, type(totTimeRounded))
                    
                    if aliasExists:
                        if int(lastWin) > int(totTimeRounded):  #if the player's last win took more time then rewrite it, otherwise don't append file
                            with open("winners.txt", "r") as file:
                                allLines = file.readlines()
                                
                                if int(totTime_seconds) > 9:  #both the mins and seconds are double digit numbers - so no need to pad with 0s
                                    allLines[aliasLine] = (f"{alias} {totTimeRounded}s")
                                else:
                                    allLines[aliasLine] = (f"{alias} 0{totTimeRounded}s")

                                writeAllLines = open("winners.txt", "w")
                                writeAllLines.writelines(allLines)
                                writeAllLines.close()
                    else:
                        with open("winners.txt", "a") as file:
                            if int(totTime_seconds) > 9:
                                file.writelines(f"\n{alias} {totTimeRounded}s")
                            else:
                                file.writelines(f"\n{alias} 0{totTimeRounded}s")

                            file.close()
                

                print("\n    " + blank_top*numOfLetters, end="\n    ")

                for letter in hiddenWord:
                    print((blank_mid_left + strColour_GREEN + letter.upper() + strColour_DEFAULT + blank_mid_right), end="")

                print("\n    ", end="")

                for letter in hiddenWord:
                    print((blank_bot_left + strColour_GREEN + symbol_rightPos + strColour_DEFAULT + blank_bot_right), end="")

                print("\n")

                if int(totTime_mins) > 9:
                    print(f"\nCORRECT! The word was {strColour_GREEN}{hiddenWord.upper()}{strColour_DEFAULT}!\nYou took a total of {strColour_BLUE}{totTime_mins} minutes{strColour_DEFAULT} and {strColour_BLUE}{totTime_seconds} seconds{strColour_DEFAULT} to find the word.")
                else:
                    if int(totTime_mins) > 1 and int(totTime_mins) < 10:
                        print(f"\nCORRECT! The word was {strColour_GREEN}{hiddenWord.upper()}{strColour_DEFAULT}!\nYou took {strColour_BLUE}{totTime_mins} minutes{strColour_DEFAULT} and {strColour_BLUE}{totTime_seconds} seconds{strColour_DEFAULT} to find the word.")
                    elif int(totTime_mins) == 1:
                        print(f"\nCORRECT! The word was {strColour_GREEN}{hiddenWord.upper()}{strColour_DEFAULT}!\nYou took {strColour_BLUE}{totTime_mins} minute{strColour_DEFAULT} and {strColour_BLUE}{totTime_seconds} seconds{strColour_DEFAULT} to find the word.")
                    else:  #guess only took seconds
                        print(f"\nCORRECT! The word was {strColour_GREEN}{hiddenWord.upper()}{strColour_DEFAULT}!\nYou took {strColour_BLUE}{totTime_seconds} seconds{strColour_DEFAULT} to find the word.")
                
                print("\n > Try Again [1]\n > Quit to Menu [2]\n")
            else:
                print(f"\n{strColour_RED}YOU WON BUT TOOK TOO LONG!{strColour_DEFAULT} The word was indeed {strColour_GREEN}{hiddenWord.upper()}{strColour_DEFAULT} but because you took too long it's not counted as a win...\nSorry about that. Got to play by the rules you know!")
                print("\n > Try Again [1]\n > Quit to Menu [2]\n")
            

            def wonOptions():
                """
                > Allow the player to select from given options using the function option_select()
                > If input is valid then carry out desired operation.

                Next main fn > choose_word() or main_menu()
                """

                option_input, valid, exceptionString = option_select(1, 2)

                if valid:
                    if option_input == "1":
                        
                        choose_word(numOfLetters, difficultySet, turnsSet, hintsSet, turnTimerSet, totalSolveTimeSet)
                        
                    elif option_input == "2":
                        
                        main_menu(True, True, numOfLetters, difficultySet, turnsSet, hintsSet, turnTimerSet, totalSolveTimeSet)

                else:
                    print("\n", exceptionString, " Please try again.\n", sep="")

                    wonOptions()

            wonOptions()

        else:
            if gaveUp:
                print(f"The word was {strColour_MAGENTA}" + hiddenWord + f"{strColour_DEFAULT}!\n")
                
                def givenUp_options():
                    """
                    > Allow the player to select from given options using the function option_select()
                    > If input is valid then carry out desired operation.

                    Next main fn > choose_word() or main_menu()
                    """
                    
                    print("\nWhat would you like to do?\n > Try Again [1]\n > Quit to Menu [2]\n > What kind of a word do you call THAT?! [3]\n")

                    option_input1, valid1, exceptionString1 = option_select(1, 3)

                    if valid1:
                        
                        if option_input1 == "1":
                            
                            choose_word(numOfLetters, difficultySet, turnsSet, hintsSet, turnTimerSet, totalSolveTimeSet)
                        
                        elif option_input1 == "2":
                            
                            main_menu(True, True, numOfLetters, difficultySet, turnsSet, hintsSet, turnTimerSet, totalSolveTimeSet)

                        elif option_input1 == "3":
                            randomNum = random.randrange(1, 5)
                            
                            if randomNum == 1:
                                print("\nSorry! I don't exactly choose the words...")
                            if randomNum == 2:
                                print("\nI KNOW RIGHT? I guess that's just your luck...")
                            if randomNum == 3:
                                print("\nSome of them are, odd. Yes I am aware. Sorry, but I'm given the chosen word at random... As us programs say: not my module, not my problem!")
                            if randomNum == 4:
                                print("\nAPOLOGIES! At least I don't give you words like \"you've\" and \"can't\" - my creator got one of those once, hence why you don't get them now...")

                            givenUp_options()
                    
                    else:
                        print("\n", exceptionString1, " Please try again.\n", sep="")

                        givenUp_options()


                givenUp_options()
               
            elif quitToMenu:
                
                main_menu(True, True, numOfLetters, difficultySet, turnsSet, hintsSet, turnTimerSet, totalSolveTimeSet)

            else:  #run out of turns
                
                if int(totTime_mins) > 1:
                    print(f"\nOh no you\'ve run out of turns! You took {strColour_BLUE}{totTime_mins} minutes{strColour_DEFAULT} and {strColour_BLUE}{totTime_seconds} seconds{strColour_DEFAULT} trying to find the hidden word.")
                elif int(totTime_mins) == 1:
                    print(f"\nOh no you\'ve run out of turns! You took {strColour_BLUE}{totTime_mins} minute{strColour_DEFAULT} and {strColour_BLUE}{totTime_seconds} seconds{strColour_DEFAULT} trying to find the hidden word.")
                else:
                    print(f"\nOh no you\'ve run out of turns! You took {strColour_BLUE}{totTime_seconds} seconds{strColour_DEFAULT} trying to find the hidden word.")
                
                end_game(False, False, endGameTimer, True, False)


    def refresh(useDisplayOptions, useDisplayUpdateTiles, turnsUpdated, hintsUpdated, turnTimer, continueTimer, wordGuessed, correctLetters, incorrectLetters, won):
        """
        > Uses global variable midGameTimer and sets it to the value of the monotonic clock when the turn starts
        > If the player has not already won and they still have turns left then...
            > Display necessary game elements (based on passed arguments)
            > Allow the player to guess a word
            > If the guess is a number:
                > If it is a valid number command (1,2,3 or 4) then carry out the operation of the input command (such as show hint etc.)
                > Otherwise ask the player to guess again
            > Otherwise check if input is only alphabetical with validate_input()
                > If the player has more than 0 turns left
                    > If the guess is the hidden word
                        > Call end_game()
                        > Otherwise tell the player they took too long and lost instead
                    > If the guess is not the hidden word
                        > If the player is in hard mode then don't accept guesses not containing already found letters
                        > If the player is in relaxed mode don't use any timers to remove an extra turn
                        > If the player is not in hard or relaxed mode then use the timer

                        > Refresh with the guessed word being printed in the display_updateTiles() and the correct ammount of turns
                > Otherwise call function end_game() with the ran out of time parameters
    
        Next main fn > end_game()
        """
        global midGameTimer
        
        if not continueTimer:
            midGameTimer = time.monotonic()  #get the value of the monotonic clock at the start of each turn

        if not won:
            
            def display_options():
                """
                > At the start of the game this function will be called to print the possible options the player has during the game
                """

                if difficultySet == "God Mode":
                    print(
                        f"\nOptions:\n⎺⎺⎺⎺⎺⎺⎺⎺\n > Use Hint {strColour_YELLOW}[1]{strColour_DEFAULT}       > Give Up {strColour_MAGENTA}[3]{strColour_DEFAULT}\n",
                        f"> Vocab Help {strColour_BLUE}[2]{strColour_DEFAULT}     > Quit to Menu [4]\n\n",
                        "Difficulty: " + strColour_MAGENTA + difficultySet + strColour_DEFAULT + "\n"*2,
                        "Guess the", numOfLetters, "letter word:\n\n",
                    )
                else:
                    print(
                        f"\nOptions:\n⎺⎺⎺⎺⎺⎺⎺⎺\n > Use Hint {strColour_YELLOW}[1]{strColour_DEFAULT}       > Give Up {strColour_MAGENTA}[3]{strColour_DEFAULT}\n",
                        f"> Vocab Help {strColour_BLUE}[2]{strColour_DEFAULT}     > Quit to Menu [4]\n\n",
                        "Difficulty: " + strColour_BLUE + difficultySet + strColour_DEFAULT + "\n"*2,
                        "Guess the", numOfLetters, "letter word:\n\n",
                    )
                
                return


            def display_updateTiles(turnsSetNew, hintsSetNew):
                """
                > If the word guessed is in the English dictionary.
                    > Initialise and append the needed lists with the player's guess or hidden word.
                    > Depending on how many repeating letters there are in the player's guess compared to the hidden word:
                        > Go through the letters in the guessed word, change the flag lists int of times the same letter apears in both 
                          the hiddenWord and guess to the timesToColourLetter.
                            > If the letter is in the correct position in the guess and hiddenWord then change the flag lists int of times letter 
                              in guess is in correct position.
                        > Again for the letters in the guessed word, based on the flag lists print the letters in the tiles with their correct colours.
                        > Same as above but for the symbols _ + *.
                        (See in-line comments on the letter colouring (as the symbols are the same) for more detail)
                
                > If word is not in the english dictionary then print the guessed word in red in the tiles.
                > Print the rest of the display and incorrect letters list.
                """

                if difficultySet == "God Mode":
                    print(f"\n Hidden word = {strColour_MAGENTA}{hiddenWord}{strColour_DEFAULT}\n")

                if not len(incorrectLetters) < 1:
                    
                    incorrectLetters.sort()

                print("\n    " + blank_top*numOfLetters + "\t"*2 + f"Turns Left: " + strColour_RED + "♡ "*turnsSetNew + strColour_DEFAULT, end="\n    ")
                
                if (wordGuessed in selected_list) or wordGuessed == "?"*numOfLetters:  #wordGuessed is in the list created from the dictionary file
                    wordLetters = []
                    wordGuessedLetters = []
                    wordGuessedLettersNoRepeats = []

                    flagsLetters = []  #[[letter as str, num of times same letter apears in both hiddenWord and guess, num of times letter in guess is in correct position],[...]]
                    flagsSymbols = []

                    for letter in wordGuessed:
                        wordGuessedLetters.append(letter)

                        if not letter in wordGuessedLettersNoRepeats:
                            wordGuessedLettersNoRepeats.append(letter)
                            flagsLetters.append([letter, 0, 0])
                            flagsSymbols.append([letter, 0, 0])

                    for letter in hiddenWord:
                        wordLetters.append(letter)

                    count = 0

                    for letter in wordGuessed:
                        if letter in hiddenWord:
                            differenceOfRepeats = wordGuessedLetters.count(letter) - wordLetters.count(letter)
                            timesToColourLetter = wordGuessedLetters.count(letter) - differenceOfRepeats
                            
                            #print("for the word", hiddenWord, "letter", letter, "will be colored this many times:", timesToColourLetter)
                            
                            flagsLetters[wordGuessedLettersNoRepeats.index(letter)][1] = timesToColourLetter
                            flagsSymbols[wordGuessedLettersNoRepeats.index(letter)][1] = timesToColourLetter
                            
                            if letter == hiddenWord[count]:
                                flagsLetters[wordGuessedLettersNoRepeats.index(letter)][2] += 1
                                flagsSymbols[wordGuessedLettersNoRepeats.index(letter)][2] += 1

                        count += 1
                    
                    #print(flagsLetters, flagsSymbols, sep="\n")


                    ##Letters - printed line 2##
                    
                    countLetters = 0
                    
                    for letter in wordGuessed:  #for loop is used for colouring the letters whether or not they are in the correct pos, wrong pos or not in the hiddenWord
                        if letter in hiddenWord:
                            differenceOfRepeats = wordGuessedLetters.count(letter) - wordLetters.count(letter)
                            timesToColourLetter = wordGuessedLetters.count(letter) - differenceOfRepeats
                            
                            if letter == hiddenWord[countLetters]:  #* if the current index letter in the player's guess is equal to the letter in the same position of the correct hiddenWord
                                print((blank_mid_left + strColour_GREEN + letter.upper() + strColour_DEFAULT + blank_mid_right), end="")
                                
                                flagsLetters[wordGuessedLettersNoRepeats.index(letter)][1] -= 1
                                #print(flagsLetters, end="  ")
                            else:
                            
                                if flagsLetters[wordGuessedLettersNoRepeats.index(letter)][1] == 1:
                                    if timesToColourLetter == flagsLetters[wordGuessedLettersNoRepeats.index(letter)][2]:  #_ or + depending if the guessed repeated letters are both in correct pos **
                                        print((blank_mid_left + strColour_RED + letter.upper() + strColour_DEFAULT + blank_mid_right), end="")
                                    else:
                                        print((blank_mid_left + strColour_YELLOW + letter.upper() + strColour_DEFAULT + blank_mid_right), end="")
                                        
                                        flagsLetters[wordGuessedLettersNoRepeats.index(letter)][1] -= 1
                                
                                elif flagsLetters[wordGuessedLettersNoRepeats.index(letter)][1] > 1:  #_ or + depending if there is a correct letter but not yet printed
                                    if timesToColourLetter == flagsLetters[wordGuessedLettersNoRepeats.index(letter)][2]:
                                        print((blank_mid_left + strColour_RED + letter.upper() + strColour_DEFAULT + blank_mid_right), end="")
                                    else:
                                        if flagsLetters[wordGuessedLettersNoRepeats.index(letter)][2] >= 1 or flagsLetters[wordGuessedLettersNoRepeats.index(letter)][2] == 0:
                                            print((blank_mid_left + strColour_YELLOW + letter.upper() + strColour_DEFAULT + blank_mid_right), end="")
                                            
                                            flagsLetters[wordGuessedLettersNoRepeats.index(letter)][1] -= 1
                                        
                                        else:
                                            print((blank_mid_left + strColour_RED + letter.upper() + strColour_DEFAULT + blank_mid_right), end="")

                                elif flagsLetters[wordGuessedLettersNoRepeats.index(letter)][1] == 0:
                                    print((blank_mid_left + strColour_RED + letter.upper() + strColour_DEFAULT + blank_mid_right), end="")
                                
                        else:  #_ not in hiddenWord
                            print((blank_mid_left + strColour_RED + letter.upper() + strColour_DEFAULT + blank_mid_right), end="")
                        
                        countLetters += 1

                    ##

                    print("\t"*2 + f"Time for Current Turn: {str(turnTimerSet)}s", end="\n    ")
                    
                    ##Symbols - printed line 3##
                    
                    countSymbols = 0

                    for letter in wordGuessed:  #for loop is the same as above but uses symbols
                        if letter in hiddenWord:
                            differenceOfRepeats = wordGuessedLetters.count(letter) - wordLetters.count(letter)
                            timesToColourLetter = wordGuessedLetters.count(letter) - differenceOfRepeats
                            
                            if letter == hiddenWord[countSymbols]:
                                print((blank_bot_left + strColour_GREEN + symbol_rightPos + strColour_DEFAULT + blank_bot_right), end="")
                                
                                flagsLetters[wordGuessedLettersNoRepeats.index(letter)][1] -= 1
                            else:
                            
                                if flagsSymbols[wordGuessedLettersNoRepeats.index(letter)][1] == 1:
                                    if timesToColourLetter == flagsSymbols[wordGuessedLettersNoRepeats.index(letter)][2]:
                                        print((blank_bot_left + strColour_RED + symbol_notInWord + strColour_DEFAULT + blank_bot_right), end="")
                                    else:
                                        print((blank_bot_left + strColour_YELLOW + symbol_wrongPos + strColour_DEFAULT + blank_bot_right), end="")
                                        
                                        flagsSymbols[wordGuessedLettersNoRepeats.index(letter)][1] -= 1
                                
                                elif flagsSymbols[wordGuessedLettersNoRepeats.index(letter)][1] > 1:
                                    if timesToColourLetter == flagsSymbols[wordGuessedLettersNoRepeats.index(letter)][2]:
                                        print((blank_bot_left + strColour_RED + symbol_notInWord + strColour_DEFAULT + blank_bot_right), end="")
                                    else:
                                        if flagsSymbols[wordGuessedLettersNoRepeats.index(letter)][2] >= 1 or flagsSymbols[wordGuessedLettersNoRepeats.index(letter)][2] == 0:
                                            print((blank_bot_left + strColour_YELLOW + symbol_wrongPos + strColour_DEFAULT + blank_bot_right), end="")
                                            
                                            flagsSymbols[wordGuessedLettersNoRepeats.index(letter)][1] -= 1
                                        
                                        else:
                                            print((blank_bot_left + strColour_RED + symbol_notInWord + strColour_DEFAULT + blank_bot_right), end="")

                                elif flagsSymbols[wordGuessedLettersNoRepeats.index(letter)][1] == 0:
                                    print((blank_bot_left + strColour_RED + symbol_notInWord + strColour_DEFAULT + blank_bot_right), end="")
                                
                        else:
                            print((blank_bot_left + strColour_RED + symbol_notInWord + strColour_DEFAULT + blank_bot_right), end="")
                        
                        countSymbols += 1

                    ##
                    incorrectLettersJoined = " ".join(incorrectLetters)

                    print(
                        "\t"*2 + f"Hints Left: {strColour_YELLOW}" + str(hintsSetNew) + f"{strColour_DEFAULT}  | Use {strColour_YELLOW}[1]{strColour_DEFAULT}",
                        "\n    " + "     "*numOfLetters + "\t"*2 + f"Incorrect Letters: {strColour_GRAY}{incorrectLettersJoined}{strColour_DEFAULT}\n",
                        "\n    " + "     "*numOfLetters + "\t"*2 + f"Vocab Help [2]  Give Up {strColour_MAGENTA}[3]{strColour_DEFAULT}"
                    )
                    
                else:
                    incorrectLettersJoined = " ".join(incorrectLetters)

                    for i in wordGuessed:
                        print((blank_mid_left + strColour_RED + i.upper() + strColour_DEFAULT + blank_mid_right), end="")

                    print(
                        "\t"*2 + f"Time for Current Turn: {str(turnTimerSet)}s",
                        "\n    " + blank_bot*numOfLetters + "\t"*2 + f"Hints Left: {strColour_YELLOW}" + str(hintsSetNew) + f"{strColour_DEFAULT}  | Use {strColour_YELLOW}[1]{strColour_DEFAULT}",
                        "\n    " + "     "*numOfLetters + "\t"*2 + f"Incorrect Letters: {strColour_GRAY}{" ".join(incorrectLetters)}{strColour_DEFAULT}\n",
                        "\n    " + "     "*numOfLetters + "\t"*2 + f"Vocab Help [2]  Give Up {strColour_MAGENTA}[3]{strColour_DEFAULT}"
                    )

            ####

            if turnsUpdated > 0:

                if useDisplayOptions:
                    
                    display_options()
                    display_updateTiles(turnsUpdated, hintsUpdated)
                

                if useDisplayUpdateTiles:
                    
                    display_updateTiles(turnsUpdated, hintsUpdated)
                

                playerGuess = None

                print(" > Your Guess ✎  ", end="")

                playerGuess = input("")

                optionScopeStart = 1
                optionScopeEnd = 4

                playerGuess = playerGuess.lower()  #change answer to lowercase to match the dictionary file's words
            
                if playerGuess.isnumeric():
                    
                    if (int(playerGuess) < optionScopeStart) or (int(playerGuess) > optionScopeEnd):
                        
                        print("\nInput must be a guess or a numerical option as provided. Please try again.\n")
                        
                        refresh(False, False, turnsUpdated, hintsUpdated, turnTimer, True, playerGuess, correctLetters, incorrectLetters, False)
                                
                    else:  #valid
                        if playerGuess == "1":
                            if hintsUpdated > 0:
                                print(f"You have used {strColour_YELLOW}1{strColour_DEFAULT} hint:\n")
                                
                                if len(lettersNotFound) == 0:
                                    print("Looks like you have found all the letters in the hidden word so I can't help you...\n")
                                    
                                    hintsUpdatedNew = hintsUpdated - 1

                                    refresh(False, False, turnsUpdated, hintsUpdatedNew, turnTimer, False, playerGuess, correctLetters, incorrectLetters, False)

                                else:
                                    if not len(lettersNotFound) == 0:
                                        randNum = random.randrange(0, len(lettersNotFound))
                                        randHintLetter = lettersNotFound[randNum]
                                        
                                        hintLetters.append(randHintLetter)
                                        lettersNotFound.pop(randNum)  #stops the same letter being shown as a hint
                                        
                                        print("Here's a letter in the hidden word you have not yet used...")
                                        
                                        print("\n    " + blank_top,
                                            "\n    " + blank_mid_left + strColour_YELLOW + randHintLetter + strColour_DEFAULT + blank_mid_right,
                                            "\n    " + blank_bot + "\n"
                                        )
                                    else:
                                        print("\nSorry that's all I can help you with - you now know all the letters that appear in the hidden word.\n")

                                    hintsUpdatedNew = hintsUpdated - 1
                                    
                                    if (not difficultySet.strip() == "Relaxed") and (not difficultySet.strip() == "Easy"):
                                        if time.monotonic() - midGameTimer > turnTimer:  #if player took longer than the turn timer to make their guess
                                            turnsUpdatedNew = turnsUpdated - 2
                                            print(f"\nOh no, you took longer than {turnTimer}s to guess!\nTurn has been lost {strColour_RED}♡{strColour_DEFAULT} ")
                                        else:
                                            turnsUpdatedNew = turnsUpdated - 1
                                    else:
                                        turnsUpdatedNew = turnsUpdated

                                    refresh(False, False, turnsUpdatedNew, hintsUpdatedNew, turnTimer, False, playerGuess, correctLetters, incorrectLetters, False)
                                    
                            else:
                                print("\nOh no, you have no hints left!\n")
                                
                                refresh(False, False, turnsUpdated, hintsUpdated, turnTimer, True, playerGuess, correctLetters, incorrectLetters, False)
                                
                        elif playerGuess == "2":
                            
                            possibleWords = []
                            wordCount = 1

                            for iteration in range(len(dictionary_file_lines)):
                                if (len(dictionary_file_lines[iteration]) == numOfLetters +1):#and (dictionary_file_lines[iteration].isalpha()):
                                    wordNoRepeats = []  
                                    matchingLetterCount = 0
                                    incorrectLetterCount = 0

                                    for i in dictionary_file_lines[iteration].strip("\n"):
                                        if not i.upper() in wordNoRepeats and i.isalpha():
                                            wordNoRepeats.append(i.upper())
                                    
                                    for i in range(len(lettersFound)):
                                        if lettersFound[i] in wordNoRepeats:
                                            matchingLetterCount += 1
                                            
                                    for i in range(len(incorrectLetters)):
                                        if incorrectLetters[i] in wordNoRepeats:
                                            incorrectLetterCount += 1
                                    
                                    #print(matchingLetterCount, len(lettersFound))
                                    if (matchingLetterCount == len(lettersFound)) and (not dictionary_file_lines[iteration] in possibleWords) and (not incorrectLetterCount > 0):
                                        possibleWords.append(dictionary_file_lines[iteration])
                                    
                                wordCount += 1
                            
                            print(f"\nThere are {len(possibleWords)} words that could be the answer based on the correct letters gathered:\n")

                            if len(possibleWords) > 10:
                                count = 0
                                
                                for i in range(0, int(len(possibleWords)/10)):
                                    print("".join(possibleWords[count].split("\n")), "".join(possibleWords[count+1].split("\n")), "".join(possibleWords[count+2].split("\n")), 
                                        "".join(possibleWords[count+3].split("\n")), "".join(possibleWords[count+4].split("\n")), "".join(possibleWords[count+5].split("\n")),
                                        "".join(possibleWords[count+6].split("\n")), "".join(possibleWords[count+7].split("\n")), "".join(possibleWords[count+8].split("\n")),
                                        "".join(possibleWords[count+9].split("\n")), sep="\t")
                                    
                                    count += 10
                                
                                if len(possibleWords)%10 != 0:
                                    for i in range(0, len(possibleWords)%10):  #takes care of the remainder words that weren't divided into the 10 columns
                                        print("".join(possibleWords[count+i].split("\n")), end="\t")

                                print("\n")

                            elif len(possibleWords) >= 1:
                                print("".join(possibleWords))

                            refresh(False, False, turnsUpdated, hintsUpdated, turnTimer, False, playerGuess, correctLetters, incorrectLetters, False)
                            
                        elif playerGuess == "3":
                            
                            endGameTimer = time.monotonic()

                            end_game(False, False, endGameTimer, True, False)
                            
                        elif playerGuess == "4":
                            
                            endGameTimer = time.monotonic()

                            end_game(False, False, endGameTimer, False, True)
                            
                else:  #either a guessed hiddenWord or incorrect input
                    
                    valid_validate, exceptionString_validate = validate_input("alOnly", playerGuess, numOfLetters, numOfLetters)
                    
                    if valid_validate:
                        if playerGuess in selected_list:
                            if playerGuess == hiddenWord:
                                ###WON###
                                
                                endGameTimer = time.monotonic()

                                if not difficultySet.strip() == "Relaxed":
                                    if (endGameTimer - midGameTimer > turnTimer) and turnsUpdated == 1:  #if player took longer than the turn timer to make their guess and there was only one life left
                                        print(f"\nOh no, you took longer than {turnTimer}s to guess!\nTurn has been lost {strColour_RED}♡{strColour_DEFAULT} ")
                                        
                                        end_game(True, True, endGameTimer, False, False)
                                    
                                    else:
                                    
                                        end_game(True, False, endGameTimer, False, False)
                                
                                else:

                                    end_game(True, False, endGameTimer, False, False)
                                
                            else:
                                ###Incorrect Guess###
                                
                                for i in playerGuess:
                                    if not difficultySet.strip() == "Hard":
                                        if (not i in hiddenWord) and (not i.upper() in incorrectLetters):
                                            
                                            incorrectLetters.append(i.upper())

                                        elif i in hiddenWord:
                                            if i.upper() in lettersNotFound:
                                                
                                                lettersNotFound.remove(i.upper())
                                            
                                            if not i.upper() in lettersFound:
                                                
                                                lettersFound.append(i.upper())
                                        
                                
                                if difficultySet.strip() == "Hard":
                                    hardModeCount = 0
                                    wordGuessedLettersNoRepeats = []
                                    
                                    for letter in playerGuess:
                                        if not letter.upper() in wordGuessedLettersNoRepeats:
                                            wordGuessedLettersNoRepeats.append(letter.upper())
                                        
                                    for i in "".join(wordGuessedLettersNoRepeats):
                                        if i in lettersFound:
                                            hardModeCount += 1
                                    
                                    if hardModeCount >= len(lettersFound):
                                        
                                        for i in playerGuess:  #must have this here otherwise the lettersFound can be added to before the wordGuessed is checked for use of all correct letters
                                            if (not i in hiddenWord) and (not i.upper() in incorrectLetters):
                                            
                                                incorrectLetters.append(i.upper())

                                            elif i in hiddenWord:
                                                if i.upper() in lettersNotFound:
                                                    
                                                    lettersNotFound.remove(i.upper())
                                                
                                                if not i.upper() in lettersFound:
                                                    
                                                    lettersFound.append(i.upper())

                                        print(hardModeCount, len(lettersFound), wordGuessedLettersNoRepeats)
                                    
                                        turnsUpdatedNew = turnsUpdated - 1

                                        refresh(False, True, turnsUpdatedNew, hintsUpdated, turnTimer, False, playerGuess, correctLetters, incorrectLetters, False)
                                        
                                    else:
                                        print(f"You need to include ALL letters marked with {strColour_GREEN}*{strColour_DEFAULT} and {strColour_YELLOW}+{strColour_DEFAULT}!")
                                        turnsUpdatedNew = turnsUpdated

                                        refresh(False, False, turnsUpdatedNew, hintsUpdated, turnTimer, True, playerGuess, correctLetters, incorrectLetters, False)
                                
                                elif difficultySet.strip() == "Relaxed":
                                    if time.monotonic() - midGameTimer > turnTimer:
                                        turnsUpdatedNew = turnsUpdated - 2
                                        print(f"\nOh no, you took longer than {turnTimer}s to guess!\nTurn has been lost {strColour_RED}♡{strColour_DEFAULT} ")
                                    else:
                                        turnsUpdatedNew = turnsUpdated - 1
                                else:
                                    turnsUpdatedNew = turnsUpdated - 1

                                refresh(False, True, turnsUpdatedNew, hintsUpdated, turnTimer, False, playerGuess, correctLetters, incorrectLetters, False)
                                    
                        else:
                            print(f"\nWord is not in the English dictionary, {strColour_RED}♡{strColour_DEFAULT} current turn has been lost.")
                            
                            if not difficultySet.strip() == "Relaxed": 
                                if time.monotonic() - midGameTimer > turnTimer:
                                    turnsUpdatedNew = turnsUpdated - 2
                                    print(f"\nOh no, you took longer than {turnTimer}s to guess!\nTurn has been lost {strColour_RED}♡{strColour_DEFAULT} ")
                                else:
                                    turnsUpdatedNew = turnsUpdated - 1
                            else:
                                turnsUpdatedNew = turnsUpdated - 1

                            refresh(False, True, turnsUpdatedNew, hintsUpdated, turnTimer, False, playerGuess, correctLetters, incorrectLetters, False)
                            
                    else:
                        print("\n", exceptionString_validate, " Please try again.\n", sep="")
                        
                        refresh(False, False, turnsUpdated, hintsUpdated, turnTimer, True, playerGuess, correctLetters, incorrectLetters, False)
                        
            else:
                
                endGameTimer = time.monotonic()

                end_game(False, False, endGameTimer, False, False)

                return
                                    
    
    refresh(True, False, turnsSet, hintsSet, turnTimerSet, False, ("?"*numOfLetters), correctLetters, incorrectLetters, False)         

        
###CHOOSE WORD###

def choose_word(numOfLetters, difficultySet, turnsSet, hintsSet, turnTimerSet, totalSolveTimeSet):
    """
    > Based on the number of letters chosen to play with, set the contents of the list selected_list to all the words of length selected (length_x_words variables 
    have been set in the fn main()).
    > Choose a random number from 0 to the length of the num of words in selected_list.
    > Hidden word is set as the word at the index of random num chosen in selected_list.
        > If the word is alphabetical then continue, otherwise choose another word by running this fn again (prevents words such as isn't being chosen).

    Next main fn > display_game()
    """
    
    selected_list = []  #used instead of re-writing blocks of code for different length words
    
    if numOfLetters == 4:
        selected_list = length_4_words
    elif numOfLetters == 5:
        selected_list = length_5_words
    elif numOfLetters == 6:
        selected_list = length_6_words
    
    #print(len(selected_list))

    random_number = random.randrange(0, len(selected_list) +1)  #chooses a random integer number between 0 and the number of elements in the selected list
    hiddenWord = selected_list[random_number]
    #hiddenWord = "sybil"  #use for testing
    
    #print(random_number, hiddenWord, hintsSet)  #check to see the random number is valid and which word is associated with it

    if hiddenWord.isalpha():  #ensures abbreviations such as "isn't" are NOT selected as the hidden word
        
        display_game(numOfLetters, selected_list, hiddenWord, difficultySet, turnsSet, hintsSet, turnTimerSet, totalSolveTimeSet)  #call display to start the game with the number of letters in the hiddenWord as the argument

    else:
        
        choose_word(numOfLetters, difficultySet, turnsSet, hintsSet, turnTimerSet, totalSolveTimeSet)

    

###///MENU OPTIONS///###

###SET WORD LENGTH###

def menu_setWordLength(wordLengthSet, difficultySet, turnsSet, hintsSet, turnTimerSet, totalSolveTimeSet):
    """
    > Prompt the player to choose a word length of either 4, 5 or 6.
        > If the difficulty chosen previously means num of hints = word length, then update accordingly for the main menu display.

    Next fn > main_menu()
    """
    
    player_word_length = input("\n > Enter a word length [4, 5 or 6]: ")

    valid, exceptionString = validate_input("numOnly", player_word_length, 4, 6)

    if valid:
        if difficultySet.strip() == "Relaxed" or difficultySet == "God Mode".strip():
            hintsSetNew = int(player_word_length)
        else:
            hintsSetNew = hintsSet

        main_menu(True, True, player_word_length, difficultySet, turnsSet, hintsSetNew, turnTimerSet, totalSolveTimeSet)  #call main_menu again with the updated word length

    else:
        print("\nCurrently the only lengths supported are 4, 5 and 6! Please try again.")

        menu_setWordLength(wordLengthSet, difficultySet, turnsSet, hintsSet, turnTimerSet, totalSolveTimeSet)
    

###SET DIFFICULTY###

def menu_setDifficulty(initialDisplay, wordLengthSet, difficultySet, turnsSet, hintsSet, turnTimerSet, totalSolveTimeSet):
    """
    > If not already displayed the options, print the difficulties that can be chosen from.
        > Set the difficulty, turns, hints and turn time based on the difficulty chosen.

    Next fn > main_menu()
    """

    if initialDisplay:  
        print(f"\nSet the difficulty of the game:\n > Relaxed [1]\n > Easy [2]\n > Normal [3]\n > Hard [4]\n {strColour_MAGENTA}> You Know the Word Mode (God Mode) [5]{strColour_DEFAULT}\n")

    option_select_difficulty, valid, exceptionString = option_select(1, 5)

    if valid:
        if option_select_difficulty == "1":
            player_difficulty = "Relaxed "
            player_turns = "12"
            player_hints = wordLengthSet
            player_turnTime = "∞ "

            main_menu(True, True, wordLengthSet, player_difficulty, player_turns, player_hints, player_turnTime, totalSolveTimeSet)
        
        elif option_select_difficulty == "2":
            player_difficulty = "Easy    "
            player_turns = "6 "
            player_hints = 3
            player_turnTime = 45

            main_menu(True, True, wordLengthSet, player_difficulty, player_turns, player_hints, player_turnTime, totalSolveTimeSet)
            
        elif option_select_difficulty == "3":
            player_difficulty = "Normal  "
            player_turns = "6 "
            player_hints = 1
            player_turnTime = 30

            main_menu(True, True, wordLengthSet, player_difficulty, player_turns, player_hints, player_turnTime, totalSolveTimeSet)
        
        elif option_select_difficulty == "4":
            player_difficulty = "Hard    "
            player_turns = "6 "
            player_hints = 1
            player_turnTime = 25

            main_menu(True, True, wordLengthSet, player_difficulty, player_turns, player_hints, player_turnTime, totalSolveTimeSet)
        
        elif option_select_difficulty == "5":
            player_difficulty = "God Mode"
            player_turns = "12"
            player_hints = wordLengthSet
            player_turnTime = 10

            main_menu(True, True, wordLengthSet, player_difficulty, player_turns, player_hints, player_turnTime, totalSolveTimeSet)

    else:
        print("\n", exceptionString, " Please try again.\n", sep="")

        menu_setDifficulty(False, wordLengthSet, difficultySet, turnsSet, hintsSet, turnTimerSet, totalSolveTimeSet)


###HOW TO PLAY###

def menu_howToPlay(initialDisplay, wordLengthSet, difficultySet, turnsSet, hintsSet, turnTimerSet, totalSolveTimeSet):
    """
    > If not already displayed the content of howToPlay.py then print howToPlay.howToPlay.
        > Prompt a return to the main menu display.

    Next fn > main_menu()
    """

    if initialDisplay:
        if strColour_DEFAULT == "":
            print(howToPlay.howToPlay)
        else:
            print(howToPlay.howToPlay_ColourDisplay)

        print("\nOptions:\n⎺⎺⎺⎺⎺⎺⎺⎺\n > Return to Menu  [1]\n")

    option_input, valid, exceptionString = option_select(1, 1)

    if valid:
        
        main_menu(True, True, wordLengthSet, difficultySet, turnsSet, hintsSet, turnTimerSet, totalSolveTimeSet)

    else:
        print("\n", exceptionString, " Please try again.\n", sep="")

        menu_howToPlay(False, wordLengthSet, difficultySet, turnsSet, hintsSet, turnTimerSet, totalSolveTimeSet)


###SHOW WINNERS###

def menu_showWinners(initialDisplay, wordLengthSet, difficultySet, turnsSet, hintsSet, turnTimerSet, totalSolveTimeSet):
    """
    > If not already displayed the content of winners.txt files then print contents of winners.txt file in ascending order based on the time scores.
        > Prompt a return to the main menu display.

    Next fn > main_menu()
    """

    if initialDisplay:

        print("\nTOP SCORES:\n⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺")

        with open("winners.txt", "r") as file:
            lines = [line.rstrip() for line in file.readlines()]  #make a list containing the lines of winners.txt

        lines = [chars.split() for chars in lines]  #for each line split into name and score
        lines.sort(key=lambda chars:chars[1])  #sort based on the second element (at index 1) in the list

        lines = [" ".join(chars) for chars in lines]  #join the names and scores

        print("\n".join(lines) + "\n\nOptions:\n⎺⎺⎺⎺⎺⎺⎺⎺\n > Return to Menu  [1]\n")  #print the contents of the lines list joined with escape char \n to separate onto a new line each time

    option_input, valid, exceptionString = option_select(1, 1)

    if valid:
        
        main_menu(True, True, wordLengthSet, difficultySet, turnsSet, hintsSet, turnTimerSet, totalSolveTimeSet)

    else:
        print("\n", exceptionString, " Please try again.\n", sep="")

        menu_showWinners(False, wordLengthSet, difficultySet, turnsSet, hintsSet, turnTimerSet, totalSolveTimeSet)



###///ALIAS AND MAIN MENU///###

###SET ALIAS###

def set_session_alias():
    """
    > Tells the player to set an alias.
        > If alias is 3-20 characters and is alphanumeric check if alias exists in the winners.txt file.
            >  If alias does not exist ask to confirm and welcome the player to the game.
            >  If alias exists ask if they wish to continue as that alias, then welcome the player back.
    
    Next fn > main_menu()
    """
    
    global alias

    alias = input("\n > Enter your alias ✎  ")

    valid, exceptionString = validate_input("alnumOnly", alias, 3, 20)  #3 = min num of chars, 20 = max

    if valid:
        aliasExists = False
        lastWin = ""
        
        count = 0

        for i in winners_file_lines:
            if i[:str.find(i, " ")] == alias:  #alias exists in the winners.txt file
                aliasExists = True
                lastWin = i[str.find(i, " "):-1].strip("s").strip()

                break

            count += 1
        
        if not aliasExists:

            print(f"\nAre you sure you want your alias to be set as {strColour_BLUE}" + alias + f"{strColour_DEFAULT}?\n > Yes [1]\n > No [2]\n")

            option_input1, valid1, exceptionString1 = option_select(1, 2)

            if valid1:
                if option_input1 == "1":
                    alias = alias

                    print(f"\nYour alias for this session has been successfully set as {strColour_BLUE}" + alias + f"{strColour_DEFAULT}.",
                        f"Looks like you're new here {strColour_BLUE}" + alias + f"{strColour_DEFAULT}!\n > Enter [4] to learn how to play.")

                    main_menu(True, True, init__wordLength, init__difficulty, init__turns, init__hints, init__turnTime, init__totalSolveTime)

                elif option_input1 == "2":

                    set_session_alias()
            else:
                print("\n", exceptionString1, " Please try again.\n", sep="")

                set_session_alias()
            
        else:
            print(f"\n{strColour_RED}This alias already exists!{strColour_DEFAULT} You can either continue as this alias or make a new one.\n\n > Continue [1]\n > Create New [2]\n")
            
            option_input2, valid2, exceptionString2 = option_select(1, 2)

            if valid2:
                if option_input2 == "1":
                    print(f"\nGood to see you again {strColour_BLUE}" + alias + f"{strColour_DEFAULT}! Ready to beat that high score of {strColour_BLUE}{lastWin}s{strColour_DEFAULT}?")

                    main_menu(True, True, init__wordLength, init__difficulty, init__turns, init__hints, init__turnTime, init__totalSolveTime)

                elif option_input2 == "2":
                    
                    set_session_alias()
                    
            else:
                print("\n", exceptionString2, " Please try again.\n", sep="")

                set_session_alias()
        
    else:
        print("\n", exceptionString, " Please try again.\n", sep="")

        set_session_alias()


###MAIN MENU###

def main_menu(aliasSet, printMenu, wordLengthSet, difficultySet, turnsSet, hintsSet, turnTimerSet, totalSolveTimeSet):
    """
    > Prompts the player to set an alias.
        > When alias is set print the current game display and options.
        > Allow the player to select one of the options by calling option_select()
    
    Next main fn > choose_word()
    """

    if not aliasSet:  #if alias is not yet set:
        
        set_session_alias()

    else:  #player has 'logged in' as an alias

        if int(turnsSet) == 6:
            turnsSet = "6 "

        if difficultySet == "God Mode":
            strColour_set = strColour_MAGENTA
        else:
            strColour_set = strColour_BLUE

        if printMenu:
            print(
                """
┆ Current Game:
┆ ⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺
┆   ╔═════════════════════════════════════════╗
┆   ║ Difficulty: {}                    ║
┆   ║ Word Length: {}                          ║
┆   ║ Turns: {}                               ║
┆   ║ Hints: {}                                ║
┆   ║ Time per Turn (s): {}                   ║
┆   ╚═════════════════════════════════════════╝
┆   
┆ Options:
┆ ⎺⎺⎺⎺⎺⎺⎺⎺
┆  > Play ⏵ [1]
┆
┆  > Set Word Length [2]
┆  > Set Difficulty [3]
┆ 
┆  > How to Play Wordle [4]
┆  > Show Winners [5]
                """.format((strColour_set + difficultySet + strColour_DEFAULT),
                           (strColour_BLUE + str(wordLengthSet) + strColour_DEFAULT),
                           (strColour_RED + str(turnsSet) + strColour_DEFAULT),
                           (strColour_YELLOW + str(hintsSet) + strColour_DEFAULT),
                           str(turnTimerSet))
                )

        ##Option Select##

        option_input, valid, exceptionString = option_select(1, 5)

        if valid:
            if option_input == "1":
                
                choose_word(int(wordLengthSet), difficultySet, int(turnsSet), hintsSet, turnTimerSet, totalSolveTimeSet)
                
            elif option_input == "2":
                
                menu_setWordLength(wordLengthSet, difficultySet, turnsSet, hintsSet, turnTimerSet, totalSolveTimeSet)

            elif option_input == "3":

                menu_setDifficulty(True, wordLengthSet, difficultySet, turnsSet, hintsSet, turnTimerSet, totalSolveTimeSet)

            elif option_input == "4":
                
                menu_howToPlay(True, wordLengthSet, difficultySet, turnsSet, hintsSet, turnTimerSet, totalSolveTimeSet)
                
            elif option_input == "5":
                
                menu_showWinners(True, wordLengthSet, difficultySet, turnsSet, hintsSet, turnTimerSet, totalSolveTimeSet)

        else:
            print("\n", exceptionString, " Please try again.\n", sep="")

            main_menu(aliasSet, False, wordLengthSet, difficultySet, turnsSet, hintsSet, turnTimerSet, totalSolveTimeSet)



###///START OF GAME///###

###WELCOME###

def display_welcome():
    """
    > Print the welcome display.
    
    Next fn > main_menu()
    """

    print(
    """
             Welcome to           
 ╔═══╗ ╔═══╗ ╔═══╗ ╔═══╗ ╔═══╗ ╔═══╗
 ║ W ║ ║ O ║ ║ R ║ ║ D ║ ║ L ║ ║ E ║ 
 ╚═══╝ ╚═══╝ ╚═══╝ ╚═══╝ ╚═══╝ ╚═══╝
 ═══════════════════════════════════""")

    main_menu(False, True, init__wordLength, init__difficulty, init__turns, init__hints, init__turnTime, init__totalSolveTime)  #pass all the changable variables as arguments


###MAIN###

def main():
    """
    > Appends 3 lists with words from the dictionary.txt file with lengths of either 4, 5 or 6.
    > Asks the player if text appears coloured - just incase the escape characters used to colour text in the console aren't printing correctly.
        > Therefore, set the global strColour variables to either their escape characters or to empty strings.
    
    Next fn > display_welcome()
    """

    count_4_letter = 0  #counter that will show how many words have a specific number of letters (for checking purposes)
    count_5_letter = 0  
    count_6_letter = 0
    
    for i in range(len(dictionary_file_lines)):  #append lists for words with different numbers of letters
        if len(dictionary_file_lines[i]) == 4 +1:  #if the length of the current word is equal to 4
            
            length_4_words.append(dictionary_file_lines[i].strip("\n"))  #append the list length_4_words with this word
            
            count_4_letter += 1
        elif len(dictionary_file_lines[i]) == 5 +1:
            
            length_5_words.append(dictionary_file_lines[i].strip("\n"))
            
            count_5_letter += 1
        elif len(dictionary_file_lines[i]) == 6 +1:
            
            length_6_words.append(dictionary_file_lines[i].strip("\n"))
            
            count_6_letter += 1

    strColour_DEFAULT = "\033[37m"
    strColour_GREEN = "\033[32m"
    strColour_YELLOW = "\033[33m"
    strColour_MAGENTA = "\033[35m"
    
    print(f"\n{strColour_MAGENTA}Welcome {strColour_YELLOW}to {strColour_GREEN}Wordle!{strColour_DEFAULT}\n\nDoes the above text appear coloured?\n > Yes [1]  > No [2]\n")  #incase a player's setup isn't compatable with the use of colours in the console
    
    def chooseColourMode():

        global strColour_GRAY
        global strColour_RED
        global strColour_GREEN
        global strColour_YELLOW
        global strColour_BLUE
        global strColour_MAGENTA
        global strColour_SEABLUE

        global strColour_DEFAULT
        
        option_input, valid, exceptionString = option_select(1, 2)

        if valid:
            if option_input == "1":
                strColour_DEFAULT = "\033[37m"
                strColour_GRAY = "\033[30m"
                strColour_RED = "\033[31m"
                strColour_GREEN = "\033[32m"
                strColour_YELLOW = "\033[33m"
                strColour_BLUE = "\033[34m"
                strColour_MAGENTA = "\033[35m"
                strColour_SEABLUE = "\033[36m"

                strColour_DEFAULT = "\033[37m"
                
                display_welcome()
                
            elif option_input == "2":
                strColour_DEFAULT = ""
                strColour_GRAY = ""
                strColour_RED = ""
                strColour_GREEN = ""
                strColour_YELLOW = ""
                strColour_BLUE = ""
                strColour_MAGENTA = ""
                strColour_SEABLUE = ""

                strColour_DEFAULT = ""

                display_welcome()
                
        else:
            print("\n", exceptionString, " Please try again.\n", sep="")

            chooseColourMode()
    

    chooseColourMode()



if __name__ == "__main__":

    main()


"""
LIST
> The script will randomly select one 5 letter word from the
given dictionary (dictionary.txt). This random word is the
answer that the user must find within 6 turns. ###DONE###

> During each turn the user provides a word as a guess. This
must be a real word i.e. a word that exists within the given
dictionary. If the word does not exist, the user gets a warning
and losses a turn. ###DONE###

> After every guess, the code should provide a clue by
assigning the symbols: *, + and _ for each letter of the guess.
The symbol * indicates that the letter is correct and in the
correct position, the symbol + means that the corresponding
letter is in the answer but not in the right position, while the
symbol _ indicates the corresponding letter is not in the
answer at all. The above symbols should be separated by
space when printed at the terminal. For example: if the user
guess is the word: audio, and the provided clue from the
program is _ * _ + _, it means that the letter u is part of the
randomly selected word and at the correct position, the letter i
is also part of the randomly selected word but it is not at the
correct position. The other letters (a,d,o) are not part of the
random word. In this case the correct answer could be the
word: judge ###DONE###

> Multiple instances of the same letter in a guess, such as the
"o"s in "robot", will be assigned a * or + only if the letter also
appears multiple times in the answer; otherwise, all the
repeated letters will be assigned with _. ###DONE###

> The player should have the option to give up at any-time by
ending the game using an appropriate input. In this case, the
randomly selected word should be revealed. ###DONE###

> If the player fails to find the answer within 6 turn or gives up,
they lose the game. If the correct answer is found, they win
the game. In both cases, an appropriate message should be
printed. ###DONE###

Desired Features:

> The code should ask the user at the beginning of the game, to
provide a name or alias and measure the time in seconds that
they needed to solve the puzzle. That info should be stored in
a winners.txt file which has to be updated only after a win.
The user may have the option to see the past winners and
their time (contents of the winners.txt) before the beginning of
a puzzle. ###DONE###

> After each guess from the user, the programme should
provide, in addition to the clue, a list with all the letters that the
user has used but are not part of the correct answer. ###DONE###

> The player is given 30 seconds to make a guess. If they
provide a word after the 30 seconds, their turn is lost. ###DONE###

> Any erroneous input from the players should be handled
appropriately and not result to crashing or unhandled
exceptions. ###DONE###

Advanced Features:

> The player can select to play with a four, five or six letter word
and they also have the option of a hard mode for each. The
hard mode requires players to include letters marked as * and
+ in subsequent guesses. ###DONE###

> The player has the option to use a hint only once. This hint
will provide a letter that is part of the answer but will not 
provide its location. The player loses one turn when using the
hint ###DONE###

> The player can ask for help with the vocabulary. This will
provide all the words in the dictionary that are tentative
solutions and satisfy the clues that have been provided so far
during the game. ###DONE###
"""
