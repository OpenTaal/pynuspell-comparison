#!/usr/bin/env sh

FILES='compare.py'
echo '*PYDOCSTYLE'
pydocstyle --convention=numpy $FILES
echo '* FLAKE8'
# --ignore E252
flake8 $FILES
echo '* PYLINT'
# --import-graph a.gv
# --ignore-imports
pylint --notes FIXME --extension-pkg-allow-list hunspell,ucto --import-graph pylint-imports.gv $FILES
echo '* PYFLAKES'
pyflakes $FILES
echo '* MYPY'
# --implicit-optional
mypy --ignore-missing-imports --implicit-optional $FILES
