from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from matplotlib.colors import makeMappingArray
from palettable.colorbrewer.diverging import Spectral_4
from collections import Counter
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def display_wordcloud(tokens, title, fname):
    tokens_upper = [token.upper() for token in tokens]
    cloud_mask = np.array(Image.open("cloud_mask.png"))
    wordcloud = WordCloud(max_font_size=100, 
                          max_words=50, width=2500, 
                          height=1750,mask=cloud_mask, 
                          background_color="white").generate(" ".join(tokens_upper))
    plt.figure()
    fig, ax = plt.subplots(figsize=(14, 8))
    plt.title(title, fontsize=20)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(fname  + '.png')   
    plt.show()
    return

def join_edited_string(edited_tweets):
    
    edited_string = ''
    for row in edited_tweets:
        edited_string = edited_string + ' ' + row
        
    return edited_string

joined_string = join_edited_string(scrapedData['edited'])

# Get tokens
tokens = joined_string.split(' ')

display_wordcloud(tokens, 'Wordcloud of tweets', 'WordCloud_during_onlinestorm')