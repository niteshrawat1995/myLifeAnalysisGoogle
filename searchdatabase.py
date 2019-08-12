import mysql.connector
import json
import os
import datetime
import time
from tqdm import tqdm

db = mysql.connector.connect(
    host="localhost", user="nitesh", password="password", database="mylife")
cur = db.cursor()
# cur.execute("SELECT * FROM openedx.auth_user")
# data = cur.fetchall()
# print(data)

SEARCH_ACTIVITY = os.path.join(
    os.getcwd(), "takeout-20190811T082416Z-001/Takeout/My Activity/Search", "MyActivity.json")


def make_table():
    cur.execute("""
    CREATE TABLE IF NOT EXISTS words(id int(10) NOT NULL AUTO_INCREMENT PRIMARY KEY, timestamp DECIMAL(13,1), word TEXT)
    """)


def search_data():
    stop_words = ["a", "about", "above", "after", "again", "against", "ain", "all", "am", "an", "and", "any", "are", "aren", "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can", "couldn", "couldn't", "d", "did", "didn", "didn't", "do", "does", "doesn", "doesn't", "doing", "don", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn", "hadn't", "has", "hasn", "hasn't", "have", "haven", "haven't", "having", "he", "her", "here", "hers", "herself", "him", "himself", "his", "how", "i", "if", "in", "into", "is", "isn", "isn't", "it", "it's", "its", "itself", "just", "ll", "m", "ma", "me", "mightn", "mightn't", "more", "most", "mustn", "mustn't", "my", "myself", "needn", "needn't", "no", "nor", "not", "now", "o", "of", "off", "on", "once", "only", "or", "other", "our", "ours", "ourselves", "out",
                  "over", "own", "re", "s", "same", "shan", "shan't", "she", "she's", "should", "should've", "shouldn", "shouldn't", "so", "some", "such", "t", "than", "that", "that'll", "the", "their", "theirs", "them", "themselves", "then", "there", "these", "they", "this", "those", "through", "to", "too", "under", "until", "up", "ve", "very", "was", "wasn", "wasn't", "we", "were", "weren", "weren't", "what", "when", "where", "which", "while", "who", "whom", "why", "will", "with", "won", "won't", "wouldn", "wouldn't", "y", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves", "could", "he'd", "he'll", "he's", "here's", "how's", "i'd", "i'll", "i'm", "i've", "let's", "ought", "she'd", "she'll", "that's", "there's", "they'd", "they'll", "they're", "they've", "we'd", "we'll", "we're", "we've", "what's", "when's", "where's", "who's", "why's", "would"]

    with open(SEARCH_ACTIVITY, "r", encoding='utf-8') as f:
        data = json.load(f)

        for val in tqdm(data):
            try:
                word = val["title"].strip().lower()
                date = val["time"].split("T")[0]
                timestamp = time.mktime(
                    datetime.datetime.strptime(date, "%Y-%m-%d").timetuple())
                # print(timestamp)
                if "searched for" in word:
                    search_string = word.replace(
                        "searched for ", "").split()

                    for w in search_string:
                        if w not in stop_words:
                            insert_query = """INSERT INTO words(timestamp, word) values ({}, "{}")""".format(
                                timestamp, w)
                            # print(insert_query)
                            cur.execute(insert_query)
            except Exception as e:
                print(e)


make_table()
search_data()
db.commit()
db.close()
