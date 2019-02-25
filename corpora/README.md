# Corpora

## Gold-standard corpora

### S800

To download and convert the S800 corpus to CoNLL format, follow the instructions in the readme of [this](https://github.com/spyysalo/s800) repository.

### Variome

TODO.

## Silver-standard corpora

### CALBC-III-Small

The processed corpus we used in this study is available at `corpora/CALBC_BIO_100K_blacklisted.tar.bz2`. The pre-processing steps are outlined below

#### Pre-processing

These instructions assume you have git cloned the repository and changed directory to `code`

```
git clone https://github.com/BaderLab/Towards-reliable-BioNER.git
cd Towards-reliable-BioNER/code
```

Download the CALBC-III-Small-allcomer corpus & expand it:

```
$ curl -O http://ftp.ebi.ac.uk/pub/databases/CALBC/resources/small/175k-allcomer-xtype.gz
$ gunzip 175k-allcomer-xtype.gz
```

Use the conversion script to convert it to Standoff format:

```
$ python3 iexml_to_standoff.py -i 175k-allcomer-xtype -o CALBC_Standoff
```

> This script is lazy, skips converting a document when an error occurs. Therefore the # of output documents is smaller than the number of input documents.

Remove the blacklisted PMIDs and entities

```
$ python3 blacklist_pmids.py -i CALBC_Standoff -b ../supplementary/pmid_blacklists/all_pmids_blacklist.txt
$ python3 blacklist_entities.py --ssc CALBC_Standoff --blacklist ../supplementary/entity_blacklists/all_entities_blacklist.txt --replace
```

Clean the Standoff corpus:

```
$ python3 clean_standoff.py -i CALBC_Standoff
```

This script removes any files which contain annotations that do not match the corresponding text span, and removes any lone `.ann`/`.txt` pairs. Why these occur is not clear, likely bugs in `iexml_to_standoff.py`.

Split your `CALBC_Standoff` corpus into train/valid/test partitions

```
$ python3 split_train_test_valid.py -i CALBC_Standoff
```

Finally, convert to CoNLL format:

```
$ git clone https://github.com/JohnGiorgi/standoff2conll.git
$ mkdir CALBC_CoNLL
$ for PARTITION in train valid test
  do
    python2 standoff2conll/standoff2conll.py CALBC_Standoff/$PARTITION > CALBC_CoNLL/$PARTITION.tsv
  done
```
