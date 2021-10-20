from pathlib import Path
from typing import Any, List
from note_utils.pitch_dictionary import PitchDictionary
from note_utils.note import Note
from reader_utils.txt_reader import TxtReader
from note_utils.note_translator import NoteTranslator
import pickle
import functools
import operator
from collections import Counter


def create_pitch_dictionary(pitc_dict_file_path: str) -> None:
    """Creates a pitch dictionary from txt formatted SymbTr files.

    Args:
        pitc_dict_file_path (str): Path of the dictionary file to be created.

    Returns:
        None.

    Examples:
    >>> create_pitch_dictionary("dataset_objects/pitches_dict.txt")
    """
    nt = NoteTranslator()
    txt_reader = TxtReader(nt)

    txt_path = Path("data/SymbTr/txt")
    all_files = list(txt_path.glob("*.txt"))
    unique_pitches = set()

    for file in all_files:
        notes = txt_reader.read_txt(file)
        unique_pitches.update(set(notes))

    unique_pitches = sorted(unique_pitches)
    unique_pitches_dict = []
    for pitch_num in unique_pitches:
        unique_pitches_dict.append(str(pitch_num) + ":" +
                                   nt.int_to_name(pitch_num))

    with Path(pitc_dict_file_path).open(mode="w") as pitches_file:
        pitches_file.write("\n".join(unique_pitches_dict))


def create_full_corpus(pitc_dict_file_path: str, symbtr_files_dir: str,
                       target_file_path: str, is_raw: bool = False,
                       as_pitch_classes: bool = False) -> None:
    """Creates a pitch dictionary from txt formatted SymbTr files.

    Args:
        pitc_dict_file_path (str): Path of the dictionary file to be created.
        src_files_dir (str): Path of the text corpus directory.
        target_file_path (str): Path of the target file for storing the full numeric corpus.
        is_raw (bool, optional): Defaults to False. Corpus is created as note strings rather than note IDs when set True.
        as_pitch_classes (bool, optional): Defaults to False. Corpus is created as pitch classes when set True.
    Returns:
        None.

    Examples:
    >>> create_full_corpus("dataset_objects/pitches_dict.txt", 
                            "data/SymbTr/txt",
                            "dataset_objects/full_corpus")
    """
    p_dict = None
    if not is_raw:
        p_dict = PitchDictionary(pitc_dict_file_path)

    txt_path = Path(symbtr_files_dir)
    all_files = list(txt_path.glob("*.txt"))

    nt = NoteTranslator()
    txt_reader = TxtReader(nt)

    full_corpus = []
    for file in all_files:
        notes = txt_reader.read_txt(file, as_names=True)
        if not is_raw:
            notes = [p_dict.get_int_from_str(note) for note in notes]
        if as_pitch_classes:
            notes = [Note.convert_to_pitch_class(note) for note in notes]
        full_corpus.append(notes)

    with Path(target_file_path).open(mode="wb") as corpus_file:
        pickle.dump(full_corpus, corpus_file)


def read_full_corpus(corpus_path: str) -> List[List[int]]:
    """Reads the full corpus from corpus_path location.

    Args:
        corpus_path (str): Path of the full binary corpus.
    Returns:
        List of all songs in the corpus as note ID lists.

    Examples:
    >>> read_full_corpus("dataset_objects/full_corpus")
    [[121, 215, ..., 204], ..., [143, 177, ..., 166]]
    """
    with Path(corpus_path).open(mode="rb") as corpus_file:
        return pickle.load(corpus_file)


def count_pitches(as_names: str = True) -> Counter:
    """A script to count all pitches in the full corpus.

    Args:
        as_names (bool, optional): Defaults to True. 
            If set to False, note IDs are returned as integers instead of names.
    Returns:
        Counts of all pitches in the corpus.

    Examples:
    >>> count_pitches()
    dict_items([('do5', 93865), ('fa5', 45492), ..., ('la3#7', 4)])
    """
    p_dict = PitchDictionary("dataset_objects/pitches_dict.txt")
    corpus = read_full_corpus("dataset_objects/full_corpus")
    flat_corpus = functools.reduce(operator.iconcat, corpus, [])
    if as_names:
        flat_corpus = [p_dict.get_str_from_int(n) for n in flat_corpus]

    return Counter(flat_corpus)


def get_dropped_pitches(drop_limit: int, as_names: str = True) -> List[Any]:
    """"""
    counts = count_pitches(as_names=as_names)
    return [note for note, count in counts.items()
            if count < drop_limit]
