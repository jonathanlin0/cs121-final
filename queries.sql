
-- ADMIN QUERIES
-- insert new order

INSERT INTO orders (user_id, order_timestamp, store_id)
VALUES (1, NOW(), 2);
SET @order_id = LAST_INSERT_ID();
CALL add_new_order(@order_id, '[1370, 1376]', '[15504, 21576]');

-- update name of product
UPDATE products
SET product_name = 'Uncle Irohs Jasmine Dragon Tea'
WHERE product_id = 3;



-- CLIENT QUERIES

-- TODO : explain queries more in detail

SELECT 
    s.store_id, 
    s.city, 
    store_efficiency(s.store_id) AS supplier_efficiency, 
    (
        SELECT COUNT(*) 
        FROM products_in_order p
        NATURAL JOIN orders o
        WHERE o.store_id = s.store_id
    ) AS num_purchased_products
FROM stores s
ORDER BY supplier_efficiency DESC, num_purchased_products DESC;


-- look at the 
SELECT product_name, COUNT(*) AS total_orders
FROM orders o
NATURAL JOIN products_in_order
NATURAL JOIN products
GROUP BY product_id
ORDER BY total_orders DESC
LIMIT 15;

-- -- Query: Insert a New Order
SELECT aisle, COUNT(*) AS order_count
FROM orders o
NATURAL JOIN products_in_order
NATURAL JOIN products
NATURAL JOIN aisles
GROUP BY aisle
ORDER BY order_count DESC
LIMIT 15;