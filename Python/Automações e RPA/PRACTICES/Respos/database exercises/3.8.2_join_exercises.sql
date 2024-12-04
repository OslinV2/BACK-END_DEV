-- Objective: Understand what it means to join tables, the difference between a left and right join and how to join multiple tables to a query

-- 1. Use join_example_db
USE join_example_db;
SELECT * FROM users;
SELECT * FROM roles;

-- 2. Use JOIN, LEFT JOIN and RIGHT JOIN to combine results of the users and roles tables
-- INNER JOIN
SELECT users.id, users.name, users.email, roles.name as roles 
FROM users
JOIN roles
ON users.id=roles.id;

-- LEFT JOIN
SELECT users.id, users.name, users.email, roles.name as roles 
FROM users
LEFT JOIN roles
ON users.id=roles.id;

-- RIGHT JOIN
SELECT users.id, users.name, users.email, roles.name as roles 
FROM users
RIGHT JOIN roles
ON users.id=roles.id;

--

-- 1. Use employees database
USE employees;
 
-- 2. Write a query that shows each department along with the name of the current manager for that department
SELECT d.dept_name AS Department_Name, CONCAT(e.first_name, ' ', e.last_name) AS Department_Manager
FROM employees AS e

JOIN dept_manager AS dm
ON dm.emp_no = e.emp_no

JOIN departments AS d 
ON d.dept_no = dm.dept_no

WHERE dm.to_date = '9999-01-01' ORDER BY d.dept_name;

-- 3. Find the name of all departments currently manages by women
SELECT d.dept_name AS department_name, CONCAT(e.first_name, ' ', e.last_name) AS department_manager 
FROM employees AS e

JOIN dept_manager AS dm
ON dm.emp_no = e.emp_no

JOIN departments AS d 
ON d.dept_no = dm.dept_no

WHERE dm.to_date = '9999-01-01' AND gender = 'F' ORDER BY d.dept_name;

-- 4. Find the curent titles of employees currently working in the Customer Service department
SELECT title, COUNT(*) FROM titles

JOIN dept_emp AS de
ON de.emp_no = titles.emp_no

JOIN departments AS d
ON d.dept_no = de.dept_no

WHERE de.to_date = "9999-01-01" AND titles.to_date = "9999-01-01" AND dept_name = "customer service"
GROUP BY title;

-- 5. Find the current salary of all current manager
SELECT dept_name AS department_name, CONCAT(e.first_name, ' ', e.last_name) AS name, s.salary AS salary
FROM dept_manager AS dm

JOIN employees AS e
ON e.emp_no = dm.emp_no

JOIN salaries AS s
ON s.emp_no = dm.emp_no

JOIN departments AS d
ON d.dept_no = dm.dept_no

WHERE dm.to_date = "9999-01-01" AND s.to_date = "9999-01-01" ORDER BY dept_name ASC
;

-- 6. Find the number of employees in each department
SELECT de.dept_no, d.dept_name AS dept_name, COUNT(*) AS num_employees
FROM dept_emp AS de

JOIN departments AS d
ON d.dept_no = de.dept_no

JOIN employees AS e
ON e.emp_no = de.emp_no

WHERE de.to_date = '9999-01-01' 
GROUP BY de.dept_no, d.dept_name;

-- 7. Which department has the highest average salary?
SELECT d.dept_name AS dept_name, AVG(s.salary) AS average_salary
FROM dept_emp AS de

JOIN departments AS d
ON d.dept_no = de.dept_no

JOIN salaries AS s
ON s.emp_no = de.emp_no

WHERE de.to_date = "9999-01-01" AND s.to_date = "9999-01-01"
GROUP BY d.dept_name
ORDER BY average_salary DESC
LIMIT 1;

-- 8. Who is the highest paid employee in the Marketing department?
SELECT e.first_name AS first_name, e.last_name AS last_name
FROM employees AS e

JOIN dept_emp AS de
ON de.emp_no=e.emp_no

JOIN salaries AS s
ON s.emp_no=e.emp_no

JOIN departments AS d
ON d.dept_no=de.dept_no

WHERE d.dept_no= 'd001' AND s.to_date= '9999-01-01' AND de.to_date= '9999-01-01'
ORDER BY s.salary DESC
LIMIT 1;

-- 9. Which current department manager has the highest salary?
SELECT e.first_name AS first_name, e.last_name AS last_name, s.salary AS salary, d.dept_name AS dept_name
FROM employees AS e

JOIN dept_manager AS dm
ON dm.emp_no=e.emp_no

JOIN salaries AS s
ON s.emp_no=e.emp_no

JOIN departments AS d
ON d.dept_no=dm.dept_no

WHERE dm.to_date = '9999-01-01' AND s.to_date = '9999-01-01' 
ORDER BY s.salary DESC
LIMIT 1;

-- 10. Bonus - Find the names of all current employees, their department name, and their current manager's name
-- (Rework to show all employees)
SELECT CONCAT(e.first_name, " ", e.last_name) AS Employee_Name, d.dept_name AS Department_Name, CONCAT(e.first_name, " ", e.last_name) AS Manager_Name
FROM employees AS e

JOIN dept_emp AS de
ON de.emp_no=e.emp_no

JOIN dept_manager AS dm
ON dm.emp_no=e.emp_no

JOIN departments AS d
ON d.dept_no=dm.dept_no

WHERE de.to_date= '9999-01-01' AND dm.to_date= '9999-01-01';

-- 11. Bonus Find the highest paid employee in each department
SELECT CONCAT(e.first_name, " ", e.last_name) AS Employee_name, d.dept_name AS Department, s.salary AS Salary
FROM employees AS e

