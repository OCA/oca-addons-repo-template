# Contribution guideline

## Set up a virtual environment for development

```bash
# Clone
git clone https://github.com/OCA/oca-addons-repo-template
cd oca-addons-repo-template
# Install development environment
python3 -m venv .venv
```

From now on, whenever you want to enter this development environment shell, just:

```bash
source .venv/bin/activate
```

Specifically, to run tests:

```bash
pip install -r test-requirements.txt
pytest
```

## General OCA guidelines

Please follow the official guide from the
[OCA Guidelines page](https://odoo-community.org/page/contributing) where applicable
(most of it relates to Odoo-specific code, while this one is a template and some things
just don't apply here).

## General open source contribution guidelines

Here you will find a good guide so you know how to contribute to this and many other
projects: https://opensource.guide/how-to-contribute/
