from bs4 import BeautifulSoup
import os
import pandas as pd

all = []


def make_rank_df(filename):
    with open(filename, 'rb') as f:
        collection = f.read()
        soup = BeautifulSoup(collection, "lxml")
        games = soup.find_all('item')
        path, file = filename.split('/')
        file2 = file.replace('.xml', '')

        for game in games:
            name = game.find('name').text
            stats = game.find('stats')
            rating = stats.find('rating')
            all.append({'game': name, 'rating': rating.attrs['value'], 'username': file2})


path = 'Test'

for filename in os.listdir(path):
    make_rank_df(path + "/" + filename)

df = pd.DataFrame(all)

# saving the df as csv
df.to_csv('rankings', sep='\t', encoding='utf-8')