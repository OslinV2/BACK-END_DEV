-- Objective: Use SELECT statement to read data, use WHERE

-- 2. Use albums_db
USE albums_db;

-- 3. Explore sturcture of albums
DESCRIBE albums;

-- 4. Write queries to find the following information.

-- The name of all albums by Pink Floyd
SELECT * FROM albums WHERE artist='Pink Floyd';

-- The year Sgt. Pepper's Lonely Hearts Club Band was released
SELECT release_date FROM albums WHERE name = 'Sgt. Pepper\'s Lonely Hearts Club Band';

-- The genre for the album Nevermind
SELECT genre FROM albums WHERE name = 'Nevermind';

-- Which albums were released in the 1990s
SELECT * FROM albums WHERE release_date >= 1990 AND release_date < 2000;

-- Which albums had less than 20 million certified sales
SELECT * FROM albums WHERE sales < 20;

-- All the albums with a genre of 'Rock'
SELECT * FROM albums WHERE genre = 'rock';
SELECT * FROM albums WHERE genre ='Progressive rock';
SELECT * FROM albums WHERE genre = 'Hard rock';
-- Hard rock and Progressive rock are in a different category, we are searching very specifically for 'Rock'
SELECT * FROM albums WHERE genre LIKE '%rock%';