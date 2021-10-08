from pathlib import Path
from reader_utils.corpus_builder_utils import *
from note_utils.pitch_dictionary import PitchDictionary


def main():
    p_dict = PitchDictionary(
        Path("dataset_objects/pitches_dict.txt"))
    print(p_dict.get_str_from_int(1))


if __name__ == "__main__":
    main()
