import os

def get_pmids(directory):
    pmids = []
    for filename in get_filenames(directory):
        if filename.endswith('.txt'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as f:
                pmids.extend(f.readlines())
    return list(set(pmids))

def get_filenames(directory):
    """
    Returns list of filenames in `directory`.

    Args:
        directory (str): path to input directory

    Returns: list of filenames in `directory`.
    """
    return [os.fsdecode(file) for file in os.listdir(directory)]

pmids = get_pmids('/Users/johngiorgi/Documents/dev/Towards-robust-and-reliable-BioNER/supplementary/blacklists')

with open('all_PMIDs.txt', 'w') as f:
    for pmid in pmids:
        f.write('{}'.format(pmid))
