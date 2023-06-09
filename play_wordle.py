#!/usr/bin/env python3
"""
    Script to help with Wordle

    Dave O'Brien 2023
"""
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

    return all_words


def import_local_wordle_words():
    """
    Import all 5 letter words from the local backup of Wordle words
    """
    all_words = []
    try:
        with open('./wordle.words', 'r', encoding='utf8') as infh:
            all_words = json.loads(infh.read())
    except FileNotFoundError:
        print('Local wordle.words file not found.\n'
              'Try with --system/-s or --wordle/-w.')
        all_words = []
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
        src="https://www.nytimes.com/games-assets/v2/202.2c26bc40168ecbf65013.js">
        src="https://www.nytimes.com/games-assets/v2/wordle.d8eba58d244471b4cafe.js">
    """
    url = r'https://www.nytimes.com/games/wordle/index.html'
    response = requests.get(url, timeout=30)
    source = response.content.decode()
    # Look for Variables
    script = re.compile(r'\"(https://www.nytimes.com/games-assets/.*?.js)\"')
    wordlists = re.compile(r'=(\[\"[a-z]{5}\",.*?,\"[a-z]{5}\"\]),')
    urls = []
    words = []
    # timestamp = datetime.strftime(datetime.now(), '%Y%m%d')
    for match in script.finditer(source):
        js_url = match[1]
        urls.append(js_url)
        js_req = requests.get(js_url, timeout=30)
        js_source = js_req.content.decode()
        encoding = js_req.encoding
        for idx, wordlist in enumerate(wordlists.finditer(js_source)):
            words = json.loads(wordlist[1])
            print(f'{idx}: {words[:5]}...{words[-5:]}')
            with open('wordle.words', 'w', encoding=encoding) as outfh:
                outfh.write(json.dumps(words))
    return words


def summarise_list(caption, my_list, ins_outs=5):
    """
    Summarise a list with the length, first and last elements
    """
    print(f'{caption} ({len(my_list)}):',
          f'{my_list[:ins_outs]} ... {my_list[-ins_outs:]}')


def process_greens():
    """
    process the green list to make a regexp like the amber list
    """
    green_list = ['', '', '', '', '']
    green_letters = []
    for green in params['green']:
        groups = re.findall(r'[a-z][0-9]+', green)
        for group in groups:
            # these are of the form: '[a-z][1-5]+', 1 more than array index
            letter = group[0:1]
            green_letters.append(letter)
            positions = [int(p) for p in list(group[1:])]
            for position in positions:
                # Can only have one green
                green_list[position-1] += f'{letter}'

    greens = ''.join(set(green_letters))
    return greens, green_list


def process_ambers():
    """
    Process the parameters to provide a list of ambers as:
        ambers: str, amber_list: list of str for each position
        params is global
    """
    amber_list = ['', '', '', '', '']
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
    return ambers, amber_list


def make_regexp(grexp_list, green_list, amber_list):
    """
    Make the Regular Expression:
    This should have the green letter if there is one there, and the amber
    letters if not.
    """
    regex_list = []
    for grexp, green, amber in zip(grexp_list, green_list, amber_list):
        if grexp != '.':
            regex_list.append(grexp)
        elif green != '':
            regex_list.append(f'[{green}]')
        elif len(amber) > 0:
            regex_list.append(f'[{amber}]')
        else:
            regex_list.append('.')
    return ''.join(regex_list)


def main():
    """
        Main routine.
    """
    if params['words'] == 'system':
        words = import_system_words()
    elif params['words'] == 'local':
        words = import_local_wordle_words()
    else:
        words = import_wordle_words()
    summarise_list('All possible words', words)

    # 1. Eliminate the words with black letters
    # 2. only include the words with amber or green letters
    ambers, amber_list = process_ambers()
    greens, green_list = process_greens()
    print(f'Ambers: {amber_list}, {ambers}, Greens: {green_list}, {greens}')

    regexp = make_regexp(list(params['grexp']), green_list, amber_list)
    print((f'Searching for /{regexp}/, '
           f'must include any of [{ambers}] at least once.'))

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

    # using numpy to format a list *might* be overkill
    print(f'Final remaining word(s): ({len(remaining)}):')
    print(np.array(remaining))


def parse_params():
    """
    Parse the command line for:
        -g, --grexp - right letters in the right place: s...k, once only
        -g, --green - right letters in the right place, can be repeated
        -g, --grexp - right letters in the right place: s...k, once only
        -b, --black - wrong letters: list of the wrong letters, can be repeated
        -w, --wordle - : Use the NYTimes Wordle words instead of the system one
        -l, --local - : Use the local Wordle words file instead of the system
        -s, --system - : Use the system Dictionary
    """
    param_dict = {'grexp': '.....',
                  'green': [],
                  'amber': [],
                  'black': '',
                  'words': 'local'
                  }
    options = sys.argv[1:]
    while len(options) > 0:
        arg = options.pop(0)
        if arg in ['-g', '--green']:
            green = options.pop(0)
            if re.match(r'^[a-z.]{5}$', green):
                # a standard green regexp
                param_dict['grexp'] = green
            else:
                param_dict['green'].append(green)
        if arg in ['-a', '--amber']:
            param_dict['amber'].append(options.pop(0))

        if arg in ['-b', '--black']:
            param_dict['black'] += options.pop(0)
        if arg in ['-w', '--wordle']:
            param_dict['words'] = 'wordle'
        if arg in ['-s', '--system']:
            param_dict['words'] = 'system'
    param_dict['black'] = ''.join(sorted(set(param_dict['black'])))
    print('Parameters: ', json.dumps(param_dict, indent=4))
    return param_dict


if __name__ == '__main__':
    params = parse_params()
    main()
