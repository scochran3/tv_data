import pandas as pd
from datetime import datetime, timedelta
from bokeh.io import output_file, show
from bokeh.layouts import column, gridplot, layout, row
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, LinearColorMapper, NumeralTickFormatter, Range1d, HoverTool, Span, Label, Panel, Tabs, LabelSet, SingleIntervalTicker, LinearAxis, DatetimeTickFormatter
from bokeh.embed import components
from bokeh.transform import cumsum
from bokeh.palettes import Category20
from jsmin import jsmin
from bokeh.models import Span, Legend
import time
from bokeh.io import curdoc
from bokeh.themes import Theme
import itertools
from jsmin import jsmin
import numpy as np
import math



'''
GLOBAL FIGURE SETTINGS
'''
curdoc().theme = Theme(json={'attrs': {

    # apply defaults to Figure properties
    'Figure': {
        'toolbar_location': None,
        'outline_line_color': None,
        'min_border_right': 10,
        'plot_width': 1000,
        'plot_height':500,
    },

    'Grid': {
    	'grid_line_color': None,
    },
    'Title': {
        'text_font_size': '14pt'
    },

    # apply defaults to Axis properties
    'Axis': {
        'minor_tick_out': None,
        'minor_tick_in': None,
        'major_label_text_font_size': '11pt',
        'axis_label_text_font_size': '13pt',
        'axis_label_text_font': 'Work Sans'
    },
     # apply defaults to Legend properties
    'Legend': {
        'background_fill_alpha': 0.8,
    }
}})


def plotEpisodeRatingsOverTime(df):

	# Create the plot
	source = ColumnDataSource(df)
	p = figure(sizing_mode='stretch_both', y_range=Range1d(bounds=(0, 1)),
             x_range=Range1d(bounds=(0, 1)), tools=[])
	p.line(x='episode_number', y='rating', line_width=3, line_color='#8B0000', source=source)

	# Format plot
	p.xaxis.axis_label = 'Episode Number'
	# p.yaxis.axis_label = 'Rating (/10)'
	p.yaxis.formatter = NumeralTickFormatter(format="0.0")
	p.y_range=Range1d(0, 10)
	p.x_range=Range1d(1, df['episode_number'].max()+1)
	p.yaxis.major_label_text_font = 'Work Sans'
	p.xaxis.major_label_text_font = 'Work Sans'
	p.yaxis.axis_label_text_font = 'Work Sans'
	p.xaxis.axis_label_text_font = 'Work Sans'

	# Return the figure
	script, div = components(p)
	script = jsmin(script)

	# Get data for the paragraph
	episodeMeanScore = round(df['rating'].mean(), 2)
	episodeMaxScore = round(df['rating'].max(), 2)
	episodeMinScore = round(df['rating'].min(), 2)
	numberOfEpisodes = len(df)
	episodeTitleWithMaxScore = df['episode_title'][df['rating'].idxmax()]
	episodeTitleWithMinScore = df['episode_title'][df['rating'].idxmin()]

	return script, div, episodeMeanScore, episodeMaxScore, episodeTitleWithMaxScore, episodeMinScore, episodeTitleWithMinScore, numberOfEpisodes


def plotEpisodeRatingHistogram(df):

	# Create the histogram data
	hist, edges = np.histogram(df['rating'], bins=int(len(df)/4), range=[0,10])
	hist_df = pd.DataFrame({'counts': hist, 'left': edges[:-1], 'right': edges[1:]})

	# Create the blank plot
	source = ColumnDataSource(hist_df)
	p = figure(x_axis_label = 'Rating (/10)', y_axis_label = 'Number of Episodes with Score', sizing_mode='stretch_both', tools=[])

	# Add a quad glyph
	p.quad(bottom=0, top='counts',  left='left', right='right',  
			fill_color='#191970', line_color='black', hover_color='#A9A9A9',
			hover_line_color='#000000', source=source)
	p.y_range=Range1d(0, hist_df['counts'].max()*1.05)

	# Format chart
	p.yaxis.major_label_text_font = 'Work Sans'
	p.xaxis.major_label_text_font = 'Work Sans'
	p.yaxis.axis_label_text_font = 'Work Sans'
	p.xaxis.axis_label_text_font = 'Work Sans'

	# Add Hover Tool
	tooltips = """
		<div class="tooltip-section">
			<h5 class="tooltip-header">Score Range: </h5><h5 class="tooltip-content">@left{0.0} to @right{0.0} </h5>
		</div>
		<div class="tooltip-section">
			<h5 class="tooltip-header">Number of Episodes: </h5><h5 class="tooltip-content">@counts</h5>
		</div>"""

	p.add_tools(HoverTool(tooltips=tooltips))

	# Return the figure
	script, div = components(p)
	script = jsmin(script)
	return script, div


def plotNumberOfRatingsOverTime(df):

	# Create the plot
	source = ColumnDataSource(df)
	p = figure(sizing_mode='stretch_both', tools=[])
	p.line(x='episode_number', y='number_of_ratings', line_width=3, line_color='#8B0000', source=source)

	# Format plot
	p.xaxis.axis_label = 'Episode Number'
	# p.yaxis.axis_label = 'Number of Ratings'
	p.yaxis.formatter = NumeralTickFormatter(format="0,0")
	p.y_range=Range1d(0, df['number_of_ratings'].max()*1.05)
	p.x_range=Range1d(1, df['episode_number'].max()+1)

	# Return the figure
	script, div = components(p)
	script = jsmin(script)

	# Get the numbers for the paragraph
	episodeWithMostRatings = df['episode_title'][df['number_of_ratings'].idxmax()]
	episodeWithMostRatingsCount = df['number_of_ratings'].max()
	episodeWithLeastRatings = df['episode_title'][df['number_of_ratings'].idxmin()]
	episodeWithLeastRatingsCount = df['number_of_ratings'].min()
	averageNumberOfReviews = int(df['number_of_ratings'].mean())

	return script, div, episodeWithMostRatings, episodeWithMostRatingsCount, episodeWithLeastRatings, episodeWithLeastRatingsCount, averageNumberOfReviews


def plotRatingsPerSeason(df):

	# Group By Season
	df_grouped = df.groupby('season')[['rating']].mean().reset_index()

	# Create the plot
	source = ColumnDataSource(df_grouped)
	p = figure(sizing_mode='stretch_both', tools=[])
	p.line(x='season', y='rating', line_width=3, line_color='#8B0000', source=source)
	p.circle(x='season', y='rating', size=10, 
			line_color='#8B0000', fill_color='#FFFFFF', hover_color='#A9A9A9', 
			hover_line_color='#000000', line_width=3, source=source)

	# Format plot
	p.xaxis.axis_label = 'Season Number'
	# p.yaxis.axis_label = 'Rating (/10)'
	p.yaxis.formatter = NumeralTickFormatter(format="0.0")
	p.y_range=Range1d(0, 10)
	p.x_range=Range1d(.5, df_grouped['season'].max()+1)
	p.yaxis.major_label_text_font = 'Work Sans'
	p.xaxis.major_label_text_font = 'Work Sans'
	p.yaxis.axis_label_text_font = 'Work Sans'
	p.xaxis.axis_label_text_font = 'Work Sans'

	# Add Hover Tool
	tooltips = """
		<div class="tooltip-section">
			<h5 class="tooltip-header">Season: </h5><h5 class="tooltip-content">@season</h5>
		</div>
		<div class="tooltip-section">
			<h5 class="tooltip-header">Average Rating for Season: </h5><h5 class="tooltip-content">@rating{0.0}</h5>
		</div>
		"""

	p.add_tools(HoverTool(tooltips=tooltips))


	# Return the figure
	script, div = components(p)
	script = jsmin(script)

	# Get seasons with highest, lowest scores and mean score
	seasonAverage = round(df_grouped['rating'].mean(), 2)
	bestSeason = df_grouped['season'][df_grouped['rating'].idxmax()]
	bestSeasonRating = round(df_grouped['rating'].max(), 2)
	worstSeason = df_grouped['season'][df_grouped['rating'].idxmin()]
	worstSeasonRating = round(df_grouped['rating'].min(), 2)

	
	# Returna all the data
	return script, div, seasonAverage, bestSeason, bestSeasonRating, worstSeason, worstSeasonRating


def highestLowestRatedEpisodes(df):

	# Sort by rating
	df = df[['episode_number', 'episode_title', 'rating', 'season']]
	df['season-episode'] = (df.groupby(['season']).cumcount()) + 1
	df['episode_title'] = df['episode_title'] + " (S" + df["season"].astype(str) + "E" + df["season-episode"].astype(str) + ")"
	df = df.sort_values(by='rating', ascending=False)

	# Get top and lowest rated
	highest_rated = df.head(5)[::-1]
	lowest_rated = df.tail(5)

	# Check if episode name repeats (two part episode)
	highestRatedEpisodes, lowestRatedEpisodes = [], []
	for i in highest_rated['episode_title']:
		if i not in highestRatedEpisodes:
			highestRatedEpisodes.append(i)
		else:
			highestRatedEpisodes.append('{} Part 2'.format(i))

	for i in lowest_rated['episode_title']:
		if i not in highestRatedEpisodes:
			lowestRatedEpisodes.append(i)
		else:
			lowestRatedEpisodes.append('{} Part 2'.format(i))

	highest_rated['episode_title'] = highestRatedEpisodes
	lowest_rated['episode_title'] = lowestRatedEpisodes

	# Create bar charts
	# Top chart
	source_highest = ColumnDataSource(highest_rated)
	p_highest = figure(y_range=highest_rated['episode_title'], sizing_mode='stretch_both', tools=[])
	p_highest.hbar(y='episode_title', right='rating', height=.4, color='#191970', source=source_highest)
	labels_scores = LabelSet(x='rating', y='episode_title', 
						text='rating', level='glyph', source=source_highest, 
						text_font_size='10pt', text_font_style='bold',
						x_offset=8, y_offset=-7)
	p_highest.add_layout(labels_scores)

	labels_episode_titles = LabelSet(x=0, y='episode_title', 
						text='episode_title', level='glyph', source=source_highest, 
						text_font_size='11pt', text_font_style='bold',
						x_offset=0, y_offset=25)
	p_highest.add_layout(labels_episode_titles)
	

	# Bottom Chart
	source_lowest = ColumnDataSource(lowest_rated)
	p_lowest = figure(y_range=lowest_rated['episode_title'], sizing_mode='stretch_both', tools=[])
	p_lowest.hbar(y='episode_title', right='rating', height=.4, color='#8B0000', source=source_lowest)
	labels = LabelSet(x='rating', y='episode_title', 
						text='rating', level='glyph', source=source_lowest, 
						text_font_size='10pt', text_font_style='bold',
						x_offset=8, y_offset=-7, text_font='Work Sans')
	p_lowest.add_layout(labels)

	labels_episode_titles = LabelSet(x=0, y='episode_title', 
						text='episode_title', level='glyph', source=source_lowest, 
						text_font_size='11pt', text_font_style='bold',
						x_offset=0, y_offset=25)
	p_lowest.add_layout(labels_episode_titles)

	# Style the charts
	p_highest.xaxis.visible = False
	p_highest.yaxis.axis_line_color = None
	p_highest.yaxis.major_tick_line_color = None
	p_highest.x_range=Range1d(0, highest_rated['rating'].max()*1.1)
	p_highest.yaxis.major_label_text_font_size = '0pt'
	p_lowest.xaxis.visible = False
	p_lowest.yaxis.axis_line_color = None
	p_lowest.yaxis.major_tick_line_color = None
	p_lowest.x_range=Range1d(0, lowest_rated['rating'].max()*1.1)
	p_lowest.yaxis.major_label_text_font_size = '0pt'

	# Return the figure
	script_high, div_high = components(p_highest)
	script_high = jsmin(script_high)
	script_low, div_low = components(p_lowest)
	script_low = jsmin(script_low)
	return script_high, div_high, script_low, div_low


def ratingsVsNumberOfReviews(df):

	# Create size and color palette
	df['sizing'] = (df['number_of_ratings'] / df['number_of_ratings'].mean()) * 10
	color_mapper = LinearColorMapper(palette=['#8B0000', '#B22222', '#FF8C00', 
												'#FFD700', '#FFFF00', '#228B22',
												'#006400'], low=6, high=10)
	
	# Create chart
	source = ColumnDataSource(df)
	p = figure(sizing_mode='stretch_both', tools=[])
	p.circle(x='number_of_ratings', y='rating', source=source, size='sizing', 
				color={'field': 'rating', 'transform': color_mapper}, alpha=.7, 
				line_color='#000000', hover_color='#A9A9A9')

	# Format chart
	p.xaxis.formatter = NumeralTickFormatter(format='0,0')
	p.yaxis.formatter = NumeralTickFormatter(format='0.0')
	p.x_range = Range1d(0, df['number_of_ratings'].max()*1.1)
	p.y_range = Range1d(0,11)
	p.xaxis.axis_label = 'Number Of Ratings'


	# Add Hover Tool
	tooltips = """
		<div class="tooltip-section">
			<h5 class="tooltip-header">Episode: </h5><h5 class="tooltip-content">@episode_title</h5>
		</div>
		<div class="tooltip-section">
			<h5 class="tooltip-header">Episode Air Date: </h5><h5 class="tooltip-content">@air_date{%Y-%m-%d}</h5>
		</div>
		<div class="tooltip-section">
			<h5 class="tooltip-header">Episode Rating: </h5><h5 class="tooltip-content">@rating{0.0}</h5>
		</div>
		<div class="tooltip-section">
			<h5 class="tooltip-header">Number of Ratings: </h5><h5 class="tooltip-content">@number_of_ratings</h5>
		</div>
		<div class="tooltip-section">
			<h5 class="tooltip-header">Season: </h5><h5 class="tooltip-content">@season</h5>
		</div>
		"""

	p.add_tools(HoverTool(tooltips=tooltips, formatters={'air_date': 'datetime'}))

	# Return the figure
	script, div = components(p)
	script = jsmin(script)
	return script, div


def compareOverallRating(df1, df2):

	# Adjust datatypes
	df1['rating'] = df1['rating'].astype(float)
	df2['rating'] = df1['rating'].astype(float)

	# Group by season
	df1_rating = df1.groupby('show')[['rating']].mean().reset_index()
	df2_rating = df2.groupby('show')[['rating']].mean().reset_index()
	df_combined = df1_rating.append(df2_rating)
	df_combined['color'] = ['#8B0000', '#191970']
	df_combined['rating_rounded'] = round(df_combined['rating'], 2)

	# Create plot
	source = ColumnDataSource(df_combined)
	p = figure(sizing_mode='stretch_both', y_range=df_combined['show'], tools=[])
	p.hbar(y='show', right='rating', height=.55, source=source, color='color')

	# Style the plot
	p.yaxis.visible=False
	p.xaxis.visible=False
	p.x_range = Range1d(0, df_combined['rating'].max()*1.1)

	# Data points
	show_1_rating = round(df_combined['rating'].iloc[0], 2)
	show_1_number_of_episodes = df1['episode_number'].max()
	show_2_rating = round(df_combined['rating'].iloc[1], 2)
	show_2_number_of_episodes = df2['episode_number'].max()

	labels = LabelSet(x='rating', y='show', 
						text='rating_rounded', level='glyph', source=source, 
						text_font_size='13pt', text_font_style='bold',
						x_offset=20, y_offset=-14, angle=math.pi/2)
	p.add_layout(labels)

	labels_show_title = LabelSet(x=0, y='show', 
						text='show', level='glyph', source=source, 
						text_font_size='14pt', text_font_style='bold',
						x_offset=3, y_offset=40)
	p.add_layout(labels_show_title)

	# Return the figure
	script, div = components(p)
	script = jsmin(script)

	return {'script':script, 'div':div, 'show_1_rating':show_1_rating, 
			'show_2_rating':show_2_rating, 'show_1_number_of_episodes': show_1_number_of_episodes,
			'show_2_number_of_episodes': show_2_number_of_episodes}


def compareSeasons(df1, df2):

	# Adjust datatypes
	df1['rating'] = df1['rating'].astype(float)
	df2['rating'] = df2['rating'].astype(float)

	# Group by season
	df1_by_season = df1.groupby('season')[['rating']].mean().reset_index()
	df2_by_season = df2.groupby('season')[['rating']].mean().reset_index()

	print (df2_by_season)

	# Create the figure
	source1, source2 = ColumnDataSource(df1_by_season), ColumnDataSource(df2_by_season)
	p = figure(sizing_mode='stretch_both', tools=[])
	p.line(x='season', y='rating', line_width=2, source=source1, name=df1['show'].iloc[0], legend=df1['show'].iloc[0], color='#8B0000')
	p.circle(x='season', y='rating', size=10, source=source1, name=df1['show'].iloc[0], legend=df1['show'].iloc[0], color='#8B0000')
	p.line(x='season', y='rating', line_width=2, source=source2, name=df2['show'].iloc[0], legend=df2['show'].iloc[0], color='#191970')
	p.circle(x='season', y='rating', size=10, source=source2, name=df2['show'].iloc[0], legend=df2['show'].iloc[0], color='#191970')

	# Style the plot
	p.y_range = Range1d(0, 10)
	p.xaxis.axis_label = 'Season'
	p.yaxis.formatter = NumeralTickFormatter(format="0.0")
	p.legend.location = 'bottom_left'

	# Calculate data variables
	season_1_average = round(df1_by_season['rating'].mean(), 2)
	season_2_average = round(df2_by_season['rating'].mean(), 2)
	season_1_max = round(df1_by_season['rating'].max(), 2)
	season_2_max = round(df2_by_season['rating'].max(), 2)
	season_1_min = round(df1_by_season['rating'].min(), 2)
	season_2_min = round(df2_by_season['rating'].min(), 2)

	# Return the figure
	script, div = components(p)
	script = jsmin(script)

	return {'script': script, 'div': div, 'season_1_average':season_1_average, 'season_2_average':season_2_average,
			'season_1_max':season_1_max, 'season_2_max':season_2_max, 'season_1_min':season_1_min, 'season_2_min':season_2_min}


def compareNumberOfEpisodes(df1, df2):

	# Group by season
	df1_episodes = df1.groupby('show')[['episode_number']].max().reset_index()
	df2_episodes = df2.groupby('show')[['episode_number']].max().reset_index()
	df_combined = df1_episodes.append(df2_episodes)
	df_combined['color'] = ['#8B0000', '#191970']

	# Create plot
	source = ColumnDataSource(df_combined)
	p = figure(sizing_mode='stretch_both', y_range=df_combined['show'], tools=[])
	p.hbar(y='show', right='episode_number', height=.55, source=source, color='color')

	# Style the plot
	p.xaxis.visible = False
	p.yaxis.visible = False
	p.x_range=Range1d(0, df_combined['episode_number'].max()*1.1)

	labels = LabelSet(x='episode_number', y='show', 
						text='episode_number', level='glyph', source=source, 
						text_font_size='13pt', text_font_style='bold',
						x_offset=20, y_offset=-12, angle=math.pi/2)
	p.add_layout(labels)

	labels_show_title = LabelSet(x=0, y='show', 
						text='show', level='glyph', source=source, 
						text_font_size='14pt', text_font_style='bold',
						x_offset=3, y_offset=40)
	p.add_layout(labels_show_title)

	# Data points
	show_1_episodes = df_combined['episode_number'].iloc[0]
	show_2_episodes = df_combined['episode_number'].iloc[1]

	# Return the figure
	script, div = components(p)
	script = jsmin(script)

	return {'script':script, 'div':div, 'show_1_episodes':show_1_episodes, 'show_2_episodes':show_2_episodes}
	

def compareNumberOfRatings(df1, df2):

	# Create figure
	show1_source, show2_source = ColumnDataSource(df1), ColumnDataSource(df2)
	p = figure(sizing_mode='stretch_both', tools=[])
	p.line(x='episode_number', y='number_of_ratings', source=show1_source, color='#8B0000', line_width=2)
	p.line(x='episode_number', y='number_of_ratings', source=show2_source, color='#191970', line_width=2)
	
	# Format the chart
	p.yaxis.formatter = NumeralTickFormatter(format="0,0")
	# p.yaxis.axis_label = "Number of Ratings"
	p.xaxis.axis_label = "Episode Number"

	# Data points
	show_1_total_ratings = df1['number_of_ratings'].sum()
	show_2_total_ratings = df2['number_of_ratings'].sum()
	show_1_average_ratings = round(df1['number_of_ratings'].mean(), 2)
	show_2_average_ratings = round(df2['number_of_ratings'].mean(), 2)
	show_1_max_ratings = df1['number_of_ratings'].max()
	show_2_max_ratings = df2['number_of_ratings'].max()

	# Return the figure
	script, div = components(p)
	script = jsmin(script)

	return {'script': script, 'div': div, 'show_1_total_ratings': show_1_total_ratings,
			'show_2_total_ratings':show_2_total_ratings, 'show_1_average_ratings': show_1_average_ratings,
			'show_2_average_ratings': show_2_average_ratings, 'show_1_max_ratings': show_1_max_ratings,
			 'show_2_max_ratings': show_2_max_ratings}


def compareTopEpisodes(df1, df2):

	# Top 5 shows per show
	df1_top_shows = df1.sort_values(by='rating', ascending=False).head(10)[['episode_title', 'rating', 'season']][::-1]
	df2_top_shows = df2.sort_values(by='rating', ascending=False).head(10)[['episode_title', 'rating', 'season']][::-1]

	# Create episode number
	df1_top_shows['season-episode'] = (df1_top_shows.groupby(['season']).cumcount()) + 1
	df1_top_shows['episode_title'] = df1_top_shows['episode_title'] + " (S" + df1_top_shows["season"].astype(str) + "E" + df1_top_shows["season-episode"].astype(str) + ")"
	df2_top_shows['season-episode'] = (df2_top_shows.groupby(['season']).cumcount()) + 1
	df2_top_shows['episode_title'] = df2_top_shows['episode_title'] + " (S" + df2_top_shows["season"].astype(str) + "E" + df2_top_shows["season-episode"].astype(str) + ")"

	# Check for two part episodes
	# Check if episode name repeats (two part episode)
	show1HighestEpisodes, show2HighestEpisodes = [], []
	for i in df1_top_shows['episode_title']:
		if i not in show1HighestEpisodes:
			show1HighestEpisodes.append(i)
		else:
			show1HighestEpisodes.append('{} Part 2'.format(i))

	for i in df2_top_shows['episode_title']:
		if i not in show2HighestEpisodes:
			show2HighestEpisodes.append(i)
		else:
			show2HighestEpisodes.append('{} Part 2'.format(i))

	df1_top_shows['episode_title'] = show1HighestEpisodes
	df2_top_shows['episode_title'] = show2HighestEpisodes

	# Create the first figure
	show1_source, show2_source = ColumnDataSource(df1_top_shows), ColumnDataSource(df2_top_shows)
	p1 = figure(sizing_mode="stretch_both", y_range=df1_top_shows["episode_title"], tools=[])
	p1.hbar(y="episode_title", right="rating", height=.4, color="#8B0000", source=show1_source)

	# Style the chart
	p1.x_range=Range1d(0,11)
	p1.xaxis.visible = False
	p1.yaxis.visible = False

	labels_ratings = LabelSet(x='rating', y='episode_title', 
						text='rating', level='glyph', source=show1_source, 
						text_font_size='10pt', text_font_style='bold',
						x_offset=3, y_offset=-7)

	labels_titles = LabelSet(x=0, y='episode_title', 
						text='episode_title', level='glyph', source=show1_source, 
						text_font_size='10pt', text_font_style='bold',
						x_offset=3, y_offset=12)

	p1.add_layout(labels_ratings)
	p1.add_layout(labels_titles)


	# Create the second figure
	p2 = figure(sizing_mode="stretch_both", y_range=df2_top_shows["episode_title"], tools=[])
	p2.hbar(y="episode_title", right="rating", height=.4, color="#191970", source=show2_source)
	p2.x_range=Range1d(0,11)
	p2.xaxis.visible = False
	p2.yaxis.visible = False

	labels = LabelSet(x='rating', y='episode_title', 
						text='rating', level='glyph', source=show2_source, 
						text_font_size='10pt', text_font_style='bold',
						x_offset=3, y_offset=-7)

	labels_titles = LabelSet(x=0, y='episode_title', 
						text='episode_title', level='glyph', source=show2_source, 
						text_font_size='10pt', text_font_style='bold',
						x_offset=0, y_offset=12)
	p2.add_layout(labels)
	p2.add_layout(labels_titles)

	# Return the figure
	script1, div1 = components(p1)
	script1 = jsmin(script1)

	script2, div2 = components(p2)
	script2 = jsmin(script2)


	return {'script1':script1, 'script2': script2, 'div1':div1, 'div2':div2}


def bestOfTheBestTopShows(df):

	# Group by the shows
	df['rating'] = df['rating'].astype(float)
	df = df.groupby('show')[['rating']].mean().reset_index().sort_values(by='rating', ascending=False).head(10)[::-1]
	df['rating'] = round(df['rating'], 2)
	
	# Create the figure
	source = ColumnDataSource(df)
	p = figure(sizing_mode='stretch_both', y_range=df['show'], tools=[])
	p.hbar(y="show", height=.35, right="rating", color="#8B0000", source=source)

	# Format the chart
	labels = LabelSet(x='rating', y='show', 
						text='rating', level='glyph', source=source, 
						text_font_size='10pt', text_font_style='bold',
						x_offset=8, y_offset=-7)
	p.add_layout(labels)

	labels_show_title = LabelSet(x=0, y='show', 
						text='show', level='glyph', source=source, 
						text_font_size='10pt', text_font_style='bold',
						x_offset=0, y_offset=10)
	p.add_layout(labels_show_title)

	p.x_range=Range1d(0,11)
	p.xaxis.visible = False
	p.yaxis.visible = False
	
	# Return the figure
	script, div = components(p)
	script = jsmin(script)
	return {'script': script, 'div': div}


def bestOfTheBestTopSeasons(df):

	# Create the season-show field
	df['rating'] = df['rating'].astype(float)
	df['season-show'] = df['show'] + ' S' + df['season'].astype(str)
	df = df.groupby('season-show')[['rating']].mean().reset_index().sort_values(by='rating', ascending=False).head(10)[::-1]
	df['rating'] = round(df['rating'], 2)

	# Create the figure
	source = ColumnDataSource(df)
	p = figure(sizing_mode='stretch_both', y_range=df['season-show'], tools=[])
	p.hbar(y="season-show", height=.35, right="rating", color="#191970", source=source)

	# Format the chart
	labels = LabelSet(x='rating', y='season-show', 
						text='rating', level='glyph', source=source, 
						text_font_size='10pt', text_font_style='bold',
						x_offset=8, y_offset=-7)
	p.add_layout(labels)

	labels = LabelSet(x=0, y='season-show', 
						text='season-show', level='glyph', source=source, 
						text_font_size='10pt', text_font_style='bold',
						x_offset=0, y_offset=10)
	p.add_layout(labels)

	p.x_range=Range1d(0,11)
	p.xaxis.visible = False
	p.yaxis.visible = False
	
	# Return the figure
	script, div = components(p)
	script = jsmin(script)
	return {'script': script, 'div': div}


def bestOfTheBestTopEpisodes(df):

	# Create the season-show field
	df['rating'] = df['rating'].astype(float)
	df['episode_title'] = df['episode_title'] + " (" + df['show'] + ", S" + df['season'].astype(str) + ")"
	df = df.groupby('episode_title')[['rating']].mean().reset_index().sort_values(by='rating', ascending=False).head(10)[::-1]

	# Create the figure
	source = ColumnDataSource(df)
	p = figure(sizing_mode='stretch_both', y_range=df['episode_title'], tools=[])
	p.hbar(y="episode_title", height=.35, right="rating", color="#8B0000", source=source)

	# Format the chart
	labels = LabelSet(x='rating', y='episode_title', 
						text='rating', level='glyph', source=source, 
						text_font_size='10pt', text_font_style='bold',
						x_offset=8, y_offset=-7)
	p.add_layout(labels)

	labels_episode_titles = LabelSet(x=0, y='episode_title', 
						text='episode_title', level='glyph', source=source, 
						text_font_size='10pt', text_font_style='bold',
						x_offset=0, y_offset=10)
	p.add_layout(labels)
	p.add_layout(labels_episode_titles)
	p.x_range=Range1d(0,11)
	p.xaxis.visible=False
	p.yaxis.visible = False
	
	# Return the figure
	script, div = components(p)
	script = jsmin(script)
	return {'script': script, 'div': div}


def bestOfTheBestMostPopularEpisodes(df):

	# Create the season-show field
	df['rating'] = df['rating'].astype(float)
	# df['episode_title'] = df['episode_title'] + " (" + df['show'] + ", Season " + df['season'].astype(str) + ")"
	df = df.groupby('episode_title')[['number_of_ratings']].max().reset_index().sort_values(by='number_of_ratings', ascending=False).head(10)[::-1]
	df['label'] = ['{:,}'.format(i) for i in df['number_of_ratings'].tolist()]

	# Create the figure
	source = ColumnDataSource(df)
	p = figure(sizing_mode='stretch_both', y_range=df['episode_title'], tools=[])
	p.hbar(y="episode_title", height=.35, right="number_of_ratings", color="#191970", source=source)

	# Format the chart
	labels = LabelSet(x='number_of_ratings', y='episode_title', 
						text='label', level='glyph', source=source, 
						text_font_size='10pt', text_font_style='bold',
						x_offset=8, y_offset=-7)
	p.add_layout(labels)

	labels_episode_titles = LabelSet(x=0, y='episode_title', 
						text='episode_title', level='glyph', source=source, 
						text_font_size='10pt', text_font_style='bold',
						x_offset=0, y_offset=10)
	p.add_layout(labels)
	p.add_layout(labels_episode_titles)


	p.x_range=Range1d(0,df['number_of_ratings'].max()*1.3)
	p.xaxis.visible=False
	p.yaxis.visible = False
	
	# Return the figure
	script, div = components(p)
	script = jsmin(script)

	return {'script': script, 'div': div}


def bestOfTheBestRatingsOverTime(df):
	
	# Sort by airdate
	df = df.groupby('air_date')[['rating']].mean().reset_index()
	df['air_date'] = pd.to_datetime(df['air_date'], format='%Y-%m-%d')
	df = df.set_index('air_date')
	df = df.resample('Q').mean().reset_index()

	# Create the figure
	source = ColumnDataSource(df)
	p = figure(sizing_mode='stretch_both', x_axis_type='datetime', tools=[])
	p.line(x='air_date', y='rating', line_width=2, color='#191970', source=source)
	p.y_range = Range1d(0, 10)
	
	# Format chart
	p.xaxis.axis_label = "Year"
	# p.yaxis.axis_label = "Rating (/10)"

	# Return the figure
	script, div = components(p)
	script = jsmin(script)

	return {'script': script, 'div': div}


def bestOfTheBestBestShowPerYear(df):

	# Convert date and pull air year
	df['air_date'] = pd.to_datetime(df['air_date'], format='%Y-%m-%d')
	df['aired_year'] = df['air_date'].dt.year

	# Group by year and show
	df_grouped = df.groupby(['aired_year', 'show'])[['rating']].mean().reset_index()
	df_grouped = df_grouped.sort_values(by=['aired_year', 'rating'])
	best_show_per_year = df_grouped.loc[df_grouped.groupby('aired_year').rating.idxmax()]
	
	# Create the table
	table = """
				<table class="table" id="table-best-show-per-year" text-align="center">
					<tr></tr>
					<thead>
						<tr>
							<th align="center" style="background-color: #4CAFCF; color: #000">Year</th>
							<th style="background-color: #4CAFCF; color: #000">Show</th>
							<th style="background-color: #4CAFCF; color: #000">Average Rating</th>
						</tr>
					</thead>
					<tbody>
				"""
	for i in range(len(best_show_per_year)):
		table = table + """
					<tr>
						<td><strong>{}</strong></td>
						<td>{}</td>
						<td>{}</td>
					</tr>
					""".format(best_show_per_year['aired_year'].iloc[i],
								best_show_per_year['show'].iloc[i],
								round(best_show_per_year['rating'].iloc[i], 2))
	table += "</tbody></table>"

	return table


if __name__ == '__main__':
	bestOfTheBestBestShowPerYear(df=pd.read_csv('episodes.csv'))