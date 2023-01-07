# ___  _   _ ___ _  _ ____ _  _ _ ____    ___  ____ ___
# |__]  \_/   |  |__| |  | |\ | | |       |__] [__   |
# |      |    |  |  | |__| | \| | |___    |__] ___]  |
# <=<=<<https://github.com/squillero/pythonic-bst>>=>=>

# Copyright 2022 Giovanni Squillero.
# SPDX-License-Identifier: 0BSD

#bumpver update --patch
pip-compile pyproject.toml
python -m build
twine upload dist/*