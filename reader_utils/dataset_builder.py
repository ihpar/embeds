import numpy as np
import pickle
import tensorflow as tf
import tqdm
from pathlib import Path
from typing import List, Tuple
from tensorflow.python.framework.ops import Tensor
SEED = 42
AUTOTUNE = tf.data.AUTOTUNE


class DatasetBuilder:
    """Builds the training set from the raw binary corpus file."""

    def __init__(self, corpus_path: str) -> None:
        self.__corpus_path = corpus_path

    def build_word_to_vec_dataset(self, vocab_size: int, window_size: int, num_ns: int, skip_amount: int = 1):
        songs = None
        with Path(self.__corpus_path).open(mode="rb") as corpus_file:
            songs = pickle.load(corpus_file)

        songs = [songs[i] for i in range(0, len(songs), skip_amount)]

        # dataset => (((num_targets,), (num_targets, num_ns+1)), (num_targets, num_ns+1))
        # ((target note), (1 * positive context + num_ns * negative samples)) -> (1, num_ns * 0)
        targets, contexts, labels = [], [], []

        for song in tqdm.tqdm(songs):
            positive_skip_grams = self.create_positive_skip_grams(
                song, vocab_size, window_size)

            # Iterate over each positive skip-gram pair to produce training examples
            # with positive context word and negative samples.
            for target_word, context_word in positive_skip_grams:
                context_class = tf.expand_dims(
                    tf.constant([context_word], dtype="int64"), 1)

                negative_sampling_candidates = self.create_negative_samples(
                    context_class, num_ns, vocab_size)

                # Build context and label vectors (for one target word)
                negative_sampling_candidates = tf.expand_dims(
                    negative_sampling_candidates, 1)

                context = tf.concat(
                    [context_class, negative_sampling_candidates], 0)

                label = tf.constant([1] + [0]*num_ns, dtype="int64")

                # Append each element from the training example to global lists.
                targets.append(target_word)
                contexts.append(context)
                labels.append(label)

        targets = np.array(targets)
        contexts = np.array(contexts)[:, :, 0]
        labels = np.array(labels)

        BATCH_SIZE = 1024
        BUFFER_SIZE = 10000
        dataset = tf.data.Dataset.from_tensor_slices(
            ((targets, contexts), labels))

        dataset = dataset.shuffle(BUFFER_SIZE).batch(
            BATCH_SIZE, drop_remainder=True)

        dataset = dataset.cache().prefetch(buffer_size=AUTOTUNE)
        return dataset

    def create_positive_skip_grams(self, song: List[int], vocab_size: int, window_size: int) -> List[Tuple]:
        positive_skip_grams, _ = tf.keras.preprocessing.sequence.skipgrams(
            song,
            vocabulary_size=vocab_size,
            window_size=window_size,
            negative_samples=0)

        return positive_skip_grams

    def create_negative_samples(self, context_class: Tensor, num_ns: int, vocab_size: int) -> Tensor:
        negative_sampling_candidates, _, _ = tf.random.log_uniform_candidate_sampler(
            true_classes=context_class,
            num_true=1,
            num_sampled=num_ns,
            unique=True,
            range_max=vocab_size,
            seed=SEED,
            name="negative_sampling")

        return negative_sampling_candidates
