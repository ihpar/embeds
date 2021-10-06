from typing import Tuple


class Note:
    """Encapsulates necessary details related to a TMM note.

    Attributes:
      root_note (str): Stripped note name without octave or accidental identifiers. Ex: "re"
      octave (int): Note's octave number.
      accidental (str): TMM accidental identifier. Ex: "b5"
      accidental_direction (str): Accidental direction. (None, "b", or "#")
      accidental_amount (int): Magnitude of accidental. (None, or int) 
      name (str): Full note name. Ex: "la4b5"
    """

    def __init__(self, root, octave, accidental) -> None:
        self.root_note = root
        self.octave = octave
        self.accidental = accidental

        self.accidental_direction = None
        self.accidental_amount = None
        if self.accidental:
            self.accidental_direction = str(self.accidental[0])
            self.accidental_amount = int(self.accidental[1])

        self.name = root + str(octave) + accidental

    @staticmethod
    def parse_note_str(note_str: str) -> Tuple[str, int, str, int]:
        accidental_amount = 0
        accidental_direction = None
        note_body = note_str

        if "b" in note_str:  # note has a flat accidental
            accidental_direction = "b"
        elif "#" in note_str:  # note has a sharp accidental
            accidental_direction = "#"

        if accidental_direction:
            accidental_index = note_str.find(accidental_direction) + 1
            accidental_amount = int(note_str[accidental_index:])
            note_body = note_str[:accidental_index-1]

        octave_no = int(note_body[-1])
        note_body = note_body[:-1]

        return note_body, octave_no, accidental_direction, accidental_amount

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name
