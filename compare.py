#!/usr/bin/env python3
"""Compare spelling checker functionality and performance."""

import heapq
from platform import python_version
import sys
import time

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

from pynuspell import load_from_path
from hunspell import Hunspell

BASE_W: str = '/usr/share/dict/'
BASE_H: str = '/usr/share/hunspell/'
LISTS: dict = {
    'de_DE_frami': 'ngerman',
    'en_US': 'american-english',
    'es_ES': 'spanish',
    'fr': 'french',
    'nl': 'dutch',
}
plt.rcParams['font.family'] = 'monospace'
plt.rcParams['font.monospace'] = 'Noto Mono'
plt.rcParams['legend.loc'] = 'upper right'
FIGSIZE = (19.20, 10.80)
plt.figure(figsize=FIGSIZE)
MAX_SUGGEST = 1000
MAX_SUGGEST_NL = 1000
TOPX = 12

# pylint:disable=unspecified-encoding


def get_nuspell(code: str):
    """Get Nuspell."""
    return load_from_path(f'{BASE_H}{code}')


def get_hunspell(code: str):
    """Get Hunspell."""
    if code == 'en_US':
        return Hunspell(code)
    return Hunspell(code, hunspell_data_dir=BASE_H)  # TODO Create issue.


def histo(code: str, file: str, name_n: str, name_h: str, function: str,
          data: dict):
    """Plot histogram to PNG file."""
    df = pd.DataFrame({name_h: data['tim_h'], name_n: data['tim_n']})
    ax = df.plot.hist(alpha=0.5, bins=32, edgecolor='black',
                      color=['blue', 'orange'], figsize=FIGSIZE)
    plt.title(f"Histogram {function} with dictionary '{code}' on file '{file}'"
              f' for {data["len_h"]} words in Python {python_version()}')
    if function == 'suggest()':
        scale = ' µs'
        plt.xlabel(f'processing time [{scale[1:]}]')
    elif function == 'len(suggest())':
        scale = ''
        plt.xlabel('number of words [n]')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    else:
        scale = ' ns'
        plt.xlabel(f'Process Time [{scale[1:]}]')
    plt.ylabel('frequency [log(n)]')
    plt.yscale('log')
    plt.grid(True)
    if function == 'len(suggest())':
        leg_h = f'{name_h} slowest words\n'
        leg_n = f'{name_n} slowest words\n'
    else:
        leg_h = f'{name_h} total time {int(data["tot_h"]):,d}{scale},' \
                f' fastest word {int(data["min_h"]):,d}{scale},' \
                ' slowest words\n'
        leg_n = f'{name_n} total time {int(data["tot_n"]):,d}{scale},' \
                f' fastest word {int(data["min_n"]):,d}{scale},' \
                ' slowest words\n'
    for tim, word in sorted(data['hea_h'], reverse=True):
        leg_h += f'{int(tim):>11,d}{scale} {word}\n'
    leg_h = leg_h[:-1]
    more = False
    for tim, word in sorted(data['hea_n'], reverse=True):
        if function == 'len(suggest())' and tim > 15:
            leg_n += f'{int(tim):>11,d}{scale}*{word}\n'
            more = True
        else:
            leg_n += f'{int(tim):>11,d}{scale} {word}\n'
    if more:
        leg_n += '* more than 15 suggestions in the result'
    elif function == 'suggest()':
        leg_n += '() the number of suggestions in the result'
    else:
        leg_n = leg_n[:-1]
    plt.legend([leg_h, leg_n], alignment='left')
    plt.savefig(f'{function.replace("(", "").replace(")", "")}-{code}'
                f'-{file.replace(".tsv", "")}')
    plt.close()


def check(path, checker):
    """Check all words with spelling checker and get suggestions for fails."""
    res = {}
    values_spelling = []
    slowest_spelling = []
    with open(path) as file:
        incorrect = set()
        cnt = 0
        for line in file:
            line = line.strip().split('\t')[0]
            if line != '':
                start = time.process_time_ns()
                tmp = checker.spell(line)
                tim = time.process_time_ns() - start
                values_spelling.append(tim)
                heapq.heappush(slowest_spelling, (tim, line))
                if len(slowest_spelling) > TOPX:
                    heapq.heappop(slowest_spelling)
                if not tmp:
                    incorrect.add(line)
            cnt += 1
            if cnt % 50000 == 0:
                print(f'    spell {cnt:07d}')
        if cnt % 50000:
            print(f'    spell {cnt:07d}')
    res['len_spe'] = len(values_spelling)
    res['min_spe'] = min(values_spelling)
    res['tot_spe'] = sum(values_spelling)
    res['values_spelling'] = values_spelling
    res['hea_spe'] = slowest_spelling

    values_suggest = []
    values_lensuggest = []
    slowest_suggest = []
    slowest_lensuggest = []
    cnt = 0
    for line in incorrect:
        start = time.process_time_ns()
        tmp = checker.suggest(line)
        lentmp = len(tmp)
        tim = float(time.process_time_ns() - start) / 1000  # microseconds
        values_suggest.append(tim)
        heapq.heappush(slowest_suggest, (tim, f'{line} ({lentmp})'))
        if len(slowest_suggest) > TOPX:
            heapq.heappop(slowest_suggest)
        values_lensuggest.append(lentmp)
        heapq.heappush(slowest_lensuggest, (lentmp, line))
        if len(slowest_lensuggest) > TOPX:
            heapq.heappop(slowest_lensuggest)
        cnt += 1
        if cnt % 50 == 0:
            print(f'    suggest {cnt:07d}')
        if path.endswith('dutch') or path.endswith('.tsv'):
            if cnt == MAX_SUGGEST_NL:
                break
        else:
            if cnt == MAX_SUGGEST:
                break
    if cnt % 50:
        print(f'    suggest {cnt:07d}')
    res['len_sug'] = len(values_suggest)
    res['min_sug'] = min(values_suggest)
    res['tot_sug'] = sum(values_suggest)
    res['tim_sug'] = values_suggest
    res['hea_sug'] = slowest_suggest

    res['len_cnt'] = len(values_lensuggest)
    res['min_cnt'] = 0
    res['tot_cnt'] = 0
    res['tim_cnt'] = values_lensuggest
    res['hea_cnt'] = slowest_lensuggest

    return res


def compare(code: str, file: str) -> None:
    """Compare spelling checking and suggestions."""
    if file.endswith('.tsv'):
        path = f'../opentaal-wordlist/elements/{file}'
    else:
        path = f'{BASE_W}{file}'
    name_h = 'cyhunspell-py310'
    print(f'  {name_h}')
    res_h = check(path, get_hunspell(code))
    name_n = 'pynuspell'
    print(f'  {name_n}')
    res_n = check(path, get_nuspell(code))

    spe = {}
    spe['len_h'] = res_h['len_spe']
    spe['min_h'] = res_h['min_spe']
    spe['tot_h'] = res_h['tot_spe']
    spe['tim_h'] = res_h['values_spelling']
    spe['hea_h'] = res_h['hea_spe']

    spe['len_n'] = res_n['len_spe']
    spe['min_n'] = res_n['min_spe']
    spe['tot_n'] = res_n['tot_spe']
    spe['tim_n'] = res_n['values_spelling']
    spe['hea_n'] = res_n['hea_spe']
    histo(code, file, name_n, name_h, 'spell()', spe)

    sug = {}
    sug['len_h'] = res_h['len_sug']
    sug['min_h'] = res_h['min_sug']
    sug['tot_h'] = res_h['tot_sug']
    sug['tim_h'] = res_h['tim_sug']
    sug['hea_h'] = res_h['hea_sug']

    sug['len_n'] = res_n['len_sug']
    sug['min_n'] = res_n['min_sug']
    sug['tot_n'] = res_n['tot_sug']
    sug['tim_n'] = res_n['tim_sug']
    sug['hea_n'] = res_n['hea_sug']
    histo(code, file, name_n, name_h, 'suggest()', sug)

    cnt = {}
    cnt['len_h'] = res_h['len_cnt']
    cnt['min_h'] = res_h['min_cnt']
    cnt['tot_h'] = res_h['tot_cnt']
    cnt['tim_h'] = res_h['tim_cnt']
    cnt['hea_h'] = res_h['hea_cnt']

    cnt['len_n'] = res_n['len_cnt']
    cnt['min_n'] = res_n['min_cnt']
    cnt['tot_n'] = res_n['tot_cnt']
    cnt['tim_n'] = res_n['tim_cnt']
    cnt['hea_n'] = res_n['hea_cnt']
    histo(code, file, name_n, name_h, 'len(suggest())', cnt)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        MAX_SUGGEST = 100
        MAX_SUGGEST_NL = 25
    for code, file in sorted(LISTS.items()):
        print(f'{code} {file}')
        compare(code, file)
    code = 'nl'
    file = 'corrections.tsv'
    print(f'{code} {file}')
    compare(code, file)
