-- drop tables if they exist to reset the database
DROP TABLE IF EXISTS order_products;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS aisles;
DROP TABLE IF EXISTS departments;

-- table for aisles
CREATE TABLE aisles (
    aisle_id INT PRIMARY KEY,
    aisle VARCHAR(255) NOT NULL
);

-- table for departments
CREATE TABLE departments (
    department_id INT PRIMARY KEY,
    department VARCHAR(255) NOT NULL
);

-- table for products
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    aisle_id INT NOT NULL,
    department_id INT NOT NULL,
    FOREIGN KEY (aisle_id) REFERENCES aisles(aisle_id) 
        ON DELETE CASCADE,
    FOREIGN KEY (department_id) REFERENCES departments(department_id) 
        ON DELETE CASCADE
);

-- table for orders
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    -- order number for a given customer. e.g., will be 1 if it's their first order, 
    -- 2 for second, etc
    customer_order_number INT NOT NULL,
    order_dow TINYINT NOT NULL CHECK (order_dow BETWEEN 0 AND 6),
    order_hour_of_day TINYINT NOT NULL CHECK (order_hour_of_day BETWEEN 0 AND 23),
    days_since_prior_order FLOAT DEFAULT NULL
);

-- table for relationship between orders and products
CREATE TABLE order_products (
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    add_to_cart_order INT NOT NULL,
    reordered TINYINT NOT NULL CHECK (reordered IN (0,1)),
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id) 
        ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id) 
        ON DELETE CASCADE
);