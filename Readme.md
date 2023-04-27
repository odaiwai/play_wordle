# Play Wordle

Use regexps to show remaining options for Wordle.

Use the options:

    -g | --green "....." positional with the green letters in the right place
                         position would be "..x..", if x is letter 3.

    -y | --amber "[a-z][0-5]+": A letter in the wrong place, with the places it 
                         shouldn't be. There can be multiple amber lists, and 
                         they'll be built into a single list.

    -b | --black "abcde" just a list of the letters that aren't in the word. There
                         can be multiple instances of this and they'll be
                         conccvatenated into a single set.

    -w | --wordle        use the current word list from the NYTimes website, 
                         otherwise the system dictionary is used.

    e.g.$./play_wordle.py -w -b atne -a o3 -b sup -g .o... 
    Parameters:  {
        "green": ".og..",
        "amber": [
            "o3"
        ],
        "black": "aenpstu",
        "words": "wordle"
    }
    ['aahed', 'aalii', 'aapas', 'aargh', 'aarti']...['butch', 'stalk', 'flack', 'widow', 'augur']
    All possible words (14855): ['aahed', 'aalii', 'aapas', 'aargh', 'aarti'] ... ['butch', 'stalk', 'flack', 'widow', 'augur']
    ['', '', '^o', '', '', '']
    Searching for /.og../, must include any of [o] at least once.
    Remaining possible words (78): ['bogan', 'bogey', 'boggy', 'bogie', 'bogle'] ... ['logic', 'dogma', 'vogue', 'login', 'roger']
    Can't include /aenpstu/
    Final remaining word(s): (11):
    ['boggy' 'doggo' 'doggy' 'dogly' 'hogoh' 'loggy' 'logoi' 'moggy' 'yogic'
    'foggy' 'logic']
    
The script will show the regexp it generates.
