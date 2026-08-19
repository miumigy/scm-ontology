from pathlib import Path
import re


def test_primary_launch_release_package_surface_exists():
    root = Path(__file__).resolve().parents[1]
    required = (
        "README.md",
        "README.ja.md",
        "LICENSE",
        "CHANGELOG.md",
        "CONTRIBUTING.md",
        "BACKLOG.yaml",
        "docs/launch/README.md",
        "docs/launch/primary-launch.md",
        "docs/launch/golden-path.md",
        "docs/launch/demo.md",
        "docs/launch/acceptance.md",
        "docs/launch/limitations.md",
        "docs/launch/release-checklist.md",
        "docs/launch/release-notes-v0.1.0.md",
    )
    missing = [path for path in required if not (root / path).exists()]
    assert not missing, missing


def test_package_version_is_0_1_0():
    root = Path(__file__).resolve().parents[1]
    pyproject = (root / "pyproject.toml").read_text(encoding="utf-8")
    assert re.search(r'^version\s*=\s*"0\.1\.0"$', pyproject, re.MULTILINE)


def test_release_docs_use_release_oriented_numbering():
    root = Path(__file__).resolve().parents[1]
    backlog = (root / "BACKLOG.yaml").read_text(encoding="utf-8")
    assert "post_primary_launch" in backlog
    assert "do not extend" in backlog

    handoff = (root / "docs/primary-launch-handoff.md").read_text(encoding="utf-8")
    assert "v0.1.0" in handoff
    assert "Do **not** create an endless new sequence" in handoff
