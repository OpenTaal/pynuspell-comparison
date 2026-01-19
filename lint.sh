#!/usr/bin/env sh

. .venv/bin/activate
FILES=*.py
echo '* PYDOCSTYLE'
pydocstyle --convention=numpy $FILES
echo '* FLAKE8'
flake8 --ignore=E501 $FILES
echo '* PYLINT'
# --import-graph a.gv
# --ignore-imports
pylint --disable=C0301 --notes FIXME --extension-pkg-allow-list hunspell,ucto --import-graph pylint-imports.gv $FILES
echo '* PYFLAKES'
pyflakes $FILES
echo '* PYRIGHT-ALRIGHT'
pyright-alright $FILES
echo '* MYPY'
# --ignore-missing-imports --implicit-optional
mypy $FILES