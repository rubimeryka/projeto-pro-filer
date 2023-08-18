import pytest
from pro_filer.actions.main_actions import show_preview  # NOQA


@pytest.fixture
def context_with_files_and_dirs():
    return {
        "all_files": [
            "src/__init__.py",
            "src/app.py",
            "src/utils/__init__.py",
            "src/test1",
            "src/test2",
            "src/xxxxx",
        ],
        "all_dirs": ["src", "src/utils"],
    }


@pytest.fixture
def empty_context():
    return {"all_files": [], "all_dirs": []}


def test_preview_with_files_and_dirs(capsys, context_with_files_and_dirs):
    show_preview(context_with_files_and_dirs)
    captured = capsys.readouterr()
    expected_output = (
        "Found 6 files and 2 directories\n"
        "First 5 files: ['src/__init__.py', 'src/app.py', "
        "'src/utils/__init__.py', 'src/test1', 'src/test2']\n"
        "First 5 directories: ['src', 'src/utils']\n"
    )
    assert captured.out == expected_output


def test_preview_with_no_files_or_dirs(capsys, empty_context):
    show_preview(empty_context)
    captured = capsys.readouterr()
    expected_output = "Found 0 files and 0 directories\n"
    assert captured.out == expected_output
