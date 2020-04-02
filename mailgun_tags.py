import time
import requests
import json
import pandas as pd
import pprint

# fill in with your api key
API_KEY = 'censored'

# make api request
r = requests.get("https://api.mailgun.net/v3/afts.com/tags",auth=("api", API_KEY))

# API response comes in JSON format
# use built-in json decoding method to parse it to a dictionary
response_dict = r.json()

# display the response in a way that's easier to read
pp = pprint.PrettyPrinter()
pp.pprint(response_dict)


items = response_dict["items"]

# a list of all the tags in the response
tags = [item["tag"] for item in items]

print("Total number of tags:", len(tags))


def filter_out_2020(tags: list):
    # filter out all the tags that contain the string '2020'
    return [tag for tag in tags if "2020" not in tag]

# print("Tags not containing 2020:")
# print(filter_out_2020(tags))


def delete_tag(TAG_STRING):
    return requests.delete(
        "https://api.mailgun.net/v3/afts.com/tags/" + TAG_STRING,
        auth=("api", API_KEY))

# a list of all the tags that don't contain '2020'
tags_not_2020 = filter_out_2020(tags)

# replace this with whatever list of tags you want to delete
tags_to_delete = ["Alderwood-2019-JUN-26"]  # or tags_not_2020

# delete each tag one by one
for tag in tags_to_delete:
    response = delete_tag(tag)

    # it returns 200 even if the tag didn't exist
    if response.status_code == 200:
        print("Tag " + tag + " successfully deleted or doesn't exist")
    else:
        print("ERROR deleting tag " + tag + ": ")
        pp.pprint(response.json())
