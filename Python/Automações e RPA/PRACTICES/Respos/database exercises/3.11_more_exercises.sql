-- Objective: Get extra practice with SQL by using newly learned skills

USE employees;

-- 1. How much do the current managers of each department get paid, relative to the average salary for the department? Is there any department where the department manager get paid less than the average salary?

-- Average salary for each department
SELECT d.dept_name AS department, AVG(s.salary) AS avg_salary
FROM dept_emp AS de

JOIN departments AS d
ON d.dept_no=de.dept_no

JOIN salaries AS s
ON s.emp_no=de.emp_no

WHERE de.to_date = "9999-01-01" AND s.to_date = "9999-01-01"
GROUP BY d.dept_no
ORDER BY dept_name;

-- Current managers salaries
SELECT CONCAT(e.first_name, " ", e.last_name) AS current_manager, d.dept_name AS dept_name, s.salary AS salary
FROM employees AS e

JOIN dept_manager AS dm
ON dm.emp_no=e.emp_no

JOIN departments AS d
ON d.dept_no=dm.dept_no

JOIN salaries AS s
ON s.emp_no=e.emp_no

WHERE s.to_date = "9999-01-01" AND dm.to_date = "9999-01-01"
ORDER BY dept_name;


USE world;

-- 1. What languages are spoken in Santa Monica?
SELECT language, percentage FROM countrylanguage AS cl

JOIN city
ON city.countrycode=cl.countrycode

WHERE city.id=4060
ORDER BY percentage ASC, language ASC;

-- 2. How many different countries are in each region?
SELECT region, COUNT(name) AS num_countries 
FROM country
GROUP BY region
ORDER BY num_countries ASC;

-- 3. What is the population for each region?
SELECT region, SUM(population) AS population FROM country
GROUP BY region
ORDER BY population DESC;

-- 4. What is the population for each continent?
SELECT continent, SUM(population) AS population 
FROM country
GROUP BY continent
ORDER BY population DESC;

-- 5. What is the average life expectancy globally?
SELECT AVG(LifeExpectancy) AS average_life_expectancy FROM country;

-- 6. What is the average life expectancy for each region, each continent? Sort the results from shortest too longest.

-- Average region life expectancy
SELECT region, AVG(LifeExpectancy) AS life_expectancy FROM country
GROUP BY region ASC
ORDER BY life_expectancy ASC;

-- Average continent life expectancy
SELECT continent, AVG(LifeExpectancy) AS life_expectancy FROM country
GROUP BY continent
ORDER BY life_expectancy ASC;

-- Bonus Find all the countries whose local name is different from the official name
SELECT name, LocalName FROM country
WHERE name != localname;

-- Bonus How many countries have a life expectancy less than Solomon Islands?
SELECT name, LifeExpectancy FROM country
WHERE name = "Solomon Islands";

SELECT COUNT(name) AS Less_LifeExpectancy FROM country
WHERE LifeExpectancy < 71.3
;

-- Bonus What state is city Tafuna located in?
SELECT district FROM city
WHERE name = "Tafuna";

-- Bonus What region of the world is city Tafuna located in?
SELECT region FROM country AS c

JOIN city 
ON city.countrycode=c.Code

WHERE c.code = "ASM" AND city.name = "Tafuna";

-- Bonus What country (use the human readable name) is city Merlo located in?
SELECT country.name FROM country

JOIN city
ON city.countrycode = country.code

WHERE country.code = "ARG" AND city.name = "Merlo";

-- Bonus What is the life expectancy in city Zwolle?
SELECT city.name, LifeExpectancy FROM country

JOIN city
ON city.countrycode = country.code

WHERE country.code = "NLD" AND city.name = "Zwolle";


USE sakila;

-- 1. Display the first and last names in all lowercase of all the actors.
SELECT LOWER(first_name) AS first_name, LOWER(last_name) AS last_name FROM actor;

-- 2. You need to find the ID number, first name, and last name of an actor, of whom you know only the first name, "Joe". What is one query you could use to obtain this information?
SELECT actor_id, first_name, last_name FROM actor
WHERE first_name = "Joe";

-- 3. Find all actors whose last name contains the letters "gen".
SELECT * FROM actor
WHERE last_name LIKE "%gen%";

-- 4. Find all actors whose last names contain the letters "li". This time, order the rows by last name and first name, in that order.
SELECT * FROM actor
WHERE last_name LIKE "%li%"
ORDER BY last_name, first_name;

-- 5. Using IN, display the country_id and country colums for the following countries: Afghanistan, Bangladesh, and China.
SELECT country_id, country FROM country
WHERE country IN ('Afghanistan', 'Bangladesh', 'China');

-- 6. List the last names of all the actors, as well as how many actors have taht last name.
SELECT last_name, COUNT(last_name) AS count FROM actor
GROUP BY last_name
ORDER BY count DESC;

-- 7. List last names of actors and the number of actors who have that last name, but only for names that are shared by at least two actors.
SELECT last_name, COUNT(last_name) AS count FROM actor 
GROUP BY last_name
HAVING COUNT(last_name) > 1
ORDER BY count DESC;

-- 8. *** You cannot locate the schema of the address table. Which query would you use to recreate it?
CREATE TABLE address

-- 9. Use JOIN to display the first and last names, as well as the address, of each staff member.
SELECT first_name, last_name, a.address FROM staff AS s

JOIN address AS a USING(address_id);

-- 10. Use JOIN to display the total amount rung up by each staff member in August of 2005.
SELECT first_name, last_name, COUNT(r.staff_id) AS total_rung_up FROM staff

JOIN rental AS r USING(staff_id)
WHERE rental_date LIKE "%2005-%-08%" 
GROUP BY staff_id;

-- 11. List each film and the number of actors who are listed for that film.
SELECT title, COUNT(actor_id) AS num_of_actors FROM film
LEFT JOIN film_actor as fa USING (film_id)
GROUP BY title
ORDER BY num_of_actors ASC;

-- 12. How many copies of the film Hunchback Impossible exist in the inventory system?
SELECT title, COUNT(title) AS count FROM film
JOIN inventory USING (film_id)
WHERE film.title = "Hunchback Impossible"
GROUP BY title;

-- 13. The music Queen and Kris Kristofferson have seen an unlikely reasurgence. As an unintended consequence, films starting with the letters K and Q have also soared in popularity. Use subqueries to display the titles of movies starting with the letters K and Q whose language is English.
SELECT title FROM film 
WHERE title LIKE 'k%' OR title LIKE 'q%' AND language_id IN (
	SELECT language_id FROM language
	WHERE name = "English");
	
-- 14. Use subqueries to display all actors who appear in the film Alone Trip.	
SELECT CONCAT(first_name, " ", last_name) AS full_name FROM actor
WHERE actor_id IN (
	SELECT actor_id FROM film_actor
	WHERE film_id IN (
		SELECT film_id FROM film
		WHERE title = "Alone Trip"
	));

-- 15. You want to run an email marketing campaign in Canada, for which you will need the names and email address of all Canadian customers. 
SELECT CONCAT(first_name, " ", last_name) AS full_name, email FROM customer

JOIN address USING (address_id) 

JOIN city USING (city_id)

JOIN country USING (country_id)

WHERE country.country = "Canada";

-- 16. Sales have been lagging among young families, and you wish to target all family movies for a promotion. Identify all movies categorized as family films.
SELECT title, c.name AS category FROM film

JOIN film_category AS fc
ON fc.film_id=film.film_id

JOIN category AS c
ON c.category_id=fc.category_id

WHERE c.name = "Family";

-- 17. Write a query to display how much business, in dollars, each store brought in.
SELECT s.store_id, SUM(p.amount) AS dollar_amount FROM store AS s
JOIN inventory AS i
ON i.store_id=s.store_id

JOIN rental AS r
ON r.inventory_id=i.inventory_id

JOIN payment AS p
ON p.rental_id=r.rental_id

GROUP BY s.store_id;

-- 18. Write a query to display for each store its store ID, city and country.
SELECT s.store_id AS store_id, c.city AS city, cr.country AS country FROM store AS s

JOIN address AS a
ON a.address_id=s.address_id

JOIN city AS c
ON c.city_id=a.city_id

JOIN country AS cr
ON cr.country_id=c.country_id;

-- 19. List the top five genres in gross revenue in descending order. 
SELECT c.name, SUM(p.amount) AS gross_revenue FROM category AS c

JOIN film_category AS fc
ON fc.category_id=c.category_id

JOIN inventory AS i
ON i.film_id=fc.film_id

JOIN rental AS r
ON r.inventory_id=i.inventory_id

JOIN payment AS p
ON p.rental_id=r.rental_id

GROUP BY c.name
ORDER BY gross_revenue DESC
LIMIT 5;


-- 1. SELECT Statements
-- A. SELECT all colums from the actor table.
SELECT * FROM actor;

-- B. SELECT only the last_name column from the actor table.
SELECT last_name FROM actor;

-- C. Select only the following _ columns from the film table.
SELECT title, description, release_year FROM film;


-- 2. DISTINCT Operator
-- A. SELECT all distinct last names from the actor table.
SELECT DISTINCT last_name FROM actor;

-- B. Select all distinct postal codes from the address table.
SELECT DISTINCT postal_code FROM address;

-- C. Select all distinct ratings from the film table.
SELECT DISTINCT rating FROM film;


-- 3. WHERE Clause
-- A. Select the title, description, rating, movie length columns from the films table that last 3 hours or longer.
SELECT title, description, rating, length FROM film
WHERE length > 180;

-- B. Select the payment id, amount, and payment date columns from the payments table for payments made on or after 05/27/2005.
SELECT payment_id, amount, payment_date FROM payment
WHERE payment_date BETWEEN "2005-05-27" AND NOW()
ORDER BY payment_date;

-- C. Select the primary key, amount, and payment date columns from the payment table for payments made on 05/27/2005.
SELECT payment_id, amount, payment_date FROM payment 
WHERE payment_date LIKE "%2005-05-27%";

-- D. Select all columns from the customer table for rows that have a last names beginning with S and a first names ending with N.
SELECT * FROM customer
WHERE last_name LIKE "s%" AND first_name LIKE "%n";

-- E. Select all columns from the customer table for rows where the customer is inactive or has a last name beginning with "M".
SELECT * FROM customer
WHERE active = 0 OR last_name LIKE "m%";

-- F. Select all columns from the category table for rows where the primary key is greater than 4 and the name field begins with either C, S or T.
SELECT * FROM category
WHERE category_id > 4 AND name LIKE 'c%' OR name LIKE 's%' OR name LIKE 't%';

-- G. Select all columns minus the password column from the staff table for rows that contain a password.
SELECT * FROM staff
WHERE password IS NOT NULL;

-- H. Select all columns minus the password column from the staff table for rows that do not contain a password.
SELECT * FROM staff
WHERE password IS NULL;


-- 4. IN Operator
-- A. Select the phone and district columns from the address table for addresses in California, England, Taipei, or West Java.
SELECT phone, district FROM address
WHERE district IN ('California', 'England', 'Taipei', 'West Java');

-- B. Select the payment id, amount, and payment date columns from the payment table for payments made on 05/25/2005, 05/27/2005, and 05/29/2005. (Use the IN operator and the DATE function, instead of the AND operator as in previous exercises.)
SELECT payment_id, amount, payment_date FROM payment
WHERE DATE(payment_date) IN ('2005-05-25', '2005-05-27', '2005-05-29');

-- C. Select all columns from the film table for films rated G, PG-13 or NC-17.
SELECT * FROM film
WHERE rating IN ('G', 'PG-13', 'NC-17');


-- 5. BETWEEN Operator
-- A. Select all columns from the payment table for payments made between midnight 05/25/2005 and 1 second before midnight 05/26/2005.
SELECT * FROM payment 
WHERE payment_date BETWEEN '2005-05-25 00:00:00' AND '2005-05-25 11:59:59';

-- B. Select the following columns from the film table for films where the length of the description is between 100 and 120. ***
SELECT * FROM film 
WHERE length BETWEEN '100' AND '120' AND rental_duration * rental_rate;


-- 6. LIKE Operator
-- A. Select the following columns from the film table for rows where the description begins with "A Thoughtful".
SELECT * FROM film
WHERE description LIKE 'A Thoughtful%';

-- B. Select the following columns from the film table for rows where the description ends with the word "Boat".
SELECT * FROM film
WHERE description LIKE '%Boat';

-- C. Select the following columns from the film table where the description contains the word "Database" and the length of the film is greater than 3 hours.
SELECT * FROM film
WHERE description LIKE '%Database%' AND length > 180;


-- 7. LIMIT Operators
-- A. Select all columns from the payment table and only include the first 20 rows.
SELECT * FROM payment
LIMIT 20;

-- B. Select the payment date and amount columns from the payment table for rows where the payment amount is greater than 5, and only select rows whose zero-based index in the result set is between 1000-2000.
SELECT payment_date, amount FROM payment
WHERE amount > 5
LIMIT 1000 OFFSET 2000;

-- C. Select all columns from the customer table, limiting results to those where the zero-based index is between 101-200
SELECT * FROM customer 
LIMIT 101 OFFSET 200;


-- 8. ORDER BY Statement
-- A. Select all columns from the film table and order rows by the length field in ascending order.
SELECT * FROM film
ORDER BY length ASC;

-- B. Select all distinct ratings from the film table ordered by rating in descending order.
SELECT DISTINCT rating FROM film
ORDER BY rating DESC;

-- C. Select the payment date and amount columns from the payment table for the first 20 payments ordered by payment amount in descending order.
SELECT payment_date, amount FROM payment
ORDER BY amount DESC
LIMIT 20;

-- D. Select the title, description, special features, length, and rental duration columns from the film table for the first 10 films with behind the scenes footage under 2 hours in length and a rental duration between 5 and 7 days, ordered by length in descending order.
SELECT title, description, special_features, length, rental_duration FROM film
WHERE rental_duration BETWEEN 5 AND 7 AND special_features = "Behind the scenes" AND length < 120
ORDER BY length DESC
LIMIT 10;


-- 9. JOINS
/* A. Select customer first_name/last_name and actor first_name/last_name columns from performing a left join between the customer and actor column on the last_name column in each table. (i.e. customer.last_name = actor.last_name)
Label customer first_name/last_name columns as customer_first_name/customer_last_name
Label actor first_name/last_name columns in a similar fashion.
returns correct number of records: 599 */
SELECT c.first_name AS customer_first_name, c.last_name AS customer_last_name, a.first_name AS actor_first_name, a.last_name AS actor_last_name FROM customer c
LEFT JOIN actor AS a USING (last_name);

/* B. Select the customer first_name/last_name and actor first_name/last_name columns from performing a /right join between the customer and actor column on the last_name column in each table. (i.e. customer.last_name = actor.last_name)
returns correct number of records: 200 */
SELECT c.first_name AS customer_first_name, c.last_name AS customer_last_name, a.first_name AS actor_first_name, a.last_name AS actor_last_name FROM customer c
RIGHT JOIN actor AS a USING (last_name);

/* C. Select the customer first_name/last_name and actor first_name/last_name columns from performing an inner join between the customer and actor column on the last_name column in each table. (i.e. customer.last_name = actor.last_name)
returns correct number of records: 43 */
SELECT c.first_name AS customer_first_name, c.last_name AS customer_last_name, a.first_name AS actor_first_name, a.last_name AS actor_last_name FROM customer c
JOIN actor AS a USING (last_name);

/* D. Select the city name and country name columns from the city table, performing a left join with the country table to get the country name column.
Returns correct records: 600 */
SELECT c.city AS city, ctr.country AS country FROM city AS c
LEFT JOIN country AS ctr USING (country_id);

/* E. Select the title, description, release year, and language name columns from the film table, performing a left join with the language table to get the "language" column.
Label the language.name column as "language"
Returns 1000 rows */
SELECT f.title, f.description, f.release_year, l.name AS language FROM film AS f
LEFT JOIN language AS l USING (language_id);

/* F. Select the first_name, last_name, address, address2, city name, district, and postal code columns from the staff table, performing 2 left joins with the address table then the city table to get the address and city related columns.
returns correct number of rows: 2 */
SELECT s.first_name, s.last_name, a.address, a.address2, c.city, a.district, a.postal_code FROM staff AS s

LEFT JOIN address AS a
USING (address_id)

LEFT JOIN city AS c
USING (city_i);

-- 

-- 1. What is the average replacement cost of a film? 
SELECT AVG(replacement_cost) FROM film;

-- Does this change depending on the rating of the film?
SELECT rating, AVG(replacement_cost) FROM film
GROUP BY rating;

-- 2. How many different films of each genre are in the database?
SELECT c.name AS name, COUNT(title) AS count FROM film

JOIN film_category AS fc USING (film_id)

JOIN category AS c USING (category_id)

GROUP BY c.name;

-- 3. What are the 5 frequently rented films?
SELECT f.title, COUNT(*) AS total FROM film AS f

JOIN inventory AS i
USING (film_id)

JOIN rental AS r
USING (inventory_id)

GROUP BY f.title
ORDER BY total DESC
LIMIT 5;

-- 4. What are the most profitable films (in terms of gross revenue)?
SELECT f.title, SUM(p.amount) AS total FROM film AS f

JOIN inventory AS i
USING (film_id)

JOIN rental AS r
USING ( inventory_id)

JOIN payment AS p
USING (rental_id)

GROUP BY f.title
ORDER BY total DESC
LIMIT 5;

-- 5. Who is the best customer?
SELECT CONCAT(c.first_name, " ", c.last_name) AS name, SUM(p.amount) AS total FROM payment AS p

JOIN rental AS r
ON r.rental_id=p.rental_id

JOIN customer AS c
ON c.customer_id=r.customer_id

GROUP BY name
ORDER BY total DESC
LIMIT 1;

-- 6. Who are the most popular actors (that have appeared in the most films)?
SELECT CONCAT(a.first_name, " ", a.last_name) AS actor_name, COUNT(*) AS total FROM actor AS a

JOIN film_actor AS fa
ON fa.actor_id=a.actor_id

JOIN film AS f
ON f.film_id=fa.film_id

GROUP BY a.actor_id
ORDER BY total DESC
LIMIT 5;

-- 7. What are the sales for each store for each month in 2005?

-- 8. Bonus Find the film title, customer name, customer phone number, and customer address for all the outstanding DVDs.