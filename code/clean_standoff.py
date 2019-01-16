#!/usr/bin/env python3
import argparse
import os
import subprocess


# I believe these hang around after a file has been deleted...
def rm_hidden_files(corpus_dir):
    """
    Removes files with filenames beginning with '._'.

    Args:
        corpus_dir (str): path to corpus
    """
    counter = 0
    print('[INFO] Removing hidden files...', end=' ')
    for filename in get_filenames(corpus_dir):
        filepath = os.path.join(filename, corpus_dir)
        # remove any hidden files
        if filename.startswith("._"):
            subprocess.run(["rm", filepath])
            counter += 1
    print('Done. Removed {} file(s).'.format(counter))

def rm_lone_pairs(corpus_dir):
    """
    Removes any lone .ann or .txt in corpus at `corpus_dir`.

    Args:
        corpus_dir (str): path to corpus
    """
    counter = 0
    print('[INFO] Removing lone pairs...', end=' ')
    for filename in get_filenames(corpus_dir):
        # get filepaths
        filepath = os.path.join(corpus_dir, filename)
        txt_filepath = filepath.replace('.ann', '.txt')
        ann_filepath = filepath.replace('.txt', '.ann')
        # for each file in the corpus, if the corresponding
        # .txt or .ann file does not exist, remove its pair.
        if not os.path.isfile(txt_filepath) or not os.path.isfile(ann_filepath):
            if os.path.isfile(txt_filepath): subprocess.run(["rm", txt_filepath])
            if os.path.isfile(ann_filepath): subprocess.run(["rm", ann_filepath])
            counter += 1
    print('Done. Removed {} file pairs.'.format(counter))

def rm_invalid_ann(corpus_dir):
    """
    Removes any annotation file in `corpus_dir` which contains one or more invalid annotations.

    Args:
        corpus_dir (str): path to corpus
    """
    counter = 0
    print('[INFO] Removing invalid .txt .ann pairs...', end=' ')
    for filename in get_filenames(corpus_dir):
        if filename.endswith('.ann'):
            ann_filepath = os.path.join(corpus_dir, filename) # relative filepath
            txt_filepath = ann_filepath.replace('.ann', '.txt') # corresponding text file
            # open <filename>.ann and <filename>.text
            txt_file = open(txt_filepath, 'r')
            ann_file = open(ann_filepath, 'r')
            # read in contents of <filename>.ann and <filename>.text
            text = txt_file.read()
            annotations = ann_file.readlines()
            # if the annotated entity text in the annotation file does not exactly match
            # the labeled text in the text file, remove both <filename>.ann and <filename>.text
            for ann in annotations:
                split_line = ann.split('\t')
                start_idx = int(split_line[1].split(' ')[1])
                end_idx = int(split_line[1].split(' ')[2])
                entity = split_line[2].strip()
                if text[start_idx:end_idx] != entity:
                    ann_file.close()
                    txt_file.close()
                    # remove offending files
                    subprocess.run(["rm", ann_filepath])
                    subprocess.run(["rm", txt_filepath])
                    counter += 1
                    # early exit the loop, only looking for 1 or more invalid annotations.
                    break
            # close files on each loop
            ann_file.close()
            txt_file.close()
    print('Done. Removed {} file pairs.'.format(counter))

def get_filenames(directory):
    """
    Returns list of filenames in `directory`.

    Args:
        directory (str): path to input directory

    Returns: list of filenames in `directory`.
    """
    return [os.fsdecode(file) for file in os.listdir(directory)]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Performs validation/cleaning on Standoff format corpus.')
    parser.add_argument('-i', '--input', type=str, required=True, help='Filepath to the Standoff formatted corpus.')
    args = parser.parse_args()

    rm_hidden_files(args.input)
    rm_lone_pairs(args.input)
    rm_invalid_ann(args.input)
