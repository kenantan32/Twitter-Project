import twint
from deep_translator import GoogleTranslator, single_detection
import pandas as pd


def twint_to_pd(columns):
    return twint.output.panda.Tweets_df[columns]

c = twint.Config()
c.Search = 'covid' #Search tweet that contain the word "covid"
c.Geo = "1.352083,103.819839,20km" #Geo define the geolocation of the origin of the Tweet. Hence, Singapore's Geo Location will be use in this Singapore-Based Project
c.Since = "2021-09-24" #Search tweet from the date 2021/09/24
c.Limit = '20' #Limit Define the number of tweet to Extract
c.Pandas = True 
twint.run.Search(c)


data = twint_to_pd(['id', 'conversation_id', 'created_at', 'date', 'timezone', 'place',
       'tweet', 'language', 'hashtags', 'cashtags', 'user_id', 'user_id_str',
       'username', 'name', 'day', 'hour', 'link', 'urls', 'photos', 'video',
       'thumbnail', 'retweet', 'nlikes', 'nreplies', 'nretweets', 'quote_url',
       'search', 'near', 'geo', 'source', 'user_rt_id', 'user_rt',
       'retweet_id', 'reply_to', 'retweet_date', 'translate', 'trans_src',
       'trans_dest'])

data.to_csv("DataSet.csv", index=False) #Data Scraped for twint is written to a CSV. 

df=pd.read_csv("DataSet.csv")
df.drop(df[df['language'] == 'und'].index, inplace = True) #No language detection when tweets contain only URL. Such tweets is labeled as "und" by twint.
df.to_csv("DataSet.csv", index=False) #Write/update changes to CSV file

num = len(df['tweet'])
count = 1

for i in range(0,num,1):
    lang = single_detection(df['tweet'][i], api_key='882c59b16ed56b80efb9405b96bc6926')
    if lang != 'en':
        df._set_value(i, 'tweet',GoogleTranslator(source='auto', target='en').translate(df['tweet'][i]))
        df.to_csv("DataSet.csv", index=False)
        count += 1
        print("Row Number:"+str(count) + " (Translated Tweet)")
    else:
        count += 1
        print("Row Number:"+str(count) + " (English Tweet)")

print("Refer to DataSet.csv for result")