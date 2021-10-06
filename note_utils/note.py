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

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name
