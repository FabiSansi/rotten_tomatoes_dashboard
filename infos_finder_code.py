import pandas as pd
import imdb
import requests
import time

# Initialize the IMDb object
ia = imdb.IMDb()

# OMDb API key (Replace with your own key)
omdb_api_key = '77ce9f63'

# Function to extract Rotten Tomatoes rating
def get_rotten_tomatoes_rating(ratings):
    for rating in ratings:
        if rating['Source'] == 'Rotten Tomatoes':
            return rating['Value']
    return 'N/A'

# Load the CSV file
df = pd.read_csv('part_netflix_titles.csv')

# Add new columns to store the movie data from OMDb API
df['imdbID'] = ''
df['Year'] = ''
df['Rated'] = ''
df['Released'] = ''
df['Runtime'] = ''
df['Genre'] = ''
df['Director'] = ''
df['Writer'] = ''
df['Actors'] = ''
df['Plot'] = ''
df['Language'] = ''
df['Country'] = ''
df['Awards'] = ''
df['Poster'] = ''
df['RottenTomatoesRating'] = ''

# Iterate over the movie titles
for index, row in df.iterrows():
    title = row['title']
    try:
        # Search for the movie on IMDb using the title
        search_results = ia.search_movie(title)
        if search_results:
            # Get the IMDb ID of the first search result
            imdb_id = search_results[0].movieID

            # Construct the OMDb API URL
            omdb_url = f"https://www.omdbapi.com/?i=tt{imdb_id}&apikey={omdb_api_key}"
            
            # Make a request to the OMDb API
            response = requests.get(omdb_url)
            movie_json = response.json()

            if movie_json.get('Response') == 'True':
                # Update the DataFrame with the extracted information
                df.at[index, 'imdbID'] = movie_json.get('imdbID', '')
                df.at[index, 'Year'] = movie_json.get('Year', '')
                df.at[index, 'Rated'] = movie_json.get('Rated', '')
                df.at[index, 'Released'] = movie_json.get('Released', '')
                df.at[index, 'Runtime'] = movie_json.get('Runtime', '')
                df.at[index, 'Genre'] = movie_json.get('Genre', '')
                df.at[index, 'Director'] = movie_json.get('Director', '')
                df.at[index, 'Writer'] = movie_json.get('Writer', '')
                df.at[index, 'Actors'] = movie_json.get('Actors', '')
                df.at[index, 'Plot'] = movie_json.get('Plot', '')
                df.at[index, 'Language'] = movie_json.get('Language', '')
                df.at[index, 'Country'] = movie_json.get('Country', '')
                df.at[index, 'Awards'] = movie_json.get('Awards', '')
                df.at[index, 'Poster'] = movie_json.get('Poster', '')
                df.at[index, 'RottenTomatoesRating'] = get_rotten_tomatoes_rating(movie_json.get('Ratings', []))
                print(f"IMDb search complete for title: {title}")
            # Respect API rate limits
            time.sleep(1)
        else:
            print(f"IMDb search failed for title: {title}")

    except Exception as e:
        print(f"Error processing title '{title}': {e}")

# Save the updated DataFrame back to the CSV file
df.to_csv('part_netflix_titles.csv', index=False)

print("CSV file updated successfully!")