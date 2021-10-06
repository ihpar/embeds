import pandas as pd

from note_utils.note_digitizer import NoteDigitizer


class TxtReader:
    def __init__(self) -> None:
        pass

    def read_txt(self, file_path: str, note_digitizer: NoteDigitizer) -> None:
        txt_df = pd.read_csv(file_path, delimiter="\t")
        txt_df.dropna(subset=["Nota53"], inplace=True)
        notes = [note.lower() for note in txt_df["Nota53"]]
        mini, maxi = 1000, -1
        for note in notes:
            note_digit = note_digitizer.get_num_by_name(note)
            if (not note_digit) and (note_digit != 0):
                print("Nooo", note_digit, note)
                print(file_path)
            else:
                if note_digit > 0 and note_digit < mini:
                    mini = note_digit
                if note_digit > maxi:
                    maxi = note_digit

        return mini, maxi
