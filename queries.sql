-- Query: Top 10 Popular Products
SELECT p.product_name, COUNT(*) AS total_orders
FROM orders o
JOIN order_products oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.product_id, p.product_name
ORDER BY total_orders DESC
LIMIT 10;

-- Query: Top 10 Popular Aisles
SELECT a.aisle, COUNT(*) AS order_count
FROM orders o
JOIN order_products oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
JOIN aisles a ON p.aisle_id = a.aisle_id
GROUP BY a.aisle
ORDER BY order_count DESC
LIMIT 10;


-- Query: Customer Order History
SELECT o.order_id, o.order_timestamp, p.product_name
FROM orders o
JOIN order_products oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.user_id = 7;

-- Query: Insert a New Order
INSERT INTO orders (order_id, user_id, order_timestamp, store_id) 
VALUES (12345, '7', NOW(), '2');

-- Query: Update a Product Name
UPDATE products 
SET product_name = 'Lego Monkey' 
WHERE product_id = '3423';