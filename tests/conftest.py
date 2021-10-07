import os
from pathlib import Path

import pytest
import yaml
from plumbum import local
from plumbum.cmd import git

PROJECT_ROOT = Path(__file__).parent.parent
COPIER_SETTINGS = yaml.safe_load((PROJECT_ROOT / "copier.yml").read_text())

# Different tests test different Odoo versions
ALL_ODOO_VERSIONS = tuple(COPIER_SETTINGS["odoo_version"]["choices"])
LAST_ODOO_VERSION = max(ALL_ODOO_VERSIONS)
SELECTED_ODOO_VERSIONS = (
    frozenset(map(float, os.environ.get("SELECTED_ODOO_VERSIONS", "").split()))
    or ALL_ODOO_VERSIONS
)


@pytest.fixture(params=ALL_ODOO_VERSIONS)
def odoo_version(request) -> float:
    """Returns any usable odoo version."""
    if request.param not in SELECTED_ODOO_VERSIONS:
        pytest.skip("odoo version not in selected range")
    return request.param


@pytest.fixture()
def cloned_template(tmp_path_factory):
    """This repo cloned to a temporary destination.

    The clone will include dirty changes, and it will have a 'test' tag in its HEAD.

    It returns the local `Path` to the clone.
    """
    patches = [git("diff", "--cached"), git("diff")]
    with tmp_path_factory.mktemp("cloned_template_") as dirty_template_clone:
        git("clone", PROJECT_ROOT, dirty_template_clone)
        with local.cwd(dirty_template_clone):
            for patch in patches:
                if patch:
                    (git["apply", "--reject"] << patch)()
                    git("add", ".")
                    git(
                        "commit",
                        "--author=Test<test@test>",
                        "--message=dirty changes",
                        "--no-gpg-sign",
                        "--no-verify",
                    )
            git("tag", "--force", "v999999999.999999999.999999999")
        yield dirty_template_clone
