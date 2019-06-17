import requests
from bs4 import BeautifulSoup
from requests_futures.sessions import FuturesSession
import pickle
from ast import literal_eval

#Function to take a website and return all the users

def username_extractor(website):
    page = requests.get(website)
    soup = BeautifulSoup(page.text, "lxml")
    usernames_full = soup.find_all('div', attrs={'class':'username'})
    usernames = []
    for username in usernames_full:
        usernames.append(username.select('a')[0].get_text())
    return usernames

#list of most popular zipcodes in each state and DC

ziplist_pre = ['20011',
           '99504',
           '35242',
           '71913',
           '85032',
           '90201',
           '80013',
           '06010',
           '19720',
           '33157',
           '30044',
           '96797',
           '50317',
           '83301',
           '60629',
           '46227',
           '66062',
           '41042',
           '70072',
           '02301',
           '20906',
           '04011',
           '48180',
           '55106',
           '63376',
           '39503',
           '59102',
           '28269',
           '58103',
           '68104',
           '03103',
           '08701',
           '87121',
           '89110',
           '10025',
           '43613',
           '74012',
           '97007',
           '19120',
           '02860',
           '29483',
           '57106',
           '37211',
           '79936',
           '84015',
           '22314',
           '05401',
           '98115',
           '53215',
           '26003',
           '82001']

#Zipcodes not read as numbers, so had to make them strings and then declare them integars
ziplist = list(map(int, ziplist_pre))

#Making the username extractor work better with futures

def username_extractor2(future):
    soup = BeautifulSoup(future.text, "lxml")
    usernames_full = soup.find_all('div', attrs={'class':'username'})
    usernames = []
    for username in usernames_full:
        usernames.append(username.select('a')[0].get_text())
    return usernames


# creating a bunch of requests to ask the internet for things
session = FuturesSession()

futures = []
for zipcode in ziplist:
    futures.append(session.get(
        f'https://boardgamegeek.com/findgamers.php?action=findclosest&country=US&srczip={zipcode}&maxdist=100&B1=Submit'))

usernames = []
for future in futures:
    usernames.extend(username_extractor2(future.result()))

#Saving usernames as a pickle object
with open('usernames.pkl', 'wb') as f:
    pickle.dump(usernames, f)

#Want to make sure no one is being double counted as from two different zipcodes
usernames_saved_set = set(usernames_saved)

#Pickling over the old list
with open('usernames.pkl', 'wb') as f:
    pickle.dump(usernames_saved, f)

#Opening the new, unique. saved usernames. Start here in the future
with open('usernames.pkl', 'rb') as f:
    usernames = pickle.load(f)

#Getting the list of usernames that did not scrape correctly
with open("mistakes.txt") as f:
    content = f.readlines()
#Removing whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]

cleaned_strings = []
for string in content:
    cleaned_strings.append(literal_eval(string)[0])

#Cleaned version of usernames that needed to have their info accessed again
with open('mistakes.pkl', 'wb') as f:
    pickle.dump(cleaned_strings, f)