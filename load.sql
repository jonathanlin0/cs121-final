-- Load data into aisles table
LOAD DATA LOCAL INFILE 'instacart_dataset/aisles.csv' 
INTO TABLE aisles
FIELDS TERMINATED BY ',' ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS 
(aisle_id, aisle);

-- Load data into departments table
LOAD DATA LOCAL INFILE 'instacart_dataset/departments.csv' 
INTO TABLE departments
FIELDS TERMINATED BY ',' ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS 
(department_id, department);

-- Load data into products table
LOAD DATA LOCAL INFILE 'instacart_dataset/products.csv' 
INTO TABLE products
FIELDS TERMINATED BY ',' ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS 
(product_id, product_name, aisle_id, department_id);

-- Load data into orders table
LOAD DATA LOCAL INFILE 'instacart_dataset/orders.csv' 
INTO TABLE orders
FIELDS TERMINATED BY ',' ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS 
(order_id, user_id, eval_set, order_number, order_dow, order_hour_of_day, days_since_prior_order);

-- Load data into sample_submission table
LOAD DATA LOCAL INFILE 'instacart_dataset/sample_submission.csv' 
INTO TABLE sample_submission
FIELDS TERMINATED BY ',' ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS 
(order_id, products);