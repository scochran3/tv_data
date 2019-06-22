from django.shortcuts import render
import gatherIMDBData
from .models import Show, Episode
from django.shortcuts import redirect
from django.utils.text import slugify
from django_pandas.io import read_frame
import createIMDBVisualizations
from fuzzywuzzy import fuzz, process
from django.db.models import Max
from django.template import RequestContext

def index(request):

	# Show search bar processing
	if request.method == 'POST':
		show_title, result = checkShow(request)

		print (result)
		print ('!!!!!!!!!!!!!!!!!!')

		if result == "Show In Database":
			return redirect('view_show', show_title=slugify(show_title))
		elif result == "Show Added":
			return redirect('view_show', show_title=slugify(show_title))
		elif result == "Show Not Found":
			return redirect(request.path_info)
		
	return render(request, 'tv_data/index.html', {})


def error(request, exception):
    return render(request,'tv_data/404.html')

def view_show(request, show_title):

	# Show search bar processing
	if request.method == 'POST':
		show_title, result = checkShow(request)

		if result == "Show In Database":
			return redirect('view_show', show_title=slugify(show_title))
		elif result == "Show Added":
			return redirect('view_show', show_title=slugify(show_title))
		elif result == "Show Not Found":
			return redirect(request.path_info)


	# Pull data for this show
	this_show = Show.objects.get(title_slugged=show_title)
	episodes = Episode.objects.filter(show=this_show)
	episodes_df = read_frame(episodes)
	episodes_df['rating'] = episodes_df['rating'].astype(float)
	episodes_df = episodes_df.sort_values(by='episode_number', ascending=True)

	episodes_df.to_csv('seinfeld.csv')

	# Create Charts
	numberOfRatingsOverTime = createIMDBVisualizations.plotNumberOfRatingsOverTime(episodes_df)
	episodeRatingsOverTime = createIMDBVisualizations.plotEpisodeRatingsOverTime(episodes_df)
	episodeRatingsHistogram = createIMDBVisualizations.plotEpisodeRatingHistogram(episodes_df)
	ratingPerSeason = createIMDBVisualizations.plotRatingsPerSeason(episodes_df)
	highestLowestRatedEpisodes = createIMDBVisualizations.highestLowestRatedEpisodes(episodes_df)
	ratingsVsNumberOfReviews = createIMDBVisualizations.ratingsVsNumberOfReviews(episodes_df)

	# Create other data points
	numberOfSeasons = len(episodes_df['season'].unique())
	numberOfEpisodes = len(episodes_df)
	lengthOfShowMinutes = this_show.runtime * len(episodes_df)
	lengthOfShowHours = round(lengthOfShowMinutes / 60, 1)
	lengthOfShowDays = round(lengthOfShowMinutes / (60*24), 1)

	# Return data to page
	context = {'this_show': this_show,
				'numberOfRatingsOverTime': numberOfRatingsOverTime,
				'episodeRatingsOverTime': episodeRatingsOverTime,
				'episodeRatingsHistogram': episodeRatingsHistogram,
				'ratingPerSeason': ratingPerSeason,
				'highestLowestRatedEpisodes': highestLowestRatedEpisodes,
				'ratingsVsNumberOfReviews': ratingsVsNumberOfReviews,
				'numberOfSeasons': numberOfSeasons,
				'numberOfEpisodes': numberOfEpisodes,
				'lengthOfShowMinutes': lengthOfShowMinutes,
				'lengthOfShowHours': lengthOfShowHours,
				'lengthOfShowDays': lengthOfShowDays
				}

	return render(request, 'tv_data/view_show.html', context)


def all_shows(request):

	# Show search bar processing
	if request.method == 'POST':
		show_title, result = checkShow(request)

		if result == "Show In Database":
			return redirect('view_show', show_title=slugify(show_title))
		elif result == "Show Added":
			return redirect('view_show', show_title=slugify(show_title))
		elif result == "Show Not Found":
			return redirect(request.path_info)

	# Query shows per letter
	a_shows = Show.objects.filter(title__istartswith='a')
	b_shows = Show.objects.filter(title__istartswith='b')
	c_shows = Show.objects.filter(title__istartswith='c')
	d_shows = Show.objects.filter(title__istartswith='d')
	e_shows = Show.objects.filter(title__istartswith='e')
	f_shows = Show.objects.filter(title__istartswith='f')
	g_shows = Show.objects.filter(title__istartswith='g')
	h_shows = Show.objects.filter(title__istartswith='h')
	i_shows = Show.objects.filter(title__istartswith='i')
	j_shows = Show.objects.filter(title__istartswith='j')
	k_shows = Show.objects.filter(title__istartswith='k')
	l_shows = Show.objects.filter(title__istartswith='l')
	m_shows = Show.objects.filter(title__istartswith='m')
	n_shows = Show.objects.filter(title__istartswith='n')
	o_shows = Show.objects.filter(title__istartswith='o')
	p_shows = Show.objects.filter(title__istartswith='p')
	q_shows = Show.objects.filter(title__istartswith='q')
	r_shows = Show.objects.filter(title__istartswith='r')
	s_shows = Show.objects.filter(title__istartswith='s')
	t_shows = Show.objects.filter(title__istartswith='t')
	u_shows = Show.objects.filter(title__istartswith='u')
	v_shows = Show.objects.filter(title__istartswith='v')
	w_shows = Show.objects.filter(title__istartswith='w')
	x_shows = Show.objects.filter(title__istartswith='x')
	y_shows = Show.objects.filter(title__istartswith='y')
	z_shows = Show.objects.filter(title__istartswith='z')

	# Return the data
	context = {
				'a_shows': a_shows,
				'b_shows': b_shows,
				'c_shows': c_shows,
				'd_shows': d_shows,
				'e_shows': e_shows,
				'f_shows': f_shows,
				'g_shows': g_shows,
				'h_shows': h_shows,
				'i_shows': i_shows,
				'j_shows': j_shows,
				'k_shows': k_shows,
				'l_shows': l_shows,
				'm_shows': m_shows,
				'n_shows': n_shows,
				'o_shows': o_shows,
				'p_shows': p_shows,
				'q_shows': q_shows,
				'r_shows': r_shows,
				's_shows': s_shows,
				't_shows': t_shows,
				'u_shows': u_shows,
				'v_shows': v_shows,
				'w_shows': w_shows,
				'x_shows': x_shows,
				'y_shows': y_shows,
				'z_shows': z_shows
				}

	return render(request, 'tv_data/all_shows.html', context)


def show_comparer(request):

	# Show search bar processing
	if request.method == 'POST':
		show_title, result = checkShow(request)

		if result == "Show In Database":
			return redirect('show_comparer')
		elif result == "Show Added":
			if "add-show" in request.POST:
				return redirect("show_comparer")
			else:
				return redirect('view_show', show_title=slugify(show_title))
		elif result == "Show Not Found":
			return redirect(request.path_info)

	if request.GET.get('show1'):

		# Pull two selected shows
		show1 = request.GET.get('show1').lower().replace(' ', '-')
		show2 = request.GET.get('show2').lower().replace(' ', '-')

		# If the selected shows match
		if show1 == show2:
			request.session["shows_match"] = "Please select two different shows to compare."
			return redirect('show_comparer')
		else:
			request.session["shows_match"] = None

		return redirect('show_comparer_shows', show1=show1, show2=show2)

	shows = Show.objects.all().order_by('title')

	context = {'shows': shows}

	return render(request, 'tv_data/show_comparer.html', context)


def show_comparer_shows(request, show1, show2):

	# Show search bar processing
	if request.method == 'POST':
		show_title, result = checkShow(request)

		if result == "Show In Database":
			return redirect('view_show', show_title=slugify(show_title))
		elif result == "Show Added":
			return redirect('view_show', show_title=slugify(show_title))
		elif result == "Show Not Found":
			return redirect(request.path_info)

	if request.GET.get('show1'):

		# Pull two selected shows
		show1 = request.GET.get('show1').lower().replace(' ', '-')
		show2 = request.GET.get('show2').lower().replace(' ', '-')

		# If the selected shows match
		if show1 == show2:
			request.session["shows_match"] = "Please select two different shows to compare."
			return redirect('show_comparer')
		else:
			request.session["shows_match"] = ''

		return redirect('show_comparer_shows', show1=show1, show2=show2)

	# Bring in the data for the two selected shows
	shows = Show.objects.all().order_by('title')
	show1 = Show.objects.get(title_slugged=show1)
	show2 = Show.objects.get(title_slugged=show2)
	show1_episodes = Episode.objects.filter(show=show1)
	show2_episodes = Episode.objects.filter(show=show2)
	show1_df = read_frame(show1_episodes)
	show1_df = show1_df.sort_values(by='episode_number', ascending=False)
	show2_df = read_frame(show2_episodes)
	show2_df = show2_df.sort_values(by='episode_number', ascending=False)

	# Create comparison charts
	compareSeasons = createIMDBVisualizations.compareSeasons(show1_df, show2_df)
	numberOfEpisodes = createIMDBVisualizations.compareNumberOfEpisodes(show1_df, show2_df)
	compareOverallRating = createIMDBVisualizations.compareOverallRating(show1_df, show2_df)
	compareNumberOfRatings = createIMDBVisualizations.compareNumberOfRatings(show1_df, show2_df)
	compareTopEpisodes = createIMDBVisualizations.compareTopEpisodes(show1_df, show2_df)

	# Show lengths
	show_1_length_minutes = show1.runtime * show1_df['episode_number'].max()
	show_2_length_minutes = show2.runtime * show2_df['episode_number'].max()

	if show_1_length_minutes > show_2_length_minutes:
		longer_show = show1
		shorter_show = show2
		longer_show_minutes = show_1_length_minutes
		longer_show_hours = round(longer_show_minutes / 60, 1)
		shorter_show_minutes = show_2_length_minutes
		shorter_show_hours = round(shorter_show_minutes / 60, 1)
	else:
		longer_show = show2
		shorter_show = show1
		longer_show_minutes = show_2_length_minutes
		longer_show_hours = round(longer_show_minutes / 60, 1)
		shorter_show_minutes = show_1_length_minutes
		shorter_show_hours = round(shorter_show_minutes / 60, 1)

	context = {'shows': shows,
				'show1': show1,
				'show2': show2,
				'compareSeasons': compareSeasons,
				'numberOfEpisodes': numberOfEpisodes,
				'compareOverallRating': compareOverallRating,
				'compareTopEpisodes': compareTopEpisodes,
				'longer_show': longer_show,
				'shorter_show': shorter_show,
				'longer_show_minutes': longer_show_minutes,
				'longer_show_hours': longer_show_hours,
				'shorter_show_minutes': shorter_show_minutes,
				'shorter_show_hours': shorter_show_hours,
				'compareNumberOfRatings': compareNumberOfRatings}

	return render(request, 'tv_data/show_comparer_shows.html', context)


def best_of_the_best(request):

	# Show search bar processing
	if request.method == 'POST':
		show_title, result = checkShow(request)

		if result == "Show In Database":
			return redirect('view_show', show_title=slugify(show_title))
		elif result == "Show Added":
			return redirect('view_show', show_title=slugify(show_title))
		elif result == "Show Not Found":
			return redirect(request.path_info)

	# Bring in shows and episodes data
	shows = Show.objects.all()
	episodes = Episode.objects.all()
	shows_df = read_frame(shows)
	episodes_df = read_frame(episodes)

	# Create figures
	bestOfTheBestTopShows = createIMDBVisualizations.bestOfTheBestTopShows(episodes_df)
	bestOfTheBestTopSeasons = createIMDBVisualizations.bestOfTheBestTopSeasons(episodes_df)
	bestOfTheBestTopEpisodes = createIMDBVisualizations.bestOfTheBestTopEpisodes(episodes_df)
	bestOfTheBestMostPopularEpisodes = createIMDBVisualizations.bestOfTheBestMostPopularEpisodes(episodes_df)
	bestOfTheBestRatingsOverTime = createIMDBVisualizations.bestOfTheBestRatingsOverTime(episodes_df)
	bestOfTheBestBestShowPerYear = createIMDBVisualizations.bestOfTheBestBestShowPerYear(episodes_df)

	context = {'bestOfTheBestTopShows': bestOfTheBestTopShows,
				'bestOfTheBestTopSeasons': bestOfTheBestTopSeasons,
				'bestOfTheBestTopEpisodes': bestOfTheBestTopEpisodes,
				'bestOfTheBestMostPopularEpisodes': bestOfTheBestMostPopularEpisodes,
				'bestOfTheBestRatingsOverTime': bestOfTheBestRatingsOverTime,
				'bestOfTheBestBestShowPerYear': bestOfTheBestBestShowPerYear}

	return render(request, 'tv_data/best_of_the_best.html', context)


def about_us(request):

	# Show search bar processing
	if request.method == 'POST':
		show_title, result = checkShow(request)

		if result == "Show In Database":
			return redirect('view_show', show_title=slugify(show_title))
		elif result == "Show Added":
			return redirect('view_show', show_title=slugify(show_title))
		elif result == "Show Not Found":
			return redirect(request.path_info)

	return render(request, 'tv_data/about_us.html')


def checkShow(request):

	# Pull all shows
	all_shows = Show.objects.all()

	# Get show title input
	show_title = request.POST.get('show_title').lower().title().strip()

	# Check if the string is a typo using fuzzy logic
	for show in all_shows:
		if fuzz.ratio(show_title, show.title) > 80 and show.title != show_title:

			# Set redirection notification
			request.session["redirection"] = 'You entered a show of "{}", but we think you meant {}, so we redirected your search. If this is incorrect please search again.'.format(show_title, show.title)
			request.session["error"] = None

			# Set show title
			show_title = show.title
			this_show = Show.objects.get(title=show_title)

			# Check if seasons in database matches seasons of show
			number_of_seasons = gatherIMDBData.getShowIMBDID(show_title)[1]
			number_of_seasons_database = Episode.objects.filter(show=this_show).aggregate(Max('season'))['season__max']

			# If we already have all the seasons
			if  number_of_seasons == number_of_seasons_database:
				return show_title, "Show In Database"

			# Otherwise update it
			else:
				# Pull data for the show
				number_of_episodes_already_in_database = len(Episode.objects.filter(show=this_show))
				episode_data = gatherIMDBData.getEpisodesData(show=show_title, first_season_to_scrape=number_of_seasons_database+1, 
												number_of_episodes_already_in_database=number_of_episodes_already_in_database)

				episode_data_df = episode_data[0]

				# Create episode objects
				objects = [Episode(show=this_show, 
									episode_title=episode_data_df.episode_title.iloc[i], 
									air_date=episode_data_df.episode_air_date.iloc[i], 
									rating=episode_data_df.episode_rating.iloc[i], 
									number_of_ratings=episode_data_df.episode_number_of_ratings.iloc[i], 
									episode_number=episode_data_df.episode_number.iloc[i], 
									season=episode_data_df.season_number.iloc[i], 
									imdb_episode_id=episode_data_df.episode_id.iloc[i])
							
							for i in range(len(episode_data_df))]

				Episode.objects.bulk_create(objects)

				# Redirect to new show page 
				return show_title, "Show Added"
		

	# If the show is not found
	if not gatherIMDBData.getShowIMBDID(show_title):
		request.session["error"] = "Sorry, the show {} was not found. Please try a different show.".format(show_title)
		request.session["redirection"] = ''
		return show_title, "Show Not Found"
	else:
		request.session["error"] = None
		request.session["redirection"] = None


	# If they show already exists in the database
	if Show.objects.filter(title=show_title):

		# Set error to nothing
		request.session["redirection"] = None

		# Filter for the show
		this_show = Show.objects.get(title=show_title)

		# Check if seasons in database matches seasons of show
		number_of_seasons = gatherIMDBData.getShowIMBDID(show_title)[1]
		number_of_seasons_database = Episode.objects.filter(show=this_show).aggregate(Max('season'))['season__max']

		if  number_of_seasons == number_of_seasons_database:
			return show_title, "Show In Database"
		else:
			# Pull data for the show
			number_of_episodes_already_in_database = len(Episode.objects.filter(show=this_show))
			episode_data = gatherIMDBData.getEpisodesData(show=show_title, first_season_to_scrape=number_of_seasons_database+1, 
											number_of_episodes_already_in_database=number_of_episodes_already_in_database)
			episode_data_df = episode_data[0]

			# Create episode objects
			objects = [Episode(show=this_show, 
								episode_title=episode_data_df.episode_title.iloc[i], 
								air_date=episode_data_df.episode_air_date.iloc[i], 
								rating=episode_data_df.episode_rating.iloc[i], 
								number_of_ratings=episode_data_df.episode_number_of_ratings.iloc[i], 
								episode_number=episode_data_df.episode_number.iloc[i], 
								season=episode_data_df.season_number.iloc[i], 
								imdb_episode_id=episode_data_df.episode_id.iloc[i])
						
						for i in range(len(episode_data_df))]

			Episode.objects.bulk_create(objects)

			# Redirect to new show page 
			return show_title, "Show Added"
		return show_title, "Show In Database"

	# Show not in database
	if not Show.objects.filter(title=show_title):

		try:
			# Pull data for the show
			episode_data = gatherIMDBData.getEpisodesData(show_title)
			episode_data_df = episode_data[0]
			imdb_show_id = episode_data[1]
			release_date = episode_data[2]
			rated = episode_data[3]
			poster_url = episode_data[4]
			runtime = episode_data[5]

			# Create new show
			new_show = Show.objects.create(
				title=show_title,
				imdb_id=episode_data[1],
				released=release_date,
				rated=rated,
				poster_url=poster_url,
				runtime=runtime
				)

			# Create episode objects
			objects = [Episode(show=new_show, 
								episode_title=episode_data_df.episode_title.iloc[i], 
								air_date=episode_data_df.episode_air_date.iloc[i], 
								rating=episode_data_df.episode_rating.iloc[i], 
								number_of_ratings=episode_data_df.episode_number_of_ratings.iloc[i], 
								episode_number=episode_data_df.episode_number.iloc[i], 
								season=episode_data_df.season_number.iloc[i], 
								imdb_episode_id=episode_data_df.episode_id.iloc[i])
						
						for i in range(len(episode_data_df))]

			Episode.objects.bulk_create(objects)

			# Redirect to new show page 
			return show_title, "Show Added"

		except AttributeError:
			request.session["error"] = "Sorry, the show {} was not found. Please try a different show.".format(show_title)
			request.session["redirection"] = ''
			return show_title, "Show Not Found"