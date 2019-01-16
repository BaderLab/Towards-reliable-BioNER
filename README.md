# Towards Reliable Named Entity Recognition in the Biomedical Domain

This repository contains supplementary data, and links to the model and corpora used for the paper: "_Towards reliable named entity recognition in the biomedical domain_".

## Model

The model used in this study is __Saber__, a tool we are building for text-mining and information extraction of biomedical text. The named entity recognizer (NER) implemented in Saber is based on a bi-directional long short term memory network-conditional random field (BiLSTM-CRF) [[1](#citations)]. The tool can be accessed [here](https://github.com/BaderLab/saber).

Documentation for the tool can be found [here](https://baderlab.github.io/saber/).

## Data

### Word Embeddings

The word embeddings used in this study were obtained from [here](http://bio.nlplab.org/#word-vectors) [[2](#citations)].

### Corpora

All corpora used in this study (which can be re-distributed) are in the `corpora` folder (given in Brat-standoff format).

> Data can be uncompressed with the following command: `tar -zxvf <name_of_corpora>`.

Alternatively, the corpora can be publicly accessed at the following links:

| Corpora | Text Genre | Standard | Entities | Publication |
| --- | --- | --- | --- | --- |
| [BioCreative II GM](https://sourceforge.net/projects/biocreative/files/biocreative2entitytagging/1.1/) | Scientific Article | Gold | genes/proteins | [link](https://doi.org/10.1186/gb-2008-9-s2-s2) |
| [CALBC-III-Small](http://ftp.ebi.ac.uk/pub/databases/CALBC/) | Scientific Article | Silver | chemicals, diseases, species, genes/proteins | [link](https://s3.amazonaws.com/academia.edu.documents/45849509/CALBC_silver_standard_corpus20160522-3059-1j189nl.pdf?AWSAccessKeyId=AKIAIWOWYYGZ2Y53UL3A&Expires=1537536482&Signature=hyYEo5%2BVtlPYeaNQwO5KP4o2HMY%3D&response-content-disposition=inline%3B%20filename%3DCalbc_Silver_Standard_Corpus.pdf) |
| [CRAFT](https://github.com/UCDenver-ccp/CRAFT) | Scientific Article | Gold | chemicals, species, genes/proteins, sequence ontology, gene ontology, cell lines  | [link](https://doi.org/10.1186/1471-2105-13-161) |
| [BC5CDR](http://www.biocreative.org/tasks/biocreative-v/track-3-cdr/) | Scientific Article | Gold | chemicals, diseases | [link](academic.oup.com/database/article/doi/10.1093/database/baw068/2630414) |
|[CHEMDNER Patent](http://www.biocreative.org/tasks/biocreative-v/track-2-chemdner/)| Patent | Gold | chemicals|[link](https://jcheminf.springeropen.com/articles/10.1186/1758-2946-7-S1-S2)|
|[Linneaus](http://linnaeus.sourceforge.net/)| Scientific Article | Gold | species | [link](http://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-11-85)|
|[NCBI disease](https://www.ncbi.nlm.nih.gov/CBBresearch/Dogan/DISEASE/)| Scientific Article | Gold | diseases|[link](http://www.sciencedirect.com/science/article/pii/S1532046413001974)|
|[S800](http://species.jensenlab.org/)| Scientific Article | Gold | species|[link](http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0065390)|
|[Variome](http://www.opennicta.com.au/home/health/variome)| Scientific Article | Gold | diseases, species, genes/proteins|[link](http://database.oxfordjournals.org/content/2013/bat019.abstract)|

Many of these corpora were originally collected from [here](https://github.com/cambridgeltl/MTL-Bioinformatics-2016) [[3](#citations)].

### Supplementary Information

Blacklists used during transfer learning can be found in `supplementary`. There are two sets:

1. `entity_blacklists`: Contain a list of single-token entities that were annotated in the silver-standard corpus (SSC) and present in at least one of the gold-standard corpora but never annotated.
2. `pmid_blacklists`: PMIDs corresponding to documents in the gold-standard corpora (GSCs).

### Citations

1. Lample, G., Ballesteros, M., Subramanian, S., Kawakami, K., & Dyer, C. (2016). Neural architectures for named entity recognition. arXiv preprint arXiv:1603.01360.
2. Moen, S. P. F. G. H., & Ananiadou, T. S. S. (2013). Distributional semantics resources for biomedical text processing. In Proceedings of the 5th International Symposium on Languages in Biology and Medicine, Tokyo, Japan (pp. 39-43).
3. Crichton, G., Pyysalo, S., Chiu, B., & Korhonen, A. (2017). A neural network multi-task learning approach to biomedical named entity recognition. BMC bioinformatics, 18(1), 368.
