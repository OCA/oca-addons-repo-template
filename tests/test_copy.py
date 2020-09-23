from pathlib import Path

import yaml
from copier import copy

# Change this one in case it becomes a mandatory check
SOME_PYLINT_OPTIONAL_CHECK = "too-complex"

# These are arbitrarily picked, but in case anything changes (very unlikely),
# modify these variables to avoid failing tests
REPO_SLUG = "server-tools"
REPO_ID = 149


def test_bootstrap(tmp_path: Path, odoo_version: float, cloned_template: Path):
    """Test that a project is properly bootstrapped."""
    data = {
        "odoo_version": odoo_version,
        "repo_slug": REPO_SLUG,
        "repo_name": "Test repo",
        "repo_description": "Test repo description",
    }
    copy(str(cloned_template), tmp_path, data=data, force=True)
    # When loading YAML files, we are also testing their syntax is correct, which
    # can be a little bit tricky due to the way both Jinja and YAML handle whitespace
    answers = yaml.safe_load((tmp_path / ".copier-answers.yml").read_text())
    for key, value in data.items():
        assert answers[key] == value
    # Assert linter config files look like they were looking before
    pylintrc_mandatory = (tmp_path / ".pylintrc-mandatory").read_text()
    assert "disable=all\n\nenable=" in pylintrc_mandatory
    assert f"valid_odoo_versions={odoo_version}" in pylintrc_mandatory
    assert SOME_PYLINT_OPTIONAL_CHECK not in pylintrc_mandatory
    pylintrc_optional = (tmp_path / ".pylintrc").read_text()
    assert "disable=all\n\n# This .pylintrc" in pylintrc_optional
    assert f"valid_odoo_versions={odoo_version}" in pylintrc_optional
    assert SOME_PYLINT_OPTIONAL_CHECK in pylintrc_optional
    flake8 = (tmp_path / ".flake8").read_text()
    assert "[flake8]" in flake8
    isort = (tmp_path / ".isort.cfg").read_text()
    assert "[settings]" in isort
    assert not (tmp_path / ".gitmodules").is_file()
    # Assert other files
    contributing = tmp_path / "CONTRIBUTING.md"
    assert contributing.is_file()
    license_ = (tmp_path / "LICENSE").read_text()
    assert "GNU AFFERO GENERAL PUBLIC LICENSE" in license_
    # Assert badges in readme; this is testing the repo_id macro
    readme = (tmp_path / "README.md").read_text()
    assert (
        f"[![Runbot Status](https://runbot.odoo-community.org/runbot/badge/flat/{REPO_ID}/{odoo_version}.svg)](https://runbot.odoo-community.org/runbot/repo/github-com-oca-{REPO_SLUG}-{REPO_ID})"  # noqa: B950
        in readme
    )
    assert (
        f"[![Build Status](https://travis-ci.com/OCA/{REPO_SLUG}.svg?branch={odoo_version})](https://travis-ci.com/OCA/{REPO_SLUG})"  # noqa: B950
        in readme
    )
    assert (
        f"[![codecov](https://codecov.io/gh/OCA/{REPO_SLUG}/branch/{odoo_version}/graph/badge.svg)](https://codecov.io/gh/OCA/{REPO_SLUG})"  # noqa: B950
        in readme
    )
    odoo_version_tr = str(odoo_version).replace(".", "-")
    assert (
        f"[![Translation Status](https://translation.odoo-community.org/widgets/{REPO_SLUG}-{odoo_version_tr}/-/svg-badge.svg)](https://translation.odoo-community.org/engage/{REPO_SLUG}-{odoo_version_tr}/?utm_source=widget)"  # noqa: B950
        in readme
    )
    assert "# Test repo" in readme
    assert data["repo_description"] in readme
    # Assert no stuff specific for this repo is found
    garbage = (
        "setup.cfg",
        "tests",
        "vendor",
        "copier.yml",
        ".gitmodules",
        "poetry.lock",
        "pyproject.toml",
    )
    for file_ in garbage:
        assert not (tmp_path / file_).exists()
