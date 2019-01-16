import argparse
import errno
import math
import os
import random
import subprocess

random.seed(42)

def main(directory):
    """Splits Standoff format corpus at `directory` into train/valid/test partitions.
    """
    filenames = get_filenames(directory)
    filenames = list(set([filename.split('.')[0] for filename in filenames]))
    random.shuffle(filenames)

    train_end = math.floor(0.85 * len(filenames))
    valid_end = train_end + math.floor(int(0.10 * len(filenames)))

    train_filenames = filenames[:train_end]
    valid_filenames = filenames[train_end:valid_end]
    test_filenames = filenames[valid_end:]

    # train
    train_dir = os.path.join(directory, 'train')
    make_dir(train_dir)
    for filename in train_filenames:
        filepath = os.path.join(directory, filename)
        subprocess.call(['mv', filepath + '.ann', train_dir])
        subprocess.call(['mv', filepath + '.txt', train_dir])
    # valid
    valid_dir = os.path.join(directory, 'valid')
    make_dir(valid_dir)
    for filename in valid_filenames:
        filepath = os.path.join(directory, filename)
        subprocess.call(['mv', filepath + '.ann', valid_dir])
        subprocess.call(['mv', filepath + '.txt', valid_dir])
    # test
    test_dir = os.path.join(directory, 'test')
    make_dir(test_dir)
    for filename in test_filenames:
        filepath = os.path.join(directory, filename)
        subprocess.call(['mv', filepath + '.ann', test_dir])
        subprocess.call(['mv', filepath + '.txt', test_dir])

    return True

# https://stackoverflow.com/questions/273192/how-can-i-create-a-directory-if-it-does-not-exist#273227
def make_dir(dir_path):
    """Creates a directory (directory_filepath) if it does not exist.

    Args:
        directory_filepath: filepath of directory to create
    """
    # create output directory if it does not exist
    try:
        os.makedirs(dir_path)
    except OSError as err:
        if err.errno != errno.EEXIST:
            raise

    return True

def get_filenames(directory):
    """
    Returns list of filenames in `directory`.

    Args:
        directory (str): path to input directory

    Returns: list of filenames in `directory`.
    """
    return [os.fsdecode(file) for file in os.listdir(directory)]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=('Splits Standoff format corpus at '
                                                  '`directory` into train/valid/test '
                                                  'partitions.'))
    parser.add_argument('-i', '--input', type=str, required=True, help=('Path to the Standoff '
                                                                        'formatted corpus.'))
    args = parser.parse_args()

    main(args.input)
