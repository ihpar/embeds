from pathlib import Path
from note_utils.note_translator import NoteTranslator


class PitchDictionary:
    """Handles the final conversions between the textual representations of TMM pitches and their integer IDs for training the model.
    """

    def __init__(self, pitch_dict_path: str) -> None:
        self.__vocabulary = None
        self.__unk_str = "<unk>"
        self.__note_str_to_int = {}
        self.__note_int_to_str = {}
        self.__note_translator = NoteTranslator()

        with Path(pitch_dict_path).open(mode="r") as p_d_file:
            self.__vocabulary = [line.rstrip().split(":")[1]
                                 for line in p_d_file.readlines()]

        self.__vocabulary = [self.__unk_str] + self.__vocabulary

        for i, v in enumerate(self.__vocabulary):
            self.__note_str_to_int[v] = i
            self.__note_int_to_str[i] = v

    def get_int_from_str(self, note_name: str) -> int:
        """Converts note string to note ID.

        Args:
            note_name (str): String representation of TMM note.
        Returns:
            ID of the given note, or unknown.

        Examples:
        >>> get_int_from_str("la4b3")
        19
        """

        # first check whether the given note str exists in
        # self.__note_str_to_int
        if note_name in self.__note_str_to_int:
            return self.__note_str_to_int[note_name]

        # then check whether the NoteTranslator can translate
        # the given string to int
        nt_index = self.__note_translator.name_to_int(note_name)
        nt_name = self.__note_translator.int_to_name(nt_index)
        if nt_name in self.__note_str_to_int:
            return self.__note_str_to_int[nt_name]

        # note could not be found in both dictionaries,
        # return the ID of <unk>
        return self.__note_str_to_int[self.__unk_str]

    def get_str_from_int(self, note_id: int) -> str:
        """Converts note ID to note string.

        Args:
            note_id (int): ID of the given TMM note.
        Returns:
            String representation of the given note, or <unk>.

        Examples:
        >>> get_str_from_int(19)
        "la4b3"
        """

        # first check whether the given note is not in
        # self.__note_int_to_str, return <unk>
        if note_id not in self.__note_int_to_str:
            return self.__note_int_to_str[self.__note_str_to_int[self.__unk_str]]

        # return note string from self.__note_int_to_str
        return self.__note_int_to_str[note_id]
