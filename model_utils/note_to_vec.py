import tensorflow as tf
from tensorflow.keras import layers


class Note2Vec(tf.keras.Model):
    def __init__(self, vocab_size, embedding_dim, num_ns, embedding_layer_name):
        super(Note2Vec, self).__init__()

        self.target_embedding = layers.Embedding(vocab_size,
                                                 embedding_dim,
                                                 input_length=1,
                                                 name=embedding_layer_name)

        self.context_embedding = layers.Embedding(vocab_size,
                                                  embedding_dim,
                                                  input_length=num_ns+1)

    def call(self, pair):
        target, context = pair
        # target: (batch, dummy?)  # The dummy axis doesn't exist in TF2.7+
        # context: (batch, context)
        if len(target.shape) == 2:
            target = tf.squeeze(target, axis=1)
        # target: (batch,)
        word_emb = self.target_embedding(target)
        # word_emb: (batch, embed)
        context_emb = self.context_embedding(context)
        # context_emb: (batch, context, embed)
        dots = tf.einsum('be,bce->bc', word_emb, context_emb)
        # dots: (batch, context)
        return dots
