#train_spacy.py
import pandas as pd
import spacy
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.svm import LinearSVC
from sklearn.svm import LinearSVC
import pickle
import re

nlp = spacy.load('en_core_web_sm')

def remove_url(text):
    url = re.compile(r"https?://\S+|www\.\S+")
    return url.sub(r"", text)

def remove_html(text):
    html = re.compile(r"<.*?>")
    return html.sub(r"", text)

def remove_emoji(text):
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub(r"", text)

def text_data_cleaning(sentence):
    sentence = remove_url(sentence)
    sentence = remove_html(sentence)
    sentence = remove_emoji(sentence)
    doc = nlp(sentence)

    tokens = []
    for token in doc:
        if token.lemma_ != "-PRON-":
            temp = token.lemma_.lower().strip()
        else:
            temp = token.lower_
        tokens.append(temp)
    
    cleaned_tokens = []
    for token in tokens:
        if token not in nlp.Defaults.stop_words and token not in punct:
            cleaned_tokens.append(token)
    return cleaned_tokens


'''####MAIN#########

PATH_DATA = './data/data_nlp/'
AD1_FILE = PATH_DATA + 'MeTooHate.csv'
CHUNK_SIZE = 1000

#Clean data
df = pd.read_csv(AD1_FILE)
df.drop(columns=['status_id', 'created_at', 'favorite_count', 'retweet_count',
       'location', 'followers_count', 'friends_count', 'statuses_count',
       ], inplace=True)

df.dropna(inplace=True)

#create spacy
nlp = spacy.load('en_core_web_sm')
punct = string.punctuation

###tfidf and classifier
tfidf = TfidfVectorizer(tokenizer=text_data_cleaning)
classifier = LinearSVC(verbose=True)

#Train/test data
X = df.text
y = df.category
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42 )

clf = Pipeline([('tfidf', tfidf), ('clf', classifier)], verbose=True)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

print(classification_report(y_test,y_pred))

print('Confusion matrix: ',confusion_matrix(y_test, y_pred))

#Save model in pickle
filename = './data/data_nlp/classifier.sav'
pickle.dump(clf, open(filename, 'wb'))'''