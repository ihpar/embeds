from reader_utils.corpus_builder_utils import *


def main():
    # corpus_path = "dataset_objects/raw_full_corpus"
    corpus_path = "dataset_objects/raw_full_corpus_pitch_classes"
    """
    # first create the full corpus
    create_full_corpus("dataset_objects/pitches_dict.txt",
                       "data/SymbTr/txt",
                       corpus_path,
                       is_raw=True)
    """

    """ create_full_corpus("dataset_objects/pitches_dict.txt",
                       "data/SymbTr/txt",
                       corpus_path, is_raw=True, as_pitch_classes=True) """
    corpus = read_full_corpus(corpus_path)
    print(len(corpus), corpus[1])


if __name__ == "__main__":
    main()
