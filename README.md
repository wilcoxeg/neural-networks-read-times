
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

### generate_sentences.py

• generates line-separated natural text randitions of the `bnc-brown` and `natural-stories` corpus, which can be fed into a neural LM to get by-word surprisal values.

• To generate bnc-brown, the script takes `brown_spr.csv` which should be in the same folder.

• To generate natural-stories, the script takes the `all_stories.txt` (or `all_stories.tok`) file from the `natural_stories/naturalstories_RTS` subdirectory of the natural stories corpus, which can be found [here on github](https://github.com/languageMIT/naturalstories/tree/master/naturalstories_RTS)

## Data

• Download the data-directory here: https://drive.google.com/file/d/1Fbn-MeABFZ0GE901TjPPIQnzBpEYAgjB

• For scripts to work, put the `data` directory at the top level of this directory.

### Corpora

• `brown_spr.csv` and `natural_stories_rts.csv` have by-word reading times for the bnc-brown and natural stories corpus. These are not averaged across subjects. Cross-subject averaging happens in the `average_sprs_script.rmd` file.

• `bnc-brown.txt` and `natural_stories.txt` are sentence-tokenized versions of these corpora, which can be fed into neural LMs to get word-by-word surprisal values.

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

## Notes:

