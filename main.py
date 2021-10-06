import numpy as np
import pandas as pd
from note_utils.note_digitizer import NoteDigitizer


def main():
    nd = NoteDigitizer()
    note = nd.get_note_by_num(250)
    print(note, note.accidental, note.accidental_direction, note.accidental_amount)


if __name__ == "__main__":
    main()
