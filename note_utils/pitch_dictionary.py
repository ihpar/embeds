from pathlib import Path


class PitchDictionary:
    def __init__(self, pitch_dict_path: Path) -> None:
        self.__vocabulary = None
        with pitch_dict_path.open(mode="r") as p_d_file:
            self.__vocabulary = [line.rstrip().split(":")[1]
                                 for line in p_d_file.readlines()]

        print(self.__vocabulary)
