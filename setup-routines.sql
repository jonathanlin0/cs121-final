-- Drop existing UDF, procedures, and triggers if they exist
DROP FUNCTION IF EXISTS avg_order_interval;
DROP PROCEDURE IF EXISTS add_product;
DROP PROCEDURE IF EXISTS sp_create_order;
DROP TRIGGER IF EXISTS trg_update_aisle_stats;

DELIMITER //

-- --------------------------------------------------------
-- UDF: avg_order_interval
-- This user-defined function calculates the average number of days 
-- between consecutive orders placed by a specific user.
-- It returns the average time interval (in days) between orders.
-- If a user has only one order, it returns 0.
-- --------------------------------------------------------

CREATE FUNCTION avg_order_interval(user_id INT) 
RETURNS INT DETERMINISTIC
BEGIN
    DECLARE avg_days INT;
    
    -- Calculate the average difference (in days) between consecutive orders
    SELECT AVG(DATEDIFF(o2.order_timestamp, o1.order_timestamp)) INTO avg_days
    FROM orders o1
    JOIN orders o2 ON o1.user_id = o2.user_id 
        AND o2.order_timestamp > o1.order_timestamp
    WHERE o1.user_id = user_id;
    
    RETURN COALESCE(avg_days, 0);
END //

-- --------------------------------------------------------
-- Procedure: add_product
-- This stored procedure adds a new product to the database.
-- If a product with the same name already exists, it does not insert a duplicate.
-- The procedure takes three parameters:
--  - product_name: The name of the product to add.
--  - aisle_id: The aisle in which the product is located.
--  - department_id: The department associated with the product.
-- --------------------------------------------------------'

CREATE PROCEDURE add_product(
    IN product_name VARCHAR(255), 
    IN aisle_id INT, 
    IN department_id INT
)
BEGIN
    -- Check if product already exists
    IF NOT EXISTS (
        SELECT 1 FROM products WHERE products.product_name = product_name
    ) THEN
        INSERT INTO products (product_name, aisle_id, department_id)
        VALUES (product_name, aisle_id, department_id);
    END IF;
END //

-- --------------------------------------------------------
-- Procedure: sp_create_order
-- This procedure creates a new order by inserting a record into the
-- orders table and then, based on a comma-separated list of product IDs,
-- inserts corresponding entries into the products_in_order table.
-- The add_to_cart_order is incremented in the order the product IDs appear.
-- --------------------------------------------------------

CREATE PROCEDURE sp_create_order(
  IN p_user_id INT,
  IN p_store_id SMALLINT,
  IN p_order_timestamp TIMESTAMP,
  IN p_product_ids TEXT
)
BEGIN
  DECLARE new_order_id INT;
  DECLARE product_id_str VARCHAR(255);
  DECLARE comma_pos INT;

  -- Insert a new order record
  INSERT INTO orders (user_id, order_timestamp, store_id)
  VALUES (p_user_id, p_order_timestamp, p_store_id);

  -- Get the ID of the newly inserted order
  SET new_order_id = LAST_INSERT_ID();
  
  -- Loop over the comma-separated list of product IDs
  WHILE CHAR_LENGTH(p_product_ids) > 0 DO
    SET comma_pos = LOCATE(',', p_product_ids);
    IF comma_pos > 0 THEN
      SET product_id_str = SUBSTRING(p_product_ids, 1, comma_pos - 1);
      SET p_product_ids = SUBSTRING(p_product_ids, comma_pos + 1);
    ELSE
      SET product_id_str = p_product_ids;
      SET p_product_ids = '';
    END IF;
    
    -- Insert product into the order
    INSERT INTO products_in_order (order_id, product_id)
    VALUES (new_order_id, CAST(product_id_str AS UNSIGNED));
    
  END WHILE;
  
  -- Return the new order ID
  SELECT new_order_id AS order_id;
END //

-- --------------------------------------------------------
-- Trigger: trg_update_aisle_stats
-- This row-level AFTER INSERT trigger fires on the products_in_order table.
-- For each new record inserted, it retrieves the associated aisle_id from the
-- products table and updates the materialized view (assumed to be a table named aisle_stats)
-- by incrementing the count of products sold for that aisle.
-- --------------------------------------------------------

--for demonstration
CREATE TABLE IF NOT EXISTS aisle_stats (
    aisle_id INT PRIMARY KEY,
    products_sold INT DEFAULT 0
);


CREATE TRIGGER trg_update_aisle_stats
AFTER INSERT ON products_in_order
FOR EACH ROW
BEGIN
  DECLARE v_aisle_id INT;
  DECLARE cnt INT;
  
  -- Get the aisle_id for the inserted product.
  SELECT aisle_id INTO v_aisle_id
  FROM products
  WHERE product_id = NEW.product_id;
  
  -- Check if the aisle already exists in aisle_stats.
  SELECT COUNT(*) INTO cnt
  FROM aisle_stats
  WHERE aisle_id = v_aisle_id;
  
  IF cnt > 0 THEN
    -- Increment the products_sold count for this aisle.
    UPDATE aisle_stats
    SET products_sold = products_sold + 1
    WHERE aisle_id = v_aisle_id;
  ELSE
    -- Insert a new record for this aisle.
    INSERT INTO aisle_stats (aisle_id, products_sold)
    VALUES (v_aisle_id, 1);
  END IF;
  
END //

DELIMITER ;
