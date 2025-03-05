NOTE: this isn't the readme for the final project

These are just temporary notes that will be replaced by our actual readme for when we submit

load data via csv file. remove "IGNORE 1 ROWS" if no column names at top of csv file.
run this in terminal to enter: `sudo mysql --local-infile=1`
```
LOAD DATA LOCAL INFILE '[table_name].csv' INTO TABLE [table_name]
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';
```
LOAD DATA LOCAL INFILE 'is_member_of.csv' INTO TABLE is_member_of
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';

note: use python 3.10
this system was only tested on python 3.10. Functionality is not guaranteed on other systems


drop database final; create database final; use final; source setup.sql; source load-data.sql; source setup-passwords.sql; source grant-permissions.sql;