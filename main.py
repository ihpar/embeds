from pathlib import Path
from reader_utils.corpus_builder_utils import *
from note_utils.pitch_dictionary import PitchDictionary


def main():
    p_dict = PitchDictionary("dataset_objects/pitches_dict.txt")
    corpus = read_full_corpus("dataset_objects/full_corpus")
    fs = corpus[0]
    print([p_dict.get_str_from_int(n) for n in fs])


if __name__ == "__main__":
    main()
