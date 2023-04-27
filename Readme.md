# Play Wordle

Use regexps to show remaining options for Wordle.

Use the options:

    -g | --green "....." positional with the green letters
                         position would be "..x.."
    -y | --amber "[a-z][0-5]+": A letter in the wrong place, with the places it 
                         shouldn't be.
    -b | --black "abcde" just a list of the letters that aren't in the word.

    e.g.$./play_wordle.py -w -b atne -a o3 -b sup -g .o... 
    
The script will should the regexp it generates.
