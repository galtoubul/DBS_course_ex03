import mysql.connector as SQLC


host = 'localhost'
port = '3305'
user = 'DbMysql25'
password = 'DbMysql25'
db_name = 'DbMysql25'

# connect to db
db_con = SQLC.connect(host=host, port=port, user=user,passwd=password)
cursor = db_con.cursor()

# use db
cursor.execute(f"use {db_name}")
db_con.commit()

# create Poster table
cursor.execute("""CREATE TABLE IF NOT EXISTS Poster(
                  PosterId SMALLINT UNSIGNED AUTO_INCREMENT,
                  Url VARCHAR(2083) NOT NULL,
                  PRIMARY KEY (PosterId)
    );""")
db_con.commit()

# create ImdbRating table
cursor.execute("""CREATE TABLE IF NOT EXISTS ImdbRating(
                  ImdbId VARCHAR(255),
                  Votes INT UNSIGNED NOT NULL DEFAULT 0,
                  RatingValue SMALLINT UNSIGNED,
                  PRIMARY KEY (ImdbId)
    );""")
db_con.commit()

# create Movie table
cursor.execute("""CREATE TABLE IF NOT EXISTS Movie(
                  MovieId SMALLINT UNSIGNED AUTO_INCREMENT,
                  Name VARCHAR(255) NOT NULL,
                  ReleaseDate DATE,
                  RunningTime SMALLINT UNSIGNED,
                  Rating ENUM('G','PG','PG-13','R','NC-17','TV-MA','TV-PG','TV-14','TV-Y','TV-Y7','TV-G','Approved'),
                  Plot TEXT,
                  Awards TEXT,
                  MetaScore DECIMAL(6,3) UNSIGNED,
                  BoxOffice INT UNSIGNED,
                  PosterId SMALLINT UNSIGNED,
                  ImdbRatingId VARCHAR(255),
                  FOREIGN KEY (PosterId) REFERENCES Poster(PosterId) ON DELETE CASCADE ON UPDATE CASCADE,
                  FOREIGN KEY (ImdbRatingId) REFERENCES ImdbRating(ImdbId) ON DELETE CASCADE ON UPDATE CASCADE,
                  PRIMARY KEY (MovieId),
                  FULLTEXT (Plot),
                  FULLTEXT (Awards)
    );""")
db_con.commit()

# create Rating table
cursor.execute("""CREATE TABLE IF NOT EXISTS Rating(
                  RatingId SMALLINT UNSIGNED AUTO_INCREMENT,
                  Source VARCHAR(255) NOT NULL,
                  RatingValue TINYINT UNSIGNED,
                  MovieId SMALLINT UNSIGNED,
                  FOREIGN KEY (MovieId) REFERENCES Movie(MovieId) ON DELETE CASCADE ON UPDATE CASCADE,
                  PRIMARY KEY (RatingId)
    );""")
db_con.commit()

# create Staff table
cursor.execute("""CREATE TABLE IF NOT EXISTS Staff(
                  StaffId SMALLINT UNSIGNED AUTO_INCREMENT,
                  FirstName VARCHAR(255) NOT NULL,
                  MiddleName VARCHAR(255),
                  LastName VARCHAR(255),
                  Profession ENUM('Actor', 'Director', 'Writer') NOT NULL,
                  PRIMARY KEY (StaffId)
    );""")
db_con.commit()

# create StaffMovie table
cursor.execute("""CREATE TABLE IF NOT EXISTS StaffMovie(
                  StaffId SMALLINT UNSIGNED,
                  MovieId SMALLINT UNSIGNED,
                  FOREIGN KEY (StaffId) REFERENCES Staff(StaffId) ON DELETE CASCADE ON UPDATE CASCADE,
                  FOREIGN KEY (MovieId) REFERENCES Movie(MovieId) ON DELETE CASCADE ON UPDATE CASCADE
    );""")
db_con.commit()

# create Country table
cursor.execute("""CREATE TABLE IF NOT EXISTS Country(
                  CountryId SMALLINT UNSIGNED AUTO_INCREMENT,
                  Name VARCHAR(255) NOT NULL,
                  PRIMARY KEY (CountryId)
    );""")
db_con.commit()

# create CountryMovie table
cursor.execute("""CREATE TABLE IF NOT EXISTS CountryMovie(
                  CountryId SMALLINT UNSIGNED,
                  MovieId SMALLINT UNSIGNED,
                  FOREIGN KEY (CountryId) REFERENCES Country(CountryId) ON DELETE CASCADE ON UPDATE CASCADE,
                  FOREIGN KEY (MovieId) REFERENCES Movie(MovieId) ON DELETE CASCADE ON UPDATE CASCADE
    );""")
db_con.commit()

# create Language table
cursor.execute("""CREATE TABLE IF NOT EXISTS Language(
                  LanguageId SMALLINT UNSIGNED AUTO_INCREMENT,
                  Name VARCHAR(255) NOT NULL,
                  PRIMARY KEY (LanguageId)
    );""")
db_con.commit()

# create LanguageMovie table
cursor.execute("""CREATE TABLE IF NOT EXISTS LanguageMovie(
                  LanguageId SMALLINT UNSIGNED,
                  MovieId SMALLINT UNSIGNED,
                  FOREIGN KEY (LanguageId) REFERENCES Language(LanguageId) ON DELETE CASCADE ON UPDATE CASCADE,
                  FOREIGN KEY (MovieId) REFERENCES Movie(MovieId) ON DELETE CASCADE ON UPDATE CASCADE
    );""")
db_con.commit()

# create Genre table
cursor.execute("""CREATE TABLE IF NOT EXISTS Genre(
                  GenreId SMALLINT UNSIGNED AUTO_INCREMENT,
                  Name VARCHAR(255) NOT NULL UNIQUE,
                  PRIMARY KEY (GenreId)
    );""")
db_con.commit()

# create GenreMovie table
cursor.execute("""CREATE TABLE IF NOT EXISTS GenreMovie(
                  GenreId SMALLINT UNSIGNED,
                  MovieId SMALLINT UNSIGNED,
                  FOREIGN KEY (GenreId) REFERENCES Genre(GenreId) ON DELETE CASCADE ON UPDATE CASCADE,
                  FOREIGN KEY (MovieId) REFERENCES Movie(MovieId) ON DELETE CASCADE ON UPDATE CASCADE
    );""")
db_con.commit()

# create Picture table
cursor.execute("""CREATE TABLE IF NOT EXISTS Picture(
                  PictureId SMALLINT UNSIGNED AUTO_INCREMENT,
                  Type VARCHAR(255),
                  Url VARCHAR(2083) NOT NULL,
                  Height SMALLINT UNSIGNED,
                  Width SMALLINT UNSIGNED,
                  PRIMARY KEY (PictureId)
    );""")
db_con.commit()

# create Link table
cursor.execute("""CREATE TABLE IF NOT EXISTS Link(
                  LinkId SMALLINT UNSIGNED AUTO_INCREMENT,
                  Type VARCHAR(255),
                  Url VARCHAR(2083) NOT NULL,
                  SuggestedLinkText TEXT,
                  PRIMARY KEY (LinkId)
    );""")
db_con.commit()

# create Review table
cursor.execute("""CREATE TABLE IF NOT EXISTS Review(
                  ReviewId SMALLINT UNSIGNED AUTO_INCREMENT,
                  Headline VARCHAR(511) NOT NULL,
                  CriticsPick TINYINT UNSIGNED,
                  Summary TEXT,
                  PublicationDate DATE,
                  CreationDate DATE,
                  UpdateDate DATETIME,
                  PictureId SMALLINT UNSIGNED,
                  LinkId SMALLINT UNSIGNED,
                  MovieId SMALLINT UNSIGNED,
                  FOREIGN KEY (PictureId) REFERENCES Picture(PictureId) ON DELETE CASCADE ON UPDATE CASCADE,
                  FOREIGN KEY (LinkId) REFERENCES Link(LinkId) ON DELETE CASCADE ON UPDATE CASCADE,
                  FOREIGN KEY (MovieId) REFERENCES Movie(MovieId) ON DELETE CASCADE ON UPDATE CASCADE,
                  PRIMARY KEY (ReviewId)
    );""")
db_con.commit()

cursor.close()
