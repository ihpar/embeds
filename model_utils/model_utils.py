from tensorflow.keras.losses import CategoricalCrossentropy
from model_utils.note_to_vec import Note2Vec


def build_note_to_vec_model(vocab_size, embedding_dim, num_ns, embedding_layer_name):
    model = Note2Vec(vocab_size, embedding_dim, num_ns, embedding_layer_name)

    model.compile(optimizer='adam',
                  loss=CategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    return model
