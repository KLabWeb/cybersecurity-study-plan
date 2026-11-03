"""Build the plan PDF: python -m pdf_builder, run from the PDF Builder folder."""

import sys

from pdf_builder.interface.cli import main

if __name__ == "__main__":
    sys.exit(main())
