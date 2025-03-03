-- Drop the users if they already exist
DROP USER IF EXISTS 'appadmin'@'localhost';
DROP USER IF EXISTS 'appclient'@'localhost';

-- Create admin user with full privileges
CREATE USER 'appadmin'@'localhost' IDENTIFIED BY 'admin';

-- Create client user with read-only privileges
CREATE USER 'appclient'@'localhost' IDENTIFIED BY 'client';

-- Grant all privileges on the supermarketdb to the admin user
GRANT ALL PRIVILEGES ON final.* TO 'appadmin'@'localhost';

-- Grant only SELECT privileges on the supermarketdb to the client user
GRANT SELECT ON final.* TO 'appclient'@'localhost';

-- Ensure that the new privileges take effect immediately
FLUSH PRIVILEGES;