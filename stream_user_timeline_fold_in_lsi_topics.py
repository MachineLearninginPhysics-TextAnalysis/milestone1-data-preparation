# -*- coding: utf-8 -*-
"""stream_user_timeline_fold_in_lsi_topics.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ioMH6roe66K8UJinzNhh100FEfggkXbE
"""

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)

import tweepy as tw

# define keys
consumer_key= 'gEJhQtgiIvxzNB50u4JPic8f4'
consumer_secret= 'iEfTG65lFX8cAzKJ4QIhJklvuh3tfWdaRAAWO3b17082dZaSiu'
access_token= '1369691334051852293-IGWGrIUKFY6rTwmrA5WD3YLkJrlUk5'
access_token_secret= '7ftmxYiYnso7PNkPOWOWKCkNrguFFMhwwPTHhQ6bFVvgG'
# authenticate and create api object
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

import re

# just see how iterate through first 3 user's timeline pages with cursor
for page in tw.Cursor(api.user_timeline,
                      id="indykaila", exclude_replies=True,
                      include_rts=False, tweet_mode='extended').pages(3):
    for status in page:
        # preprocess documents (remove links and punctuations) to raw texts
        print(status.full_text)
        print(status.full_text.lower().split())
        link_removed = re.sub(r'\bhttps:\S+', '', status.full_text.lower())
        punc_link_removed = re.sub(r'[–,-.!":]\D', ' ', link_removed)
        print(punc_link_removed.split(), '\n---')

"""# Corpora"""

class MyTexts:
    """implement a generator object on a specific user timeline
    and preprocess (remove links and punctuations)
    to yield as row tokenized texts"""
    def __init__(self, pagination_num=3):
        self.pagination_num = pagination_num
        # cursor on user's timeline
        self.cursor = tw.Cursor(api.user_timeline, id="indykaila",
                              exclude_replies=True, include_rts=False,
                              tweet_mode='extended').pages(self.pagination_num)
    def __iter__(self):
        for page in self.cursor:
            for status in page:
                # cleaning: removing links and some punctuations
                link_removed = re.sub(r'\bhttps:\S+', '', status.full_text.lower())
                punc_link_removed = re.sub(r'[–,-.!":]\D', '', link_removed)
                yield punc_link_removed.split()

"""> Collect statistics about corpus, preprocess it and store training corpus"""

from gensim import corpora

texts = MyTexts(3)
# colloct statistics about all tokens
dictionary = corpora.Dictionary(texts)
# preprocess: remove stop words and only once words from dictionary
stop_words = set('for of a an and the to in'.split())
stop_word_ids = [dictionary.token2id[stopword]
                 for stopword in stop_words
                 if stopword in dictionary.token2id]
once_word_ids = [tokenid
                 for tokenid, docfreq in dictionary.dfs.items()
                 if docfreq == 1]
dictionary.filter_tokens(stop_word_ids + once_word_ids)
dictionary.compactify()
print(dictionary.dfs)
# store training corpus in bow representation for later use
# prefer work with generators (corpus streaming) instead of creating lists of documents
# train_texts = [text for text in MyTexts(3)]
train_texts = MyTexts(3)
'''note that every token that removed from dictionary is a "blah" for doc2bow method
and wouldn't count in corpus bow representation
but I use them in train_texts just for see the full texts somewhere'''
# train_corpus_bow = [dictionary.doc2bow(text) for text in train_texts]
train_corpus_bow = (dictionary.doc2bow(text) for text in train_texts)
corpora.MmCorpus.serialize('train_corpus_bow.mm', train_corpus_bow)

dictionary.dfs

train_texts = MyTexts(3)
for text in train_texts:
    print(text)

train_corpus_bow = corpora.MmCorpus('train_corpus_bow.mm')
for doc in train_corpus_bow:
    print(doc)

"""# Train the Models with Training Corpus"""

from gensim import models

# load training corpus in bow from disk
train_corpus_bow = corpora.MmCorpus('train_corpus_bow.mm')
# initialize a tfidf model with training corpus in bow: training
tfidf_model = models.TfidfModel(train_corpus_bow)
# tranform training corpus bow->tfidf
train_corpus_tfidf = tfidf_model[train_corpus_bow]
# train a LSI model with training corpus in tfidf
lsi_model = models.LsiModel(train_corpus_tfidf, id2word=dictionary, num_topics=2)
# tfidf->fold-in-lsi
train_corpus_lsi = lsi_model[train_corpus_tfidf]
train_corpus_lsi

lsi_model.print_topics()

train_texts = MyTexts(3)
for doc_lsi, as_text in zip(train_corpus_lsi, train_texts):
    print(doc_lsi, as_text)