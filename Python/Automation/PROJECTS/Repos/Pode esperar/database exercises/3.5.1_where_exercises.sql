-- Objective: Use the WHERE clause

-- 1. Use employees database
USE employees;
SELECT * FROM employees;

-- 2. Find all employees with first names Irena, Vidya, or Maya
SELECT * FROM employees WHERE first_name IN ('Irena', 'Vidya', 'Maya');

-- 3. Find all employees whose last name starts with 'E'
SELECT * FROM employees WHERE last_name LIKE 'e%';

-- 4. Find all employees hired in the 90s
SELECT * FROM employees WHERE hire_date BETWEEN '1990-01-01' AND '1999-12-31';

-- 5. Find all employees born on Christmas
SELECT * FROM employees WHERE birth_date LIKE '%-12-25';

-- 6. Find all employees with a 'q' in their last name
SELECT * FROM employees WHERE last_name LIKE '%q%';

--

-- 1. Update query for Irena, Vidya, or Maya to use OR instead of IN
SELECT * FROM employees WHERE first_name = 'Irena' OR first_name='Vidya' OR first_name= 'Maya';

-- 2. Add a condtionto the previous query to find everybody with those names who is also male
SELECT * FROM employees WHERE (first_name = 'Irena' OR first_name='Vidya' OR first_name= 'Maya') AND gender='M';

-- 3. Find all employees whose last name starts or ends with 'E'
SELECT * FROM employees WHERE last_name LIKE 'e%' OR last_name LIKE '%e';

-- 4. Duplicate the previous query and update it to find all employees whose lat name starts and ends with 'E'
SELECT * FROM employees WHERE last_name LIKE 'e%e';

-- 5. Find all employees hired in the 90s and born on Christmas
SELECT * FROM employees WHERE hire_date BETWEEN '1990-01-01' AND '2000-01-01' AND birth_date LIKE '%-12-25';

-- 6. Find all employees with a 'q' in their last name but not 'qu'
SELECT * FROM employees WHERE last_name LIKE '%q%' AND last_name NOT LIKE '%qu%';