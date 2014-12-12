from math import hypot
import numpy as np
import pandas as pd
import random
from IPython import display
from IPython.display import Image as PyImage

"""
Prepare our master DataFrame
Combination of the GIF data, the links data, and the GIF emotion data
"""

gif_data = pd.read_csv('data/buzzfeed_gifs_master.csv')
GIFs = pd.read_csv('data/crowdsourced_gif_emotions/gifs.csv', names=['id', 'gif_id', 'x', 'y'])
links = pd.read_csv('data/crowdsourced_gif_emotions/links.csv', names=['gif_id', 'url'])

master = pd.merge(gif_data, links, how='right', left_on='URL', right_on='url')

master = master.merge(GIFs)
master['GIF_x'] = master.apply(lambda gif: (gif['x']-0.5),axis=1)
master['GIF_y'] = master.apply(lambda gif: (-1.0*gif['y']+0.5),axis=1)

"""
Read in the sentiment dictionary and calculate the sentiment means
"""

sentiment_dict = pd.read_csv("data/sentiment-dictionary.csv", index_col='Word')
sentiments = sentiment_dict[['V.Mean.Sum', 'A.Mean.Sum', 'V.SD.Sum', 'A.SD.Sum']]

vm = sentiments['V.Mean.Sum']
vm = (vm - vm.mean()) / (vm.max() - vm.min())
sentiments['valence_mean'] = vm

am = sentiments['A.Mean.Sum']
am = (am - am.mean()) / (am.max() - am.min())
sentiments['arousal_mean'] = am


def estimate_word_sentiment(word):
    """
    Given a word, estimate the valence and arousal of the word 
    (placing it on the x,y coordinate plane)
    """
    valence_mean = sentiments.ix[word]['valence_mean']
    valence_std = sentiments.ix[word]['V.SD.Sum']
    
    arousal_mean = sentiments.ix[word]['arousal_mean']
    arousal_std = sentiments.ix[word]['A.SD.Sum']
    
    return valence_mean, arousal_mean, valence_std,  arousal_std
    
def estimate_phrase_sentiment(phrase):
    """
    Given a phrase, estimate the sentiment of the phrase
    Based on the aggregation of word sentiments
    """
    
    words = phrase.split(' ')
    
    total_vm = 0.0
    total_am = 0.0
    total_vsd = 0.0
    total_asd = 0.0
    count = 0
    
    for word in words:
        if word in sentiments.index:
            vm, am, vsd,  asd = estimate_word_sentiment(word)
            total_vm += vm
            total_am += am
            total_vsd += vsd
            total_asd += asd
            count += 1
    
    if count == 0:
        return False
    
    return (total_vm/count, total_am/count, total_vsd/count, total_asd/count)

def extract_points_to_plot(text_col):
    """
    Given text, do the sentiment analysis above
    Then place the sentiment on the x,y sentiment plane.
    """
    
    xs = []
    ys = []
    
    for text in text_col:
        
        sentiment = estimate_phrase_sentiment(text)
        
        if sentiment:
            xs.append(sentiment[0])
            ys.append(sentiment[1])
        else:
            xs.append(None)
            ys.append(None)
            
    return xs, ys

xs, ys = extract_points_to_plot(master['Text'].fillna(''))
master['text_x'] = xs
master['text_y'] = ys

print 'Sentiment Analysis Engine Initialized'