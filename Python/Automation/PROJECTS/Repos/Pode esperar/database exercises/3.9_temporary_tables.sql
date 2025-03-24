-- Objective: Learn about temporary tables

use bayes_818;

-- 1. Recreate the employees_with_departments table
CREATE TEMPORARY TABLE employees_with_departments AS
SELECT emp_no, first_name, last_name, dept_no, dept_name
FROM employees.employees
JOIN employees.dept_emp USING(emp_no)
JOIN employees.departments USING(dept_no);

SELECT * FROM employees_with_departments;

-- A. Add a column to this table called full_name with a VARCHAR length the sum of the first_name and last_name columns
ALTER TABLE employees_with_departments ADD full_name VARCHAR(30);

SELECT * FROM employees_with_departments;

-- B. Update the table so that the full name column contains the correct data
UPDATE employees_with_departments 
SET full_name = CONCAT(first_name, " ", last_name);

SELECT * FROM employees_with_departments;

-- C. Remove the first_name and last_name columns from the table
ALTER TABLE employees_with_departments DROP COLUMN first_name;
ALTER TABLE employees_with_departments DROP COLUMN last_name;

-- D. What is another way to create the same table?

-- 2. Create a temporary table based on the payment table from sakila database
CREATE TEMPORARY TABLE pay AS
SELECT * FROM sakila.payment;

SELECT * from pay;

-- Turn the amount column from a float to an integer, ex. 1.99 into 199
ALTER TABLE pay ADD cent_amount INT UNSIGNED; 

SELECT * from pay;

UPDATE pay
SET cent_amount = pay.amount * 100;

-- ALTER TABLE pay DROP COLUMN amount

-- 3. Find out how the average pay in each department compares to the overall average pay. In order to make the comparison easier, you should use the Z-score for salaries. In terms of salary, what is the best department to work for? The worst?

CREATE TEMPORARY TABLE stdev_salary
SELECT dept_name, AVG(salary) 