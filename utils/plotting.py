# __author__ = 'dimitrios'
import matplotlib
matplotlib.use('Agg')   # for server use
import matplotlib.pyplot as plt

def plot_bars(data, legend, color='blue'):
    plt.bar(range(len(data)), data, color=color, label=legend, alpha=0.75)


def save_bars(filename, data, names, xlabel=None):
    """
    saves a histogram in the filename
    data is a list of lists
    all sublists must have the same number of elements
    :param filename:
    :param data:
    :return:
    """
    colors = ['blue', 'red', 'green', 'cyan', 'yellow']
    i = 0
    for d in data:
        plot_bars(d, names[i], color=colors[i])
        i += 1

    plt.legend(loc='upper right')
    if xlabel is not None:
        plt.xlabel(xlabel)
    plt.grid(True)
    plt.savefig(filename)
