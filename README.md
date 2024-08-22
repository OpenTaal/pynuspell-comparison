# pynuspell-comparison

Comparing Python moduel for Nuspell with those for Hunspell

## Installation

     sudo apt-get install libnuspell5 libhunspell-1.7 hunspell-en-us \
     hunspell-es hunspell-de-de-frami hunspell-fr-comprehensive hunspell-nl \
     wamerican wspanish wngerman wfrench wdutch
     pip install -U pandas matplotlib pynuspell cyhunspell-py310

## Running

Run

    ./compare.py

and the results are in PNG files. Note the break to limit total test time for suggestions.

## Results

`spell()`

[![](spell-en_US-american-english.png)](spell-en_US-american-english.png)
[![](spell-es_ES-spanish.png)](spell-es_ES-spanish.png)
[![](spell-de_DE_frami-ngerman.png)](spell-de_DE_frami-ngerman.png)
[![](spell-fr-french.png)](spell-fr-french.png)
[![](spell-nl-dutch.png)](spell-nl-dutch.png)
[![](spell-nl-corrections.png)](spell-nl-corrections.png)

`suggest()`

[![](suggest-en_US-american-english.png)](suggest-en_US-american-english.png)
[![](suggest-es_ES-spanish.png)](suggest-es_ES-spanish.png)
[![](suggest-de_DE_frami-ngerman.png)](suggest-de_DE_frami-ngerman.png)
[![](suggest-fr-french.png)](suggest-fr-french.png)
[![](suggest-nl-dutch.png)](suggest-nl-dutch.png)
[![](suggest-nl-corrections.png)](suggest-nl-corrections.png)

`len(suggest())`

[![](lensuggest-en_US-american-english.png)](lensuggest-en_US-american-english.png)
[![](lensuggest-es_ES-spanish.png)](lensuggest-es_ES-spanish.png)
[![](lensuggest-de_DE_frami-ngerman.png)](lensuggest-de_DE_frami-ngerman.png)
[![](lensuggest-fr-french.png)](lensuggest-fr-french.png)
[![](lensuggest-nl-dutch.png)](lensuggest-nl-dutch.png)
[![](lensuggest-nl-corrections.png)](lensuggest-nl-corrections.png)

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
