import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from pprint import pprint
import json
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import time
import Config

def getShowIMBDID(show):

	# API parameters
	credentials = Config.read_credentials()
	API_KEY  = credentials['imdb']['api_key']
	END_POINT = 'http://www.omdbapi.com/?apikey={}&'.format(API_KEY)

	# Make request
	url = END_POINT + 't={}&r=json'.format(show)
	r = requests.get(url)
	data = json.loads(r.content)
	
	try:
		# Parse data
		imbd_id = data['imdbID']
		total_seasons = int(data['totalSeasons'])
		released = datetime.strptime(data['Released'].strip().replace('.', ''), '%d %b %Y').date()
		rated = data['Rated']
		poster = data['Poster']
		runtime = int(data['Runtime'].replace(' min', ''))
	except KeyError:
		return None

	pprint (data)

	return imbd_id, total_seasons, released, rated, poster, runtime


def getEpisodesData(show):

	# Slugified show
	show_slugged = show.replace(' ', '_').lower()

	# Get seasons and IMDB id
	if getShowIMBDID(show):
		imdb_id, number_of_seasons, released, rated, poster, runtime = getShowIMBDID(show)
	else:
		return None

	# Loop over seasons and pull data
	all_titles, all_ratings, all_air_dates, all_number_of_ratings, all_episode_id, all_season_numbers = [], [], [], [], [], []
	for i in range(1,number_of_seasons+1):
		endpoint = 'https://www.imdb.com/title/{}/episodes?season={}'.format(imdb_id, i)
		r = requests_retry_session().get(endpoint)
		print (i)
		print ('-----------------')
		soup = BeautifulSoup(r.content, 'html.parser')

		# Parse the website
		episodeData = soup.find_all('div', {'class': 'list_item'})

		# Scrape data
		for episode in episodeData:
			
			# If there is an error on the date conversion it is generally for a future episode, which we don't want
			try:
				air_date = datetime.strptime(episode.find('div', {'class': 'airdate'}).text.strip().replace('.', ''), '%d %b %Y').date()
			except ValueError:
				break

			# Abort if the air date is in the future
			if air_date > datetime.today().date():
				break

			# If everything is peachy parse the data
			rating = float(episode.find('span', {'class': 'ipl-rating-star__rating'}).text)
			number_of_ratings = int(episode.find('span', {'class': 'ipl-rating-star__total-votes'}).text.replace('(','').replace(')', '').replace(',',''))
			episode_link = episode.find('a', {'itemprop':'name'})
			title = episode_link.text
			episode_id = episode_link['href'][7:-1]

			# Append lists
			all_titles.append(title)
			all_ratings.append(rating)
			all_air_dates.append(air_date)
			all_number_of_ratings.append(number_of_ratings)
			all_episode_id.append(episode_id)
			all_season_numbers.append(i)

	# Add all of our data to a dataframe
	df = pd.DataFrame(data={'show':show,
							'episode_title':all_titles,
							'episode_air_date': all_air_dates,
							'episode_rating':all_ratings,
							'episode_number_of_ratings':all_number_of_ratings,
							'episode_id': all_episode_id,
							'season_number': all_season_numbers})

	df = df.set_index('show')
	df['episode_number'] = df.reset_index().index+1

	return df, imdb_id, released, rated, poster, runtime


def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
	):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

if __name__=='__main__':
	getShowIMBDID('The Leftovers')