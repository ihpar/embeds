from reader_utils.corpus_builder_utils import *
import matplotlib.pyplot as plt
plt.rcParams["font.size"] = 12
plt.rcParams["font.family"] = "Times New Roman"


def plot_pitch_frequencies():
    counts = count_pitches(as_names=False)

    y_vals = sorted(counts.values(), reverse=True)
    x_vals = [x for x in range(len(y_vals))]

    fig = plt.figure()
    plt.bar(x_vals, y_vals)
    fig.suptitle("Pitch occurence frequencies")
    plt.xlabel("Pitch (sorted by occurence frequencies)")
    plt.ylabel("Pitch occurence frequency")
    plt.show()
