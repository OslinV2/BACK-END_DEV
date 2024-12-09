-- Objective: Run queries to see how they work and compare the output of the commands.

show databases;

-- shows all databases
select * from mysql.user;

-- mysql.user means use the mysql database and read from the user table
select user, host from mysql.user;

-- select all columns from the help_topic table on the mysql database
select * from mysql.help_topic;

-- select only the help_topic_id, help_category_id, and url columns
select help_topic_id, help_category_id, url from mysql.help_topic;