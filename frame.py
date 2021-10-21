import pandas as pd

file_path = 'DataSet.csv'

#id,conversation_id,created_at,date,timezone,place,tweet,language,hashtags,cashtags,user_id,user_id_str,username,name,day,hour,link,urls,photos,video,thumbnail,retweet,nlikes,nreplies,nretweets,quote_url,search
def convertToDF(x):
    global file_path
    file_path = x
    file_name = file_path  # In same Folder
    file = pd.read_csv(file_name, sep=",")  # Opens CSV in same folder as the .py file
    df = pd.DataFrame(file)  # Converts to dataframe for easier handling
    df.columns = ["ID", "Conversation ID", "Created At", "Date", "Timezone", "Place", "Tweet",
                  "Language", "Hashtags", "Cashtags", "user_id", "user_id_str", "username", "name", "", "",  "", "",  "", "",  "", "",  "", "",  "", "",  "", "",  "", "",  ""]  # Rename Columns
    return df


def getCaseID():
    df = convertToDF(file_path)
    ID = df.get("ID")  # Type == str
    return ID


def getConversationID():
    df = convertToDF(file_path)
    conversationID = df.get("Conversation ID")  # Type == str
    return conversationID

def getLanguage():
    df = convertToDF(file_path)
    language = df.get("Language")  # Type == float
    return language



