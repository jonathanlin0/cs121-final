-- Query: Calculate the efficiency of every store
SELECT 
    s.store_id, 
    s.city, 
    store_efficiency(s.store_id) AS supplier_efficiency, 
    (
        SELECT COUNT(*) 
        FROM products_in_order p
        JOIN orders o ON p.order_id = o.order_id
        WHERE o.store_id = s.store_id
    ) AS num_purchased_products
FROM stores s
ORDER BY supplier_efficiency DESC, num_purchased_products DESC;




-- Query: Reassign order 482516 to store 1
CALL reassign_order_store(482516, 1);


-- -- Query: Customer Order History
-- SELECT o.order_id, o.order_timestamp, p.product_name
-- FROM orders o
-- JOIN products_in_order oi ON o.order_id = oi.order_id
-- JOIN products p ON oi.product_id = p.product_id
-- WHERE o.user_id = 7;

-- -- Query: Insert a New Order
-- INSERT INTO orders (order_id, user_id, order_timestamp, store_id) 
-- VALUES (12345, '7', NOW(), '2');

-- -- Query: Update a Product Name
-- UPDATE products 
-- SET product_name = 'Lego Monkey' 
-- WHERE product_id = '3423';