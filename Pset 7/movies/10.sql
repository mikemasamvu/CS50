SELECT DISTINCT(name) FROM people, movies, directors, ratings
WHERE people.id = directors.person_id
AND directors.movie_id = movies.id
AND movies.id = ratings.movie_id
AND directors.movie_id IN (SELECT movie_id FROM ratings WHERE rating >= 9.0);
