-- Create admin user with full privileges
CREATE USER 'appadmin'@'localhost' IDENTIFIED BY 'admin';

-- Create client user with read-only privileges
CREATE USER 'appclient'@'localhost' IDENTIFIED BY 'client';

-- Grant all privileges on the supermarketdb to the admin user
GRANT ALL PRIVILEGES ON supermarketdb.* TO 'appadmin'@'localhost';

-- Grant only SELECT privileges on the supermarketdb to the client user
GRANT SELECT ON supermarketdb.* TO 'appclient'@'localhost';

-- Ensure that the new privileges take effect immediately
FLUSH PRIVILEGES;