import numpy as np
import pickle
import tensorflow as tf
import functools
import operator
from collections import Counter
from tensorflow.python.data.ops.dataset_ops import Dataset
from tqdm import tqdm
from pathlib import Path
from typing import List
from tensorflow.python.framework.ops import Tensor
from note_utils.pitch_dictionary import PitchDictionary
SEED = 42
AUTOTUNE = tf.data.AUTOTUNE


class DatasetBuilder:
    """Builds the training set from the raw binary corpus file."""

    def __init__(self, corpus_path: str) -> None:
        self.__corpus_path = corpus_path

    def build_word_to_vec_dataset(self, vocab_size: int, window_size: int, num_ns: int, skip_amount: int = 1, drop_limit: int = 0) -> Dataset:
        """Builds the w2v dataset from the full corpus.

        Args:
            vocab_size (int): Path of the target txt file.
            vocab_size (int): Path of the target txt file.
            vocab_size (int): Path of the target txt file.
            skip_amount (int, optional): Defaults to 1. 
                If set to True, note names are returned as strings instead of IDs.
            drop_limit (int, optional): Defaults to 0. 
                If set to a positive number N, notes with frequency < N are dropped from the dataset.

        Returns:
            Dataset object to be consumed by tf model.

        Examples:
            >>> dataset = build_word_to_vec_dataset(123, 4, 10, 1)
        """
        songs = self.get_full_corpus(drop_limit=drop_limit)

        if skip_amount > 1:
            songs = [songs[i] for i in range(0, len(songs), skip_amount)]

        # dataset => (((num_targets,), (num_targets, num_ns+1)), (num_targets, num_ns+1))
        # ((target note), (1 * positive context + num_ns * negative samples)) -> (1, num_ns * 0)
        targets, contexts, labels = [], [], []

        for song in tqdm(songs):
            positive_skip_grams = self.__create_positive_skip_grams(
                song, vocab_size, window_size)

            # Iterate over each positive skip-gram pair to produce training examples
            # with positive context word and negative samples.
            for target_word, context_word in positive_skip_grams:
                context_class = tf.expand_dims(
                    tf.constant([context_word], dtype="int64"), 1)

                negative_sampling_candidates = self.__create_negative_samples(
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

        dataset = tf.data.Dataset.from_tensor_slices(
            ((targets, contexts), labels))

        BATCH_SIZE = 1024
        BUFFER_SIZE = 10000
        dataset = dataset.shuffle(BUFFER_SIZE).batch(
            BATCH_SIZE, drop_remainder=True)

        dataset = dataset.cache().prefetch(buffer_size=AUTOTUNE)
        return dataset

    def __create_positive_skip_grams(self, song: List[int], vocab_size: int, window_size: int):
        positive_skip_grams, _ = tf.keras.preprocessing.sequence.skipgrams(
            song,
            vocabulary_size=vocab_size,
            window_size=window_size,
            negative_samples=0)

        return positive_skip_grams

    def __create_negative_samples(self, context_class: Tensor, num_ns: int, vocab_size: int):
        negative_sampling_candidates, _, _ = tf.random.log_uniform_candidate_sampler(
            true_classes=context_class,
            num_true=1,
            num_sampled=num_ns,
            unique=True,
            range_max=vocab_size,
            seed=SEED,
            name="negative_sampling")

        return negative_sampling_candidates

    def get_full_corpus(self, drop_limit: int = 0) -> List[List[int]]:
        songs = None
        with Path(self.__corpus_path).open(mode="rb") as corpus_file:
            songs = pickle.load(corpus_file)

        if not drop_limit:
            return songs

        flattened_corpus = functools.reduce(operator.iconcat, songs, [])
        counts = Counter(flattened_corpus)
        dropped_notes = [note for note, count in counts.items()
                         if count < drop_limit]

        pd = PitchDictionary("dataset_objects/pitches_dict.txt")
        unk_id = pd.get_unknown_id()

        for song_index, song in enumerate(songs):
            songs[song_index] = [
                unk_id if note in dropped_notes else note for note in song]

        return songs
