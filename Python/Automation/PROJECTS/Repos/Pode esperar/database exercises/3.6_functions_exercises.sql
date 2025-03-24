-- Objective: Use functions within queries

-- 1. Use employees database
USE employees;

-- 2. Update query and use CONCAT() to combine their first and last name together as a single column named 'full_name'
SELECT CONCAT(first_name,' ', last_name) AS full_name 
FROM employees 
WHERE CONCAT(first_name,' ', last_name) 
LIKE 'e%e';

-- 3. Convert names produced in last query to all uppercase
SELECT UPPER(CONCAT(first_name,' ', last_name)) AS full_name 
FROM employees 
WHERE CONCAT(first_name,' ', last_name) 
LIKE 'e%e';

-- 4. Use DATEDIFF() to find how many days they have been working at the company 
SELECT first_name, last_name, DATEDIFF(CURDATE(), hire_date) AS days_with_company 
FROM employees 
WHERE hire_date BETWEEN '1990-01-01' AND '1990-12-31' AND birth_date LIKE '%-12-25';

-- 5. Find the smallest and largest salary from the salaries table
SELECT MIN(salary) FROM salaries;
SELECT MAX(salary) FROM salaries;

-- 6. Create a username for employees, should be all lowercase, consist of the first character of the employees first name, the first four characters of the employees last name, an underscore, the month the employee was born and the last two digits of the year they were born.
SELECT LOWER(SUBSTR(CONCAT(first_name), 1, 1)) FROM employees;

SELECT LOWER(SUBSTR(CONCAT(last_name), 1, 4)) FROM employees;

SELECT LOWER(SUBSTR(CONCAT(birth_date), 6, 2)) FROM employees;

SELECT LOWER(SUBSTR(CONCAT(birth_date), 3, 2)) FROM employees;

SELECT
	LOWER(CONCAT(
			SUBSTR(first_name, 1, 1),
			SUBSTR(last_name, 1, 4),
			'_',
			SUBSTR(birth_date, 6, 2),
			SUBSTR(birth_date, 3, 2)
		)
	),
	first_name,
	last_name,
	birth_date

FROM employees;

SELECT LOWER(CONCAT(LEFT(first_name,1),LEFT(last_name,4), '_', SUBSTR(birth_date, 6, 2), SUBSTR(birth_date, 3, 2))) AS user_name FROM employees;