#!/usr/bin/env python3
"""Compare spelling checkers."""

import time

import pandas as pd
import matplotlib.pyplot as plt

from pynuspell import load_from_path
from hunspell import Hunspell

BASE_W: str = '/usr/share/dict/'
BASE_H: str = '/usr/share/hunspell/'
LISTS: dict = {
    'en_US': 'american-english',
    'es_ES': 'spanish',
    'de_DE': 'ngerman',
    'nl': 'dutch',
}

# pylint:disable=unspecified-encoding


def get_nuspell(code: str):
    """Get Nuspell."""
    return load_from_path(f'{BASE_H}{code}')


def get_hunspell(code: str):
    """Get Hunspell."""
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
    plt.title(f'Histograms {function} with {code} on {file} for'
              f' {data["len_h"]} words')
    if function == 'suggest':
        plt.xlabel('Process Time [µs]')
    else:
        plt.xlabel('Process Time [ns]')
    plt.ylabel('Frequency [log]')
    plt.yscale('log')
    plt.grid(True)
    leg_h = f'{name_h} total={int(data["tot_h"]):,d}' \
            f' min={int(data["min_h"]):,d}' \
            f' max={int(data["max_h"]):,d} for {data["slo_h"]}'
    leg_n = f'{name_n} total={int(data["tot_n"]):,d}' \
            f' min={int(data["min_n"]):,d}' \
            f' max={int(data["max_n"]):,d} for {data["slo_n"]}'
    plt.legend([leg_h, leg_n])
    plt.savefig(f'{function}-{code}-{file.replace(".tsv", "")}.png')


def check(path, checker):
    """Check all words with spelling checker and get suggestions for fails."""
    res = {}
    tim_spe = []
    with open(path) as file:
        incorrect = set()
        max_spe = 0
        slo_spe = ''
        cnt = 0
        for line in file:
            line = line.strip().split('\t')[0]
            if line != '':
                start = time.process_time_ns()
                tmp = checker.spell(line)
                tim = time.process_time_ns() - start
                if tim > max_spe:
                    max_spe = tim
                    slo_spe = line
                tim_spe.append(tim)
                if not tmp:
                    incorrect.add(line)
            cnt += 1
            if cnt % 50000 == 0:
                print(f'    spe {cnt:07d}')
        if cnt % 50000:
            print(f'    spe {cnt:07d}')
    res['len_spe'] = len(tim_spe)
    res['min_spe'] = min(tim_spe)
    res['max_spe'] = max_spe
    res['tot_spe'] = sum(tim_spe)
    res['tim_spe'] = tim_spe
    res['slo_spe'] = slo_spe

    tim_sug = []
    max_sug = 0.0
    slo_sug = ''
    cnt = 0
    for line in incorrect:
        start = time.process_time_ns()
        checker.suggest(line)
        tim = float(time.process_time_ns() - start) / 1000  # microseconds
        if tim > max_sug:
            max_sug = tim
            slo_sug = line
        tim_sug.append(tim)
        cnt += 1
        if cnt % 50 == 0:
            print(f'    sug {cnt:07d}')
        if path.endswith('dutch') or path.endswith('.tsv'):
            if cnt == 150:
                break
        else:
            if cnt == 500:
                break
    if cnt % 50:
        print(f'    sug {cnt:07d}')
    res['len_sug'] = len(tim_sug)
    res['min_sug'] = min(tim_sug)
    res['max_sug'] = max(tim_sug)
    res['tot_sug'] = sum(tim_sug)
    res['tim_sug'] = tim_sug
    res['slo_sug'] = slo_sug

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
    spe['max_h'] = res_h['max_spe']
    spe['tot_h'] = res_h['tot_spe']
    spe['tim_h'] = res_h['tim_spe']
    spe['slo_h'] = res_h['slo_spe']
    spe['len_n'] = res_n['len_spe']
    spe['min_n'] = res_n['min_spe']
    spe['max_n'] = res_n['max_spe']
    spe['tot_n'] = res_n['tot_spe']
    spe['tim_n'] = res_n['tim_spe']
    spe['slo_n'] = res_n['slo_spe']
    histo(code, file, name_n, name_h, 'spell', spe)

    sug = {}
    sug['len_h'] = res_h['len_sug']
    sug['min_h'] = res_h['min_sug']
    sug['max_h'] = res_h['max_sug']
    sug['tot_h'] = res_h['tot_sug']
    sug['tim_h'] = res_h['tim_sug']
    sug['slo_h'] = res_h['slo_sug']
    sug['len_n'] = res_n['len_sug']
    sug['min_n'] = res_n['min_sug']
    sug['max_n'] = res_n['max_sug']
    sug['tot_n'] = res_n['tot_sug']
    sug['tim_n'] = res_n['tim_sug']
    sug['slo_n'] = res_n['slo_sug']
    histo(code, file, name_n, name_h, 'suggest', sug)


if __name__ == '__main__':
    for code, file in sorted(LISTS.items()):
        print(f'{code} {file}')
        compare(code, file)
    code = 'nl'
    file = 'corrections.tsv'
    print(f'{code} {file}')
    compare(code, file)
