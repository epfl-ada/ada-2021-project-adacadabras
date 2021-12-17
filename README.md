# MeToo, a catalyst for change?

___Study of the influence of the movement on women's mediatic representation___

## Project's Notebook available [here](https://github.com/epfl-ada/ada-2021-project-adacadabras/blob/main/notebook/metoo-media-impact-women.ipynb)

The complete notebook of our project can be found in our repository, it is called:
`metoo-media-impact-women.ipynb`. For a better reading experience, please download the given notebook. Anchors will better help you navigate in our notebook.

## Project's Data Story available [here](https://ldrame21.github.io/metoo-media-impact/)

The Data story we created for this project can be found at the following URL:
https://ldrame21.github.io/metoo-media-impact/.

## Abstract

“#MeToo". Two words, a hashtag, civil rights movement with tremendous impacts on our society. Everything starts on October 15th, 2017, with a viral Twitter hashtag from Alyssa Milano. The movement, initially created by Tarana Burke, spread all over the world, inviting women to break silence on sexual harassment, violence, discrimination via social networks. The medias stepped in with widespread coverage and enhanced the movement's influence. Finally, women inequalities and the unsafe climate created by actors of society became a trending and polarizing topic on all media. Still, the question of the size of MeToo's impact on women's discrimination is to be answered. Via the metric of women's mediatic coverage, our project aims at assessing and quantifying the impact of #MeToo on the place of women in society. By using Quotebank dataset from 2015 to 2020, we will investigate the evolution of women’s mediatization through time and correlate it to #MeToo's key turning points.

## Research questions

* How has the mediatization of women been tuned by the emergence of the MeToo movement?
  A) What is the evolution of the general mediatic perspective of the MeToo movement? Are there any gender or generational biases observable in its mediatic coverage?
  B) Linguistic analysis of women's mediatic representation: how did the terms and tones used by the speakers in media (when speaking of women) change through time ? Are there any gender or generational biases observable?
  C) Is the evolution of women's mediatization (addressed in sub-question B) correlated to the tendency of MeToo's mediatic perspective (addressed in sub-question A)?

## Proposed additional datasets

* **AD1 : [Wikidata speakers_attribute.parquet](https://drive.google.com/drive/folders/1VAFHacZFh0oxSxilgNByb1nlNsqznUf0)**: dataset provided in the scope of the ADA course, to access Wikidata metadata on Quotebank speakers. The format of the data can be found in the schema_speakers_attribute.txt file. We scrap only the attributes "fields date_of_birth", "party" and "gender" for the investigation of biases in the speakers addressing the MeToo movement in media.
* **AD2 : [online-misogyny-eacl2021](https://github.com/ellamguest/online-misogyny-eacl2021)**  : dataset created to train NLP models to detect misogynistic speech in redit posts and contents. We are using only the final_labels.csv.
  * Train dataset : composed of 6'567 english.
  * Comma-separated with the following fields used for our classifier: “level 1” with possible values "misogynistic" and "non-misogynistic".
  * Based on this [paper](https://aclanthology.org/2021.eacl-main.114.pdf).

## Methods

**Step 1: Data scraping, pre-processing and dataset construction.**

* Dataset D1 : MeToo dataset containing quotes linked to the movement, in which the movement is mentioned
  * D1.1 : Subsets by gender of speaker
  * D1.2 : Subsets by age of speaker
  * D1.3 : Subsets by tone of speech (Positive, Negative, Neutral - NLTK Sentiment analysis) per age & gender categories.
  
* Dataset D2 : Dataset containing quotes in which a woman is mentioned
  * D2.1: Subset by gender of speaker
  * D2.2 : Subsets by age of speaker
  * D2.3 : Subsets by tone of speech (Positive, Negative, Neutral - NLTK Sentiment analysis) per age & gender categories.
  
  *The subsets are built later on during their respective Steps.*

**Step 2: General preliminary analysis using Quotebank entire dataset**
Weekly percentage and counts of quotes by author’s gender (men, women, other, unkown) from 2015 to 2020.

**Step 3: Generate annual/monthly word clouds based on dataset D2, general women coverage, with this [library.](https://github.com/amueller/word_cloud)**

**Step 4: Investigate general women perception via dataset D2 in medias to answer question B).**
Train SpaCy [SpaCy NLP model](https://spacy.io/usage/training) model on AD2 for misogynistic or non misogynistic. Classification thanks to trained model on D2.

**Step 5: Investigate gender and generational biases in general women coverage using NLP to answer question B).**
Subdivision of D2 into D2.1, D2.2 for biases investigation. Weekly percentage and counts of quotes by age and gender categories. Classification of quotes : NLTK, Vader models models for positive, negative or neutral probabilities and compounds. Subdivision of D2 into D2.3. Descriptive analysis of D1.3 over time.

**Step 6: Investigate gender and generational biases in MeToo coverage using NLP to answer question A).**
Subdivision of D1 into D1.1, D1.2 and D1.3 for biases investigation. Weekly percentage and counts of quotes by age and gender categories. Classification of quotes : NLTK, Vader models for positive, negative or neutral probabilities and compounds. Subdivision of D1 into D1.3. Descriptive analysis of D1.3 over time.

**Step 7: Correlate and investigate causation between MeToo general perception and women’s mediatic place to answer question C).**
Plot previously collected (Step 2, Step 5, Step 6) data distributions according to time. Comparison with key turning points of MeToo. Investigation of the statistical significance of detected changes before and after MeToo in Step 2, Step 5 and Step 6.

**Step 8: Github site building and Datastory redaction.**

**Further details on the proposed data pipelines can be found in the notebook.**

**Note: Since Milestone 2, we redirected some aspects of our project, namely the aditionnal datasets have changed due to ungranted access. Additionally, some steps of the data analysis pipeline have been reframed along the in-depth discovery and analysis of the build datasets.**

## Timeline

* Step 2: 22/11/21
* Step 3, 4: 29/11/21
* Step 5: 06/12/21
* Step 6, 7, 8: 13/12/21

## Organization within the team

Paul: Wikidata scrapping. Descriptive analysis of data. Speaker analysis. Construction of subsets D1.1-3, D2.1-3. Statistical analysis.
Joseph: Pre-processing of Quotebank dataset. Construction of D1, D2, D3. Website development. Datastory. Plots.
Amaëlle: NLP pipeline and Wordcloud processing. Notebook cleaning and discussions. Read_me. General project planning. Statistical analysis.
Louis: SpaCy Training on AD2 with a classifier on misogynist quotes. Read_me. General project planning. Website development. Plots. Statistical analysis.

