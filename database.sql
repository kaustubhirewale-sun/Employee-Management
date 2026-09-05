CREATE DATABASE management_db;

USE management_db;
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL
);

CREATE TABLE employees (
    id INT PRIMARY KEY AUTO_INCREMENT,
    employee_code VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    department VARCHAR(50),
    role VARCHAR(50),
    email VARCHAR(100),
    join_date VARCHAR(50),
    birth_date VARCHAR(50),
    phone VARCHAR(20)
);
DESCRIBE employees;