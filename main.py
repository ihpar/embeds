from pathlib import Path
from reader_utils.corpus_builder_utils import *
from note_utils.pitch_dictionary import PitchDictionary


def main():
    # create_full_corpus("dataset_objects/pitches_dict.txt",
    #                    "data/SymbTr/txt", "dataset_objects/full_corpus")
    fc = read_full_corpus("dataset_objects/full_corpus")
    print(len(fc))


if __name__ == "__main__":
    main()
