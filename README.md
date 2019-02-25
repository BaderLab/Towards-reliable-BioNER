# Towards Reliable Named Entity Recognition in the Biomedical Domain

This repository contains supplementary data, and links to the model and corpora used for the paper: "_Towards reliable named entity recognition in the biomedical domain_".

## Model

The model used in this study is __Saber__, a tool we are building for text-mining and information extraction of biomedical text. The named entity recognizer (NER) implemented in Saber is based on a bi-directional long short term memory network-conditional random field (BiLSTM-CRF) [[1](#citations)]. The tool can be accessed [here](https://github.com/BaderLab/saber).

Documentation for the tool can be found [here](https://baderlab.github.io/saber/).

## Data

### Word Embeddings

The word embeddings used in this study were obtained from [here](http://bio.nlplab.org/#word-vectors) [[2](#citations)].

### Corpora

Corpora used in this study are listed below, along with links where they can be publicly accessed. With the exceptions of CALBC-III-Small, S800, and Variome (see [corpora](corpora) for pre-processing details), we obtained most corpora in a pre-processed state from [here](https://github.com/cambridgeltl/MTL-Bioinformatics-2016) [[3](#citations)].

| Corpora | Text Genre | Standard | Entities | Publication |
| --- | --- | --- | --- | --- |
| [BioCreative II GM (BC2GM)](https://sourceforge.net/projects/biocreative/files/biocreative2entitytagging/1.1/) | Scientific Article | Gold | genes/proteins | [link](https://doi.org/10.1186/gb-2008-9-s2-s2) |
| \*[BioCreative V Chemical-Disease Relation (CDR) Task Corpus (BC5CDR)](https://biocreative.bioinformatics.udel.edu/resources/corpora/biocreative-v-cdr-corpus/)   | Scientific Article  |  Gold | chemicals, diseases  | [link](https://www.ncbi.nlm.nih.gov/pubmed/27161011)  |
| [CALBC-III-Small](http://ftp.ebi.ac.uk/pub/databases/CALBC/) | Scientific Article | Silver | chemicals, diseases, species, genes/proteins | [link](https://s3.amazonaws.com/academia.edu.documents/45849509/CALBC_silver_standard_corpus20160522-3059-1j189nl.pdf?AWSAccessKeyId=AKIAIWOWYYGZ2Y53UL3A&Expires=1537536482&Signature=hyYEo5%2BVtlPYeaNQwO5KP4o2HMY%3D&response-content-disposition=inline%3B%20filename%3DCalbc_Silver_Standard_Corpus.pdf) |
| [CRAFT](https://github.com/UCDenver-ccp/CRAFT) | Scientific Article | Gold | chemicals, species, genes/proteins, sequence ontology, gene ontology, cell lines  | [link](https://doi.org/10.1186/1471-2105-13-161) |
| [BC5CDR](http://www.biocreative.org/tasks/biocreative-v/track-3-cdr/) | Scientific Article | Gold | chemicals, diseases | [link](academic.oup.com/database/article/doi/10.1093/database/baw068/2630414) |
|[Linneaus](http://linnaeus.sourceforge.net/)| Scientific Article | Gold | species | [link](http://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-11-85)|
|[NCBI-Disease](https://www.ncbi.nlm.nih.gov/CBBresearch/Dogan/DISEASE/)| Scientific Article | Gold | diseases|[link](http://www.sciencedirect.com/science/article/pii/S1532046413001974)|
|[S800](http://species.jensenlab.org/)| Scientific Article | Gold | species|[link](http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0065390)|
|[Variome](http://www.opennicta.com.au/home/health/variome)| Scientific Article | Gold | diseases, species, genes/proteins|[link](http://database.oxfordjournals.org/content/2013/bat019.abstract)|

\*Requires that you create an account at [https://biocreative.bioinformatics.udel.edu/](https://biocreative.bioinformatics.udel.edu/) to access.

### Supplementary Information

Blacklists used during transfer learning can be found in `supplementary`. There are two sets:

1. `entity_blacklists`: Contain a list of single-token entities that were annotated in the silver-standard corpus (SSC) and present in at least one of the gold-standard corpora but never annotated.
2. `pmid_blacklists`: PMIDs corresponding to documents in the gold-standard corpora (GSCs).

## Recreating the Experiments

First download and install Saber by following the instructions [here](https://baderlab.github.io/saber/).

Then clone and move into this repository

```
git clone https://github.com/BaderLab/Towards-reliable-BioNER.git
cd Towards-reliable-BioNER
```

You will then need to collect all corpora. Most GSC are available [here](https://github.com/cambridgeltl/MTL-Bioinformatics-2016/tree/master/data), pre-processed (note we used corpora with tags in the IOB format). See `corpora` for instructions for collecting S800 and Variome. The preprocessed CALBC-III-Small is given in `corpora`.

Finally, you will need to collect the word embeddings

```
$ mkdir word_embeddings
$ wget http://evexdb.org/pmresources/vec-space-models/wikipedia-pubmed-and-PMC-w2v.bin -O word_embeddings
```

The following instructions assume Saber is installed, that you have git cloned this repository and have changed directory into this repository, that datasets are available under `Towards-reliable-BioNER/datasets` and that word embeddings are available under `Towards-reliable-BioNER/word_embeddings`.

### Baseline Experiments

To run the baseline experiments (Results section 3.1, Supplementary data Table 3)

```
python -m saber.cli.train --config_filepath configs/baseline.ini
```

by default this will train on the `NCBI-Disease` corpus. To train on a different dataset, either provide its path with the `dataset_folder` argument

```
$ python -m saber.cli.train --config_filepath configs/baseline.ini --dataset_folder ./datasets/BC2GM_BIO
```
or change the value for `dataset_folder` in `configs/baseline.ini`.

### Generalization Experiments

To run the generalization experiments (Results section 3.2, Supplementary data Table 4)

```
$ python -m saber.cli.train --config_filepath configs/generalization.ini
```

note that for any out-of-corpus experiments, you will need to modify the data slightly:

- For the corpus we are to train on, combine all examples under a single `train.tsv` file (you can simply copy paste examples from `valid/dev.tsv` and `test.tsv` into `train.tsv` and then discard them).
- For the corpus we are to test on, combine all examples under a single `test.tsv` file (you can simply copy paste examples from `train.tsv` and `valid/dev.tsv` into `test.tsv` and then discard them).

Place the `train.tsv` and `test.tsv` files under a single directory, and set this as your `dataset_folder`

E.g.
```
.
├── train_on_NCBI_test_on_BC5CDR
│   ├── train.tsv
│   └── test.tsv
```

### Variational Dropout Experiments

To run the variational dropout experiments (Results section 3.3, Supplementary data Table 5 and 6)

__In-corpus__

```
$ python -m saber.cli.train --config_filepath configs/variational_dropout_in_corpus.ini
```

__Out-of-corpus__

```
$ python -m saber.cli.train --config_filepath configs/variational_dropout_out_of_corpus.ini
```

See [Generalization Experiments](#generalization-experiments) for how to prepare datasets for out-of-corpus experiments.

### Transfer Learning Experiments

To run the variational dropout experiments (Results section 3.4, Supplementary data Table 7 and 8)

TODO


### Multi-task Learning Experiments

To run the  multi-task learning experiments (Results section 3.5, Supplementary data Table 9 and 10)

__In-corpus__

```
$ python -m saber.cli.train --config_filepath configs/multi_task_learning_in_corpus.ini
```

__Out-of-corpus__

```
$ python -m saber.cli.train --config_filepath configs/multi_task_learning_out_of_corpus.ini
```

See [Generalization Experiments](#generalization-experiments) for how to prepare datasets for out-of-corpus experiments.

### Combining Modifications

To run the combined modifications experiments (Results section 3.6, Figure 1), just combine the above instructions as appropriate. E.g., to perform variational dropout and multi-task learning, set `dropout_rate` to `0.3, 0.3, 0.1`, `variational_dropout` to `True` and provide two datasets to `dataset_folder`.

### Citations

1. Lample, G., Ballesteros, M., Subramanian, S., Kawakami, K., & Dyer, C. (2016). Neural architectures for named entity recognition. arXiv preprint arXiv:1603.01360.
2. Moen, S. P. F. G. H., & Ananiadou, T. S. S. (2013). Distributional semantics resources for biomedical text processing. In Proceedings of the 5th International Symposium on Languages in Biology and Medicine, Tokyo, Japan (pp. 39-43).
3. Crichton, G., Pyysalo, S., Chiu, B., & Korhonen, A. (2017). A neural network multi-task learning approach to biomedical named entity recognition. BMC bioinformatics, 18(1), 368.
