from pathlib import Path
from reader_utils.txt_reader import TxtReader
from note_utils.note_translator import NoteTranslator


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
    all_files = sorted(list(txt_path.glob("*.txt")))
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
