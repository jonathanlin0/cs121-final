-- --------------------------------------------------------
-- UDF: reorder_ratio
-- This function calculates the ratio of orders for a given product
-- that are marked as reorders (reordered = 1) to the total orders
-- for that product. It returns a DECIMAL(5,2) value.
-- --------------------------------------------------------

DELIMITER //

CREATE FUNCTION reorder_ratio(p_product_id INT)
RETURNS DECIMAL(5,2) DETERMINISTIC
BEGIN
  DECLARE total_orders INT DEFAULT 0;
  DECLARE reorder_count INT DEFAULT 0;
  DECLARE ratio DECIMAL(5,2) DEFAULT 0.00;
  
  -- Count total orders for the given product
  SELECT COUNT(*) INTO total_orders
  FROM products_in_order
  WHERE product_id = p_product_id;
  
  -- Count orders that are reorders for the given product
  SELECT COUNT(*) INTO reorder_count
  FROM products_in_order
  WHERE product_id = p_product_id AND reordered = 1;
  
  IF total_orders = 0 THEN
    SET ratio = 0.00;
  ELSE
    SET ratio = reorder_count / total_orders;
  END IF;
  
  RETURN ratio;
END //

DELIMITER ;

-- --------------------------------------------------------
-- Procedure: sp_create_order
-- This procedure creates a new order by inserting a record into the
-- orders table and then, based on a comma-separated list of product IDs,
-- inserts corresponding entries into the products_in_order table.
-- The add_to_cart_order is incremented in the order the product IDs appear.
-- --------------------------------------------------------

DELIMITER //

CREATE PROCEDURE sp_create_order(
  IN p_user_id INT,
  IN p_order_dow TINYINT,
  IN p_order_hour_of_day TINYINT,
  IN p_days_since_prior_order FLOAT,
  IN p_product_ids TEXT
)
BEGIN
  DECLARE new_order_id INT;
  DECLARE product_id_str VARCHAR(255);
  DECLARE comma_pos INT;
  DECLARE add_to_cart_order INT DEFAULT 1;
  
  -- Insert new order record.
  INSERT INTO orders (user_id, customer_order_number, order_dow, order_hour_of_day, days_since_prior_order)
  VALUES (p_user_id, 1, p_order_dow, p_order_hour_of_day, p_days_since_prior_order);
  
  SET new_order_id = LAST_INSERT_ID();
  
  -- Loop over the comma-separated list of product IDs.
  WHILE CHAR_LENGTH(p_product_ids) > 0 DO
    SET comma_pos = LOCATE(',', p_product_ids);
    IF comma_pos > 0 THEN
      SET product_id_str = SUBSTRING(p_product_ids, 1, comma_pos - 1);
      SET p_product_ids = SUBSTRING(p_product_ids, comma_pos + 1);
    ELSE
      SET product_id_str = p_product_ids;
      SET p_product_ids = '';
    END IF;
    
    -- Insert corresponding record into products_in_order.
    INSERT INTO products_in_order (order_id, product_id, add_to_cart_order, reordered)
    VALUES (new_order_id, CAST(product_id_str AS UNSIGNED), add_to_cart_order, 0);
    
    SET add_to_cart_order = add_to_cart_order + 1;
  END WHILE;
  
END //

DELIMITER ;

-- --------------------------------------------------------
-- Trigger: trg_update_aisle_stats
-- This row-level AFTER INSERT trigger fires on the products_in_order table.
-- For each new record inserted, it retrieves the associated aisle_id from the
-- products table and updates the materialized view (assumed to be a table named aisle_stats)
-- by incrementing the count of products sold for that aisle.
-- --------------------------------------------------------

DELIMITER //

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
