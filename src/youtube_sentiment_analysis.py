#!/usr/bin/env python
# coding: utf-8

# # Sentiment Analysis on Youtube Comments


import pandas as pd
import numpy as np
import nltk
nltk.download(['vader_lexicon'])
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from collections import Counter
import matplotlib.pyplot as plt

get_ipython().run_line_magic('matplotlib', 'inline')
pd.options.mode.chained_assignment = None
pd.set_option('display.max_colwidth', 100)

with open('youtube_comments_clean.csv',encoding="utf8") as file:
    df = pd.read_csv(file)
file.close()
df.head()

df.drop(['time_uploaded','no_of_views','channel','no_contract','tokenized','lower','no_punct','no_stopwords','pos_tags','wordnet_pos'], axis=1,inplace=True)

# listify the stringed list
df["lemmatized"] = df["lemmatized"].apply(lambda comment : eval(comment))
df['lemma_str'] = [' '.join(map(str,l)) for l in df['lemmatized']]
df.head()

sia = SentimentIntensityAnalyzer()

# make a column of VADER polarity scores, with -1 being most negative and 1 being most positive
df["sentiment_compound"] = df["lemma_str"].apply(lambda comment: sia.polarity_scores(comment)["compound"])

df.head()

print(type(df['sentiment_compound']))

# graph out sentiment distribution
plt.figure(figsize=(50,30))
plt.margins(0.02)
plt.xlabel('Sentiment', fontsize=50)
plt.xticks(fontsize=40)
plt.ylabel('Frequency', fontsize=50)
plt.yticks(fontsize=40)
plt.hist(df['sentiment_compound'], bins=50)
plt.title('sentiment Distribution', fontsize=60)
plt.show()