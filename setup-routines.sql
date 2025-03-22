-- Drop existing UDF, procedures, and triggers if they exist
DROP FUNCTION IF EXISTS store_efficiency;
DROP PROCEDURE IF EXISTS reassign_order_store;
DROP TRIGGER IF EXISTS trg_after_insert_products_in_order;

-- NOTE: the data is set up such that suppliers and stores
-- are only in CA. Thus, some of the code below may not
-- check for state equivalence. The new case can easily
-- be adapted for multi-state chains by adding an equivalence
-- check for states.


-- --------------------------------------------------------
-- UDF: avg_order_interval
-- This UDF calculates the supplier efficiency of a given store.
-- This is calculated by the total number of products sold
-- in a given store whose supplier is in the same city as
-- the city divided by the total number of products sold at
-- that same store.
-- If no products, then the default efficiency is 0.
-- --------------------------------------------------------
DELIMITER !

CREATE FUNCTION store_efficiency(p_store_id SMALLINT)
RETURNS DECIMAL(5,2)
DETERMINISTIC
BEGIN
    DECLARE total_items INT;
    DECLARE efficientItems INT;
    DECLARE store_city VARCHAR(255);
    DECLARE efficiency_rate DECIMAL(5,2);

    -- Get the city for the given store
    SELECT city INTO store_city
    FROM stores
    WHERE store_id = p_store_id;

    -- Count total items for orders belonging to this store
    SELECT COUNT(*) INTO total_items
    FROM products_in_order p
    NATURAL JOIN orders o
    WHERE o.store_id = p_store_id;

    IF total_items = 0 THEN
        SET efficiency_rate = 0.0;
    ELSE
        -- Count items where the supplier's city matches the store's city
        -- don't consider state since for now, we only have california cities
        -- simply add another condition for states if the chain goes national
        -- and opens markets in other states
        SELECT COUNT(*) INTO efficientItems
        FROM products_in_order p
        NATURAL JOIN orders o
        NATURAL JOIN suppliers sup
        WHERE o.store_id = p_store_id AND sup.city = store_city;

        SET efficiency_rate = efficientItems / total_items;
    END IF;

    RETURN efficiency_rate;
END !

DELIMITER ;



-- --------------------------------------------------------
-- Procedure: add_new_order
-- This procedure adds the products associated with a given
-- (new) order into the products_in_order table. 
-- --------------------------------------------------------

DELIMITER !

CREATE PROCEDURE add_new_order(
    IN p_order_id INT,
    IN p_products JSON,
    IN p_suppliers JSON
)
BEGIN
    DECLARE i INT DEFAULT 0;
    DECLARE len INT;

    SET len = JSON_LENGTH(p_products);
    
    WHILE i < len DO
        INSERT INTO products_in_order (order_id, product_id, supplier_id)
        VALUES (
            p_order_id, 
            CAST(JSON_EXTRACT(p_products, CONCAT('$[', i, ']')) AS UNSIGNED), 
            CAST(JSON_EXTRACT(p_suppliers, CONCAT('$[', i, ']')) AS UNSIGNED)
        );
        SET i = i + 1;
    END WHILE;
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

-- Populate the did_reorder table
INSERT INTO did_reorder (user_id, product_id, is_reordered)
SELECT 
    o.user_id, 
    p.product_id, 
    CASE WHEN COUNT(*) > 1 THEN 1 ELSE 0 END AS is_reordered
FROM products_in_order p
JOIN orders o 
    ON p.order_id = o.order_id
GROUP BY o.user_id, p.product_id
ORDER BY MIN(o.order_timestamp) ASC;


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
    SELECT user_id INTO v_user_id FROM orders
      WHERE order_id = NEW.order_id
      LIMIT 1;
    
    -- Check if a did_reorder record already exists for this user and product.
    SELECT COUNT(*) INTO v_count
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
