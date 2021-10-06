from note_utils.note import Note


class NoteDigitizer:
    """Handles the conversions between the textual representations of TMM pitches and their integer IDs.
    """

    def __init__(self) -> None:
        self.__alphabet = ['do', 're', 'mi', 'fa', 'sol', 'la', 'si']
        self.__flat_alphabet = ['re', 'mi', 'fa', 'sol', 'la', 'si', 'do']
        self.__intervals = [9, 9, 4, 9, 9, 9, 4]
        self.__comma_alp = [
            ['', 'b9'],
            ['#1', 'b8'],
            ['#2', 'b7'],
            ['#3', 'b6'],
            ['#4', 'b5'],
            ['#5', 'b4'],
            ['#6', 'b3'],
            ['#7', 'b2'],
            ['#8', 'b1'],
            ['#9', '']
        ]
        self.__sharp_comma_alp = self.__comma_alp[1:]
        self.__flat_comma_alp = self.__comma_alp[:-1]
        self.__sharp_dictionary = {}
        self.__flat_dictionary = {}
        self.__natural_dictionary = {}

        self.__r_sharp_dictionary = {}
        self.__r_flat_dictionary = {}
        self.__r_natural_dictionary = {}

        self.__build_self()

    def __build_self(self) -> None:
        idx = 2
        idy = 1
        idn = 1
        self.__sharp_dictionary[0] = Note('es', '', '')
        self.__sharp_dictionary[1] = Note('do', 0, '')

        self.__flat_dictionary[0] = Note('es', '', '')
        self.__natural_dictionary[0] = Note('es', '', '')

        for octave_no in range(0, 9):
            # sharps
            for note_no in range(0, len(self.__alphabet)):
                k_idx = 0

                for koma_no in range(0, len(self.__sharp_comma_alp)):
                    if k_idx == self.__intervals[note_no]:
                        break
                    root = self.__alphabet[note_no]
                    self.__sharp_dictionary[idx] = Note(
                        root, octave_no, self.__sharp_comma_alp[koma_no][0])
                    idx += 1
                    k_idx += 1

            # flats
            for note_no in range(0, len(self.__flat_alphabet)):
                for koma_no in reversed(range(0, self.__intervals[note_no])):
                    root = self.__alphabet[(note_no + 1) %
                                           len(self.__alphabet)]
                    octave = octave_no
                    if (note_no + 1) == len(self.__alphabet):
                        octave += 1
                    self.__flat_dictionary[idy] = Note(
                        root, octave, 'b' + str(koma_no + 1))
                    idy += 1

            # naturals
            for note_no in range(0, len(self.__alphabet)):
                self.__natural_dictionary[idn] = Note(
                    self.__alphabet[note_no], octave_no, '')
                idn += self.__intervals[note_no]

        self.__flat_dictionary[idy] = Note('re', 9, 'b9')

        # build reverse dicts
        for k, v in self.__sharp_dictionary.items():
            if k in self.__natural_dictionary:
                self.__r_natural_dictionary[self.__natural_dictionary[k].name] = k

            self.__r_sharp_dictionary[v.name] = k
            self.__r_flat_dictionary[self.__flat_dictionary[k].name] = k

    def __str__(self) -> str:
        str_rep = []

        for k, v in self.__sharp_dictionary.items():
            if k in self.__natural_dictionary:
                str_rep.append(str(k) + '\t' + v.name + '\t' +
                               self.__flat_dictionary[k].name + '\t' +
                               self.__natural_dictionary[k].name)
            else:
                str_rep.append(str(k) + '\t' + v.name + '\t' +
                               self.__flat_dictionary[k].name)

        return "\n".join(str_rep)

    def get_num_by_name(self, note_name: str) -> int:
        """Returns the numeric Id of a textual TMM pitch.

        Args:
            note_name (str): textual representation of TMM pitch

        Returns:
            note_num (int): note's numeric ID, or None

        Examples:
            >>> get_num_by_name("la4#5")
            258

            >>> get_num_by_name("la4#11")
            None
        """
        note_num = None
        if note_name in self.__r_flat_dictionary:
            note_num = self.__r_flat_dictionary[note_name]
        elif note_name in self.__r_sharp_dictionary:
            note_num = self.__r_sharp_dictionary[note_name]
        elif note_name in self.__r_natural_dictionary:
            note_num = self.__r_natural_dictionary[note_name]

        return note_num

    def get_note_by_num(self, note_num: int) -> Note:
        """Returns the textual representation of a TMM pitch w.r.t its ID.

        Args:
            note_num (int): ID of a TMM pitch

        Returns:
            note (Note): Note object, or None

        Examples:
            >>> get_note_by_num(253)
            Note("si", 4, "b9")

            >>> get_note_by_num(-5)
            None
        """
        note = None
        if note_num in self.__natural_dictionary:
            note = self.__natural_dictionary[note_num]
        elif note_num in self.__flat_dictionary:
            note = self.__flat_dictionary[note_num]
        elif note_num in self.__sharp_dictionary:
            note = self.__sharp_dictionary[note_num]

        return note
