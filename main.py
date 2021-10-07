from pathlib import Path
from reader_utils.txt_reader import TxtReader
from note_utils.note_translator import NoteTranslator


def main():
    nt = NoteTranslator()
    txt_reader = TxtReader(nt)

    txt_path = Path("data/SymbTr/txt")
    all_files = sorted(list(txt_path.glob("*.txt")))

    max_note_num = 0
    min_note_num = 1000
    for file in all_files:
        notes = txt_reader.read_txt(file)
        max_of_notes = max(notes)
        min_of_notes = min(notes)
        if max_of_notes > max_note_num:
            max_note_num = max_of_notes

        if min_of_notes < min_note_num:
            min_note_num = min_of_notes

        print(file)
        # print(notes)

    print("Max note num:", max_note_num, "min note num:", min_note_num)


if __name__ == "__main__":
    main()
