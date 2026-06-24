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
    run_copy(str(cloned_template), tmp_path, data=data, defaults=True)
    with local.cwd(tmp_path):
        git("init")
        pre_commit("install-hooks")
        Path("test.xml").write_text(
            '<?xml version="1.0" encoding="utf-8" ?>\n'
            '<root><should    be="formatted" /></root>'
        )
        git("add", "test.xml")
        pre_commit("run", "prettier", retcode=1)
        formatted = (
            '<?xml version="1.0" encoding="utf-8" ?>\n'
            '<root><should be="formatted" /></root>\n'
        )
        assert Path("test.xml").read_text() == formatted
