# Corpora

## Gold-standard corpora

## Silver-standard corpora

Download the CALBC-III-Small-allcomer corpus & expand it:

```
$ curl -O http://ftp.ebi.ac.uk/pub/databases/CALBC/resources/small/175k-allcomer-xtype.gz
$ gunzip 175k-allcomer-xtype.gz
```

Use the conversion script to convert it to Standoff format:

```
$ python3 ixeml_to_standoff.py -i 175k-allcomer-xtype -o CALBC_Standoff
```

> This script is lazy, skips converting a document when an error occurs. Therefore the # of output documents is smaller than the number of input documents.

Remove the blacklisted `PMID`s:

```
$ python3 remove_blacklisted.py -i path/to/CALBC_Standoff -b path/to/all_pmids.txt
```

Clean the Standoff corpus:

```
$ python3 clean_standoff.py -i path/to/CALBC_Standoff
```

This script removes any files which contain annotations that do not match the corresponding text span, and removes any lone `.ann`/`.txt` pairs. Why these occur is not clear, likely bugs in `ixeml_to_standoff.py`.

Split your `CALBC_Standoff` corpus into train/valid/test partitions

```
$ python3 split_train_test_valid.py -i path/to/CALBC_Standoff
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
