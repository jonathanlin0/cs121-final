-- Drop existing UDF, procedures, and triggers if they exist
DROP FUNCTION IF EXISTS store_efficiency;
DROP PROCEDURE IF EXISTS reassign_order_store;
DROP TRIGGER IF EXISTS trg_after_insert_products_in_order;



-- --------------------------------------------------------
-- UDF: avg_order_interval
-- This UDF calculates the supplier efficiency of a given store.
-- This is calculated by the total number of products sold
-- in a given store whose supplier is in the same city as
-- the city divided by the total number of products sold at
-- that same store
-- --------------------------------------------------------
DELIMITER !

CREATE FUNCTION store_efficiency(p_store_id SMALLINT)
RETURNS DECIMAL(5,2)
DETERMINISTIC
BEGIN
    DECLARE totalItems INT;
    DECLARE efficientItems INT;
    DECLARE storeCity VARCHAR(255);
    DECLARE efficiencyRate DECIMAL(5,2);

    -- Get the city for the given store
    SELECT city INTO storeCity
    FROM stores
    WHERE store_id = p_store_id;

    -- Count total items for orders belonging to this store
    SELECT COUNT(*) INTO totalItems
    FROM products_in_order p
    JOIN orders o ON p.order_id = o.order_id
    WHERE o.store_id = p_store_id;

    IF totalItems = 0 THEN
        SET efficiencyRate = 1.0;
    ELSE
        -- Count items where the supplier's city matches the store's city
        SELECT COUNT(*) INTO efficientItems
        FROM products_in_order p
        JOIN orders o ON p.order_id = o.order_id
        JOIN suppliers sup ON p.supplier_id = sup.supplier_id
        WHERE o.store_id = p_store_id
          AND sup.city = storeCity;

        SET efficiencyRate = efficientItems / totalItems;
    END IF;

    RETURN efficiencyRate;
END !

DELIMITER ;



-- --------------------------------------------------------
-- Procedure: reassign_order_store
-- This procedure reassigns the store for a given order.
-- --------------------------------------------------------

DELIMITER !

CREATE PROCEDURE reassign_order_store (
    IN p_order_id INT,
    IN p_new_store_id SMALLINT
)
BEGIN
    UPDATE orders
    SET store_id = p_new_store_id
    WHERE order_id = p_order_id;
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
