#!/usr/bin/env python3
"""Compare spelling checkers."""

import time

import pandas as pd
import matplotlib.pyplot as plt

from pynuspell import load_from_path
# hunspell
# from hunspell import HunSpell
# cyhunspell-py310
from hunspell import Hunspell

BASE_W: str = '/usr/share/dict/'
BASE_H: str = '/usr/share/hunspell/'
LISTS: dict = {
    'en_US': 'american-english',
    'es_ES': 'spanish',
    'nl': 'dutch',
}

# pylint:disable=unspecified-encoding


def get_nuspell(code: str):
    """Get Nuspell."""
    return load_from_path(f'{BASE_H}{code}')


def get_hunspell(code: str):
    """Get Hunspell."""
    # hunspell
    # return HunSpell(f'{BASE_H}{code}.dic', f'{BASE_H}{code}.aff')
    # cyhunspell-py310
    if code == 'en_US':
        return Hunspell(code)
    return Hunspell(code, hunspell_data_dir=BASE_H)  # TODO Create issue


def histo(code: str, file: str, name_n: str, name_h: str, function: str,
          data: dict):
    """Plot histogram to PNG file."""
    df = pd.DataFrame({name_h: data['tim_h'], name_n: data['tim_n']})
    plt.figure(figsize=(19.20, 10.80))
    df.plot.hist(alpha=0.5, bins=32, edgecolor='black',
                 color=['blue', 'orange'], figsize=(19.20, 10.80))
    plt.title(f'Histograms {function} with {code} on {file} for {data["len_h"]} words')
    if function == 'suggest':
        plt.xlabel('Process Time [µs]')
    else:
        plt.xlabel('Process Time [ns]')
    plt.ylabel('Frequency [log]')
    plt.yscale('log')
    plt.grid(True)
    leg_h = f'{name_h} min={int(data["min_h"]):,d} max={int(data["max_h"]):,d} total={int(data["tot_h"]):,d}'
    leg_n = f'{name_n} min={int(data["min_n"]):,d} max={int(data["max_n"]):,d} total={int(data["tot_n"]):,d}'
    plt.legend([leg_h, leg_n])
    plt.savefig(f'{code}-{file}-{function}.png')


def check(path, checker):
    """Check all words with spelling checker and get suggestions for fails."""
    res = {}
    tim_spe = []
    if path.endswith('.tsv'):
        exit(1)
    with open(path) as file:
        failed = set()
        cnt = 0
        for line in file:
            line = line.strip()
            if line != '':
                start = time.process_time_ns()
                tmp = checker.spell(line)
                tim_spe.append(time.process_time_ns() - start)
                if not tmp:
                    failed.add(line)
            cnt += 1
            if cnt % 50000 == 0:
                print(f'    spe {cnt:07d}')
    res['len_spe'] = len(tim_spe)
    res['min_spe'] = min(tim_spe)
    res['max_spe'] = max(tim_spe)
    res['tot_spe'] = sum(tim_spe)
    res['tim_spe'] = tim_spe

    tim_sug = []
    cnt = 0
    for line in failed:
        start = time.process_time_ns()
        checker.suggest(line)
        tim_sug.append((time.process_time_ns() - start) / 1000)  # microseconds
        cnt += 1
        if cnt % 50 == 0:
            print(f'    sug {cnt:07d}')
        if cnt == 500:
            break
    res['len_sug'] = len(tim_sug)
    res['min_sug'] = min(tim_sug)
    res['max_sug'] = max(tim_sug)
    res['tot_sug'] = sum(tim_sug)
    res['tim_sug'] = tim_sug

    return res


def compare(code: str, file: str) -> None:
    """Compare spelling checking and suggestions."""
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
    spe['max_h'] = res_h['max_spe']
    spe['tot_h'] = res_h['tot_spe']
    spe['tim_h'] = res_h['tim_spe']
    spe['len_n'] = res_n['len_spe']
    spe['min_n'] = res_n['min_spe']
    spe['max_n'] = res_n['max_spe']
    spe['tot_n'] = res_n['tot_spe']
    spe['tim_n'] = res_n['tim_spe']
    histo(code, file, name_n, name_h, 'spell', spe)

    sug = {}
    sug['len_h'] = res_h['len_sug']
    sug['min_h'] = res_h['min_sug']
    sug['max_h'] = res_h['max_sug']
    sug['tot_h'] = res_h['tot_sug']
    sug['tim_h'] = res_h['tim_sug']
    sug['len_n'] = res_n['len_sug']
    sug['min_n'] = res_n['min_sug']
    sug['max_n'] = res_n['max_sug']
    sug['tot_n'] = res_n['tot_sug']
    sug['tim_n'] = res_n['tim_sug']
    histo(code, file, name_n, name_h, 'suggest', sug)


if __name__ == '__main__':
    for code, file in sorted(LISTS.items()):
        print(f'{code} {file}')
        compare(code, file)
    # compare(code, '../opentaal-wordlist/elements/corrections.tsv')
