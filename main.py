import numpy as np
import pandas as pd
from note_utils.note_digitizer import NoteDigitizer


def main():
    nd = NoteDigitizer()
    note = nd.get_num_by_name("la4#1")
    print(note)


if __name__ == "__main__":
    main()
