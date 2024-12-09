-- Objective: Understand how SQL tables work.

-- 3. Use employees database
use employees;

-- 4. List all tables in the daabase
show tables;

-- 5. What are the different data types present on this table?
DESCRIBE employees;
-- int, date, varchar, enum

-- 6. Which table(s) do you think contain a numeric type column?
describe salaries;

-- 7. Which table(s) contain a string type column?
describe titles;

-- 8. Which table(s) contain a data type column?
describe departments;

-- 9. What is relationship between employees and departments? 
--  The employees and departments tables create the table dept_emp, but there is no direct relationship.

-- 10. Show the SQL that created the dept_manager table.
SHOW CREATE TABLE dept_manager;