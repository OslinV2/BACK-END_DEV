from bs4 import BeautifulSoup
import requests

# Function to get movie details
def get_movie_details(movie_name):
    # Base URL of IMDB website
    base_url = 'https://www.imdb.com'
    search_query = '/search/title?title='
    
    # Empty dictionary to store movie details
    movie_details = {}
    
    # Query formation
    movie_query = search_query + '+'.join(movie_name.strip().split())
    
    # Fetch the webpage and parse it
    response = requests.get(base_url + movie_query + '&title_type=feature')
    bs = BeautifulSoup(response.text, 'html.parser')
    
    # Find the first movie result
    result = bs.find('h3', {'class': 'lister-item-header'})
    if not result:
        return None

    movie_link = base_url + result.a['href']
    movie_details['name'] = result.a.text.strip()
    
    # Fetch the movie's detailed page
    response = requests.get(movie_link)
    bs = BeautifulSoup(response.text, 'html.parser')
    
    # Year
    try:
        movie_details['year'] = bs.find('span', {'id': 'titleYear'}).a.text
    except AttributeError:
        movie_details['year'] = 'Not available'
    
    # Subtext section (contains genres, runtime, release date)
    subtext = bs.find('div', {'class': 'subtext'})
    if subtext:
        movie_details['genres'] = [genre.text for genre in subtext.find_all('a', {'title': None})]
        try:
            movie_details['rating'] = bs.find('div', {'class': 'ratingValue'}).span.text
        except AttributeError:
            movie_details['rating'] = 'Not yet rated'
        
        try:
            movie_details['runtime'] = subtext.time.text.strip()
        except AttributeError:
            movie_details['runtime'] = 'Not available'
        
        try:
            movie_details['release_date'] = subtext.find('a', {'title': 'See more release dates'}).text.strip()
        except AttributeError:
            movie_details['release_date'] = 'Not available'
    else:
        movie_details['genres'] = []
        movie_details['rating'] = 'Not available'
        movie_details['runtime'] = 'Not available'
        movie_details['release_date'] = 'Not available'

    # Credit summary section (directors, writers, cast)
    credit_summary = bs.find_all('div', {'class': 'credit_summary_item'})
    try:
        movie_details['directors'] = [director.text.strip() for director in credit_summary[0].find_all('a')]
        movie_details['writers'] = [writer.text.strip() for writer in credit_summary[1].find_all('a') if 'name' in writer['href']]
        movie_details['cast'] = [actor.text.strip() for actor in credit_summary[2].find_all('a') if 'name' in actor['href']]
    except IndexError:
        movie_details['directors'] = []
        movie_details['writers'] = 'Not found'
        movie_details['cast'] = 'Not found'
    
    # Fetch the plot summary from a separate page
    response = requests.get(movie_link + 'plotsummary')
    bs = BeautifulSoup(response.text, 'html.parser')
    try:
        movie_details['plot'] = bs.find('li', {'class': 'ipl-zebra-list__item'}).p.text.strip()
    except AttributeError:
        movie_details['plot'] = 'Plot not available'

    return movie_details


if __name__ == "__main__":
    movie_name = input('Enter the movie name to fetch details: ').strip()
    movie_details = get_movie_details(movie_name)
    if not movie_details:
        print('No movie found with the given name!')
    else:
        print(f"\n{movie_details['name']} ({movie_details['year']})")
        print(f"Rating: {movie_details['rating']}")
        print(f"Runtime: {movie_details['runtime']}")
        print(f"Release Date: {movie_details['release_date']}")
        print(f"Genres: {', '.join(movie_details['genres'])}")
        print(f"Directors: {', '.join(movie_details['directors'])}")
        print(f"Writers: {', '.join(movie_details['writers'])}")
        print(f"Cast: {', '.join(movie_details['cast'])}")
        print(f"Plot Summary:\n{movie_details['plot']}")
