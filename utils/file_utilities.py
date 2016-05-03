# __author__ = 'dimitrios'

import pickle
import time
import numpy as np
import sys
import simplejson as json
import os
import csv


def file_exists(filename):
    return os.path.isfile(filename)


def make_dir(filename):
    dir_path = os.path.dirname(filename)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def save_pickle(filename, obj):
    make_dir(filename)
    print '--> Saving ', filename, ' with pickle was ',
    sys.stdout.flush()
    t = time.time()
    with open(filename, 'wb') as gfp:
        pickle.dump(obj, gfp, protocol=pickle.HIGHEST_PROTOCOL)
    print time.time() - t


def save_array(filename, obj):
    make_dir(filename)
    print '--> Saving ', filename, ' with np.array was ',
    sys.stdout.flush()
    t = time.time()
    if not isinstance(obj, np.ndarray):
        obj = np.array(obj)
    np.save(filename, obj)
    print time.time() - t


def save_txt(filename, obj, delimiter=','):
    make_dir(filename)
    print '--> Saving ', filename, ' with np.savetxt was ',
    sys.stdout.flush()
    t = time.time()
    np.savetxt(filename, obj, delimiter=delimiter)
    print time.time() - t


def save_csv(filename, obj, verbose=True):
    """
    saves a list of lists as a csv file
    :param filename: str
    :param obj: list of lists
    :return:
    """
    make_dir(filename)
    if verbose:
        print '--> Saving ', filename, ' with csv writer was ',
        sys.stdout.flush()

    t = time.time()
    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerows(obj)

    if verbose:
        print time.time() - t


def load_pickle(filename):
    print '--> Loading ', filename, ' with pickle was ',
    sys.stdout.flush()
    t = time.time()
    with open(filename, 'rb') as gfp:
        r = pickle.load(gfp)
    print time.time() - t
    return r


def load_array(filename):
    print '--> Loading ', filename, ' with pickle was ',
    sys.stdout.flush()
    t = time.time()
    r = np.load(filename)
    print time.time() - t
    return r


def save_json(filename, obj):
    make_dir(filename)
    print '--> Saving ', filename, ' with json was ',
    sys.stdout.flush()
    t = time.time()
    with open(filename, 'w') as fp:
        json.dump(obj, fp)

    fp.close()
    print time.time() - t


def load_json(filename):
    print '--> Loading ', filename, ' with json was ',
    sys.stdout.flush()
    t = time.time()
    with open(filename, 'r') as fp:
        data = json.load(fp)

    print time.time() - t
    return data


def load_txt(filename, delimiter=','):
    print '--> Loading ', filename, ' with np.loadtxt was ',
    sys.stdout.flush()
    t = time.time()
    d = np.loadtxt(filename, delimiter=delimiter)
    print time.time() - t
    return d
