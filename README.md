
# Neural LMs as Models of Human Language Processing

Reproduction code for work assessing neural langauge models as models of human sentence processing.

## Scripts

## harmonize.py

• Takes individual model results from the `data/model_results/` directory and harmonizes them with human reading times. Words for which the tokenization between the model output and the human data presentation are discarded.

• Assumes model results and human RT results are stored in the format described below, in `data`, except for the Dundee corpus, where no code is given. In this case, the script genreates a code, which is the row-number of the word, combined with the text ID of the portion of the dundee corpus where the word occured.

• Takes a path to a corpus, which is used to calculate log frequency of words. (I have been using wikitext 2, which is also what was reported in the CogSci submission)

### analysis.Rmd

Main analysis script

• Computes log-liklihood for baseline and LM-derived models.

• Log-liklihood can be computed with a linear model, or with a GAM, however this is not set globally. You need to uncomment code in order to switch from the LM to the GAM.

#### TODO:
• Global parameter to switch between GAM and LM
• Redo analysis to account for summing between folds, as opposed to averaging
• Right now, `harmonize.py` is actually a jupyter notebook. Change to python script.
• EOL handling in the `harmonize.py` script


### average_sprs_script.rmd

• Reads in the human reading-time data from `data/corpora/bnc-brown_reference.csv` and `data/natural-stories-reference.csv` and calculates the cross-participant, by-word average. Saves each word with its reading time and a unique code into the /`data/humna_rts/` folder. For the natural stories corpus, each word is assigned a unique code.

• All codes are ordered, so the word with code 010012 immedietly proceeds 010013 in the reading-time corpus.

## Data

• Download the data-directory here: https://drive.google.com/file/d/1Gaj9xdkWh8e8aiMuZeE1U3WA_kkbwAUq/view?usp=sharing

• For scripts to work, but it at the top level of this directory

### Corpora

### Human RTs

• Human Reading Times for each of the relevant corpora: BNC-Brown, Dundee and Natural Stories

• RT results are stored with three columns `code`, `token`, `rt`.

### Model Results

• Subdirectories contain results by model type. Current models include: 5-Gram, GPT2, VanillaLSTM and RNNG
	|
	--> Sub-Subdirectories contain results by test corpus. Model results should be in the four-column LM ZOO output format: `sentence_idx`, `token_idx`, `token`, `surprisal`

### Results Cache

• A cache of results from previous Ordered Neurons runs. Eventually, we will want to delete these, however we're worried that there's a bug in the ON scripts, so they are being kept around for now, in case we need to compare model output for debugging.

## Images

• Write images to this folder

## To Do:
• Re-run bnc brown

## Notes:
• The Ordered Neurons, tx01, dundee, seed=0922, bllip-md and bllip-lg models didn't have any results.
