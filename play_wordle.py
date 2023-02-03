#!/usr/bin/env python3
"""
    Script to help with Wordle

"""

# import os
import sys
import re
import json
import requests


def printerror(msg):
    """
    Print and error message and quit
    """
    print(f'BARF! {msg} NO SOUP FOR YOU!')
    sys.exit()


def import_words():
    """
    Import all 5 letter words from the system Dictionary
    """
    all_words = []
    with open('/usr/share/dict/words', 'r', encoding='utf8') as infh:
        lines = list(infh)
        for line in lines:
            if re.match(r'^[a-z]{5}$', line.strip('\n')):
                all_words.append(line.strip('\n'))
    # print(all_words, len(all_words))
    return all_words


def import_wordle_words():
    """
    Return the latest version of the World Official List
    1. Open the Wordle Home Page
    2. Scour the Source for Javascript (*.js) links
    3. Get each JS link and look for lists of 5 letter words.
    4. extract the list and return the list

    the JS scripts look like this:
        src="https://www.nytimes.com/games-assets/v2/699.65b76772350e4f407ad2.js">
        src="https://www.nytimes.com/games-assets/v2/194.394a5bff81f32b6c09f6.js">
        src="https://www.nytimes.com/games-assets/v2/926.9ac55785ede32158ab6a.js">
        src="https://www.nytimes.com/games-assets/v2/940.510e557a044c374bfb56.js">
        src="https://www.nytimes.com/games-assets/v2/382.e39eda995c75e1cb9ce9.js">
        src="https://www.nytimes.com/games-assets/v2/621.a4a0ec303e0ca48bdd3e.js">
        src="https://www.nytimes.com/games-assets/v2/931.794bf8ab6514c5b4a826.js">
        src="https://www.nytimes.com/games-assets/v2/202.2c26bc40168ecbf65013.js">
        src="https://www.nytimes.com/games-assets/v2/wordle.d8eba58d244471b4cafe.js">
    """
    url = r'https://www.nytimes.com/games/wordle/index.html'
    response = requests.get(url)
    source = response.content.decode()
    # Look for Variables
    script = re.compile(r'\"(https://www.nytimes.com/games-assets/.*?.js)\"')
    urls = []
    words = []
    for match in script.finditer(source):
        js_url = match[1]
        # print(f'JS URL: {js_url}')
        urls.append(js_url)
        js_req = requests.get(js_url)
        js_source = js_req.content.decode()
        lst_match = re.search(r'(\[\"[a-z]+\",.*?,\"[a-z]+\"\]),', js_source)
        if lst_match:
            words = json.loads(lst_match[1])
            # print('{}...{}'.format(words[:5], words[-5:]))
    return words


def summarise_list(my_list):
    """
    Summarise a list with the length, first and last elements
    """
    print(f'Possible Words ({len(my_list)}):',
          f'{my_list[:5]}...{my_list[-5:]}')


def main():
    """
        Main routine.
    """
    words = import_words()
    summarise_list(words)
    # wordle_words = import_wordle_words()
    #
    # 1. Eliminate the words with black letters
    # 2. only include the words with amber or green letters
    # 3.
    green_list = list(params['green'])
    amber_list = ['', '', '', '', '', '']
    for amber in params['amber']:
        # these are of the form: a[1-5]+, 1 more than array index
        ambers = list(amber)
        letter = ambers[0]
        positions = [int(p) for p in ambers[1:]]
        for position in positions:
            amber_list[position-1] += f'^{letter}'
    print(amber_list)
    # need individual greps for each of the amber letters
    # FIXME!
    regex_list = []
    # print(green_list, amber_list)
    for green, amber in zip(green_list, amber_list):
        # print(green, amber)
        if green == '.':
            regex_list.append(f'[{amber}]')
        else:
            regex_list.append(green)
    regexp = ''.join(regex_list)
    print(f'Searching for {regexp}...')

    possible = []
    for word in words:
        if re.search(rf'^{regexp}$', word):
            possible.append(word)
            # print (word, possible)

    summarise_list(possible)
    for word in possible:
        if re.search(r'[A-Z{}.-]'.format(params['black']), word):
            possible.remove(word)
    print(f'Possible ({len(possible)}):{possible}')


if __name__ == '__main__':
    # Parse the command line for:
    # -g, --green - right letters in the right place: s...k, once only
    # -a, --amber - right letters in the wrong place, can be repeated
    # -b, --black - wrong letters: list of the wrong letters, can be repeater
    params = {'green': '.....',
              'amber': [],
              'black': ''
              }
    options = sys.argv[1:]
    while len(options) > 0:
        arg = options[0]
        val = options[1]
        options = options[2:]
        if arg == '-g' or arg == '--green':
            if len(val) == 5:
                params['green'] = val
            else:
                printerror('Strictly 5 letters!')
        if arg == '-a' or arg == '--amber':
            params['amber'].append(val)

        if arg == '-b' or arg == '--black':
            params['black'] += val
    print(f'Parameters: {params}')
    main()

