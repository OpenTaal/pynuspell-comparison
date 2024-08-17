# pynuspell-comparison

Comparing Python moduel for Nuspell with those for Hunspell

## Installation

     sudo apt-get install libnuspell5 libhunspell-1.7
     hunspell-en-us hunspell-es \
     hunspell-nl wamerican wspanish wdutch
     pip install -U pandas matplotlib pynuspell cyhunspell-py310

## Running

Run

    ./compare.py

and the results are in PNG files. Note the break to limit total test time for suggestions.

## Results

Spell

[![](en_US-american-english-spell.png)](en_US-american-english-spell.png)
[![](es_ES-spanish-spell.png)](es_ES-spanish-spell.png)
[![](nl-dutch-spell.png)](nl-dutch-spell.png)

Suggest

[![](en_US-american-english-suggest.png)](en_US-american-english-suggest.png)
[![](es_ES-spanish-suggest.png)](es_ES-spanish-suggest.png)
[![](nl-dutch-suggest.png)](nl-dutch-suggest.png)

## See also

See also:
- https://pypi.org/project/pynuspell/
- https://pypi.org/project/cyhunspell-py310/

Old:
- https://pypi.org/project/hunspell/
- https://pypi.org/project/chunspell/
- https://pypi.org/project/cyhunspell/
