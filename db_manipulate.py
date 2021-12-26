from os import link
import mysql.connector as SQLC
import inspect
from dateutil.parser import parse

ERR     = -1
SUCCESS = 0

host = 'localhost'
port = '3305'
user = 'DbMysql25'
password = 'DbMysql25'
db_name = 'DbMysql25'

# connect to db
db_con = SQLC.connect(host=host, port=port, user=user,passwd=password)
cursor = db_con.cursor()


db_to_api_dict = {
    'Poster': {
        'Url': 'Poster'
    },
    'ImdbRating': {
        'ImdbId': 'imdbID',
        'Votes': 'imdbVotes',
        'RatingValue': 'imdbRating'
    },
    'Movie': {
        'Name': 'Title',
        'ReleaseDate': 'Released',
        'RunningTime': 'Runtime',
        'Rating': 'Rated',
        'Plot': 'Plot',
        'Awards': 'Awards',
        'MetaScore': 'Metascore',
        'BoxOffice': 'BoxOffice',
        'fks_dict': {
            'PosterId': 'poster_id',
            'ImdbRatingId': 'imdb_id'
        }
    },
    'Rating': {
        'Source': 'Source',
        'RatingValue': 'Value',
        'fks_dict': {
            'MovieId': 'movie_id',
        }
    },
    'Staff': {
        'FirstName': 'FirstName',
        'MiddleName': 'MiddleName',
        'LastName': 'LastName',
        'Profession': 'Profession'
    },
    'StaffMovie': {
        'fks_dict': {
            'StaffId': 'staff_id',
            'MovieId': 'movie_id',
        }
    },
    'Country': {
        'Name': 'Country'
    },
    'CountryMovie': {
        'fks_dict': {
            'CountryId': 'country_id',
            'MovieId': 'movie_id',
        }
    },
    'Language': {
        'Name': 'Language'
    },
    'LanguageMovie': {
        'fks_dict': {
            'LanguageId': 'language_id',
            'MovieId': 'movie_id',
        }
    },
    'Genre': {
        'Name': 'Genre'
    },
    'GenreMovie': {
        'fks_dict': {
            'GenreId': 'genre_id',
            'MovieId': 'movie_id',
        }
    },
    'Picture': {
        'Type': 'type',
        'Url': 'src',
        'Height': 'height',
        'Width': 'width'
    },
    'Link': {
        'Type': 'type',
        'Url': 'url',
        'SuggestedLinkText': 'suggested_link_text'
    },
    'Review': {
        'Headline': 'headline',
        'MpaaRating': 'mpaa_rating',
        'CriticsPick': 'critics_pick',
        'Summary': 'summary_short',
        'PublicationDate': 'publication_date',
        'CreationDate': 'opening_date',
        'UpdateDate': 'date_updated',
        'fks_dict': {
            'PictureId': 'picture_id',
            'LinkId': 'link_id',
            'MovieId': 'movie_id'
        }
    }
}


json_to_db_dict = {
    'ImdbRating': {
        'Votes': [(',', ''),('N/A', '')],
        'RatingValue': [('N/A', '')]
    },
    'Movie': {
        'RunningTime': [('N/A', ''),(' min', '')],
        'Rating': [('N/A', ''),('Not Rated', '')],
        'MetaScore': [('N/A', '')],
        'BoxOffice': [('N/A', ''),(',', ''),('$','')],
    },
    'Rating': {
        'RatingValue': [('.','')]
    },
    'Review': {
        'MpaaRating': [('Unrated', ''), ('Not Rated','')],
        'PublicationDate': [('null','')],
        'CreationDate': [('null','')],
        'UpdateDate': [('null','')],
    }
}


def json_to_db(table, col, val):
    if table in json_to_db_dict and col in json_to_db_dict[table]:
        for r in json_to_db_dict[table][col]:
            val = val.replace(*r)

    if col == 'ReleaseDate':
        val = parse(val).strftime('%Y-%m-%d') if val != 'N/A' else ''

    if col == 'RatingValue':
        # val in ['<int>%', '<int>'\100, '<decimal without .>/10']
        val = val[0:2]

    return val


def init_insert_query(table_name):
    return f'INSERT INTO {db_name}.{table_name} ', '(', 'VALUES('


def finalize_insert_query(insert_query_cols, insert_query_vals, insert_query):
    insert_query_cols += ') '
    insert_query_vals += ');'
    insert_query += insert_query_cols + insert_query_vals
    return insert_query


def build_insert_query(table_name, data, fks_dict=None):
    insert_query, insert_query_cols, insert_query_vals = init_insert_query(table_name)
    insert_query_params_dict = {}
    is_first = True

    def update_insert_query(key, val, use_fks=False):
        nonlocal insert_query_cols, insert_query_vals, is_first, insert_query_params_dict
        actual_value = data[val] if not use_fks else fks_dict[val]
        actual_value = json_to_db(table_name, key, actual_value)
        if actual_value != '':
            if is_first:
                insert_query_cols += key
                insert_query_vals += f'%({val})s'
                is_first = False
            else:
                insert_query_cols += f', {key}'
                insert_query_vals += f', %({val})s'
            insert_query_params_dict[val] = actual_value

    for (db_format, api_format) in db_to_api_dict[table_name].items():
        if isinstance(api_format, dict):
            for (db_format, fk_format) in api_format.items():
                update_insert_query(db_format, fk_format, use_fks=True)
        elif api_format in data:
            update_insert_query(db_format, api_format)
    
    insert_query = finalize_insert_query(insert_query_cols, insert_query_vals, insert_query)
    return insert_query, insert_query_params_dict


def insert(table_name, data, fks_dict=None):
    insert_query, insert_query_params_dict = build_insert_query(table_name, data, fks_dict)
    
    caller = inspect.stack()[1].function
    print(f'\n\ninsert | caller = {caller} | table name = {table_name}\ninsert_query = \n{insert_query}\nquery_params_dict = \n{insert_query_params_dict}')
    
    try:
        cursor.execute(insert_query, insert_query_params_dict)
        db_con.commit()
    except SQLC.IntegrityError as err:
        print(f'\n\n{caller}\nerror = {err}')
        return ERR
    print(f'\n\ninsert | caller = {caller} | table name = {table_name}\nSuccesful insert! {cursor.rowcount} rows were affacted')
    return SUCCESS


def update_foreign_keys(data):
    caller = inspect.stack()[1].function

    if caller == 'add_review':
        if 'multimedia' in data:
            add_picture_rc = insert('Picture', data['multimedia'])
            picture_id = cursor.lastrowid if add_picture_rc != ERR else ''
            print(f'picture_id = {picture_id}')
        if 'link' in data:
            link_id_rc = insert('Link', data['link'])
            link_id = cursor.lastrowid if link_id_rc != ERR else ''
            print(f'link_id = {link_id}')
        return picture_id, link_id

    # caller == add_movie
    else:
        if 'Poster' in data:
            add_poster_rc = insert('Poster', data)
            poster_id = cursor.lastrowid if add_poster_rc != ERR else ''
            print(f'poster_id = {poster_id}')
        if 'imdbID' in data:
            insert('ImdbRating', data)
            imdb_id = data['imdbID']
            print(f'imdb_id = {imdb_id}')
        return poster_id, imdb_id


def add_review(review, movie_id = None):
    print(f'\n\nadd_review\n\nreview = {review}')
    picture_id, link_id = update_foreign_keys(review)
    movie_id = movie_id if movie_id not in [ERR, None] else ''
    fks = {'picture_id': picture_id, 'link_id': link_id, 'movie_id': movie_id}
    insert('Review', review, fks)


# insert values to Rating
def add_rating(movie, movie_id):
    if 'Ratings' in movie:
        fks = {'movie_id': movie_id}
        for rating in movie['Ratings']:
            insert('Rating', rating, fks)


# insert values to Staff, StaffMovie
def add_staff(movie, movie_id):
    professions = ['Writer', 'Actors', 'Director']
    for profession in professions:
        if profession in movie:
            persons = [person.strip() for person in movie[profession].split(',')]
            for person in persons:
                if person == 'N/A':
                    continue
                # remove words in paranthesis after the name
                person = (person[:person.find('(')]).strip() if '(' in person else person
                person_details = {}
                person_details['Profession'] = 'Actor' if profession == 'Actors' else profession
                writer_name = person.split()
                person_details['FirstName'] = writer_name[0]
                person_details['MiddleName'] = ' '.join(writer_name[1:-1]) if len(writer_name) > 2 else ''
                person_details['LastName'] = writer_name[-1] if len(writer_name) > 1 else ''
                add_staff_rc = insert('Staff', person_details)
                staff_id = cursor.lastrowid if add_staff_rc != ERR else ''
                fks = {'staff_id': staff_id, 'movie_id': movie_id}
                insert('StaffMovie', None, fks)


# insert values to Country, CountryMovie
def add_country(movie, movie_id):
    if 'Country' in movie:
        countries = [country.strip() for country in movie['Country'].split(',')]
        for country in countries:
            if country == 'N/A':
                continue
            add_country_rc = insert('Country', {'Country': country})
            country_id = cursor.lastrowid if add_country_rc != ERR else ''
            fks = {'country_id': country_id, 'movie_id': movie_id}
            insert('CountryMovie', None, fks)


# insert values to Language, LanguageMovie
def add_language(movie, movie_id):
    if 'Language' in movie:
        languages = [language.strip() for language in movie['Language'].split(',')]
        for language in languages:
            if language == 'N/A':
                continue
            add_language_rc = insert('Language', {'Language': language})
            language_id = cursor.lastrowid if add_language_rc != ERR else ''
            fks = {'language_id': language_id, 'movie_id': movie_id}
            insert('LanguageMovie', None, fks)


# insert values to Genre, GenreMovie
def add_genre(movie, movie_id):
    if 'Genre' in movie:
        genres = [genre.strip() for genre in movie['Genre'].split(',')]
        for genre in genres:
            if genre == 'N/A':
                continue
            add_genre_rc = insert('Genre', {'Genre': genre})
            gnere_id = cursor.lastrowid if add_genre_rc != ERR else ''
            fks = {'genre_id': gnere_id, 'movie_id': movie_id}
            insert('GenreMovie', None, fks)


def add_movie(movie):
    print(f'\n\nadd_movie\n\nmovie = {movie}')

    # insert values to Poster, ImdbRating, Movie
    poster_id, imdb_id = update_foreign_keys(movie)
    fks = {'poster_id': poster_id, 'imdb_id': imdb_id}
    add_movie_rc = insert('Movie', movie, fks)
    movie_id = cursor.lastrowid if add_movie_rc != ERR else ''

    add_rating(movie, movie_id)
    add_staff(movie, movie_id)
    add_country(movie, movie_id)
    add_language(movie, movie_id)
    add_genre(movie, movie_id)

    return movie_id if add_movie_rc != ERR else ERR




























# def insert(table_name, data, fks):
#     caller = inspect.stack()[1].function
#     insert_query = f'INSERT INTO {db_name}.{table_name} '
#     insert_query_cols = '('
#     insert_query_vals = 'VALUES('

#     insert_query_params_dict = {}
#     is_first = True
#     for (db_format, api_fk_format) in db_to_api_fk_dict[table_name].items():
#         if api_fk_format in data and data[api_fk_format] != '':
#             if not is_first:
#                 insert_query_cols += ', '
#                 insert_query_vals += ', '
#             is_first = False

#             insert_query_cols += db_format
#             insert_query_vals += f'%({api_fk_format})s'
#             insert_query_params_dict[api_fk_format] = data[api_fk_format]

#     insert_query_cols += ') '
#     insert_query_vals += ');'
#     insert_query += insert_query_cols + insert_query_vals

#     print(f'\n\ninsert | caller = {caller} | table name = {table_name}insert_query = \n{insert_query}\nquery_params_dict = \n{insert_query_params_dict}')
    
#     try:
#         cursor.execute(insert_query, insert_query_params_dict)
#         db_con.commit()
#     except SQLC.IntegrityError as err:
#         print(f'\n\n{caller}\nerror = {err}')
#         return ERR
#     print(f'\n\ninsert | caller = {caller} | table name = {table_name}\nSuccesful insert! {cursor.rowcount} rows were affacted')
#     return SUCCESS


# def add_picture(picture):
#     table_name = 'Picture'
#     insert_query = f'INSERT INTO {db_name}.{table_name} '
#     insert_query_cols = '('
#     insert_query_vals = 'VALUES('

#     insert_query_params_dict = {}
#     is_first = True
#     for (db_format, api_json_format) in db_to_api_json_dict.items():
#         if api_json_format in picture and picture[api_json_format] != '':
#             if not is_first:
#                 insert_query_cols += ', '
#                 insert_query_vals += ', '
#             is_first = False

#             insert_query_cols += db_format
#             insert_query_vals += f'%({api_json_format})s'
#             insert_query_params_dict[api_json_format] = picture[api_json_format]
    
#     insert_query_cols += ') '
#     insert_query_vals += ');'
#     insert_query += insert_query_cols + insert_query_vals

#     print(f'\n\nDB add_picture\ninsert_query = \n{insert_query}\nquery_params_dict = \n{insert_query_params_dict}')
    
#     try:
#         cursor.execute(insert_query, insert_query_params_dict)
#         db_con.commit()
#     except SQLC.IntegrityError as err:
#         print(f'\n\nDB add_picture\nerror = {err}')
#         return ERR
#     print(f'\n\nDB add_picture\nSuccesful insert! {cursor.rowcount} rows were affacted')
#     return SUCCESS
