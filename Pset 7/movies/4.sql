SELECT COUNT(*) FROM movies
INNER JOIN ratings ON movies.id = ratings.movie_id
WHERE rating = 10.0;