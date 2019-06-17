import requests
from bs4 import BeautifulSoup
from requests_futures.sessions import FuturesSession
import pickle
import numpy
import time

#Opening the new, unique, saved usernames.
with open('usernames.pkl', 'rb') as f:
    usernames = pickle.load(f)

#Need to program a long delay into requests in order to not overload BGG's Server
mistake_username_code11 = []

for i in username_makeup:
    tries = 0
    success = False
    while tries < 3 and success == False:
        tries += 1
        array_ = numpy.random.randint(0, 10, size=1)
        sleep_time = array_[0]
        time.sleep(sleep_time)
        response = requests.get(
            f"http://www.boardgamegeek.com/xmlapi2/collection?username={i}&excludesubtype=boardgameexpansion&stats=1&own=1")
        success = response.status_code == 200
    if success == True:
        # write file with i as name of file
        with open(f"{i}.xml", "wb") as file:
            file.write(response.content)


    else:
        mistake_username_code.append((i, response.status_code))
    array_ = numpy.random.randint(0, 10, size=1)
    sleep_time = array_[0]
    time.sleep(sleep_time)



#Function to make the request for a users collection info
def get_collections(list):
    mistake_username_code = []
    for i in list:
        tries = 0
        success = False
        while tries < 3 and success == False:
            tries += 1
            array_ = numpy.random.randint(0, 10, size=1)
            sleep_time = array_[0]
            time.sleep(sleep_time)
            response = requests.get(
                f"http://www.boardgamegeek.com/xmlapi2/collection?username={i}&excludesubtype=boardgameexpansion&stats=1&own=1")
            success = response.status_code == 200
        if success == True:
            # write file with i as name of file
            with open(f"{i}.xml", "wb") as file:
                file.write(response.content)
        else:
            mistake_username_code.append((i, response.status_code))
        array_ = numpy.random.randint(0, 10, size=1)
        sleep_time = array_[0]
        time.sleep(sleep_time)
    with open('mistakes.txt', 'a') as file:
        for item in mistake_username_code:
            file.write(f'{item}\n')

    get_collections.counter += 1
    print(get_collections.counter)

#Using a counter to track how far along in the list of usernames I have gotten
get_collections.counter = 0


# Set number to how many usernames I am trying to get their collections of in a particular batch. Currently getting
# 1000 before adding to the counter. The number is only important for tracking purposes
list_of_groups = zip(*(iter(usernames),) * 1000)

for list in list_of_groups:
    get_collections(list)
