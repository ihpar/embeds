from pathlib import Path
from note_utils.note_translator import NoteTranslator


class PitchDictionary:
    """Handles the conversions between the textual representations of TMM pitches and their integer IDs for training the model.
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

    def get_int_from_str(self, note_name):
        if note_name in self.__note_str_to_int:
            return self.__note_str_to_int[note_name]

        nt_index = self.__note_translator.name_to_int(note_name)
        nt_name = self.__note_translator.int_to_name(nt_index)
        if nt_name in self.__note_str_to_int:
            return self.__note_str_to_int[nt_name]

        return self.__note_str_to_int[self.__unk_str]

    def get_str_from_int(self, note_id):
        if note_id not in self.__note_int_to_str:
            return self.__note_int_to_str[self.__note_str_to_int[self.__unk_str]]
        return self.__note_int_to_str[note_id]
