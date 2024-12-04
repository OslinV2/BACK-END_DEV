-- Objective: Understand how to use the GROUP BY clause

-- 1. Use employees database
USE employees;

-- 2. Use DISTINCT to find the unique titles in the titles table
SELECT DISTINCT title FROM titles;

-- 3. Update previous query to find just the unique last names that start and end with 'E' using GROUP BY 
SELECT last_name FROM employees WHERE last_name LIKE 'e%e'
GROUP BY last_name;

-- 4. Update previous query to now find the unique combinations of first and last name where the last name starts and ends with 'E'
SELECT first_name, last_name FROM employees WHERE last_name LIKE 'e%e' GROUP BY last_name, first_name;

-- 5. Find the unique last names with a 'q' but not 'qu'
SELECT last_name FROM employees WHERE last_name LIKE '%q%' AND last_name NOT LIKE '%qu%' GROUP BY last_name;

-- 6. Add a COUNT() to your results and use GROUP BY to make it easier to find employees whose unusual name is shared with others
SELECT last_name, COUNT(last_name) FROM employees WHERE last_name LIKE '%q%' AND last_name NOT LIKE '%qu%' GROUP BY last_name ORDER BY(last_name);

-- 7. Update a previous query and useCOUNT(*) and GROUP BY to ind the number of employees foreach gender withthose names.
SELECT COUNT(*), gender FROM employees WHERE first_name IN ('Irena', 'Vidya', 'Maya') GROUP BY gender;

-- 8. Recall the username query. Are there any duplicate usernames?
SELECT
	LOWER(CONCAT(
			SUBSTR(first_name, 1, 1),
			SUBSTR(last_name, 1, 4),
			'_',
			SUBSTR(birth_date, 6, 2),
			SUBSTR(birth_date, 3, 2)
		) 
	) AS user_name, COUNT(*)
FROM employees
GROUP BY user_name
ORDER BY COUNT(*) DESC;

