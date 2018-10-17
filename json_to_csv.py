import sys
import json
import csv


# set json file path
json_file_path = "cleaned_twitter_elections_data.json"

tw_header = ['id', 'screen_name', 'place', 'country_code', 'user_location', 'name', 'text', 'favorite_count', 'retweet_count',  'created_at', 'is_quoted', "source",
             'q_id', 'q_screen_name', 'q_name', 'q_text', 'q_created_at', 'q_source']

# csv file name
csv_writer_t = csv.writer(open("status_new.csv", "w"))

csv_writer_t.writerow(tw_header)


data = json.load(open(json_file_path))

data_t = {}

total_tweets = 0
for t in data:
    for i in tw_header:
        data_t[i] = None
    try:
        data_t['id'] = t['id_str']
        data_t['screen_name'] = t['user']['screen_name']
        data_t['name'] = t['user']['name']
        data_t['text'] = t['text']
        data_t['favorite_count'] = t['favorite_count']
        data_t['retweet_count'] = t['retweet_count']
        data_t['created_at'] = t['created_at']
        data_t['is_quoted'] = t['is_quote_status']
        data_t['source'] = t['source']
        if t['place']:
            data_t['place'] = t['place']['full_name']
            data_t['country_code'] = t['place']['country_code']
        data_t['user_location'] = t['user']['location']
        if t['is_quote_status']:
            if t.get('quoted_status'):
                r = 'quoted_status'
            else:
                r = "retweeted_status"
            data_t['q_id'] = t[r]['id_str']
            data_t['q_screen_name'] = t[r]['user']['screen_name']
            data_t['q_name'] = t[r]['user']['name']
            data_t['q_text'] = t[r]['text']
            data_t['q_created_at'] = t[r]['created_at']
            data_t['q_source'] = t[r]['source']
    except Exception as e:
        data_t['is_quoted'] = False
        print("Inconsistency: " + str(e))
        print("Inconsistency at {}".format(t['id']))
    csv_writer_t.writerow(data_t.values())
    total_tweets+=1
    
print("\nSaved csv with {} rows".format(total_tweets))

