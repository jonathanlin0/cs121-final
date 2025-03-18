-- drop tables if they exist to reset the database
DROP TABLE IF EXISTS products_in_order;
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
    FOREIGN KEY (aisle_id) REFERENCES aisles(aisle_id),
    FOREIGN KEY (department_id) REFERENCES departments(department_id) 
);

-- table for stores
CREATE TABLE stores (
    -- assume number of stores will never be above 10,000
    store_id SMALLINT PRIMARY KEY,
    -- assume that online orders are routed to the nearest store to the delivery location
    -- and counts for that store's sales.
    city VARCHAR(255) NOT NULL,
    -- 2 letter state code
    state CHAR(2) NOT NULL
);

-- table for orders
CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    order_timestamp TIMESTAMP DEFAULT NULL,
    store_id SMALLINT NOT NULL,
    FOREIGN KEY (store_id) REFERENCES stores(store_id)
);

-- table for relationship between orders and products
CREATE TABLE products_in_order (
    order_id INT,
    product_id INT,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id) 
        ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id) 
        ON DELETE CASCADE
);