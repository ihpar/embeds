import numpy as np
from pathlib import Path
from note_utils.note_digitizer import NoteDigitizer
from reader_utils.txt_reader import TxtReader
from note_utils.note_translator import NoteTranslator


def main():
    nt = NoteTranslator()
    txt_reader = TxtReader()

    txt_path = Path("data/SymbTr/txt")
    all_files = list(txt_path.glob("*.txt"))

    for file in all_files:
        txt_reader.read_txt(file, nt)


if __name__ == "__main__":
    main()
