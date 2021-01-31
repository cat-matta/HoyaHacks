import pandas as pd
import numpy as numpy
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
from nltk.corpus import stopwords
import string
import contractions
import langdetect
from langdetect import detect 
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer

# Open file
with open('../data/youtube_comments.csv',encoding="utf8") as file:
    df = pd.read_csv(file)
file.close()

# check head
df.head()

# drop unnecessary columns
df.drop(['comment_posted','no_of_replies','downvotes','url','author'],axis=1, inplace=True)

# Check for missing values
for col in df.columns:
    print(col, df[col].isnull().sum())

# fill null values for upvotes ( = 0 likes) as 0
df["upvotes"].fillna(0, inplace=True)

# Check for missing values
for col in df.columns:
    print(col, df[col].isnull().sum())

df.head(5)


### expanding contractions = don't --> do not ###
# add a column with contractions removed
df['no_contract'] = df['comment'].apply(lambda x: [contractions.fix(word) for word in x.split() ])
df.loc[10]

# though sentences are tokenized, the contractions are tokenized into one token
# i.e. We've --> ["we have"] instead of ["we", "have"]
# we'll join the tokens back into singular strings so we can tokenize them later

# map(str,l) takes the iterable l (all values in df['no_contract']) and stringifies it w/ str
df['comments_str'] = [' '.join(map(str, l)) for l in df['no_contract']]
df.head()

#tokenize the comments using NLTK
df['tokenized'] = df['comments_str'].apply(word_tokenize)
df.head()

# convert characters to lowercase
df['lower'] = df['tokenized'].apply(lambda x: [word.lower() for word in x])

# remove punctuations
punct = string.punctuation
# make a list only if token is not a punctuation
df['no_punct'] = df['lower'].apply(lambda x: [word for word in x if word not in punct])

# remove stopwords
stop_words = stopwords.words('english')
df['no_stopwords'] = df['no_punct'].apply(lambda x: [word for word in x if word not in stop_words])

df.head()

# Normalization - lemmatizing
df['pos_tags'] = df['no_stopwords'].apply(nltk.tag.pos_tag)
df.head()

# we convert the speech tags into the appropriate wordnet format
def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('r'):
        return wordnet.ADV
    else:
        return wordnet.NOUN
# replace the pos tag with wordnet tags
df['wordnet_pos'] = df['pos_tags'].apply(lambda x : [(word, get_wordnet_pos(pos_tag)) for (word, pos_tag) in x])

df.head()

# lemmatize comments
lemmatizer = WordNetLemmatizer()
df['lemmatized'] = df['wordnet_pos'].apply(lambda x: [lemmatizer.lemmatize(word,tag) for (word,tag) in x])

df.head()

# finally, save cleaned data into csv file
df.to_csv('../data/youtube_comments_clean.csv')

