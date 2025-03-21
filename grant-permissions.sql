-- Drop the users if they already exist
DROP USER IF EXISTS 'appadmin'@'localhost';
DROP USER IF EXISTS 'appclient'@'localhost';

-- Create admin user with full privileges
CREATE USER 'appadmin'@'localhost' IDENTIFIED BY 'admin';

-- Create client user with read-only privileges
CREATE USER 'appclient'@'localhost' IDENTIFIED BY 'client';

-- Grant all privileges on the final to the admin user
GRANT ALL PRIVILEGES ON final.* TO 'appadmin'@'localhost';


GRANT SELECT ON final.* TO 'appclient'@'localhost';
GRANT EXECUTE ON FUNCTION final.authenticate TO 'appclient'@'localhost';
GRANT EXECUTE ON FUNCTION final.store_efficiency TO 'appclient'@'localhost';

-- Ensure that the new privileges take effect immediately
FLUSH PRIVILEGES;