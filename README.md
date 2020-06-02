
# Neural LMs as Models of Human Language Processing

This repo contains reproduction code for "On the Predictive Power of Neural Language Models for Human Real-Time Comprehension Behavior" by Wilcox, Gauthier, Hu, Qian and Levy.

Questions? Feel free to contact wilcoxeg@g.harvard.edu

## Download the Data

• Download the data-directory here: https://drive.google.com/file/d/1e-anJ4laGlTY-E0LNook1EzKBU2S1jI8. For scripts to work, put the `data` directory at the top level of this directory.

## Analysis Reproduction

• If you wish to reproduce only our analysis, we have provided an aggregated data file `harmonized_results.csv`. That contains harmonized by-word surprisal values for each model and testing corpus.

• Analysis and figure generation code can be found in `analysis.Rmd`. Images are saved to `/images/cogsci2020/`.

• Log-liklihood can be computed with a linear model, or with a GAM, however this is not set globally. You need to uncomment code in order to switch from the LM to the GAM.

One thing to note: Fittin the GAM models for the reproduction of Figure 1 takes > 1 hour on a typical PC. Instead of running the fits, feel free to use the outputs of our fits in `/data/gam_smooths.sl2013.all.csv`, which can be used for plotting and analysis.

## (1) Data Pipeline Reproduction

### Generate Data for Neural LMs

•  `generate_sentences.py` generates line-separated natural text randitions of the `bnc-brown` and `natural-stories` corpus, which can be fed into a neural LM to get by-word surprisal values. We provide the results of this script in `data/corpora/bnc-brown.txt` and `data/corpora/natural_stories.txt`

• To generate bnc-brown, the script takes `brown_spr.csv` which should be in the same folder.

• To generate natural-stories, the script takes the `all_stories.txt` (or `all_stories.tok`) file from the `natural_stories/naturalstories_RTS` subdirectory of the natural stories corpus, which can be found [here on github](https://github.com/languageMIT/naturalstories/tree/master/naturalstories_RTS)

• We do not provide code for deriving by-word surprisal values for neural LMs

## (2) Preprocess Human RT Data

• `average_sprs_script.rmd` reads in the human reading-time data from `data/corpora/bnc-brown_reference.csv` and `data/natural-stories-reference.csv` and calculates the cross-participant, by-word average. Saves each word with its reading time and a unique code into the /`data/humna_rts/` folder. For the natural stories corpus, each word is assigned a unique code.

• All codes are ordered, so the word with code 010012 immedietly proceeds 010013 in the reading-time corpus.

• `brown_spr.csv` and `natural_stories_rts.csv` have by-word reading times for the bnc-brown and natural stories corpus. These are not averaged across subjects. Cross-subject averaging happens in the `average_sprs_script.rmd` file.

• Human Reading Times can be found in `/human_rts/` for each of the relevant corpora: BNC-Brown, Dundee and Natural Stories

• RT results are stored with three columns `code`, `token`, `rt`.

• The `/Model Results/` directory contains results by model type. Current models include: 5-Gram, GPT2, VanillaLSTM and RNNG
	|
	--> Sub-Subdirectories contain results by test corpus. Model results should be in the four-column LM ZOO output format: `sentence_idx`, `token_idx`, `token`, `surprisal`

## (3) Harmonize Model Results

• `harmonize.py` takes individual model results from the `data/model_results/` directory and harmonizes them with human reading times. Words for which the tokenization between the model output and the human data presentation are discarded.

• Assumes model results and human RT results are stored in the format described below, in `data`, except for the Dundee corpus, where no code is given. In this case, the script genreates a code, which is the row-number of the word, combined with the text ID of the portion of the dundee corpus where the word occured.

• Takes a path to a corpus, which is used to calculate log frequency of words. (I have been using wikitext 2, which is also what was reported in the CogSci submission)


