-- update name of product
-- we assume the product where product_id = 3 exists.
-- the python code that utilizes this logic checks if
-- a given product_id exists for the product you want
-- to change exists before executing any sql.
-- This query is used in our RA section of reflection.pdf
UPDATE products
SET product_name = 'Uncle Irohs Jasmine Dragon Tea'
WHERE product_id = 3;


-- This function calculates the supplier efficiency for
-- all the stores and the number of products sold from
-- each store.
SELECT 
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


-- View the top performing products.
-- Similar to the next query, just using product_name.
-- This query is used in our RA section of reflection.pdf
SELECT product_name, COUNT(*) AS total_orders
FROM orders o
NATURAL JOIN products_in_order
NATURAL JOIN products
GROUP BY product_id
ORDER BY total_orders DESC
LIMIT 15;

-- View the top performing aisles.
-- Similar to the previous query, just using aisles.
-- This query is used in our RA section of reflection.pdf
SELECT aisle, COUNT(*) AS order_count
FROM orders o
NATURAL JOIN products_in_order
NATURAL JOIN products
NATURAL JOIN aisles
GROUP BY aisle
ORDER BY order_count DESC
LIMIT 10;