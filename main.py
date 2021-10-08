from pathlib import Path
from reader_utils.corpus_builder_utils import *
from note_utils.pitch_dictionary import PitchDictionary


def main():
    pitch_dictionary = PitchDictionary(
        Path("dataset_objects/pitches_dict.txt"))


if __name__ == "__main__":
    main()
