-- Objective: Understand how to get query results in batches using LIMIT

-- 1. Use employees
USE employees;

-- 2. Find all the unique last names within the company, limiting to 10
SELECT DISTINCT last_name FROM employees ORDER BY last_name DESC LIMIT 10;

-- 3. Update previous query to find just the first 5 employees
SELECT first_name, last_name FROM employees WHERE hire_date BETWEEN '1990-01-01' AND '2000-01-01' AND birth_date LIKE '%-12-25' ORDER BY birth_date ASC, hire_date DESC LIMIT 5;

-- 4. Update the query to find the 'tenth page' of results
SELECT first_name, last_name FROM employees WHERE hire_date BETWEEN '1990-01-01' AND '2000-01-01' AND birth_date LIKE '%-12-25' ORDER BY birth_date ASC, hire_date DESC LIMIT 5 OFFSET 45;
-- What is the relationship between OFFSET, LIMIT and the page number?
-- (OFFSET / LIMIT) + 1 = page number, (45 / 5) + 1 = 10 given that we were told page 10, 10 -1 = 9 * 5(LIMIT) = 45(OFFSET)