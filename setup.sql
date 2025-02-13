-- Drop tables if they exist to reset the database
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS aisles;
DROP TABLE IF EXISTS departments;

-- Table for aisles
CREATE TABLE aisles (
    aisle_id INT PRIMARY KEY,
    aisle VARCHAR(255) NOT NULL
);

-- Table for departments
CREATE TABLE departments (
    department_id INT PRIMARY KEY,
    department VARCHAR(255) NOT NULL
);

-- Table for products
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    aisle_id INT NOT NULL,
    department_id INT NOT NULL,
    FOREIGN KEY (aisle_id) REFERENCES aisles(aisle_id) ON DELETE CASCADE,
    FOREIGN KEY (department_id) REFERENCES departments(department_id) ON DELETE CASCADE
);

-- Table for orders
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    eval_set ENUM('prior', 'train', 'test') NOT NULL,
    order_number INT NOT NULL,
    order_dow TINYINT NOT NULL CHECK (order_dow BETWEEN 0 AND 6),
    order_hour_of_day TINYINT NOT NULL CHECK (order_hour_of_day BETWEEN 0 AND 23),
    days_since_prior_order FLOAT DEFAULT NULL
);

-- Sample submission table for predictions (optional)
CREATE TABLE sample_submission (
    order_id INT PRIMARY KEY,
    products TEXT NOT NULL
);
