-- Objective: Understand how to use subqueries and the difference between a subquery and JOIN

USE employees;

-- 1. Find all employees with the same hire date as employee 101010 using a subquery
SELECT first_name, last_name, hire_date FROM employees
WHERE hire_date IN (
	SELECT hire_date 
	FROM employees
	WHERE emp_no='101010');

SELECT * FROM employees
WHERE emp_no = '101010';

-- 2 Find all the titles held by all employees with the first name Aamod
SELECT title, COUNT(title) FROM titles
WHERE emp_no IN (
	SELECT emp_no 
	FROM employees
	WHERE first_name="AAmod")
	GROUP BY title;
	
-- 3. How many people in the employees table are no longer working for the company?
SELECT COUNT(emp_no) AS current_employees FROM employees
WHERE emp_no IN (
	SELECT emp_no
	FROM dept_emp
	GROUP BY emp_no
	HAVING MAX(to_date) < NOW())
	;

	
-- 4. Find all the current department managers that are female
SELECT first_name, last_name FROM employees 
WHERE gender = "F" AND emp_no IN (
	SELECT emp_no
	FROM dept_manager
	WHERE to_date="9999-01-01");
	
-- 5. Find all the employees that currently have a higher than average salary
SELECT AVG(salary) FROM salaries;

SELECT first_name, last_name, salary
FROM employees AS e

JOIN salaries AS s
ON s.emp_no = e.emp_no

WHERE to_date="9999-01-01" AND salary > (
	SELECT AVG(salary) 
	FROM salaries
	);
	
-- 6. How many current salaries are within one standard deviation of the hightest salary? ***
SELECT MAX(salary) FROM salaries;

SELECT COUNT(*) AS salaries, COUNT(*)/(SELECT COUNT(*) * 100 WHERE to_date>NOW()) AS percent FROM salaries 

WHERE to_date="9999-01-01" AND salary > (
	SELECT MAX(salary) - STD(salary) 
	FROM salaries
	);


-- Bonus 1
SELECT dept_name FROM departments AS d

WHERE to_date = "9999-01-01" AND emp_no IN (
	SELECT emp_no FROM employees 
	WHERE gender = "F")