import numpy as np
from pathlib import Path
from note_utils.note_digitizer import NoteDigitizer
from reader_utils.txt_reader import TxtReader


def main():
    nd = NoteDigitizer()
    print(nd)

    glob_mini, glob_maxi = 1000, -1
    txt_reader = TxtReader()
    txt_path = Path("data/SymbTr/txt")
    all_files = list(txt_path.glob("*.txt"))
    for file in all_files:
        mini, maxi = txt_reader.read_txt(file, nd)
        if mini < glob_mini:
            glob_mini = mini
        if maxi > glob_maxi:
            glob_maxi = maxi

    print(glob_mini, nd.get_note_by_num(glob_mini))
    print(glob_maxi, nd.get_note_by_num(glob_maxi))


if __name__ == "__main__":
    main()
