#!/usr/bin/env python3
"""
    Script to help with Wordle

"""

import os
import sys
import re
import requests
iimport json


def import_words():
    all_words = []
    with open('/usr/share/dict/words', 'r') as infh:
        lines = list(infh)
        for line in lines:
            if re.match(r'^[a-z]{5}$', line.strip('\n')):
                all_words.append(line.strip('\n'))

    print(all_words, len(all_words))


    return all_words


def import_worldle_words():
    baseurl = r'https://www.nytimes.com/games/wordle/index.html'
    js_url = r'https://www.nytimes.com/games/wordle/main.9622bc55.js'
    url_response = requests.get(js_url)
    game_source = url_response.content.decode()

    # Look for Variables
    json_general   = re.compile(r'try \{ var (.*?) = (\[\{.*?)\}catch\(e\)')
    for match in json_general.finditer(html_source):
        name = match[1]
        json_blob = match[2]
        printlog (name, '=', json_blob, len(json_blob))
        json_blobs[name] = json.loads(json_blob)
        """
            with open(fileroot + '_json_blobs.json', "a") as outfile:
            outfile.write(name + '=')
            json.dump(json_blobs[name], outfile, ensure_ascii=False)
            outfile.write('\n')
            #printlog (json.dumps(area_stats, ensure_ascii=False))
        """




def main():
    """
        Main routine.
    """
    words = import_words()
    wordle_words = import_wordle_words()
    return None


if __name__ == '__main__':
    main()

