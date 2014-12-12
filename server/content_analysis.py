import nltk.corpus
import nltk.tokenize.punkt
import string
import re
import pandas as pd
import numpy as np

data1 = pd.read_csv('data/pos_tagged_gif_data.csv')
data2 = pd.read_csv('data/categorized_emotions.csv')
data = data1.merge(data2, left_on='URL', right_on='url')

# Create a set of stopwords based on the default NLTK english stopwords
# Be sure to also include punctuation and the empty string
stopwords = nltk.corpus.stopwords.words('english')
stopwords.extend(string.punctuation)
stopwords.append('')

# Instantiate a tokenizer that tokenizes a given string
# Also instantiate the NLTK stemmer
tokenizer = nltk.tokenize.punkt.PunktWordTokenizer()
stemmer = nltk.stem.snowball.SnowballStemmer('english')

print 'Sentiment Analysis Engine Initialized'
 
def check_matching_tokens(a, b):
    """
    A fuzzy matcher that sees if significant word stems match between two strings.
    Inspired by the examples here: http://bommaritollc.com/2014/06/fuzzy-match-sentences-python/
    """
    
    tokens_a = [token.lower().strip(string.punctuation) for token in tokenizer.tokenize(a) if token.lower().strip(string.punctuation) not in stopwords]
    stems_a = [stemmer.stem(token) for token in tokens_a]
    
    tokens_b = [token.lower().strip(string.punctuation) for token in tokenizer.tokenize(b) if token.lower().strip(string.punctuation) not in stopwords]
    stems_b = [stemmer.stem(token) for token in tokens_b]
    
    match = set(stems_a) & set(stems_b)
    return len(match)


def find_matching_gifs_by_content(input_string, data=data, output=True):
    """
    Given an input string and a master dataframe (data)
    Find the GIFs with matching tokenized content stems (ordered by number of matches)
    """
    
    matches = []
    
    texts = data['Text'].fillna('')
    titles = data['Title'].fillna('')
    
    # iterate through all text and remove all weird unicode characters
    # then search for matches in our tokenized corpus
    combined_text = [texts[i] + ' ' + titles[i] for i in range(len(data))]
    for text in combined_text:
        text = re.sub(r'[^\x00-\x7F]+',' ', text)
        n_matches = check_matching_tokens(text, input_string)
        matches.append({'Match': True if n_matches > 0 else False, 'n': n_matches })

    match_table = pd.DataFrame(matches)
    df = data.copy()
    df['Match'] = match_table['Match']
    df['N Matches'] = match_table['n']
    
    # If there is one or more match, return one of the matches with the greatest number of
    # individual word matches
    if np.sum(df['Match']) > 0:
        df = df[match_table['Match']].sort(columns='N Matches', ascending=False)
        max_n = max(df['N Matches'])
        df = df[df['N Matches'] == max_n]
        i = np.random.choice(df.index, 1)[0]
        url= df.ix[i]['url']
        t = df.ix[i]['Text']
        return df
    # otherwise, return an empty list
    else:
        return pd.DataFrame()