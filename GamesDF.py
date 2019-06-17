from bs4 import BeautifulSoup
import os
import pandas as pd



all_games = {}

def make_game_df(filename):

    with open(filename, 'rb') as f:
        collection = f.read()
        soup = BeautifulSoup(collection, "lxml")
        games = soup.find_all('item')






        for game in games:
            image_obj = game.find('image')
            if image_obj:
                image = image_obj.text
            else:
                image = None



            name = game.find('name').text

            year_published_obj = game.find('yearpublished')
            if year_published_obj:
                year_published = year_published_obj.text
            else:
                year_published = None







            itemnumber = game.attrs['objectid']


            # Gathering all the stats about the game stored in the stats tag
            stats = game.find('stats')


            if 'maxplayers' in stats.attrs:
                max_players = stats.attrs['maxplayers']
            else:
                max_players = None

            if 'minplayers' in stats.attrs:
                min_players = stats.attrs['minplayers']
            else:
                min_players = None





            if 'minplaytime' in stats.attrs:
                min_playtime = stats.attrs['minplaytime']
            else:
                min_playtime = None




            num_owned = stats.attrs['numowned']


            # trying something else. this should not be necessary, but it works

            users = stats.find('usersrated')
            users_rated = users.attrs['value']
            rating_avg = stats.find('average')
            rating_average = rating_avg.attrs['value']

            # types get written in a strange format so needing to try something else again
            complete_types = []
            types = game.find_all('rank')
            for type in types:
                all_types = type.attrs['name']
                complete_types.append(all_types)

            if name not in all_games:
                all_games[name] = [image, year_published, itemnumber, max_players, min_players, min_playtime, num_owned,
                               rating_average, complete_types]








path = 'Test'

for filename in os.listdir(path):
    make_game_df(path + "/" + filename)


#print(all_games)

games_df = pd.DataFrame.from_dict(all_games, orient='index')
games_df.columns = ['image', 'year_published', 'item_number', 'max_players', 'min_players', 'min_playtime',
                    'num_owned', 'rating_average', 'complete_types']

# saving the df as csv
games_df.to_csv('games', sep='\t', encoding='utf-8')