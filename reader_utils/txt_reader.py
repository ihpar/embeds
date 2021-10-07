from typing import List
import pandas as pd

from note_utils.note_translator import NoteTranslator


class TxtReader:
    """Reads txt formatted SymbTr files.
    """

    def __init__(self, note_translator: NoteTranslator) -> None:
        self.__note_translator = note_translator

    def read_txt(self, file_path: str) -> List[int]:
        """Reads txt formatted SymbTr files and returns all the notes' IDs.

        Args:
            file_path (int): Path of the target txt file.

        Returns:
            Note's textual representation (str).

        Examples:
            >>> read_txt("song.txt")
            [88, 86, 87, ..., 66]
        """

        txt_df = pd.read_csv(file_path, delimiter="\t")
        txt_df.dropna(subset=["Nota53"], inplace=True)

        return [self.__note_translator.name_to_int(note.lower())
                for note in txt_df["Nota53"]]
