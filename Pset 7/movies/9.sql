SELECT DISTINCT(name) FROM people, movies, stars
WHERE people.id = stars.person_id
AND stars.movie_id = movies.id
AND stars.movie_id IN (SELECT id FROM movies WHERE year = 2004) ORDER BY birth ASC;