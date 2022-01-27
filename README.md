# TAU Database Systems Course Project (Fall 2022)

## Project Goal
Design and implement a useful and interesting web application related to movies.

## Project Objectives
<ol>
  <li>Design and create a demo movie-related web-application, with an underlying MySQL database schema,
      where the information originates from at least two sources which are accessed via an API</li>
  <li>The database should be populated with at least 10,000 records and have at least 5 tables</li>
  <li>The application should use at least 7 different SELECT queries:</li>
    <ul>
      <li>One full-text query</li>
      <li>Six complex queries (e.g. nested queries, group by, aggregations, EXISTS, etc.)</li>
    </ul>
</ol>

</br></br></br>

# Our App

## Overview
Our web application helps you choosing a movie to watch based on one of the following criterions:
<ol>
  <li>Movie’s parameters – The user will insert the properties of the movie he wants to watch and our web app will return all the movies that match them.</li>
  <li>Reviews – The user will insert some conditions on the desired movie’s reviews and the web app will return all the matched movies.</li>
</ol>

## Design

### Landing Page
![image](https://user-images.githubusercontent.com/58177619/151414433-e5f73ddf-dcd6-4cb7-83e5-1e0dd6801972.png)


### Choose based on movie parameters
First the user has to choose a query
![image](https://user-images.githubusercontent.com/58177619/151414686-35e243ed-8a85-4efb-be63-0ebd703011a5.png)

#### Plot
![image](https://user-images.githubusercontent.com/58177619/151414797-57cfb25c-4128-454e-854d-ed3d1948784b.png)

#### Rating
![image](https://user-images.githubusercontent.com/58177619/151414891-ae0a4475-405b-4dd8-8e3e-3f41bc0696cf.png)

#### Running time & awards
![image](https://user-images.githubusercontent.com/58177619/151414920-4b7f0feb-7a8b-4cef-8155-43c8834426ed.png)

#### Languages
![image](https://user-images.githubusercontent.com/58177619/151414959-a02aeb01-719c-41ba-a74e-c5cdba8e0355.png)


### Choose based on reviews
First the user has to choose a query
![image](https://user-images.githubusercontent.com/58177619/151415354-81562f47-1b99-4aab-8765-f27088f48839.png)

#### Not a critics pick but above IMDB avg
![image](https://user-images.githubusercontent.com/58177619/151415143-37765e59-f3e1-4f62-94fd-3c3990283d78.png)

#### Review’s publication date and release date
![image](https://user-images.githubusercontent.com/58177619/151415170-9005e93b-d655-4f26-8c3e-8c01d28f3914.png)

#### Link for the review with the biggest number of staff members
![image](https://user-images.githubusercontent.com/58177619/151415203-a2f988e8-d1d8-4036-add6-f1310486a034.png)




## License
[MIT](https://choosealicense.com/licenses/mit/)

