from reader_utils.corpus_builder_utils import *
from note_utils.pitch_dictionary import PitchDictionary
from reader_utils.dataset_builder import DatasetBuilder
from model_utils.model_utils import *
import io


def main():
    pd = PitchDictionary("dataset_objects/pitches_dict.txt")

    vocab_size = pd.get_vocabulary_size()
    window_size = 4  # 2, 4
    num_ns = 10  # 2, 5, 10
    embedding_layer_name = "n2v_embedding"

    db = DatasetBuilder("dataset_objects/full_corpus")
    dataset = db.build_word_to_vec_dataset(
        vocab_size, window_size, num_ns, skip_amount=1)

    embedding_dim = 16
    n2v = build_note_to_vec_model(
        vocab_size, embedding_dim, num_ns, embedding_layer_name)

    epochs = 20
    n2v.fit(dataset, epochs=epochs)

    vocab = pd.get_vocabulary()
    weights = n2v.get_layer(embedding_layer_name).get_weights()[0]

    file_suffix = "ws" + str(window_size) + "_ns" + str(num_ns) + \
        "_ed" + str(embedding_dim) + "_ep" + str(epochs)

    vactors_file_name = "vectors_" + file_suffix + ".tsv"
    metadata_file_name = "metadata_" + file_suffix + ".tsv"

    vectors_file = io.open(vactors_file_name, 'w', encoding='utf-8')
    metadata_file = io.open(metadata_file_name, 'w', encoding='utf-8')

    for index, word in enumerate(vocab):
        if index in [0, 1]:  # <unk> and es
            continue
        vec = weights[index]
        vectors_file.write('\t'.join([str(x) for x in vec]) + "\n")
        metadata_file.write(word + "\n")

    vectors_file.close()
    metadata_file.close()


if __name__ == "__main__":
    main()
