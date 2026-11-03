# Application Security Study Plan: PDF Builder

The PDF Builder makes the plan PDF from the plan's data.

## What's here
- **content/plan.toml**: the plan's text, as data.
- **pdf_builder/**: the code, in four layers.
  - **domain/**: the plan's rules, in plain Python.
  - **application/**: the two use cases, the build and the delivery, and the ports they reach the world through.
  - **infrastructure/**: the adapters: the plan file, the PDF drawing with reportlab, the page reading with pdfplumber, and the files on disk.
  - **interface/**: the two command entries.
- **tests/**: every test, run with pytest.
- **build.sh** and **deliver.sh**: the two commands.

Beside the PDF Builder, **UI Helper Tools/** holds two browser console scripts that open every hidden part of a saved page. They help save sources by hand; they are not part of the build, and no code check or test covers them.

## Commands
Run each from the Build System v2 folder.

Build: `bash "PDF Builder/build.sh"`. It runs every code check first and builds only when all pass. The PDF goes to `Study Plan PDFs/Study_Plan_-_Final.pdf`, in the Study Plan folder beside the Build Systems.

Deliver: `bash "PDF Builder/deliver.sh" YYYY-MM-DD`. It runs the same checks, then copies the Final PDF into `Study Plan PDFs/Cyb Study Plan (<date>)/`. Run the build first.

Tests: `.venv/bin/python -m pytest "PDF Builder/tests"`.

Code checks: `bash Linters/check_all.sh`.

## Requirements
Python 3.12 or later, in a virtual environment at `.venv` in the Build System v2 folder. `requirements.txt` holds the libraries the build needs (reportlab, pdfplumber); `requirements-dev.txt` holds the code checks. The DejaVu fonts are bundled in `pdf_builder/infrastructure/rendering/fonts/`.
