-- Drop existing UDF, procedures, and triggers if they exist
DROP FUNCTION IF EXISTS avg_order_interval;
DROP PROCEDURE IF EXISTS add_product;
DROP PROCEDURE IF EXISTS sp_create_order;
DROP TRIGGER IF EXISTS trg_after_insert_products_in_order;

DELIMITER !

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
END !

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
END !

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
END !
DELIMITER ;

-- --------------------------------------------------------
-- Trigger: trg_products_in_order_after_insert
-- This row-level AFTER INSERT trigger fires on the products_in_order table.
-- For each new record inserted, it updates the respective value
-- did_reorder.
-- --------------------------------------------------------

-- Create the did_reorder table only if it doesn't already exist.
CREATE TABLE IF NOT EXISTS did_reorder (
    user_id INT,
    product_id INT,
    is_reordered TINYINT,
    PRIMARY KEY (user_id, product_id)
);


-- Drop the trigger if it exists to avoid errors during creation.
DROP TRIGGER IF EXISTS trg_after_insert_products_in_order;

DELIMITER !

CREATE TRIGGER trg_after_insert_products_in_order
AFTER INSERT ON products_in_order
FOR EACH ROW
BEGIN
    DECLARE v_user_id INT DEFAULT 0;
    DECLARE v_count INT DEFAULT 0;
    
    -- Retrieve the user_id from the orders table for the inserted order.
    SELECT user_id 
      INTO v_user_id
      FROM orders
     WHERE order_id = NEW.order_id
     LIMIT 1;
    
    -- Check if a did_reorder record already exists for this user and product.
    SELECT COUNT(*) 
      INTO v_count
      FROM did_reorder
     WHERE user_id = v_user_id 
       AND product_id = NEW.product_id;
    
    IF v_count > 0 THEN
        -- If the record exists, update is_reordered to 1.
        UPDATE did_reorder
           SET is_reordered = 1
         WHERE user_id = v_user_id 
           AND product_id = NEW.product_id;
    ELSE
        -- Otherwise, insert a new record with is_reordered set to 0.
        INSERT INTO did_reorder (user_id, product_id, is_reordered)
        VALUES (v_user_id, NEW.product_id, 0);
    END IF;
END!
 
DELIMITER ;
