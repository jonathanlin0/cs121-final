-- CS 121 24wi: Password Management (A6 and Final Project)

-- (Provided) This function generates a specified number of characters for using as a
-- salt in passwords.
DELIMITER !
CREATE FUNCTION make_salt(num_chars INT)
RETURNS VARCHAR(20) DETERMINISTIC -- changed to deterministic cause of errors
BEGIN
    DECLARE salt VARCHAR(20) DEFAULT '';

    -- Don't want to generate more than 20 characters of salt.
    SET num_chars = LEAST(20, num_chars);

    -- Generate the salt!  Characters used are ASCII code 32 (space)
    -- through 126 ('z').
    WHILE num_chars > 0 DO
        SET salt = CONCAT(salt, CHAR(32 + FLOOR(RAND() * 95)));
        SET num_chars = num_chars - 1;
    END WHILE;

    RETURN salt;
END !
DELIMITER ;

-- Provided (you may modify in your FP if you choose)
-- This table holds information for authenticating users based on
-- a password.  Passwords are not stored plaintext so that they
-- cannot be used by people that shouldn't have them.
-- You may extend that table to include an is_admin or role attribute if you
-- have admin or other roles for users in your application
-- (e.g. store managers, data managers, etc.)
CREATE TABLE user_info (
    -- Usernames are up to 20 characters.
    username VARCHAR(20) PRIMARY KEY,

    -- Salt will be 8 characters all the time, so we can make this 8.
    salt CHAR(8) NOT NULL,

    -- We use SHA-2 with 256-bit hashes.  MySQL returns the hash
    -- value as a hexadecimal string, which means that each byte is
    -- represented as 2 characters.  Thus, 256 / 8 * 2 = 64.
    -- We can use BINARY or CHAR here; BINARY simply has a different
    -- definition for comparison/sorting than CHAR.
    password_hash BINARY(64) NOT NULL
);

-- [Problem 1a]
-- Adds a new user to the user_info table, using the specified password (max
-- of 20 characters). Salts the password with a newly-generated salt value,
-- and then the salt and hash values are both stored in the table.
DELIMITER !
CREATE PROCEDURE sp_add_user(new_username VARCHAR(20), password VARCHAR(20))
BEGIN
    -- Generate a new 8-character salt
    DECLARE new_salt CHAR(8);
    SET new_salt = make_salt(8);
    
    -- Insert the new user info record.
    -- The password is salted by prepending the salt and then hashed with SHA2.
    INSERT INTO user_info(username, salt, password_hash)
    VALUES(new_username, new_salt, SHA2(CONCAT(new_salt, password), 256));
END !
DELIMITER ;

-- [Problem 1b]
-- Authenticates the specified username and password against the data
-- in the user_info table.  Returns 1 if the user appears in the table, and the
-- specified password hashes to the value for the user. Otherwise returns 0.
DELIMITER !
CREATE FUNCTION authenticate(username VARCHAR(20), password VARCHAR(20))
RETURNS TINYINT DETERMINISTIC
BEGIN
    DECLARE stored_salt CHAR(8) DEFAULT NULL;
    DECLARE stored_hash BINARY(64) DEFAULT NULL;
    DECLARE auth_success TINYINT DEFAULT 0;
    
    -- If no row is found, set variables to NULL.
    DECLARE CONTINUE HANDLER FOR NOT FOUND 
        SET stored_salt = NULL, stored_hash = NULL;
    
    -- Retrieve the salt and hash for the provided username.
    SELECT salt, password_hash
        INTO stored_salt, stored_hash
        FROM user_info
        WHERE user_info.username = username
        LIMIT 1;
      
    -- If a row was found, check if the hashed (salt+password) equals the stored hash.
    IF stored_salt IS NOT NULL THEN
        IF SHA2(CONCAT(stored_salt, password), 256) = stored_hash THEN
            SET auth_success = 1;
        ELSE
            SET auth_success = 0;
        END IF;
    END IF;
    
    RETURN auth_success;
END !
DELIMITER ;

-- [Problem 1c]
-- Add at least two users into your user_info table so that when we run this file,
-- we will have examples users in the database.
CALL sp_add_user('alice', 'alicepass');
CALL sp_add_user('bob', 'bobpass');

-- [Problem 1d]
-- Create a procedure sp_change_password to generate a new salt and change the given
-- user's password to the given password (after salting and hashing)
DELIMITER !
CREATE PROCEDURE sp_change_password(IN p_username VARCHAR(20), IN p_new_password VARCHAR(20))
BEGIN
    -- Generate a new 8-character salt
    DECLARE new_salt CHAR(8);
    SET new_salt = make_salt(8);
    
    -- Update the user_info table with the new salt and hashed new password.
    UPDATE user_info
    SET salt = new_salt,
        password_hash = SHA2(CONCAT(new_salt, p_new_password), 256)
    WHERE username = p_username;
END !
DELIMITER ;