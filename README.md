# cuny2020
Structural Supervision &amp; Human Psycholinguistic Data

## To Do:
• EOL handling in the harmonize.py script
• Re-run bnc brown

## Cuny2020

### analysis.Rmd

Analysis script

### average_sprs_script.rmd

Reads in the human reading-time data from /corpora/bnc-brown_reference.csv and natural-stories-reference.csv and calculates the cross-participant, by-word average. Saves each word with its reading time and a unique code into the /data/humna_rts/ folder. For the natural stories corpus, each word is assigned a unique code.

All codes are ordered, so the word with code 010012 immedietly proceeds 010013 in the reading-time corpus.

## harmonize.py

This script takes individual model results from the /model_results/ directory and harmonizes them with human reading times. Words for which the tokenization between the model output and the human data presentation are discarded.

The script assums that model resutls are stored in LM_ZOO format, with for columns: sentence_idx, token_idx, token, surprisal. It assumes that human RT results are stored with three columns "code", "token", "rt". Except for the Dundee corpus, where no code is given. In this case, the script genreates a code, which is the row-number of the word, combined with the text ID of the portion of the dundee corpus where the word occured.

This script takes a path to a corpus, which is used to calculate log frequency of words. (I have been using wikitext 2, which is also what was reported in the CogSci submission)

Notes:
• The Ordered Neurons, tx01, dundee, seed=0922, bllip-md and bllip-lg models didn't have any results.
