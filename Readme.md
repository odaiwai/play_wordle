# Play Wordle

Use regexps to show remaining options for Wordle.
-g | --green "....." with the green letters
-y | --amber "....." positional with the amber letters. multiple ambers in the same
                     position would be "..[abc].."
-y | --amber "[a-z][0-5]+": A letter in the wrong place, with the places it 
                     shouldn't be
-b | --black "abcde" just a list of the letters that aren't in the word.

green and amber lists are positional
