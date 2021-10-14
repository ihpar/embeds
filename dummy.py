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


def find_cos_similar(note_name):
    dir_path = "dataset_objects/dropped_500_vectors/"
    cleaned_meta_path = dir_path + "clean_metadata_ws4_ns10_ed16_ep20.tsv"
    cleaned_vector_path = dir_path + "clean_vectors_ws4_ns10_ed16_ep20.tsv"

    meta_lines, vector_lines = None, None
    vector_dict = {}
    with Path(cleaned_meta_path).open("r") as meta_file, Path(cleaned_vector_path).open("r") as vector_file:
        meta_lines = meta_file.read().splitlines()
        vector_lines = vector_file.read().splitlines()
        for ml, vl in zip(meta_lines, vector_lines):
            vector_dict[ml] = np.array([float(v) for v in vl.split("\t")])

    # print(note_name, vector_dict[note_name])
    max_sim = -1
    target_vec = vector_dict[note_name]
    closest_pitch = [None, None]
    for n, v in vector_dict.items():
        if n == note_name:
            continue

        similarity = np.dot(target_vec, v) / \
            (np.linalg.norm(target_vec) * np.linalg.norm(v))

        if similarity > max_sim:
            max_sim = similarity
            closest_pitch[0] = n
            closest_pitch[1] = v

    print(note_name, "=>", closest_pitch[0], ":", closest_pitch[1])


def main():
    find_cos_similar("sol4#4")


if __name__ == "__main__":
    main()
