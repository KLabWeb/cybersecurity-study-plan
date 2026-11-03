"""The adapter that reaches the disk: the builder files, alone and under a real delivery."""

from pathlib import Path

from pdf_builder.application.delivery import Delivery
from pdf_builder.infrastructure.builder_files import FolderFiles, pdfs_folder

NESTED_FILE = "a/b.txt"
FILE_BYTES = b"x"


def test_folder_files_lists_a_written_file(tmp_path: Path) -> None:
    files = FolderFiles(tmp_path)
    files.write(NESTED_FILE, FILE_BYTES)
    assert files.paths() == [NESTED_FILE]


def test_folder_files_reads_back_what_it_wrote(tmp_path: Path) -> None:
    files = FolderFiles(tmp_path)
    files.write(NESTED_FILE, FILE_BYTES)
    assert files.read(NESTED_FILE) == FILE_BYTES


def test_a_delivery_works_on_a_real_folder(tmp_path: Path) -> None:
    files = FolderFiles(tmp_path)
    files.write("Study_Plan_-_Final.pdf", FILE_BYTES)
    assert Delivery(files).run("2026-10-22")


def test_pdfs_live_in_the_study_plan_folder() -> None:
    folder = pdfs_folder()
    assert folder.name == "Study Plan PDFs"
    assert folder.parent.name == "Study Plan"
