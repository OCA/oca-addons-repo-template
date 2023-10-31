import re
from pathlib import Path

import pytest
from copier import run_copy
from plumbum import local
from plumbum.cmd import git, pre_commit


def test_hooks_installable(tmp_path: Path, odoo_version: float, cloned_template: Path):
    """Test that pre-commit hooks are installable."""
    data = {
        "odoo_version": odoo_version,
        "repo_slug": "website",
        "repo_name": "Test repo",
        "repo_description": "Test repo description",
    }
    run_copy(str(cloned_template), tmp_path, data=data, defaults=True, unsafe=True)
    with local.cwd(tmp_path):
        git("init")
        pre_commit("install-hooks")


def test_no_readme_generator_conflicts(
    tmp_path: Path, cloned_template: Path, odoo_version: Path
):
    """Test that you can merge more than one PR targeting the same module."""
    if odoo_version < 14.0:
        pytest.skip("Older versions don't generate READMEs")
    # Generate a repo
    data = {
        "odoo_version": odoo_version,
        "repo_slug": "oca-addons-repo-template",
        "repo_name": "Test repo",
        "repo_description": "Test repo description",
    }
    run_copy(str(cloned_template), tmp_path, data=data, defaults=True, unsafe=True)
    with local.cwd(tmp_path):
        git("init")
        git("checkout", "-b", odoo_version)
        pre_commit("install")
        git("add", "-A")
        git("commit", "-m", "[BUILD] hello world", retcode=1)
        git("commit", "-am", "[BUILD] hello world")
        # Create a module
        Path("useless_module").mkdir()
        with local.cwd("useless_module"):
            Path("__init__.py").touch()
            Path("README.rst").touch()
            Path("__manifest__.py").write_text(
                repr(
                    {
                        "name": "Useless module",
                        "version": f"{odoo_version}.0.1.0",
                        "author": "Odoo Community Association (OCA)",
                        "summary": "A module that does nothing.",
                        "license": "LGPL-3",
                        "website": "https://github.com/OCA/oca-addons-repo-template",
                    }
                )
            )
            Path("readme").mkdir()
            Path("readme", "DESCRIPTION.md").write_text(
                "This module is absurdly useless.\n"
            )
            # Commit it and let pre-commit reformat it
            git("add", "-A")
            git("commit", "-m", "[ADD] useless_module", retcode=1)
            git("add", "-A")
            git("commit", "-m", "[ADD] useless_module")
            # At this point, the README contains the dir hash
            orig_digest = re.search(
                r"source digest: (.*)", Path("README.rst").read_text()
            ).group(1)
            assert orig_digest
            assert Path("static", "description", "index.html").is_file()
            # Change the module, and thus the digest in two different branches
            git("checkout", "-b", "change1")
            Path("readme", "USAGE.md").write_text("You cannot use this.\n")
            git("add", "-A")
            git("commit", "-m", "[IMP] useless_module: Usage", retcode=1)
            git("commit", "-am", "[IMP] useless_module: Usage")
            chg1_digest = re.search(
                r"source digest: (.*)", Path("README.rst").read_text()
            ).group(1)
            assert chg1_digest
            git("checkout", odoo_version)
            git("checkout", "-b", "change2")
            Path("readme", "CONFIGURE.md").write_text("You cannot configure this.\n")
            git("add", "-A")
            git("commit", "-m", "[IMP] useless_module: Configuration", retcode=1)
            git("commit", "-am", "[IMP] useless_module: Configuration")
            chg2_digest = re.search(
                r"source digest: (.*)", Path("README.rst").read_text()
            ).group(1)
            assert chg2_digest
            assert orig_digest != chg1_digest != chg2_digest
            git("checkout", odoo_version)
            # Merge the two branches and check there are no conflicts
            git("merge", "change1")
            assert f"source digest: {orig_digest}" not in Path("README.rst").read_text()
            assert f"source digest: {chg1_digest}" in Path("README.rst").read_text()
            assert f"source digest: {chg2_digest}" not in Path("README.rst").read_text()
            git("merge", "change2")
            assert f"source digest: {orig_digest}" not in Path("README.rst").read_text()
            assert f"source digest: {chg1_digest}" in Path("README.rst").read_text()
            assert f"source digest: {chg2_digest}" in Path("README.rst").read_text()
            # Pre-commit can still fix the README
            assert not git("status", "--porcelain=v1")
            pre_commit("run", "-a", retcode=1)
            assert git("status", "--porcelain=v1") == (
                " M useless_module/README.rst\n"
                " M useless_module/static/description/index.html\n"
            )
            assert f"source digest: {orig_digest}" not in Path("README.rst").read_text()
            assert f"source digest: {chg1_digest}" not in Path("README.rst").read_text()
            assert f"source digest: {chg2_digest}" not in Path("README.rst").read_text()
