import mysql.connector
import json
import os
import datetime
import time

from tqdm import tqdm
from collections import Counter

import matplotlib.pyplot as plt
from matplotlib import style

import numpy as np

style.use("ggplot")


db = mysql.connector.connect(
    host="localhost", user="nitesh", password="password", database="mylife")
cur = db.cursor()

WORD_IMAGES_DIR = os.path.join(
    "/home/niteshrawat/My_Projects/gdata", "word_images_per_day")

DAY = 86400
YEAR = 365 * DAY

SLIDE = 1 * DAY
WINDOW = 1 * YEAR


def words_graph():
    cur.execute("SELECT min(timestamp), MAX(timestamp) FROM words")
    min_time, max_time = cur.fetchall()[0]

    START = min_time
    END = min_time + WINDOW
    print("min_time: {}".format(str(min_time)))
    print("max_time: {}".format(str(max_time)))

    counter = 0
    while END < max_time:
        print(counter)
        if os.path.isfile(os.path.join(WORD_IMAGES_DIR, f"{counter}.png")):
            pass
        else:
            START_STR = str(START)
            END_STR = str(END)
            select_query = "SELECT word FROM words WHERE timestamp BETWEEN" + \
                " {} ".format(START_STR) + "AND" + " {} ".format(END_STR)
            cur.execute(select_query)
            data = cur.fetchall()

            words = [i[0] for i in data]
            word_counter = Counter(words)

            common_words = [i[0] for i in word_counter.most_common(10)]
            words_count = [i[1] for i in word_counter.most_common(10)]
            # print(common_words)
            # print(words_count)

            # graph_plotting
            y_pos = np.arange(len(common_words))
            # print(y_pos)
            plt.figure(figsize=(12, 7))
            plt.bar(y_pos, words_count, align="center", alpha=0.5)
            plt.xticks(y_pos, common_words)
            plt.ylabel("Volume")
            date = datetime.datetime.fromtimestamp(END).day
            month = datetime.datetime.fromtimestamp(END).month
            year = datetime.datetime.fromtimestamp(END).year

            plt.title("{}-{}-{}".format(date, month, year))
            # plt.show()
            plt.savefig(os.path.join(WORD_IMAGES_DIR, f"{counter}.png"))
            plt.close()

        counter += 1
        START += SLIDE
        END += SLIDE


words_graph()
