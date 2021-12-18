import mysql.connector as SQLC


host = 'mysqlsrv1.cs.tau.ac.il'
user = 'DbMysql25'
password = 'DbMysql25'
db_name = 'DbMysql25'

# connect to db
db_con = SQLC.connect(host=host,user=user,passwd=password)
cursor = db_con.cursor()

# use db
cursor.execute(f"use {db_name}")
db_con.commit()

# create Staff table
cursor.execute("""CREATE TABLE Staff(
                  StaffId int NOT NULL AUTO_INCREMENT,
                  FirstName VARCHAR(255) NOT NULL,
                  LastName VARCHAR(255) NOT NULL,
                  Profession ENUM('Actor', 'Director', 'Writer') NOT NULL,
                  PRIMARY KEY (StaffId)
    );""")
db_con.commit()

# create Country table
cursor.execute("""CREATE TABLE Country(
                  CountryId int NOT NULL AUTO_INCREMENT,
                  Name VARCHAR(255) NOT NULL,
                  PRIMARY KEY (CountryId)
    );""")
db_con.commit()

# create Poster table
cursor.execute("""CREATE TABLE Poster(
                  PosterId int NOT NULL AUTO_INCREMENT,
                  Url VARCHAR(2083) NOT NULL,
                  PRIMARY KEY (PosterId)
    );""")
db_con.commit()

# create Language table
cursor.execute("""CREATE TABLE Language(
                  LanguageId int NOT NULL AUTO_INCREMENT,
                  Name VARCHAR(255) NOT NULL,
                  PRIMARY KEY (LanguageId)
    );""")
db_con.commit()

# create Genre table
cursor.execute("""CREATE TABLE Genre(
                  GenreId int NOT NULL AUTO_INCREMENT,
                  Name VARCHAR(255) NOT NULL UNIQUE,
                  PRIMARY KEY (GenreId)
    );""")
db_con.commit()

# create Genre table
cursor.execute("""CREATE TABLE Picture(
                  PictureId int NOT NULL AUTO_INCREMENT,
                  Type TEXT,
                  Url VARCHAR(2083) NOT NULL,
                  Height int, Width
                  PRIMARY KEY (PictureId)
    );""")
db_con.commit()







# create Customer table
cursor.execute("""CREATE TABLE Customer(
    CustomerId INT(11) AUTO_INCREMENT PRIMARY KEY,
    CustomerName VARCHAR(255) NOT NULL DEFAULT 'guest');""")
db_con.commit()
 
# create Order table
cursor.execute("""CREATE TABLE Orders(
    OrderNumber VARCHAR(255),
    Url VARCHAR(2083),
    OrderName VARCHAR(255) NOT NULL DEFAULT 'unknown',
    Bucket ENUM('WishList', 'OnTheWay', 'Arrived') NOT NULL DEFAULT 'WishList',
    Price DECIMAL,
    Currency ENUM('ILS', 'USD', 'EUR'),
    OrderDate DATETIME,
    EstimatedArrivingDate DATETIME,
    Notes TEXT,
    CompanyName VARCHAR(255) REFERENCES Company(CompanyName) ON DELETE CASCADE ON UPDATE CASCADE,
    CustomerId INT(11) REFERENCES Customer(CustomerId) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (OrderNumber, CompanyName, CustomerId));""")
db_con.commit()

# create Movie table
cursor.execute("""CREATE TABLE Movie(
                  Name VARCHAR(255) NOT NULL,
                  ReleaseDate DATE,
                  Rating VARCHAR(255),
                  Plot TEXT,
                  Awards TEXT,
                  MetaScore FLOAT,
                  BoxOffice MONEY,
                  PRIMARY KEY (Name)
    );""")
db_con.commit()

cursor.close()