from pathlib import Path
from reader_utils.txt_reader import TxtReader
from note_utils.note_translator import NoteTranslator


def main():
    nt = NoteTranslator()
    txt_reader = TxtReader(nt)

    txt_path = Path("data/SymbTr/txt")
    all_files = sorted(list(txt_path.glob("*.txt")))

    total_num_notes = 0
    for file in all_files:
        notes = txt_reader.read_txt(file)
        total_num_notes += len(notes)

    print("Total:", total_num_notes)


if __name__ == "__main__":
    main()
