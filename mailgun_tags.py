import time
import requests
import json
import pandas as pd

# fill in with your api key
API_KEY = 'censored'



def delete_tag(TAG_STRING):
    return requests.delete(
        "https://api.mailgun.net/v3/afts.com/tags/" + TAG_STRING,
        auth=("api", API_KEY))


r = requests.get("https://api.mailgun.net/v3/afts.com/tags",auth=("api", API_KEY),
        params={"limit": 5})

# get mailgun data 
data_string = r.text
# is this json data ?
## print(data_string)

## print(" ")
## print(" -- json above ?? -- ")
## print(" ")

#convert to dict - is this a way to get the rows to access the 'tag' data
a_dict = json.loads(data_string)

## for item in a_dict.items():
##     print(item)
##     print(type(item))

## print(" ")
## print("now here")
## print(" ")

keys = a_dict.keys()
print(keys)

print(" ")
print("keys above values below")
print(" ")


values = a_dict.values()
print(values)

delete_tag("Alderwood-2019-JUN-26")
print("Tag deleted...")