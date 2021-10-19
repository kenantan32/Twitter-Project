import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer 
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import pos_tag
import re
import string
import pandas as pd

# I am adding my own stopwords list to the NLTK list.
# This way we can drop words that are irrelevant for text processing
MY_STOPWORDS = ['singapore','vaccine']
STOPLIST = set(stopwords.words('english') + list(MY_STOPWORDS))
SYMBOLS = " ".join(string.punctuation).split(" ") + ["-", "...", "”", "``", ",", ".", ":", "''","#","@"]

# The NLTK lemmatizer and stemmer classes
lemmatizer = WordNetLemmatizer()
stemmer = SnowballStemmer('english')

# read english selected tweets, no duplicates
scrapedData = pd.read_csv('demo.csv')
list = [x for x in range(0,len(scrapedData.columns))]
scrapedData.columns = list

scrapedData.head()

# Input all text values into a list.
# Each text value will be referred to in this code as a document.
data = scrapedData.text.values.tolist()
# I use the POS tagging from NLTK to retain only adjectives, verbs, adverbs 
# and nouns as a base for for lemmatization.
def get_lemmas(tweet): 
    
    # A dictionary to help convert Treebank tags to WordNet
    treebank2wordnet = {'NN':'n', 'JJ':'a', 'VB':'v', 'RB':'r'}
    
    postag = ''
    lemmas_list = []
    
    for word, tag in pos_tag(word_tokenize(tweet)):
        if tag.startswith("JJ") or tag.startswith("RB") or tag.startswith("VB") or tag.startswith("NN"):
                
            try:
                postag = treebank2wordnet[tag[:2]]
            except:
                postag = 'n'                
                            
            lemmas_list.append(lemmatizer.lemmatize(word.lower(), postag))    
    
    return lemmas_list


# We will now pre-process the tweets, following a pipeline of tokenization, 
# filtering, case normalization and lemma extraction.

# This is the function to clean and filter the tokens in each tweet
def clean_tweet(tokens):
    
    filtered = []
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            if token not in STOPLIST:
                if token[0] not in SYMBOLS:
                    if not token.startswith('http'):
                        if  '/' not in token:
                            if  '-' not in token:
                                filtered.append(token)
                                        
    return filtered


# Prior to lemmatization, I apply POS (part-of-speech) tagging to make sure that only the   
# adjectives, verbs, adverbs and nouns are retained.

# Starts the lemmatization process
def get_lemmatized(tweet):
   
    all_tokens_string = ''
    filtered = []
    tokens = []

    # lemmatize
    tokens = [token for token in get_lemmas(tweet)]
    
    # filter
    filtered = clean_tweet(tokens)

    # join everything into a single string
    all_tokens_string = ' '.join(filtered)
    
    return all_tokens_string

edited = ''
#for i, row in scrapedData.iterrows():
    #edited = get_lemmatized(scrapedData.loc[i]['text'])
    #if len(edited) > 0:
        #scrapedData.at[i,'edited'] = edited
    #else:
        #scrapedData.at[i,'edited'] = None

# After lemmatization, some tweets may end up with the same words
# Let's make sure that we have no duplicates
scrapedData.drop_duplicates(subset=['edited'], inplace=True)
scrapedData.dropna(subset=['edited'], inplace=True) 

# Using apply/lambda to create a new column with the number of words in each tweet
scrapedData['word_count'] = scrapedData.apply(lambda x: len(x['text'].split()),axis=1)
t = pd.DataFrame(scrapedData['word_count'].describe()).T 
print(t)
scrapedData.to_csv('test.csv')

import gensim
from gensim import corpora

cleanData = [clean_tweet(tokens) for tokens in data]
# Create term dictionary for corpus
corpdict = corpora.Dictionary(cleanData)

# Convert list of documents into DTM using above dictionary
docTermMatrix = [corpdict.doc2bow(doc) for doc in cleanData]

# Creating LDA model using gensim
Lda = gensim.models.ldamodel.LdaModel

# Run and Train LDA model on the DTM
model = Lda(docTermMatrix, num_topics=10, id2word=corpdict, passes=50)

# Result here
print(model.print_topics(num_topics=50, num_words=20))