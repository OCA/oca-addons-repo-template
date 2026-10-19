from pathlib import Path

from copier import run_copy
from plumbum import local
from plumbum.cmd import git, pre_commit, prek


def test_hooks_installable(tmp_path: Path, odoo_version: float, cloned_template: Path):
    """Test that pre-commit hooks are installable through prek."""
    data = {
        "odoo_version": odoo_version,
        "repo_slug": "website",
        "repo_name": "Test repo",
        "repo_description": "Test repo description",
    }
    run_copy(str(cloned_template), tmp_path, data=data, defaults=True)
    with local.cwd(tmp_path):
        git("init")
        prek("prepare-hooks")


def test_hooks_installable_with_pre_commit(
    tmp_path: Path, odoo_version: float, cloned_template: Path
):
    """Test that the generated config is still usable with plain pre-commit.

    prek is our recommended tool, but the `priority` key it adds to every hook
    must stay a harmless no-op for whoever still uses pre-commit instead.
    """
    data = {
        "odoo_version": odoo_version,
        "repo_slug": "website",
        "repo_name": "Test repo",
        "repo_description": "Test repo description",
    }
    run_copy(str(cloned_template), tmp_path, data=data, defaults=True)
    with local.cwd(tmp_path):
        git("init")
        pre_commit("install-hooks")
