from pro_filer.actions.main_actions import show_details  # NOQA
from unittest.mock import Mock, patch
import pytest
import time

# Constants
TIME_STAMP = time.mktime(time.strptime("2023-08-16", "%Y-%m-%d"))


# Mocks
def create_mock_os_path(
        exists=True, isdir=False, size=100, splitext=("Trybe_logo", ".png")
        ):
    mock = Mock()
    mock.return_value = exists
    mock.isdir.return_value = isdir
    mock.getsize.return_value = size
    mock.splitext.return_value = splitext
    mock.getmtime.return_value = TIME_STAMP
    return mock


def test_show_details_file_not_found(capsys):
    mock_os_path_exists = create_mock_os_path(exists=False)
    file_path = {"base_path": "/home/trybe/????"}

    with patch("os.path.exists", mock_os_path_exists):
        show_details(file_path)
        captured = capsys.readouterr()
        assert captured.out == "File '????' does not exist\n"


@pytest.mark.parametrize(
    "context, expected_output",
    [
        (
            {"base_path": "/home/trybe/Downloads/Trybe_logo.png"},
            (
                "File name: Trybe_logo.png\n"
                "File size in bytes: 100\n"
                "File type: file\n"
                "File extension: .png\n"
                "Last modified date: 2023-08-16\n"
            ),
        )
    ],
)
def test_show_details_file(capsys, context, expected_output):
    mock_os_path = create_mock_os_path()

    with patch("os.path", mock_os_path):
        show_details(context)
        captured = capsys.readouterr()
        assert captured.out == expected_output


@pytest.mark.parametrize(
    "context, expected_output",
    [
        (
            {"base_path": "/home/trybe/Downloads"},
            (
                "File name: Downloads\n"
                "File size in bytes: 100\n"
                "File type: directory\n"
                "File extension: [no extension]\n"
                "Last modified date: 2023-08-16\n"
            ),
        )
    ],
)
def test_show_details_directory(capsys, context, expected_output):
    mock_os_path = create_mock_os_path(isdir=True, splitext=("Downloads", ""))

    with patch("os.path", mock_os_path):
        show_details(context)
        captured = capsys.readouterr()
        assert captured.out == expected_output
