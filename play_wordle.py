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
from datetime import datetime

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
    timestamp = datetime.strftime(datetime.now(), '%Y%m%d')
    for match in script.finditer(source):
        js_url = match[1]
        # print(f'JS URL: {js_url}')
        urls.append(js_url)
        js_req = requests.get(js_url)
        js_source = js_req.content.decode()
        lst_match = re.search(r'(\[\"[a-z]+\",.*?,\"[a-z]+\"\]),', js_source)
        if lst_match:
            words = json.loads(lst_match[1])
            print('{}...{}'.format(words[:5], words[-5:]))
            with open(f'wordle_{timestamp}.words', 'w') as outfh:
                outfh.write(json.dumps(words))

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
        ambers: str, amber_list: list of str for each position
        params is global
    """
    amber_list = ['', '', '', '', '', '']
    amber_letters = []
    for amber in params['amber']:
        groups = re.findall(r'[a-z][0-9]+', amber)
        for group in groups:
            # these are of the form: '[a-z][1-5]+', 1 more than array index
            letter = group[0:1]
            amber_letters.append(letter)
            positions = [int(p) for p in list(group[1:])]
            for position in positions:
                amber_list[position-1] += f'^{letter}'

    # to handle the case where there are no amber letters:
    if len(amber_letters) > 0:
        ambers = ''.join(set(amber_letters))
    else:
        ambers = '^A-Z'

    print(amber_list)
    return ambers, amber_list


def make_regexp(green_list, amber_list):
    """
    Make the Regular Expression:
    This should have the green letter if there is one there, and the amber
    letters if not.
    """
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
    return ''.join(regex_list)


def main():
    """
        Main routine.
    """
    if params['words'] == 'system':
        words = import_system_words()
    else:
        words = import_wordle_words()
    summarise_list('All possible words', words)
    #
    # 1. Eliminate the words with black letters
    # 2. only include the words with amber or green letters
    # 3.
    ambers, amber_list = process_ambers()

    regexp = make_regexp(list(params['green']), amber_list)
    print(f'Searching for /{regexp}/, must include  any of [{ambers}] at least once.')

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
    Parse the command line for:
        -g, --green - right letters in the right place: s...k, once only
        -a, --amber - right letters in the wrong place, can be repeated
        -b, --black - wrong letters: list of the wrong letters, can be repeated
        -w, --wordle - : Use the World Dictionary instead of the system one
    """
    param_dict = {'green': '.....',
                  'amber': [],
                  'black': '',
                  'words': 'system'
                  }
    options = sys.argv[1:]
    while len(options) > 0:
        arg = options.pop(0)
        if arg in ['-g', '--green']:
            green = options.pop(0)
            if len(green) == 5:
                param_dict['green'] = green
            else:
                printerror('Strictly 5 letters!')
        if arg in ['-a', '--amber']:
            param_dict['amber'].append(options.pop(0))

        if arg in ['-b', '--black']:
            param_dict['black'] += options.pop(0)
        if arg in ['-w', '--wordle']:
            param_dict['words'] = 'wordle'
    param_dict['black'] = ''.join(sorted(set(param_dict['black'])))
    print('Parameters: ', json.dumps(param_dict, indent=4))
    return param_dict


if __name__ == '__main__':
    params = parse_params()
    main()
