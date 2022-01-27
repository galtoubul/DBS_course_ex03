import inspect
import os
from flask import Flask
from flaskext.mysql import MySQL
from config import ERR, db_host, db_user, db_password, db_database, db_port


app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = db_user
app.config['MYSQL_DATABASE_PORT'] = db_port
app.config['MYSQL_DATABASE_PASSWORD'] = db_password
app.config['MYSQL_DATABASE_DB'] = db_database
app.config['MYSQL_DATABASE_HOST'] = db_host
mysql.init_app(app)


def run_query(query, query_params_dict):
    try:
        caller = inspect.stack()[1][3]
        db_con = mysql.connect()
        cursor = db_con.cursor()
        cursor.execute(query, query_params_dict)
        db_con.commit()
    except Exception as err:
        print(f'\n\n{caller}\nerror = {str(err)}')
        return ERR
    return cursor


def q1(word: str, limit: int = 50) -> None:
    '''For each movie that follows the following condition:
       1. Contains <word> in his plot
       Prints its name and plot
       Prints at most <limit> records

       word   : a single word with at least 3 characters
       limit  : integer greater or equal 0
    '''
    query = """SELECT Name, Movie.Plot
               FROM Movie
               WHERE match(Plot)
                     against(%(word)s IN BOOLEAN MODE)
               LIMIT %(limit)s"""
    query_params_dict = {'word': f'+{word}', 'limit': limit}
    print(f'\n\nq1\nquery = {query}\nquery_params_dict = {query_params_dict}')
    
    cursor = run_query(query, query_params_dict)

    if cursor != ERR:

        try:
            results = cursor.fetchall()
        except Exception as err:
            print(f'\n\nq1\nerror = {str(err)}')
            return

        cnt = 0
        cols = (os.get_terminal_size()).columns
        print('\n\nq1 results:\n' + cols * '*')
        for res in results:
            cnt += 1
            print(f'movie name = {res[0]}')
            print(f'plot = {res[1]}')
            print(cols * '-')
        print(f'\n\nq1 returned {cnt} results')


def q2(avg_rating: int, imdb_rating: float, limit: int = 50) -> None:
    '''For each movie that follows the following conditions:
       1. Has average rating of at least <avg_rating>
       2. Has imdb rating of at list <avg_rating>
       Prints its name, average rating and IMDB rating
       Prints at most <limit> records

       avg_rating    : integer at the range 0 - 100
       imdb_rating   : integer at the range 0 - 10
       limit         : integer greater or equal 0
    '''
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
    print(f'\n\nq2\nquery = {query}\nquery_params_dict = {query_params_dict}')
    
    cursor = run_query(query, query_params_dict)

    if cursor != ERR:

        try:
            results = cursor.fetchall()
        except Exception as err:
            print(f'\n\nq2\nerror = {str(err)}')
            return
        
        cnt = 0
        cols = (os.get_terminal_size()).columns
        print('\n\nq2 results:\n' + cols * '*')
        string_format = '{0:<90} | {1:^30} | {2:>20}'
        args = (f'Name',f'Average Rating', f'IMDB rating')
        print(string_format.format(*args) + '\n' + cols * '*')
        for res in results:
            cnt += 1
            args = (res[0], res[1], res[2])
            print(string_format.format(*args) + '\n' + cols * '-')
        print(f'\n\nq2 returned {cnt} results')


def q3(wins: int, nominations: int, limit: int = 50) -> None:
    '''For each movie that follows the following conditions:
       1. Won <wins> awards
       2. Was nominated for <nominations> awards
       3. Has running time which is shorter than the average running time
       Prints its name, running time and awards and nominations
       Prints at most <limit> records
       
       wins          : integer greater or equal 0
       nominations   : integer greater or equal 0
       limit         : integer greater or equal 0
    '''

    query = """SELECT M1.Name, M1.RunningTime, M1.Awards
               FROM Movie as M1
               WHERE MATCH(M1.Awards) AGAINST (%(to_find_match)s IN BOOLEAN MODE) AND
                     M1.Awards LIKE %(to_find_like)s                                 AND
                     M1.RunningTime < (SELECT avg(M2.RunningTime)
                                       FROM Movie as M2)
               LIMIT %(limit)s;"""
    
    wins_string = f"{wins} win" if wins == 1 else f"{wins} wins"
    nominations_string = f"{nominations} nomination" if nominations == 1 else f"{nominations} nominations"
    if wins != 0 and nominations == 0:
        to_find_match = f"\"{wins_string}\" -nomination -nominations"
        to_find_like = f"{wins_string}%"
    elif wins == 0 and nominations != 0:
        to_find_match = f"\"{nominations_string}\""
        to_find_like = to_find_match[1:-1] + '%'
    else:
        to_find_match = f"\"{wins_string} & {nominations_string}\""
        to_find_like = to_find_match[1:-1] + '%'

    query_params_dict = {'to_find_match': to_find_match, 'to_find_like': to_find_like, 'limit': limit}
    print(f'\n\nq3\nquery = {query}\nquery_params_dict = {query_params_dict}')
    
    cursor = run_query(query, query_params_dict)

    if cursor != ERR:

        try:
            results = cursor.fetchall()
        except Exception as err:
            print(f'\n\nq3\nerror = {str(err)}')
            return
        
        cnt = 0
        cols = (os.get_terminal_size()).columns
        print('\n\nq3 results:\n' + cols * '*')
        string_format = '{0:<90} | {1:^30} | {2:>20}'
        args = (f'Name',f'Running Time', f'Awards')
        print(string_format.format(*args) + '\n' + cols * '*')
        for res in results:
            cnt += 1
            args = (res[0], res[1], res[2])
            print(string_format.format(*args) + '\n' + cols * '-')
        print(f'\n\nq3 returned {cnt} results')


def q4(language:str) -> None:
    '''For each movie that follows the following condition:
       1. Available in <language> language
       2. Has the largest number of languages
       Prints its name and its languages

       language: string representing one of the languages from Language table
    '''
    query = """SELECT M.Name, count(*) as number_of_languages, GROUP_CONCAT(L.Name SEPARATOR ', ')
               FROM LanguageMovie as LM,
                    Language as L,
                    Movie as M
               WHERE LM.LanguageId = L.LanguageId                  AND
                     EXISTS (SELECT *
                             FROM LanguageMovie as LM2,
                                  Language as L2
                             WHERE L2.Name = %(language)s          AND
                                   L2.LanguageId = LM2.LanguageId  AND
                                   LM2.MovieId = LM.MovieId)       AND
                     M.MovieId = LM.MovieId
               GROUP BY LM.MovieId
               ORDER BY COUNT(*) DESC
               LIMIT 1;"""
    query_params_dict = {'language': language}
    print(f'\n\nq4\nquery = {query}\nquery_params_dict = {query_params_dict}')
    
    cursor = run_query(query, query_params_dict)

    if cursor != ERR:

        try:
            results = cursor.fetchall()
        except Exception as err:
            print(f'\n\nq4\nerror = {str(err)}')
            return

        cnt = 0
        cols = (os.get_terminal_size()).columns
        print('\n\nq4 results:\n' + cols * '*')
        for res in results:
            cnt += 1
            print('{0:<12} =  '.format('Name') + str(res[0]))
            print('{0:<12} =  '.format('Languages #') + str(res[1]))
            print('{0:<12} =  '.format('Languages') + str(res[2]))
        print(f'\n\nq4 returned {cnt} results')


def q5(votes:int, limit:int) -> None:
    '''For each movie that follows the following conditions:
       1. IMDB rating is above the average IMDB rating
       2. IMDB rating is based on at least <votes> votes
       3. Wasn't selected by critics (critic's pick = 0) in his review
       Prints its name, IMDB rating and number of votes
       Ordered by IMDB rating and then votes (both decsending)
       Prints at most <limit> movies with

       votes   : integer greater or equal 0
       limit   : integer greater or equal 0
    '''
    query = """SELECT M.Name,
                      IR1.RatingValue,
                      IR1.Votes
               FROM Movie as M,
                    ImdbRating as IR1,
                    (SELECT R.MovieId
                     FROM Review as R
                     WHERE R.criticsPick = 0) as NotPicked
               WHERE IR1.RatingValue >= (SELECT AVG(IR2.RatingValue)
                                         FROM ImdbRating as IR2     ) AND
                     IR1.Votes >= %(votes)s                           AND
                     IR1.ImdbId = M.ImdbRatingId                      AND
                     M.MovieId = NotPicked.MovieID
               ORDER BY IR1.RatingValue DESC, IR1.Votes DESC
               LIMIT %(limit)s;"""
    query_params_dict = {'votes': votes, 'limit': limit}
    print(f'\n\nq5\nquery = {query}\nquery_params_dict = {query_params_dict}')
    
    cursor = run_query(query, query_params_dict)

    if cursor != ERR:

        try:
            results = cursor.fetchall()
        except Exception as err:
            print(f'\n\nq5\nerror = {str(err)}')
            return

        cnt = 0
        cols = (os.get_terminal_size()).columns
        print('\n\nq5 results:\n' + cols * '*')
        string_format = '{0:<90} | {1:^30} | {2:>20}'
        args = (f'Name',f'IMDB rating', f'Votes #')
        print(string_format.format(*args) + '\n' + cols * '*')
        for res in results:
            cnt += 1
            args = (res[0], res[1], res[2])
            print(string_format.format(*args) + '\n' + cols * '-')
        print(f'\n\nq5 returned {cnt} results')


def q6(country:str) -> None:
    '''For each movie that follows the following conditions:
       1. It was filmed in <country>
       2. Its time difference between publication date and release date is equal to the minimal time difference
          from all the movies that were filmed in that country
       3. Its review was written after its release date
       Prints its name, release date, its review publication date and the time difference between them

       country   : string that represents the name of the country (must be the exact name as it appears in OMDB Data)
    '''
    query = """SELECT M2.Name,
                      R2.PublicationDate,
                      M2.ReleaseDate,
                      TIMEDIFF(R2.PublicationDate, M2.ReleaseDate) as time_diff
               FROM (SELECT CM.MovieId
                     FROM CountryMovie as CM
                     WHERE CM.CountryId = (SELECT C.CountryId
                                           FROM Country as C
                                           WHERE C.Name = %(country)s)) as MovieFromCountry,
                    (SELECT TIMEDIFF(R.PublicationDate, M.ReleaseDate) as diff
                     FROM Movie as M,
                          Review as R,
                          (SELECT CM.MovieId
                           FROM CountryMovie as CM
                           WHERE CM.CountryId = (SELECT C.CountryId
                                                 FROM Country as C
                                                 WHERE C.Name = %(country)s)) as MovieFromCountry
                     WHERE M.MovieId = MovieFromCountry.MovieId                         AND
                           M.MovieId = R.MovieId                                        AND
                           R.PublicationDate IS NOT NULL                                AND
                           M.ReleaseDate IS NOT NULL                                    AND
                           TIMEDIFF(R.PublicationDate, M.ReleaseDate) >= "00:00:00"
                     ORDER BY TIMEDIFF(R.PublicationDate, M.ReleaseDate)
                     LIMIT 1) as MinDiff,
                    Movie M2,
                    Review R2
               WHERE M2.MovieId = MovieFromCountry.MovieId                        AND
                     M2.MovieId = R2.MovieId                                      AND
                     TIMEDIFF(R2.PublicationDate, M2.ReleaseDate) = MinDiff.diff;"""
    query_params_dict = {'country': country}
    print(f'\n\nq6\nquery = {query}\nquery_params_dict = {query_params_dict}')
    
    cursor = run_query(query, query_params_dict)

    if cursor != ERR:

        try:
            results = cursor.fetchall()
        except Exception as err:
            print(f'\n\nq6\nerror = {str(err)}')
            return

        cnt = 0
        cols = (os.get_terminal_size()).columns
        print('\n\nq6 results:\n' + cols * '*')
        string_format = '{0:<90} | {1:^30} | {2:>20} | {3:>20}'
        args = ('Name','Publication Date', 'Release Date', 'Time Diff')
        print(string_format.format(*args) + '\n' + cols * '*')
        for res in results:
            cnt += 1
            args = (res[0], str(res[1]), str(res[2]), str(res[3]))
            print(string_format.format(*args) + '\n' + cols * '-')
        print(f'\n\nq6 returned {cnt} results')


def q7() -> None:
    '''For each movie that follows the following conditions:
       1. Has the biggest amount of staff members
       Prints its name and a link to its review
    '''
    query = """SELECT M.Name,
                      L.Url
               FROM Link as L,
                    Review as R,
                    Movie as M
               WHERE L.LinkId = R.LinkId    AND
                     R.MovieId = M.MovieId  AND
                     M.MovieId = (SELECT SM.MovieId
                                  FROM StaffMovie as SM
                                  GROUP BY SM.MovieId
                                  ORDER BY count(*) DESC
                                  LIMIT 1);"""
    query_params_dict = {}
    print(f'\n\nq7\nquery = {query}\n')
    
    cursor = run_query(query, query_params_dict)

    if cursor != ERR:

        try:
            res = cursor.fetchone()
        except Exception as err:
            print(f'\n\nq7\nerror = {str(err)}')
            return

        cols = (os.get_terminal_size()).columns
        print('\n\nq7 results:\n' + cols * '-')
        print(f'movie name = {res[0]}')
        print(f'url = {res[1]}')


# Running examples
q1(word='mom', limit=4)
# q2(90, 9.5, 4)
# q3(0,5,200)
# q4('English')
# q5(500000, 100)
# q6('USA')
# q7()
