# Blacklists

In the transfer learning experiments of our paper, we first train on a large, automatically annotated silver standard corpus (SSC) before training on manually annotated gold-standard corpora (GSCs).

To reduce noise in the SSC, we semi-automatically generated a blacklist of single-token entities which were annotated in the silver-standard corpus (SSC) and present in at least one of the gold-standard corpora but never annotated.
