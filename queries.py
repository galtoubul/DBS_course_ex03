import mysql.connector as SQLC
import inspect
from flask import Flask
from flaskext.mysql import MySQL
from config import ERR, SUCCESS, db_host, db_user, db_password, db_database, db_port


app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = db_user
app.config['MYSQL_DATABASE_PORT'] = db_port
app.config['MYSQL_DATABASE_PASSWORD'] = db_password
app.config['MYSQL_DATABASE_DB'] = db_database
app.config['MYSQL_DATABASE_HOST'] = db_host
mysql.init_app(app)


def run_query(query, query_params_dict):
    caller = inspect.stack()[1][3]
    db_con = mysql.connect()
    cursor = db_con.cursor()
    try:
        cursor.execute(query, query_params_dict)
        db_con.commit()
    except SQLC.IntegrityError as err:
        print(f'\n\n{caller}\nerror = {str(err)}')
        return ERR
    return cursor


def q1(word: str, limit: int) -> None:
    '''Prints at most <limit> movies that contains <word> in their plot'''
    query = """SELECT Name
               FROM Movie
               WHERE match(Plot)
                     against(%(word)s IN BOOLEAN MODE)
               LIMIT %(limit)s"""
    query_params_dict = {'word': f'+{word}', 'limit': limit}
    print(f'\n\nq1\nquery = {query}\nquery_params_dict = {query_params_dict}')
    
    cursor = run_query(query, query_params_dict)
    if cursor != ERR:
        movies = cursor.fetchall()
        cnt = 0
        print('\n\nq1 results:\n' + 11*'-')
        for movie in movies:
            cnt += 1
            print(movie[0])
        print(f'\n\nq1 returned {cnt} results')


def q2(avg_rating: int, imdb_rating: int, limit: int) -> None:
    '''avg_rating: integer at the range 0 - 100
       imdb_rating: integer at the range 0 - 10
       Prints at most <limit> movies with
       average rating of at least <avg_rating> and
       imdb rating of at list <avg_rating>'''

    query = """SELECT DISTINCT Name, HR.avg_rating, IR.RatingValue
               FROM (SELECT R.MovieId, AVG(R.RatingValue) as avg_rating
                     FROM Rating as R
                     GROUP BY R.MovieId
                     HAVING AVG(R.RatingValue) >= %(avg_rating)s) as HR,
                     Movie as M,
                     Rating as R,
                     ImdbRating as IR
               WHERE IR.RatingValue >= %(imdb_rating)s   AND
                     IR.ImdbId = M.ImdbRatingId          AND
                     M.MovieId = R.MovieId               AND
                     HR.MovieId = R.MovieId
               ORDER BY HR.avg_rating DESC , IR.RatingValue DESC
               LIMIT %(limit)s;"""
    query_params_dict = {'avg_rating': avg_rating, 'imdb_rating': imdb_rating, 'limit': limit}
    print(f'\n\nq1\nquery = {query}\nquery_params_dict = {query_params_dict}')
    
    cursor = run_query(query, query_params_dict)
    if cursor != ERR:
        results = cursor.fetchall()
        cnt = 0
        print('\n\nq2 results:\n' + 11*'-')
        for res in results:
            cnt += 1
            string_format = '{0:<90} | {1:^30} | {2:>20}'
            args = (f'movie name = {res[0]}',f'average rating = {res[1]}', f'IMDB rating = {res[2]}')
            print(string_format.format(*args))
        print(f'\n\nq2 returned {cnt} results')


# SELECT *
# FROM Movie as M1
# WHERE M1.RunningTime NOT IN (SELECT M2.RunningTime
#                              FROM Movie as M2
#                              WHERE M1.MovieId <> M2.MovieId)

# Running examples
# q1(word='State', limit=100)
# q2(85, 8, 100)