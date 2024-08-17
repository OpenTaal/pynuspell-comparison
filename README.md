# pynuspell-comparison

Comparing Python moduel for Nuspell with those for Hunspell

## Installation

     sudo apt-get install libnuspell5 libhunspell-1.7 \
     hunspell-en-us hunspell-es hunspell-de-de hunspell-nl \
     wamerican wspanish wngerman wdutch
     pip install -U pandas matplotlib pynuspell cyhunspell-py310

## Running

Run

    ./compare.py

and the results are in PNG files. Note the break to limit total test time for suggestions.

## Results

Spell

[![](spell-en_US-american-english.png)](spell-en_US-american-english.png)
[![](spell-es_ES-spanish.png)](spell-es_ES-spanish.png)
[![](spell-de_DE-ngerman.png)](spell-de_DE-ngerman.png)
[![](spell-nl-dutch.png)](spell-nl-dutch.png)
[![](spell-nl-corrections.png)](spell-nl-corrections.png)

Suggest

[![](suggest-en_US-american-english.png)](suggest-en_US-american-english.png)
[![](suggest-es_ES-spanish.png)](suggest-es_ES-spanish.png)
[![](suggest-de_DE-ngerman.png)](suggest-de_DE-ngerman.png)
[![](suggest-nl-dutch.png)](suggest-nl-dutch.png)
[![](suggest-nl-corrections.png)](suggest-nl-corrections.png)

## See also

See also:
- https://nuspell.github.io/
- https://pypi.org/project/pynuspell/
- https://pypi.org/project/cyhunspell-py310/
- https://github.com/OpenTaal/opentaal-wordlist

Old:
- https://pypi.org/project/hunspell/
- https://pypi.org/project/chunspell/
- https://pypi.org/project/cyhunspell/
