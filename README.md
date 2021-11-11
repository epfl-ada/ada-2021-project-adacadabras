# MeToo, a catalyst for change?
___Study of the influence of the movement on women's mediatic representation___
## Abstract
“#MeToo". Two words, a hashtag, a civil rights movement with tremendous impacts on our society. Everything starts, on October 15th, 2017, with a viral hashtag on Twitter, posted by Alyssa Milano. The movement, initially created by Tarana Burke, spread all over the world, inviting women and minorities to break the silence on sexual harassment, violence, and discrimination via social networks. The medias stepped in with a widespread coverage and enhanced the movement influence. Finally, women inequalities and the unsafe climate the society offers them, became a trending and polarized topic on all medias. Still, the question of impact size of MeToo on women's importance and discrimination is to be answered. Via the metric of women's mediatic coverage, our project aims at assessing and quantifying the impact of #MeToo on the way women are given a place in our society. By using Quotebank dataset from 2015 to 2020, we will investigate the evolution of women’s mediatization through time and correlate it to #MeToo key turning points.

## Research questions
* How has the mediatization of women been tuned by the emergence of the MeToo movement?
    * A) What is the evolution of the general mediatic perspective of MeToo movement ? Are there any gender, political or generational biases observable in the mediatic coverage of the movement ? 
    * B) Linguistic analysis of women's mediatic representation: How did the terms and tones used by the speakers in medias (when speaking of women) change through time ? How does the themes discussed evolve ? 
    * C) Is the evolution of women's mediatization (addressed in sub-question B) correlated to the tendency of MeToo's mediatic perspective (addressed in sub-question A)? 

## Proposed additional dataset
*  **Wikidata speakers_attribute.parquet** (https://drive.google.com/drive/folders/1VAFHacZFh0oxSxilgNByb1nlNsqznUf0): dataset provided in the scope of the ADA course, to access Wikidata metadata on Quotebank speakers. The format of the data can be found in the schema_speakers_attribute.txt. We will scrap only the attributes "fields date_of_birth", "party" and "gender" for the investigation of biases in the speakers addressing the MeToo movement in medias.
*  **AMI (Automatic Misogyny Detection) Iber Eval dataset** (https://drive.google.com/drive/folders/13UfLXcPTvT9bEAPP8tLj2quXGGa2gsTq) : dataset created to train NLP models to detect misogynistic speech in tweets and online content. The dataset is open source but an access authorization must be requested to access the data and we thus haven’t been able to explore the data yet. However, by reading research paper that were using the same dataset and a documentation provided on the AMI website, we already know the following:
- - Divided into a train and test dataset.
- - Train dataset : composed of 3’251 english and 3’307 spanish tweets. Spanish tweets will be deleted.
- - Tab-separated with the following fields: “id” “tweet” “misogynous” “misogyny_category” “target”.
- - The misogynous category takes the value 1 if the tweet is considered misogynous and 0 if not.
- - The misogyny_category classify misogynous tweets as: “stereotype” , “dominance”, “derailing” and “sexual_harassment”.
- - Size: ~300Ko.
* **Metooma dataset** (https://huggingface.co/datasets/metooma#social-impact-of-dataset / https://github.com/huggingface/datasets/blob/master/datasets/metooma/README.md): dataset similar to AMI composed of set of tweets belonging to the #MeToo movement, labelled to train NLP models to detect tone of speech and support or opposition to the movement. Here is a list of relevant information about it:
- - Divided into a train (7979 english tweets) and test dataset (1996 english tweets).
- - Tab-separated with the following fields: TweetId (string), Text_Only_Informative (class label), Image_Only_Informative (class label), Directed_Hate (class label), Generalized_Hate (class label), Sarcasm (class label), Allegation (class label), Justification (class label), Refutation (class label), Support (class label), Oppose (class label).
- - Tweet contents should be accessed using TweetId and twitter API.
* **Allegations list** https://www.vox.com/a/sexual-harassment-assault-allegations-list/frankie-shaw : list of 262 CEO’s, celebrities, politicians and others who have been accused of sexual misconduct between 2017 and 2020 in the scope of the #MeToo movement. This list is available on the internet and will be extracted by scraping the HTML page of the website. Additional information on the profession of the aggressor is available in the data and might be used for further analysis. 

## Methods


## Proposed timeline

## Organization within the team
## Questions for TA (optional)


