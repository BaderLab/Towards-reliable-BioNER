# Blacklists

In the transfer learning experiments of our paper <cite paper here>, we first train on a large, automatically annotated silver standard corpus (SSC) before training on manually annotated gold-standard corpora (GSCs).

To ensure that we weren't training and then testing on the same documents (i.e., a document present in the training set of the SSC is not present in the testing set of any of the GSCs), we simply removed any document present in SSC that was present in any of the GSCs.

`all_pmids.txt` contain all the documents (by PMID) present in all the GSCs. If any of these documents were found in the SSC, they were removed (from the SSC).
