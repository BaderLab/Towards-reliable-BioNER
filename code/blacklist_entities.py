"""Generates a blacklist of entities for a given SSC based on a collection of GSCs and, optionally,
removes these entities from the SSC.

Usage:

To generate a blacklist for a given SSC and collection of GSCs. Assumes all copora in in CoNLL-like
format and annotated with a BIO tag scheme.

```
python blacklist.py --gsc path/to/gscs --ssc path/to/ssc --entity DISO --output path/to/output
```

To remove the blacklisted entities from the SSC

```
python blacklist.py --gsc path/to/gscs --ssc path/to/ssc --entity DISO --output path/to/output --replace
```

To use an existing blacklist to remove entities from a SSC:

```
python blacklist.py --ssc path/to/ssc --entity --blacklist path/to/blacklist --output path/to/output
```
"""
import argparse
import errno
import os
from collections import Counter
from pathlib import Path

MIN_TOKEN_LENGTH = 4

def main(gsc, ssc, output_dir, replace, blacklist, entity):
    """Generates a blacklist of entities that occur in corpus at `ssc` but not in corpora at `gsc`.
    """
    gsc_anns = []
    ssc_anns = []

    if gsc and ssc and not blacklist:
        print('[INFO] Getting entities for the GSCs...')
        for filepaths in get_filepaths(gsc):
            # accumulate annotations in GSCs on per-corpus basis
            # converting to set leads to a much faster lookup downstream
            gsc_anns.append(set(get_all_anns(filepaths)))

        print('[INFO] Getting entities for the SSC...')
        for filepaths in get_filepaths(ssc):
            ssc_anns.extend(get_all_anns(filepaths))

        # use Counter to save frequency counts
        ssc_ann_counter = Counter(ssc_anns)

        # generate the blacklist
        print('[INFO] Generating the blacklist...')
        blacklist = []

        for i in range(1, len(ssc_anns) - 1):
            # check that this is a single entity
            b_entity_tag = 'B-{}'.format(entity)
            single_token_entity = (ssc_anns[i-1][1] != 'I-' and
                                   ssc_anns[i][1] == b_entity_tag and
                                   ssc_anns[i+1][1] != 'I-')
            min_token_length = len(ssc_anns[i][0]) >= MIN_TOKEN_LENGTH

            if single_token_entity and min_token_length:
                token_in_gold = any((ssc_anns[i][0], 'O') in corpus for corpus in gsc_anns)
                ann_in_gold = any(ssc_anns[i] in corpus for corpus in gsc_anns)
                # this token appears in all the GSCs but is never annotated
                if token_in_gold and not ann_in_gold:
                    blacklist.append(ssc_anns[i])
        # take top 100 most common blacklisted entities as our final list
        blacklist = [x[0] for x in Counter({ent: ssc_ann_counter[ent] for ent in blacklist}).most_common(100)]
        # write the blacklisted annotations to disk
        save_blacklist(blacklist, output_dir)
        # remove the blacklisted annotations
        if replace:
            remove_blacklisted(blacklist, ssc, output_dir)
    elif ssc and blacklist:
        blacklist = open_blacklist(blacklist)
        remove_blacklisted(blacklist, ssc, output_dir)
    else:
        raise ValueError(('Invalid combination of arguments provided. See usage comments at the '
                          'top of this script.'))

def get_filepaths(directory, suffix='.tsv'):
    """Yields list of filepaths under the sub-directories of `directory` with extension `suffix`.

    For all subdirectories under `directory`, yields a list of filepaths that end with the extension
    `suffix` in that subdirectory.

    Args:
        directory:
    """
    for dir_ in Path(directory).glob('**'):
        if dir_.is_dir():
            yield [str(f) for f in dir_.glob('*') if f.is_file() and f.suffix == suffix]

def get_all_anns(filepaths):
    """Return a list of tuples of entity, tag pairs from CoNLL formatted corpora at `filepaths`.
    """
    annotations = []
    for filepath in filepaths:
        with open(filepath, 'r') as f:
            for line in f:
                ent = line.split('\t')[0].strip()
                tag = line.split('\t')[-1].strip()
                # get rid of newlines
                if ent != '' and tag != '':
                    annotations.append((ent, tag))

    return annotations

def remove_blacklisted(blacklist, ssc, output_dir):
    """Writes a copy of the SSC at `ssc` to disk with all entities in `blacklist` removed.
    """
    print('[INFO] Writing blacklisted corpus to {}...'.format(output_dir))
    # assuming there is only 1 SSC, so take index 0
    ssc_filepaths = list(get_filepaths(ssc))[0]
    # for faster lookup
    blacklist = set(blacklist)
    for filepath in ssc_filepaths:
        with open(filepath, 'r') as f:
            # remove blacklisted entities
            lines = f.readlines()
            for i in range(1, len(lines) - 1):
                previous_tag = 'O' if lines[i-1] == '\n' else lines[i-1].strip().split('\t')[1]
                next_tag = 'O' if lines[i+1] == '\n' else lines[i+1].strip().split('\t')[1]
                single_token_entity = (previous_tag != 'I-' and next_tag != 'I-')
                blacklisted = tuple(lines[i].strip().split('\t')) in blacklist
                if single_token_entity and blacklisted:
                    lines[i] = '{}\tO\n'.format(lines[i].split('\t')[0])
        # write blacklisted copy to disk
        corpus_name = os.path.basename(ssc) + '_blacklisted'
        output_directory = os.path.join(output_dir, corpus_name)
        make_dir(output_directory)
        output_filepath = os.path.join(output_directory, os.path.basename(filepath))
        with open(output_filepath, 'w') as f:
            for line in lines:
                f.write(line)

def open_blacklist(filepath):
    """Opens a blacklist file at `filepath`.

    Open the given blacklist file at `filepath`. Expects this file to contain one entity per line
    where each line contains the entity and its label seperated by a tab. E.g.,

    gene    B-PRGE
    disease B-DISO
    ...
    """
    with open(filepath, 'r') as f:
        blacklist = [tuple(line.strip().split('\t')) for line in f.readlines()]
    return blacklist

def save_blacklist(blacklist, output_dir):
    """Writes a copy of `blacklist` to `output_dir`, with each element written to its own line.
    """
    output_filepath = os.path.join(output_dir, 'blacklist.txt')
    print('[INFO] Writing blacklist to {}...'.format(output_filepath))
    with open(output_filepath, 'w') as f:
        for ent in blacklist:
            f.write('{}\t{}\n'.format(ent[0], ent[1]))

def make_dir(directory):
    """Creates a directory at `directory` if it does not already exist.
    """
    try:
        os.makedirs(directory)
    except OSError as err:
        if err.errno != errno.EEXIST:
            raise

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=('Generate a blacklist for a SSC by providing '
                                                  'arguments for --gsc and --ssc. Optionally, pass '
                                                  '--replace if you want return a copy of the SSC '
                                                  'with blacklisted entities removed. To provide '
                                                  'your own blacklist, simply provide the '
                                                  'arguments --ssc and --blacklist. Note that '
                                                  '--replace will be ignored in this case.'
                                                  'Finally, all output will be saved to filepath '
                                                  'at --output, which defaults to the directory '
                                                  'the script was called from'))
    parser.add_argument('--gsc', '-g', required=False, type=str,
                        help='Path to top-level directory which houses GSCs.')
    parser.add_argument('--ssc', '-s', required=True, type=str,
                        help='Path to SSC directory.')
    parser.add_argument('--entity', '-e', required=True, type=str,
                        help="Entity label to blacklist, e.g. 'PRGE'. Don't include 'B-' or 'I-'.")
    parser.add_argument('--output', '-o', default='.', type=str,
                        help="Path to output directory. Defaults to directory script was called from")
    parser.add_argument('--replace', '-r', default=False, action='store_true',
                        help='Pass this flag if blacklisted entities should be removed from the SSC.')
    parser.add_argument('--blacklist', '-b', required=False, default='',
                        help=('Path to blacklist, if provided this blacklist is used to remove '
                              'from the SSC provided in the --ssc argument.'))
    args = parser.parse_args()

    main(args.gsc, args.ssc, args.output, args.replace, args.blacklist, args.entity)
