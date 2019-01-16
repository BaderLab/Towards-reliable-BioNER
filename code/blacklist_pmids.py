#!/usr/bin/env python3
"""Removes any blacklisted documents from a corpus in Standoff formant.

For a given blacklist containing PMIDs, one per line, removes any file in a Standoff-formated
corpus with a blacklisted PMID as filename (i.e., <PMID>.ann and <PMID>.txt files are removed for
all PMIDs in the blacklist).

Run the script with:

```
python3 remove_blacklisted.py -i path/to/standoff/corpus -b path/to/blacklist.txt
```
"""
import argparse
import os
import subprocess


def main(corpus_dir, blacklist):
    """Removes all *.ann and *.txt files from `corpus_dir` based on the PMIDs given in `blacklist`.

    For a given blacklist file (`blacklist`) which contains a list of PMIDs (one per line), removes
    all *.txt and *.ann files from a given corpus in Standoff format (`corpus_dir`) which match any
    of these PMIDs.

    Args:
        corpus_dir (str): path to a corpus in Standoff format.
        blacklist (str): path to a file which contains PMIDs, one per line.
    """
    counter = 0
    print('[INFO] Removing blacklisted files...', end=' ')
    with open(blacklist, 'r') as f:
        blacklist = f.readlines()

    for pmid in blacklist:
        txt_filepath = os.path.join(corpus_dir, pmid.strip() + '.txt')
        ann_filepath = os.path.join(corpus_dir, pmid.strip() + '.ann')
        if os.path.isfile(txt_filepath):
            counter += 1
            subprocess.call(['rm', txt_filepath])
        if os.path.isfile(ann_filepath):
            subprocess.call(['rm', ann_filepath])
    print('Done. Removed {} file(s).'.format(counter))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=('Removes all .ann and .txt file from a given '
                                                  'corpus in Standoff format based on a '
                                                  'given blacklist.'))
    parser.add_argument('-i', '--input', type=str, required=True, help=('Path to the Standoff '
                                                                        'formatted corpus.'))
    parser.add_argument('-b', '--blacklist', type=str, required=True, help='Path to the Blacklist.')
    args = parser.parse_args()

    main(args.input, args.blacklist)
