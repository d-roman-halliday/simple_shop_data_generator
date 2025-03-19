-- Create the database
CREATE DATABASE simple_shop;

-- Create users with specific privileges
CREATE USER 'simple_shop_admin'@'%'   IDENTIFIED BY 'admin_password';
CREATE USER 'simple_shop_updater'@'%' IDENTIFIED BY 'updater_password';
CREATE USER 'simple_shop_reader'@'%'  IDENTIFIED BY 'reader_password';

--CREATE USER 'simple_shop_admin'@'localhost'   IDENTIFIED BY 'admin_password';
--CREATE USER 'simple_shop_updater'@'localhost' IDENTIFIED BY 'updater_password';
--CREATE USER 'simple_shop_reader'@'localhost'  IDENTIFIED BY 'reader_password';

-- Grant admin privileges
GRANT ALL PRIVILEGES ON simple_shop.* TO 'simple_shop_admin'@'%';
--GRANT ALL PRIVILEGES ON simple_shop.* TO 'simple_shop_admin'@'localhost';

-- Grant updater privileges (modify data but no DDL changes)
GRANT SELECT, INSERT, UPDATE, DELETE ON simple_shop.* TO 'simple_shop_updater'@'%';
--GRANT SELECT, INSERT, UPDATE, DELETE ON simple_shop.* TO 'simple_shop_updater'@'localhost';

-- Grant reader privileges (read-only)
GRANT SELECT ON simple_shop.* TO 'simple_shop_reader'@'%';
--GRANT SELECT ON simple_shop.* TO 'simple_shop_reader'@'localhost';

-- Apply changes
FLUSH PRIVILEGES;

