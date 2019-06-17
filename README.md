# Board Game Recommender

This project uses web scraping, API requests, and machine learning to create a board game recommender using data from  [BoardGameGeek's](https://boardgamegeek.com) publicly available  [API](https://boardgamegeek.com/wiki/page/BGG_XML_API2).


## Web Scraping

- In order to get a list of usernames to use with BGG's API, I used web scraping to find all users near the largest city of every state, and DC.
- This code can be found in data_pull.py.
- A list of users can be created from this code, but is not provided in this repository.

## Accessing Data from BGG's  API

- After collecting a list of users, I then made requests to the API to get all collection information for every user in my list (23,000).
- This code can be found in getting_data.py.

## Creating panda's data frames from the data

- In order to use this data to create my recommender, I created a parser that would store the information into two pandas dataframes.
- gamesDF.py creates a data frame of each unique game owned by at least one user in my dataset (over 46,000 games).
- rankDF.py creates a data frame of each users rankings for every game they ranked (over 1 million rankings).


## Visualization and KNN Recommender
- Visualizations_Rec_Beginnings.py contains the code to create visualizations of how many more board games have been produced in recent decades than in previous decades, as well as KNN models for the recommender. 
- This is an ongoing project.

