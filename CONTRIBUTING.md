# Contribution guideline

## Set up a development environment

To install CLI apps, you are encouraged to use
[pipx](https://pipxproject.github.io/pipx/).

To develop, you need [Poetry](https://python-poetry.org/).

Poetry will install all other dependencies for you to start hacking right away:

```bash
# Install tools
pip install pipx
pipx install poetry
pipx ensurepath
# Clone
git clone https://github.com/OCA/oca-addons-repo-template
cd oca-addons-repo-template
# Install development environment
poetry install
```

From now on, whenever you want to enter this development environment shell, just:

```bash
poetry shell
```

Specifically, to run tests:

```bash
poetry run pytest
```

## General OCA guidelines

Please follow the official guide from the
[OCA Guidelines page](https://odoo-community.org/page/contributing) where applicable
(most of it relates to Odoo-specific code, while this one is a template and some things
just don't apply here).

## General open source contribution guidelines

Here you will find a good guide so you know how to contribute to this and many other
projects: https://opensource.guide/how-to-contribute/
