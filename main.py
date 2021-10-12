from reader_utils.corpus_builder_utils import *
from note_utils.pitch_dictionary import PitchDictionary
from reader_utils.dataset_builder import DatasetBuilder
from model_utils.model_utils import *
import io


def main():
    pd = PitchDictionary("dataset_objects/pitches_dict.txt")

    vocab_size = pd.get_vocabulary_size()
    window_size = 2
    num_ns = 4
    embedding_dim = 32
    embedding_layer_name = "n2v_embedding"

    db = DatasetBuilder("dataset_objects/full_corpus")
    dataset = db.build_word_to_vec_dataset(
        vocab_size, window_size, num_ns, skip_amount=10)

    n2v = build_note_to_vec_model(
        vocab_size, embedding_dim, num_ns, embedding_layer_name)

    n2v.fit(dataset, epochs=20)

    vocab = pd.get_vocabulary()
    weights = n2v.get_layer(embedding_layer_name).get_weights()[0]
    out_v = io.open('vectors.tsv', 'w', encoding='utf-8')
    out_m = io.open('metadata.tsv', 'w', encoding='utf-8')

    for index, word in enumerate(vocab):
        vec = weights[index]
        out_v.write('\t'.join([str(x) for x in vec]) + "\n")
        out_m.write(word + "\n")

    out_v.close()
    out_m.close()


if __name__ == "__main__":
    main()
