-- Objective: Understand ORDER BY clause

-- 1. Use employees database
USE employees;

-- 2. Modify query to order by first name
SELECT * FROM employees WHERE first_name IN ('Irena', 'Vidya', 'Maya') ORDER BY first_name;

-- 3. Update query to order by first name and then last name
SELECT * FROM employees WHERE first_name IN ('Irena', 'Vidya', 'Maya') ORDER BY first_name ASC, last_name ASC;

-- 4. Change the order of clause so you can order by last name then first name 
SELECT * FROM employees WHERE first_name IN ('Irena', 'Vidya', 'Maya') ORDER BY last_name ASC, first_name ASC;

-- 5. Update query for employees with 'E' in their last name to sort the results by their employee number
SELECT * FROM employees WHERE last_name LIKE 'e%' ORDER BY emp_no ASC;
SELECT * FROM employees WHERE last_name LIKE '%e' ORDER BY emp_no ASC;

-- -- 6. Now reverse the sort order for both queries
SELECT * FROM employees WHERE last_name LIKE 'e%' ORDER BY emp_no DESC;
SELECT * FROM employees WHERE first_name IN ('Irena', 'Vidya', 'Maya') ORDER BY last_name DESC, first_name DESC;

-- 7. Change query for employees hired in 90s and born on Christmas such that the first result is the oldest employee who was hired last
SELECT * FROM employees WHERE hire_date BETWEEN '1990-01-01' AND '2000-01-01' AND birth_date LIKE '%-12-25' ORDER BY birth_date ASC, hire_date DESC;
