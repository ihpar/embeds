from note_utils.note import Note


class NoteTranslator:
    """Handles the conversions between the textual representations of TMM pitches and their integer IDs.
    """

    def __init__(self) -> None:
        self.__octave_modulus = 53
        self.__lowest_octave = 3
        self.__rest_index = 1

        self.__notes = ["do", "re", "mi", "fa", "sol", "la", "si"]
        self.__comma_indices = [2, 11, 20, 24, 33, 42, 51]

        self.__note_to_int = {n: c for n, c in
                              zip(self.__notes, self.__comma_indices)}
        self.__int_to_note = {c: n for n, c in
                              zip(self.__notes, self.__comma_indices)}

    def name_to_int(self, note_name: str) -> int:
        """Returns the numeric Id of a textual TMM pitch.

        Args:
            note_name (str): Textual representation of TMM pitch.

        Returns:
            Note's numeric ID (int).

        Examples:
            >>> get_num_by_name("fa3#1")
            25
        """

        if note_name in ["es", "rest"]:
            return self.__rest_index

        body, octave, acci_dir, acci_amt = Note.parse_note_str(note_name)

        if acci_dir == "b":
            acci_amt = -1 * acci_amt

        return self.__note_to_int[body] + \
            ((octave - self.__lowest_octave) * self.__octave_modulus) + \
            acci_amt

    def int_to_name(self, note_int: int) -> str:
        """Returns the textual representation of a TMM pitch w.r.t. its ID.

        Args:
            note_int (int): TMM pitch ID.

        Returns:
            Note's textual representation (str).

        Examples:
            >>> int_to_name(25)
            "fa3#1"
        """

        if note_int == self.__rest_index:
            return "es"

        octave, comma = divmod(note_int, self.__octave_modulus)
        octave += self.__lowest_octave
        body_index = 0
        for comma_index in self.__comma_indices:
            if comma - comma_index < 0:
                break
            body_index = comma_index

        if body_index < self.__comma_indices[0]:
            body_index = self.__comma_indices[-1]
            octave -= 1
            comma += body_index + self.__comma_indices[0]

        note_body = self.__int_to_note[body_index]

        comma_str = ""
        if comma - body_index > 0:
            comma_str = "#" + str(comma - body_index)

        return note_body + str(octave) + comma_str
