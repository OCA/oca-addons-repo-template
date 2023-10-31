from pathlib import Path

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
