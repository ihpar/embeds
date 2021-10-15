from reader_utils.corpus_builder_utils import *
from pathlib import Path
import numpy as np


def clean_below_500():
    dropped_pitches = get_dropped_pitches(500, as_names=True)

    dir_path = "dataset_objects/dropped_500_vectors/"
    meta_path = dir_path + "metadata_ws4_ns10_ed16_ep20.tsv"
    vector_path = dir_path + "vectors_ws4_ns10_ed16_ep20.tsv"
    meta_lines, vector_lines = None, None

    with Path(meta_path).open("r") as meta_file, Path(vector_path).open("r") as vector_file:
        meta_lines = meta_file.read().splitlines()
        vector_lines = vector_file.read().splitlines()

    cleaned_meta_path = dir_path + "clean_metadata_ws4_ns10_ed16_ep20.tsv"
    cleaned_vector_path = dir_path + "clean_vectors_ws4_ns10_ed16_ep20.tsv"

    with Path(cleaned_meta_path).open("w") as met_f, Path(cleaned_vector_path).open("w") as vec_f:
        for ml, vl in zip(meta_lines, vector_lines):
            if ml in dropped_pitches:
                continue
            met_f.write(ml + "\n")
            vec_f.write(vl + "\n")


def cosine_similarity(v1, v2):
    denominator = np.linalg.norm(v1) * np.linalg.norm(v2)
    if np.isclose(denominator, 0, atol=1e-32):
        return 0
    return np.dot(v1, v2) / denominator


def get_vectors(dir_path, meta_file, vector_file):
    meta_path = dir_path + meta_file
    vector_path = dir_path + vector_file

    meta_lines, vector_lines = None, None
    vector_dict = {}
    with Path(meta_path).open("r") as meta_file, Path(vector_path).open("r") as vector_file:
        meta_lines = meta_file.read().splitlines()
        vector_lines = vector_file.read().splitlines()
        for ml, vl in zip(meta_lines, vector_lines):
            vector_dict[ml] = np.array([float(v) for v in vl.split("\t")])
    return vector_dict


def find_cos_similar(note_name):
    vector_dict = get_vectors("dataset_objects/dropped_500_vectors/",
                              "clean_metadata_ws4_ns10_ed16_ep20.tsv",
                              "clean_vectors_ws4_ns10_ed16_ep20.tsv")

    target_vec = vector_dict[note_name]
    similarities = []
    for n, v in vector_dict.items():
        if n == note_name:
            continue

        similarity = cosine_similarity(target_vec, v)
        similarities.append((n, similarity, v))

    return sorted(similarities, key=lambda tup: tup[1], reverse=True)


def a_is_to_b_as_c_is_to(notes_a_b, note_c):
    vector_dict = get_vectors("dataset_objects/dropped_500_vectors/",
                              "clean_metadata_ws4_ns10_ed16_ep20.tsv",
                              "clean_vectors_ws4_ns10_ed16_ep20.tsv")
    n_a, n_b = notes_a_b
    if n_a not in vector_dict or n_b not in vector_dict or note_c not in vector_dict:
        return None

    b_minus_a = vector_dict[n_b] - vector_dict[n_a]
    vec_c = vector_dict[note_c]
    max_sim = -100
    note_d = None
    for n, v in vector_dict.items():
        if n == note_c:
            continue

        cos_sim = cosine_similarity(b_minus_a, (v - vec_c))
        if cos_sim > max_sim:
            max_sim = cos_sim
            note_d = (n, v)

    return note_d


def main():
    similarities = find_cos_similar("la4")[:5]
    for s in similarities:
        print(s[0], s[1])

    n_d = a_is_to_b_as_c_is_to(("la4", "re5"), "re4")
    print(n_d)


if __name__ == "__main__":
    main()
