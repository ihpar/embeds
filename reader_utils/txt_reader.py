from typing import List
import pandas as pd

from note_utils.note_translator import NoteTranslator


class TxtReader:
    """Reads txt formatted SymbTr files.
    """

    def __init__(self, note_translator: NoteTranslator = None) -> None:
        self.__note_translator = note_translator

    def read_txt(self, file_path: str, as_names: bool = False) -> List[int]:
        """Reads txt formatted SymbTr files and returns all the notes' IDs.

        Args:
            file_path (str): Path of the target txt file.
            as_names (bool, optional): Defaults to False. 
                If set to True, note names are returned as strings instead of IDs.

        Returns:
            List of all notes in given song as IDs or note strings.

        Examples:
            >>> read_txt("song.txt")
            [88, 86, 87, ..., 66]

            >>> read_txt("song.txt", as_names=True)
            ["do5", "re5b4" ..., "la4"]
        """

        if not self.__note_translator:
            raise TypeError("self.__note_translator is not set yet")

        txt_df = pd.read_csv(file_path, delimiter="\t")
        txt_df_notes = txt_df["Nota53"]
        txt_df_notes.dropna(inplace=True)
        txt_df_notes = txt_df_notes.str.lower()

        if as_names:
            return txt_df_notes.tolist()

        return txt_df_notes.map(lambda x: self.__note_translator.name_to_int(x)).tolist()
