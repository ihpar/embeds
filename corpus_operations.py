from reader_utils.corpus_builder_utils import *


def main():
    corpus_path = "dataset_objects/raw_full_corpus"
    """
    # first create the full corpus
    create_full_corpus("dataset_objects/pitches_dict.txt",
                       "data/SymbTr/txt",
                       corpus_path,
                       is_raw=True)
    """
    corpus = read_full_corpus(corpus_path)
    print(len(corpus), corpus[0])


if __name__ == "__main__":
    main()
