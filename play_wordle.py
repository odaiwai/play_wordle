#!/usr/bin/env python3
"""
    Script to help with Wordle

"""

# import os
import sys
import re
import json
import requests
import numpy as np


def printerror(msg):
    """
    Print and error message and quit
    """
    print(f'BARF! {msg} NO SOUP FOR YOU!')
    sys.exit()


def import_system_words():
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


def summarise_list(caption, my_list):
    """
    Summarise a list with the length, first and last elements
    """
    print(f'{caption} ({len(my_list)}):',
          f'{my_list[:5]} ... {my_list[-5:]}')


def process_ambers():
    """
    Process the parameters to provide a list of ambers as:
        []
    """


def main():
    """
        Main routine.
    """
    words = import_system_words()
    # words = import_wordle_words()
    summarise_list('All possible words', words)
    wordle_words = import_wordle_words()
    summarise_list('Wordle Words', wordle_words)
    #
    # 1. Eliminate the words with black letters
    # 2. only include the words with amber or green letters
    # 3.
    green_list = list(params['green'])
    amber_list = ['', '', '', '', '', '']
    amber_letters = []
    for amber in params['amber']:
        # these are of the form: '[a-z][1-5]+', 1 more than array index
        letter = amber[0:1]
        amber_letters.append(letter)
        positions = [int(p) for p in list(amber[1:])]
        for position in positions:
            amber_list[position-1] += f'^{letter}'
    print(amber_list)

    # Make the Regular Expression:
    # This should have the green letter if there is one there, and the amber
    # letters if not.
    regex_list = []
    # print(green_list, amber_list, chars)
    for green, amber in zip(green_list, amber_list):
        # print(green, amber)
        if green == '.' and len(amber) > 0:
            # print(f'AMBER: adding [{amber}]')
            regex_list.append(f'[{amber}]')
        else:
            # print(f'GREEN: adding {green}')
            regex_list.append(green)
    regexp = ''.join(regex_list)
    ambers = ''.join(set(amber_letters))
    print(f'Searching for /{regexp}/, must include all of [{ambers}].')

    # Make the list of remaining possible words:
    possible = []
    for word in words:
        verdict = f'{word}:'
        word_is_possible = False
        if re.search(rf'^{regexp}$', word):
            word_is_possible = True
        amber_matches = len(re.findall(rf'[{ambers}]', ''.join(set(word))))
        verdict += f' checking /{ambers}/ ({amber_matches}).'
        if amber_matches < len(ambers):
            verdict += ' Not enough matches.'
            word_is_possible = False
        else:
            verdict += f' Word contains /{ambers}/ ({amber_matches}).'
        if word_is_possible:
            possible.append(word)
            # print (word, verdict)

    summarise_list('Remaining possible words', possible)
    remaining = possible.copy()
    black = params['black']
    print(f'Can\'t include /{black}/')
    for word in possible:
        verdict = f'{word}:'
        match = re.findall(rf'[A-Z{black}\.-]', word)
        if len(match) > 0:
            matches = [match[i] for i in range(0, len(match))]
            verdict += f' Includes {len(match)} of /{black}/: {matches}.'
            remaining.remove(word)
            # print(f'{verdict}: Removing {word}', remaining)
        # else:
        #     print(f'{verdict} Keeping.')
    # using numpy to format a list *might* be overkill
    print(f'Final remaining word(s): ({len(remaining)}):')
    print(np.array(remaining))


def parse_params():
    """
    Parse the parameters
    """
    # Parse the command line for:
    # -g, --green - right letters in the right place: s...k, once only
    # -a, --amber - right letters in the wrong place, can be repeated
    # -b, --black - wrong letters: list of the wrong letters, can be repeated
    params = {'green': '.....',
              'amber': [],
              'black': ''
              }
    options = sys.argv[1:]
    while len(options) > 0:
        arg, value = options[0], options[1]
        options = options[2:]
        if arg in ['-g', '--green']:
            if len(value) == 5:
                params['green'] = value
            else:
                printerror('Strictly 5 letters!')
        if arg in ['-a', '--amber']:
            params['amber'].append(value)

        if arg in ['-b', '--black']:
            params['black'] += value
    params['black'] = ''.join(sorted(set(params['black'])))
    print('Parameters: ', json.dumps(params, indent=4))
    return params


if __name__ == '__main__':
    params = parse_params()
    main()

