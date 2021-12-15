# MeToo, a catalyst for change?

___Study of the influence of the movement on women's mediatic representation___

## Abstract

“#MeToo". Two words, a hashtag, civil rights movement with tremendous impacts on our society. Everything starts on October 15th, 2017, with a viral Twitter hashtag from Alyssa Milano. The movement, initially created by Tarana Burke, spread all over the world, inviting women to break silence on sexual harassment, violence, discrimination via social networks. The medias stepped in with widespread coverage and enhanced the movement's influence. Finally, women inequalities and the unsafe climate created by actors of society became a trending and polarizing topic on all media. Still, the question of the size of MeToo's impact on women's discrimination is to be answered. Via the metric of women's mediatic coverage, our project aims at assessing and quantifying the impact of #MeToo on the place of women in society. By using Quotebank dataset from 2015 to 2020, we will investigate the evolution of women’s mediatization through time and correlate it to #MeToo's key turning points.

## Research questions

* How has the mediatization of women been tuned by the emergence of the MeToo movement?
  A) What is the evolution of the general mediatic perspective of the MeToo movement? Are there any gender, political or generational biases observable in its mediatic coverage?
  B) Linguistic analysis of women's mediatic representation: how did the terms and tones used by the speakers in media (when speaking of women) change through time ?
  C) Is the evolution of women's mediatization (addressed in sub-question B) correlated to the tendency of MeToo's mediatic perspective (addressed in sub-question A)?

## Proposed additional datasets

* **AD1 : [Wikidata speakers_attribute.parquet](https://drive.google.com/drive/folders/1VAFHacZFh0oxSxilgNByb1nlNsqznUf0)**: dataset provided in the scope of the ADA course, to access Wikidata metadata on Quotebank speakers. The format of the data can be found in the schema_speakers_attribute.txt file. We will scrap only the attributes "fields date_of_birth", "party" and "gender" for the investigation of biases in the speakers addressing the MeToo movement in media.
* **AD2 : [AMI (Automatic Misogyny Detection) Iber Eval dataset](https://drive.google.com/drive/folders/13UfLXcPTvT9bEAPP8tLj2quXGGa2gsTq)**  : dataset created to train NLP models to detect misogynistic speech in tweets and online content. The dataset is open source but an access authorization must be requested to access the data and we thus haven’t been able to explore the data yet. However, by reading the documentation provided on the AMI website, we already know the following:
  * Divided into a train and test dataset.
  * Train dataset : composed of 3’251 english and 3’307 spanish tweets. Spanish tweets will be deleted.
  * Tab-separated with the following fields: “id” “tweet” “misogynous” “misogyny_category” “target”.
  * The misogynous category takes the value 1 if the tweet is considered misogynous and 0 if not.
  * The misogyny_category classify misogynous tweets as: “stereotype” , “dominance”, “derailing” and “sexual_harassment”.
  * Size: ~300KB.
## Methods

**Step 1: Data scraping, pre-processing and dataset construction.**

* Dataset D1 : General dataset containing quotes of women authors
* Dataset D2 : MeToo dataset containing quotes linked to the movement, in which the movement is mentioned
  * D2.1 : Subsets by gender of speaker
  * D2.2 : Subsets by age of speaker
  * D2.3 : Subsets by political parties (for politician authors) of speaker\
    *These subsets are built later on during Step 4.*
* Dataset D3 : Dataset containing quotes in which a woman is mentioned
  * D3.1: Subset by gender of speaker

**Step 2: General preliminary analysis using Quotebank entire dataset**
Weekly percentage of quotes by author’s gender (men, women, other, unkown) from 2015 to 2020.

**Step 3: Generate annual word clouds based on dataset D1 with this [library.](https://github.com/amueller/word_cloud)**

**Step 4: Investigate gender, political and generational biases in MeToo coverage using NLP to answer question A).**
Train a [SpaCy NLP model](https://spacy.io/usage/training) with dataset AD3 to perform sentiment analysis. Classification thanks to trained model on the whole dataset D2. Subdivision of D2 into D2.1, D2.2 and D2.3 for biases investigation. Clustering trials with unsupervised different ML algorithms applied on the sentiment analysis classification probabilities.

**Step 5: Investigate general women perception via dataset D3 in medias to answer question B).**
Generate word clouds. Classification of quotes : Text Blob or Vader models for positive, negative or neutral. Train SpaCy model on AD2 for misogynistic or non misogynistic. Classification thanks to trained model on D3.

**Step 6: Correlate and investigate causation between MeToo general perception and women’s mediatic place to answer question C).**
Plot previously collected (step 5) data distributions according to time. Comparison with key turning points of MeToo. Investigation of the statistical significance of detected changes before and after MeToo.

**Step 7: Github site building and Datastory redaction.**

**Further details on the proposed data pipelines can be found in the notebook.**

**Note: Since Milestone 2, we redirected some aspects of our project, namely the aditionnal datasets have changed due to ungranted access. Additionnally, some steps of the data analysis pipeline have been reframed along the in-depth discovery and analysis of the build datasets.**
## Proposed timeline

* Step 2: 22/11/21
* Step 3, 4: 29/11/21
* Step 5: 06/12/21
* Step 6, 7: 13/12/21

## Organization within the team
Paul:
Joseph: 
Amaëlle: 
Louis:

* SpaCy Training on AD2 and AD3: Teammate 1
* Datastory: Teammate 2
* Website: Teammate 3 and 4
* Steps: Teammate 1,2,3,4
