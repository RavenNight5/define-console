strColour_DEFAULT = "\033[37m"
strColour_GRAY = "\033[30m"
strColour_RED = "\033[31m"
strColour_GREEN = "\033[32m"
strColour_YELLOW = "\033[33m"
strColour_BLUE = "\033[34m"
strColour_MAGENTA = "\033[35m"
strColour_SEABLUE = "\033[36m"

strColour_DEFAULT = "\033[37m"

howToPlay_ColourDisplay = f"""
┆ BASICS
┆ ‾‾‾‾‾‾
┆ A word will be chosen at random from the English dictionary with either 4, 5 or 6 letters (depending on your current game setup).
┆ This word will be hidden from you under tiles like this:
┆ 
┆  ╭╌╌╌╮╭╌╌╌╮╭╌╌╌╮╭╌╌╌╮╭╌╌╌╮
┆  ┆ ? ┆┆ ? ┆┆ ? ┆┆ ? ┆┆ ? ┆  Where each ? is a letter in the hidden word.
┆  ╰╌╌╌╯╰╌╌╌╯╰╌╌╌╯╰╌╌╌╯╰╌╌╌╯
┆ 
┆ Depending on the difficulty of the game you will be given:
┆  > {strColour_RED}6{strColour_DEFAULT} Turns  (attemps at guessing the word, shown as lives {strColour_RED}♡ ♡ ♡ ♡ ♡ ♡{strColour_DEFAULT} )
┆  > {strColour_YELLOW}1{strColour_DEFAULT} Hint  (when used a turn is lost - unless playing in easy mode (you will also have 2 extra hints))
┆  > {strColour_BLUE}25{strColour_DEFAULT}, {strColour_BLUE}30{strColour_DEFAULT} or {strColour_BLUE}45{strColour_DEFAULT} seconds to guess a word  (depending on game mode)
┆
┆ On each turn you are allocated one guess at the hidden word.
┆ This guess should contain the same number of letters as the hidden word.
┆ If the word guessed is not a valid word in the English dictionary then a turn will be lost.
┆ 
┆ 
┆ GAMEPLAY
┆ ‾‾‾‾‾‾‾‾
┆  ╭╌╌╌╮╭╌╌╌╮╭╌╌╌╮╭╌╌╌╮╭╌╌╌╮
┆  ┆ {strColour_RED}G{strColour_DEFAULT} ┆┆ {strColour_RED}U{strColour_DEFAULT} ┆┆ {strColour_YELLOW}E{strColour_DEFAULT} ┆┆ {strColour_RED}S{strColour_DEFAULT} ┆┆ {strColour_GREEN}S{strColour_DEFAULT} ┆  Your word will be displayed in the letter tiles, with symbols below each letter.
┆  ╰ {strColour_RED}−{strColour_DEFAULT} ╯╰ {strColour_RED}−{strColour_DEFAULT} ╯╰ {strColour_YELLOW}+{strColour_DEFAULT} ╯╰ {strColour_RED}−{strColour_DEFAULT} ╯╰ {strColour_GREEN}*{strColour_DEFAULT} ╯
┆
┆  > Input: {strColour_MAGENTA}Guess{strColour_DEFAULT}
┆  > Hidden Word: {strColour_GREEN}Cares{strColour_DEFAULT}
┆
┆ The symbols will tell you how close the guessed word is to the hidden word:
┆   {strColour_GREEN}*{strColour_DEFAULT} = Correct letter in the {strColour_GREEN}correct position{strColour_DEFAULT}
┆   {strColour_YELLOW}+{strColour_DEFAULT} = Corect letter, but in the {strColour_YELLOW}wrong position{strColour_DEFAULT}
┆   {strColour_RED}_{strColour_DEFAULT} = Letter is {strColour_RED}NOT in the word{strColour_DEFAULT}
┆
┆
┆ DIFFICULTY MODES
┆ ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
┆ Relaxed:
┆  > You have no time limit for guesses.
┆  > You have {strColour_RED}12{strColour_DEFAULT} turns to guess the word.
┆  > You have {strColour_YELLOW}1 hint for each hidden letter{strColour_DEFAULT} in the word: this will provide a letter that appears in the hidden word, but NOT its location!
┆    (using these hints does NOT lose a turn)
┆
┆ Easy:
┆  > There is a {strColour_BLUE}45{strColour_DEFAULT} second time limit for each guess, if a word is not guessed during this time then a turn is lost.
┆  > You have {strColour_RED}6{strColour_DEFAULT} turns to guess the word.
┆  > You have {strColour_YELLOW}3{strColour_DEFAULT} hints: this will provide a letter that appears in the hidden word, but NOT its location!
┆    (using these hints does NOT lose a turn)
┆
┆ Normal:
┆  > There is a {strColour_BLUE}30{strColour_DEFAULT} second time limit for each guess, if a word is not guessed during this time then a turn is lost.
┆  > You have {strColour_RED}6{strColour_DEFAULT} turns to guess the word.
┆  > You have {strColour_YELLOW}1{strColour_DEFAULT} hint: this will provide a letter that appears in the hidden word, but NOT its location!
┆    (using this hint will lose a turn)
┆
┆ Hard:
┆  > There is a {strColour_BLUE}25{strColour_DEFAULT} second time limit for each guess, if a word is not guessed during this time then a turn is lost.
┆  > You have {strColour_RED}6{strColour_DEFAULT} turns to guess the word.
┆  > You have {strColour_YELLOW}1{strColour_DEFAULT} hint: this will provide a letter that appears in the hidden word, but NOT its location!
┆    (using this hint will lose a turn)
┆  {strColour_BLUE}> You must use letters marked with * and _ in all following guesses!{strColour_DEFAULT}
┆
┆ You Know the Word Mode (God Mode):
┆  > There is a {strColour_BLUE}10{strColour_DEFAULT} second time limit for each guess, if a word is not guessed during this time then a turn is lost.
┆  > You have {strColour_RED}12{strColour_DEFAULT} turns to guess the word.
┆  > You have {strColour_YELLOW}1 hint for each hidden letter{strColour_DEFAULT} in the word: this will provide a letter that appears in the hidden word, but NOT its location.
┆    (using these hints will lose a turn each time)
┆  {strColour_MAGENTA}> You can see the word (used for testing the game){strColour_DEFAULT}"""

howToPlay = """
┆ BASICS
┆ ‾‾‾‾‾‾
┆ A word will be chosen at random from the English dictionary with either 4, 5 or 6 letters (depending on your current game setup).
┆ This word will be hidden from you under tiles like this:
┆ 
┆  ╭╌╌╌╮╭╌╌╌╮╭╌╌╌╮╭╌╌╌╮╭╌╌╌╮
┆  ┆ ? ┆┆ ? ┆┆ ? ┆┆ ? ┆┆ ? ┆  Where each ? is a letter in the hidden word.
┆  ╰╌╌╌╯╰╌╌╌╯╰╌╌╌╯╰╌╌╌╯╰╌╌╌╯
┆ 
┆ Depending on the difficulty of the game you will be given:
┆  > 6 Turns  (attemps at guessing the word, shown as lives ♡ ♡ ♡ ♡ ♡ ♡ )
┆  > 1 Hint  (when used a turn is lost - unless playing in easy mode (you will also have 2 extra hints))
┆  > 25, 30 or 45 seconds to guess a word  (depending on game mode)
┆
┆ On each turn you are allocated one guess at the hidden word.
┆ This guess should contain the same number of letters as the hidden word.
┆ If the word guessed is not a valid word in the English dictionary then a turn will be lost.
┆ 
┆ 
┆ GAMEPLAY
┆ ‾‾‾‾‾‾‾‾
┆  ╭╌╌╌╮╭╌╌╌╮╭╌╌╌╮╭╌╌╌╮╭╌╌╌╮
┆  ┆ G ┆┆ U ┆┆ E ┆┆ S ┆┆ S ┆  Your word will be displayed in the letter tiles, with symbols below each letter.
┆  ╰ − ╯╰ − ╯╰ + ╯╰ − ╯╰ * ╯
┆
┆  > Input: Guess
┆  > Hidden Word: Cares
┆
┆ The symbols will tell you how close the guessed word is to the hidden word:
┆   * = Correct letter in the correct position
┆   + = Corect letter, but in the wrong position
┆   _ = Letter is NOT in the word
┆
┆
┆ DIFFICULTY MODES
┆ ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
┆ Relaxed:
┆  > You have no time limit for guesses.
┆  > You have 12 turns to guess the word.
┆  > You have 1 hint for each hidden letter in the word: this will provide a letter that appears in the hidden word, but NOT its location!
┆    (using these hints does NOT lose a turn)
┆
┆ Easy:
┆  > There is a 45 second time limit for each guess, if a word is not guessed during this time then a turn is lost.
┆  > You have 6 turns to guess the word.
┆  > You have 3 hints: this will provide a letter that appears in the hidden word, but NOT its location!
┆    (using these hints does NOT lose a turn)
┆
┆ Normal:
┆  > There is a 30 second time limit for each guess, if a word is not guessed during this time then a turn is lost.
┆  > You have 6 turns to guess the word.
┆  > You have 1 hint: this will provide a letter that appears in the hidden word, but NOT its location!
┆    (using this hint will lose a turn)
┆
┆ Hard:
┆  > There is a 25 second time limit for each guess, if a word is not guessed during this time then a turn is lost.
┆  > You have 6 turns to guess the word.
┆  > You have 1 hint: this will provide a letter that appears in the hidden word, but NOT its location!
┆    (using this hint will lose a turn)
┆  > You must use letters marked with * and _ in all following guesses!
┆
┆ You Know the Word Mode (God Mode):
┆  > There is a 45 second time limit for each guess, if a word is not guessed during this time then a turn is lost.
┆  > You have 12 turns to guess the word.
┆  > You have 1 hint for each hidden letter in the word: this will provide a letter that appears in the hidden word, but NOT its location.
┆    (using these hints will lose a turn each time)
┆  > You can see the word (used for testing the game)"""