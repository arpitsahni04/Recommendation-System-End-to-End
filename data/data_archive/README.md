# Data Files 

Update:
- data_v2 is uploaded. It comes from all the stream data that can be read now. It includes ~ 670,000 users and ~ 26800 movies.
- movie_id is added to movie_id_v2.csv, ratings_v2.csv, and movie_info_v2.csv as an unique numerical ID. The original movie_id is renamed as movie_code now.
- user_id_v2.csv is also saved as csv with a header for consistency.

Note:
- data_v1 is only part of the whole dataset. It includes ~ 100,000 users and ~ 23000 movies. It can be used for model development. The whole dataset will be uploaded once it is done.
- This dataset is generated from the server logs data and information API. Because the logs data is massive, we only process the rating records now. The user_id and movie_id are extracted from the rating records (not consider the watching records), so new users may appear during the testing.


# data_v2
## ratings_v2_1.csv, ratings_v2_2.csv
Description: Processed rating records from server logs. The data is saved in two files due to github file size limit.

Columns:
- Time
- user_id
- text: original text from server logs
- movie_code: movie ID in the original system, alphabetical
- rate
- movie_id: unique ID, numerical


## user_id_v2.csv
Description: User_ids that appear in the rating records.

Columns:
- user_id

## movie_id_v2.txt
Description: Movie_ids that appear in the rating records.

Columns:
- movie_code: movie ID in the original system, alphabetical
- movie_id: unique ID, numerical


## user_info_v2.csv
Description: User information fetched from http://128.2.204.215:8080/user/user_id.

Columns:
- user_id
- age
- occupation
- gender


## movie_info_v2.csv
Description: 
- Movie information fetched from http://128.2.204.215:8080/movie/movie_id.
- Several movies in the movie_id_v1.txt do not have the movie information.

Columns:
- movie_id, movie_code, tmdb_id, imdb_id, title, original_title
- adult, budget, genres, original_language, popularity
- production_countries, release_date, revenue, runtime, spoken_languages
- status, vote_average, vote_count

We extract most important information from the original response. Some columns that have multiple items, such as genres and production_countries, are processed to be saved as strings. The format is:
```
id1:name1|id2:name2
```
For example, 
```
'genres': [{'id': 28, 'name': 'Action'},{'id': 878, 'name': 'Science Fiction'}]
```
becomes
```
28:Action|878:Science Fiction
```


# data_v1
## ratings_v1.csv
Description: Processed rating records from server logs. This file will grow later.

Columns:
- Time
- user_id
- text: original text from server logs
- movie_id
- rate


## user_id_v1.txt
Description: User_ids that appear in the rating records.


## movie_id_v1.txt
Description: Movie_ids that appear in the rating records.


## user_info_v1.csv
Description: User information fetched from http://128.2.204.215:8080/user/user_id.

Columns:
- user_id
- age
- occupation
- gender


## movie_info_v1.csv
Description: 
- Movie information fetched from http://128.2.204.215:8080/movie/movie_id.
- Several movies in the movie_id_v1.txt do not have the movie information.

Columns:
- id, tmdb_id, imdb_id, title, original_title
- adult, budget, genres, original_language, popularity
- production_countries, release_date, revenue, runtime, spoken_languages
- status, vote_average, vote_count

