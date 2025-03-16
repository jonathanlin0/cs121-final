-- Load data into aisles table
LOAD DATA LOCAL INFILE 'data/aisles.csv' 
INTO TABLE aisles
FIELDS TERMINATED BY ',' ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS 
(aisle_id, aisle);

-- Load data into departments table
LOAD DATA LOCAL INFILE 'data/departments.csv' 
INTO TABLE departments
FIELDS TERMINATED BY ',' ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS 
(department_id, department);

-- Load data into products table
LOAD DATA LOCAL INFILE 'data/products.csv' 
INTO TABLE products
FIELDS TERMINATED BY ',' ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS 
(product_id, product_name, aisle_id, department_id);

-- Load data into stores table
LOAD DATA LOCAL INFILE 'data/stores.csv'
INTO TABLE stores
FIELDS TERMINATED BY ',' ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS 
(store_id, city, state);

-- Load data into orders table
LOAD DATA LOCAL INFILE 'data/orders.csv' 
INTO TABLE orders
FIELDS TERMINATED BY ',' ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS 
(order_id, user_id, @order_timestamp, store_id)
SET order_timestamp = NULLIF(@order_timestamp, '');

-- Load data into order_products table
LOAD DATA LOCAL INFILE 'data/order_products.csv' 
INTO TABLE order_products
FIELDS TERMINATED BY ',' ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS 
(order_id, product_id);