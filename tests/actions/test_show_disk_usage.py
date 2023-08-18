from pro_filer.actions.main_actions import show_disk_usage  # NOQA
import pytest
import os


@pytest.fixture
def create_files(tmp_path):
    file_one = tmp_path / "file_one.txt"
    file_one.write_text("Test content")

    file_two = tmp_path / "file_two.txt"
    file_two.write_text("Another test content")

    return {"all_files": [str(file_one), str(file_two)]}


def test_show_disk_usage(capsys, create_files):
    show_disk_usage(create_files)

    captured = capsys.readouterr()

    output_output_lines = captured.out.strip().split("\n")

    assert "file_two.txt" in output_output_lines[0]
    assert "Total size:" in output_output_lines[2]


def test_show_disk_usage_empty_files(capsys, create_files):
    show_disk_usage(create_files)

    captured = capsys.readouterr()
    output_output_lines = captured.out.split("\n")

    assert "file_two.txt" in output_output_lines[0]
    assert "file_one.txt" in output_output_lines[1]
    assert "Total size:" in output_output_lines[2]


def test_show_disk_usage_sorting(capsys, create_files):
    show_disk_usage(create_files)

    captured = capsys.readouterr()
    output_lines = captured.out.split("\n")

    assert "file_two.txt" in output_lines[0]
    assert "file_one.txt" in output_lines[1]
    assert "Total size:" in output_lines[2]


def test_show_disk_usage_correct_files(capsys, create_files):
    show_disk_usage(create_files)

    captured = capsys.readouterr()
    assert "Total size:" in captured.out


def test_show_disk_usage_total_size(capsys, create_files):
    total_size = sum(
        os.path.getsize(file) for file in create_files["all_files"]
    )

    show_disk_usage(create_files)

    captured = capsys.readouterr()
    assert f"Total size: {total_size}" in captured.out
