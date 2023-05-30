# Play Wordle

Use regexps to show remaining options for Wordle.

Use the options:

`-g | --green "....."` A positional regex with the green letters in the right place
                        position would be "..x..", if x is letter 3.

`-g | --green "([a-z][0-5]+)+"` A letter in the right place, with the places it 
                        should be. There can be multiple green lists, and 
                        they'll be built into a single list. The positional
                        green list takes precedence over this list.

 `-y | --amber "([a-z][0-5]+)+"` A letter in the wrong place, with the places it 
                        shouldn't be. There can be multiple amber lists, and 
                        they'll be built into a single list.

`-b | --black "abcde"` A list of the letters that aren't in the word. There
                        can be multiple instances of this and they'll be
                        concatenated into a single set.

`-w | --wordle`     use the current word list from the NYTimes website, 
                        otherwise the system dictionary is used. This adds slightly 
                        to the runtime, as the app has to go to the NYTimes site and
                        scrape the game page for the wordlist. This list is written
                        to the local files `wordle.words` once it is retrieved and
                        can be reused using the `--local` default.

`-s |  --system`       Use the system dictionary if available. This is expected in
                        /usr/share/dict/words. This may be slightly different from
                        the Wordle list and has proper nouns in it. The app makes
                        a list of all of the five letter words from the system 
                        dict.

`-l | --local`         Use the local copy of the Wordle Words file if it exists. 
                        This is now the default option.

e.g.

    $./play_wordle.py -w -b atne -a o3 -b sup -g .o... 
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
