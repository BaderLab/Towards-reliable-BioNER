# Towards Reliable Named Entity Recognition in the Biomedical Domain

This repository contains the corpora and supplementary data, along with instructions for recreating the experiments, for our paper: ["Towards reliable named entity recognition in the biomedical domain"](https://academic.oup.com/bioinformatics/advance-article/doi/10.1093/bioinformatics/btz504/5520946).

## Table of Contents

- [Model](#model)
- [Data](#Data)
  - [Word Embeddings](#word-embeddings)
  - [Datasets](#datasets)
  - [Supplementary Information](#supplementary-information)
- [Recreating the Experiments](#recreating-the-experiments)
  - [Installation](#installation)
  - [Collecting Data](#collecting-data)
  - [Recreating the Experiments](#recreating-the-experiments)
- [Issues](#issues)
- [Citations](#citations)

## Model

The model used in this study is __Saber__, a tool we are building for text-mining and information extraction of biomedical text. The named entity recognizer (NER) implemented in Saber is based on a bi-directional long short term memory network-conditional random field (BiLSTM-CRF) [[1](#citations)]. The tool can be accessed [here](https://github.com/BaderLab/saber).

Documentation for the tool can be found [here](https://baderlab.github.io/saber/).

## Data

### Word Embeddings

The word embeddings used in this study were obtained from [here](http://bio.nlplab.org/#word-vectors) [[2](#citations)].

### Datasets

Datasets used in this study are listed below, along with links where they can be publicly accessed. We obtained most datasets in a pre-processed state from [here](https://github.com/cambridgeltl/MTL-Bioinformatics-2016) [[3](#citations)]. The final, preprocessed datasets that we used in this study are available under [`datasets`](https://github.com/BaderLab/Towards-reliable-BioNER/tree/master/datasets).

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

To recreate the experiments, you must first install our package and collect the relevant data. Start by cloning and moving into this repo

```
$ git clone https://github.com/BaderLab/Towards-reliable-BioNER.git
$ cd Towards-reliable-BioNER
```

### Installation

First, you will need to install `python 3.6`. If not already installed, `python3` can be installed via

- The [official installer](https://www.python.org/downloads/)
- [Homebrew](https://brew.sh), on MacOS (`brew install python3`)
- [Miniconda3](https://conda.io/miniconda.html) / [Anaconda3](https://www.anaconda.com/download/)

> Run `python --version` at the command line to make sure installation was successful. You may need to type `python3` (not just `python`) depending on your install method.

It is also highly recommended that you use a virtual environment. See [(Optional) Creating and Activating a Virtual Environment](#optional-creating-and-activating-a-virtual-environment).

Finally, download and install the fork of [Saber](https://baderlab.github.io/saber/) that we used in this paper.

```
(saber) $ pip install -e git+https://github.com/JohnGiorgi/saber.git@master#egg=saber
```

#### (Optional) Creating and Activating a Virtual Environment

To create a virtual environment named `saber`

##### Using Conda

Using [Conda](https://conda.io/docs/) / [Miniconda](https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh)

```
$ conda create -n saber -y python=3.6
```

To activate the environment

```
$ conda activate saber
# Notice your command prompt has changed to indicate that the environment is active
(saber) $
```

##### Using virtualenv or venv

Using [virtualenv](https://virtualenv.pypa.io/en/stable/)

```
$ virtualenv --python=python3 /path/to/new/venv/saber
```

Using [venv](https://docs.python.org/3/library/venv.html)

```
$ python3 -m venv /path/to/new/venv/saber
```

To activate the environment

```
$ source /path/to/new/venv/saber/bin/activate
# Notice your command prompt has changed to indicate that the environment is active
(saber) $
```

### Collecting Data

#### Datasets

Preprocessed datasets are provided under the `datasets` directory for convenience. They just need to be unzipped

```
$ (saber) tar -xvjf datasets/datasets.tar.bz2 datasets/
```

#### Word Emebddings

Finally, you will need to collect the word embeddings

```
$ (saber) mkdir word_embeddings
$ (saber) wget -O word_embeddings/wikipedia-pubmed-and-PMC-w2v.bin http://evexdb.org/pmresources/vec-space-models/wikipedia-pubmed-and-PMC-w2v.bin
```

> Note that this file is 4GB and can take a while to download.

### Running the Experiments

The following instructions assume that you have git cloned and moved into this repository locally, that [Saber](https://baderlab.github.io/saber/) is installed, and that the datasets are available under `Towards-reliable-BioNER/datasets` and that word embeddings are available under `Towards-reliable-BioNER/word_embeddings`.

> The results of the experiments will be saved under `Towards-reliable-BioNER/output` by default. If you would like the results to be saved elsewhere, provide a different path with the `--output_folder` argument or change the `output_folder` argument value in one of the [config files](https://github.com/BaderLab/Towards-reliable-BioNER/tree/master/configs).


#### Baseline Experiments

To run the baseline experiments ([Results](https://academic.oup.com/bioinformatics/advance-article/doi/10.1093/bioinformatics/btz504/5520946#137669197) section 3.1, Supplementary data Table 3)

```
$ (saber) python -m saber.cli.train --config_filepath configs/baseline.ini
```

#### Generalization Experiments

To run the generalization experiments ([Results](https://academic.oup.com/bioinformatics/advance-article/doi/10.1093/bioinformatics/btz504/5520946#137669197) section 3.2, Supplementary data Table 4)

```
$ (saber) python -m saber.cli.train --config_filepath configs/generalization.ini
```

#### Variational Dropout Experiments

To run the variational dropout experiments ([Results](https://academic.oup.com/bioinformatics/advance-article/doi/10.1093/bioinformatics/btz504/5520946#137669197) section 3.3, Supplementary data Table 5 and 6)

```
$ (saber) python -m saber.cli.train --config_filepath configs/variational.ini
```

#### Transfer Learning Experiments

To run the transfer learning experiments ([Results](https://academic.oup.com/bioinformatics/advance-article/doi/10.1093/bioinformatics/btz504/5520946#137669197) section 3.4, Supplementary data Table 7 and 8)

TODO.

#### Multi-task Learning Experiments

To run the  multi-task learning experiments ([Results](https://academic.oup.com/bioinformatics/advance-article/doi/10.1093/bioinformatics/btz504/5520946#137669197) section 3.5, Supplementary data Table 9 and 10)

```
$ (saber) python -m saber.cli.train --config_filepath configs/multi_task_learning.ini
```

#### Choosing the Dataset

For each experiment, we provide configurations files under [`configs`](https://github.com/BaderLab/Towards-reliable-BioNER/tree/master/configs). The only thing you should need to modify is the `dataset_folder` argument. To train on a certain dataset, either provide its path with the `dataset_folder` argument

```
$ (saber) python -m saber.cli.train --config_filepath configs/baseline.ini --dataset_folder ./datasets/BC2GM_BIO
```

or change the value for `dataset_folder` in `configs/baseline.ini`.

For "in-corpus" experiments (see our [paper](https://academic.oup.com/bioinformatics/advance-article/doi/10.1093/bioinformatics/btz504/5520946)), use the standalone dataset (e.g. `"NCBI_Disease_BIO"`, `"BC5CDR_DISO_BIO"`, etc.). For the "out-of-corpus" experiments, use one of the datasets named `train_on_<x>_test_on_<y>`. In these datasets, the `train.*` and the `test.*` data come from different datasets, allowing you to evaluate how well a model trained on one dataset performs on data from another dataset.

For multi-task experiments, simply provide multiple arguments to `dataset_folder`, either at the command line, separated by a space, e.g.

```
$ (saber) python -m saber.cli.train --config_filepath configs/multi_task_learning.ini --dataset_folder ./datasets/NCBI_Disease_BIO ./datasets/BC5CDR_DISO_BIO
```

or in the `config.ini` file, separated by a comma, 

```
dataset_folder = ./datasets/NCBI_Disease_BIO, ./datasets/BC5CDR_DISO_BIO
```

#### Combining Modifications

To run the combined modifications experiments ([Results](https://academic.oup.com/bioinformatics/advance-article/doi/10.1093/bioinformatics/btz504/5520946#137669197) section 3.6, Figure 1), just combine the above instructions as appropriate. E.g., to perform variational dropout and multi-task learning, set `dropout_rate` to `0.3, 0.3, 0.1`, `variational_dropout` to `True` and provide two datasets to `dataset_folder`.

## Issues

Please open an issue if you have any questions.

## Citations

1. Lample, G., Ballesteros, M., Subramanian, S., Kawakami, K., & Dyer, C. (2016). Neural architectures for named entity recognition. arXiv preprint arXiv:1603.01360.
2. Moen, S. P. F. G. H., & Ananiadou, T. S. S. (2013). Distributional semantics resources for biomedical text processing. In Proceedings of the 5th International Symposium on Languages in Biology and Medicine, Tokyo, Japan (pp. 39-43).
3. Crichton, G., Pyysalo, S., Chiu, B., & Korhonen, A. (2017). A neural network multi-task learning approach to biomedical named entity recognition. BMC bioinformatics, 18(1), 368.
