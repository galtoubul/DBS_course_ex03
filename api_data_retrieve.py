import requests
import json
import db_manipulate as db
from os.path import isfile
from config import omdb_api_key, nyt_api_key


omdb_url_format = f'http://www.omdbapi.com/?apikey={omdb_api_key}&t={{0}}'
omdb_calls_per_day = 900
reviews_num_at_one_api_call = 20
ERR = -1

nytimes_url_format = f'https://api.nytimes.com/svc/movies/v2/reviews/all.json?offset={0}&api-key={nyt_api_key}'
nytimes_headers = {"Accept": "application/json"}

reviews_file_path = './nytimes_reviews_offset.json'


def is_valid_review(review):
    # valid review should have a headline
    if 'headline' not in review:
        return False

    # valid multimedia(picture) should have src
    if 'multimedia' in review and type(review['multimedia']) == dict and 'src' not in review['multimedia']:
        return False
        
    # valid linkshould have url
    if 'link' in review and type(review['link']) == dict and 'url' not in review['link']:
        return False

    return True


def get_offset():
    """returns: the offset of the last api call for nytimes
                In case this is the first api call returns 0
    """
    # file doesn't exist
    if not isfile(reviews_file_path):
        return 0

    with open(reviews_file_path, 'r') as reviews_offset_file:
        data = reviews_offset_file.read()
        # file isn't empty
        if len(data) > 0:
            reviews_offset_dict = json.loads(data)
            last_offset_num = int(reviews_offset_dict['offset'])
            current_offset = last_offset_num + reviews_num_at_one_api_call
        # file is empty
        else:
            current_offset = 0
        return current_offset


def update_offset(offset):
    try:
        with open(reviews_file_path, 'w') as reviews_offset_file:
            reviews_offset_file.write(f'{{\"offset\":{offset}}}')
    except OSError as err:
        print(f'\n\retrieve_data_from_nyt\n error: {err}')
        return ERR


def retrieve_review_from_nyt(offset):
    """retrieve reviews_num_at_one_api_call reviews from nytimes api
    returns: -1 in case of an error
             OW, the retrieved data as a dict
    """
    # retrieve reviews from the New York Times
    nytimes_url = nytimes_url_format.format(offset)
    try:
        response = requests.request("GET", nytimes_url, headers=nytimes_headers)
    except requests.exceptions.RequestException as err:
        print(f'\n\retrieve_data_from_nyt\n error: {err}')
        return ERR

    # parse data into a dict and check for erros
    nytimes_data_dict = response.json()
    if not('status' in nytimes_data_dict and nytimes_data_dict['status'] == 'OK'):
        print('\n\retrieve_data_from_nyt\nbreak reason: status =', nytimes_data_dict['status'])
        return ERR
    if not 'results' in nytimes_data_dict:
        print('\n\retrieve_data_from_nyt\n there isn\'t a resulsts key at the retrieved data')
        return ERR

    if update_offset(offset) is ERR:
        return ERR
    
    return nytimes_data_dict


# retrieve relevant data from omdb
def retrieve_movie_info_from_omdb(review):
    """returns: the movie info for the movie that the review was written about
    """
    if 'display_title' not in review:
        return ERR

    movie_name = review['display_title']
    omdb_url = omdb_url_format.format('+'.join(movie_name.split()))
    try:
        response = requests.request("GET", omdb_url)
    except requests.exceptions.RequestException as err:
        print(f'\n\retrieve_data_from_omdb\n error: {err}')
        return ERR

    global omdb_calls_per_day
    omdb_calls_per_day -= 1

    # return data as a dict
    omdb_data_dict = response.json()
    if omdb_data_dict['Response'] == 'False':
        print(f'\n\nretrieve_movie_info_from_omdb\nmovie = {movie_name}\nomdb_data_dict = {omdb_data_dict}')
        return ERR
    return omdb_data_dict


def retrieve_data():
    offset = get_offset()

    while omdb_calls_per_day >= reviews_num_at_one_api_call:
        nyt_data_dict = retrieve_review_from_nyt(offset)
        if nyt_data_dict == ERR:
            break
        
        reviews = nyt_data_dict['results']
        print(f'len(reviews) = {len(reviews)}')
        for review in reviews:

            movie = retrieve_movie_info_from_omdb(review)
            movie_id = ''
            if movie != ERR:
                movie_id = db.add_movie(movie)

            # check that the review is valid and insert it to the DB
            if is_valid_review(review):
                db.add_review(review, movie_id)
            
        # prepare to read another 20 reviews
        offset += reviews_num_at_one_api_call
        print(f'\n\nretrieve_data\nnext offset = {offset}')

        if not('has_more' in nyt_data_dict and nyt_data_dict['has_more'] == True):
            print('\n\nretrieve_data\nhas more = ', nyt_data_dict['has_more'])
            break
        

if __name__ == "__main__":
    retrieve_data()