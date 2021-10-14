import pandas as pd

#all im trying to do here is append numbers as columns for the dataframe
scrapedData = pd.read_csv('demo.csv')
list = [x for x in range(0,len(scrapedData.columns))]
scrapedData.columns = list
scrapedData["text"] = scrapedData[10].str.lstrip('"tweet": ')

#ignore the code below here
scrapedData[3] = scrapedData[3].map(lambda x: x.lstrip('"date": "').rstrip('"'))
scrapedData[4] = scrapedData[4].map(lambda x: x.lstrip('"time": "').rstrip('"'))
scrapedData["dateTime"] = scrapedData[3] + ' ' + scrapedData[4]

scrapedData['dateTime'] = pd.to_datetime(scrapedData['dateTime'])

print(scrapedData[["dateTime","text"]])