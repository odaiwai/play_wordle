# Play Wordle

Use regexps to show remaining options for Wordle.

Use the options:
    -g | --green "....." with the green letters
                         position would be "..[abc].."
    -y | --amber "[a-z][0-5]+": A letter in the wrong place, with the places it 
                         shouldn't be
    -b | --black "abcde" just a list of the letters that aren't in the word.

    e.g.$./play_wordle.py -w -b atne -a o3 -b sup -g .o... 
green and amber lists are positional
