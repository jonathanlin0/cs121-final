load data via csv file. remove "IGNORE 1 ROWS" if no column names at top of csv file.
run this in terminal to enter: `sudo mysql --local-infile=1`
```
LOAD DATA LOCAL INFILE '[table_name].csv' INTO TABLE [table_name]
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';
```
LOAD DATA LOCAL INFILE 'is_member_of.csv' INTO TABLE is_member_of
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';

note: use python 3.10
this system was only tested on python 3.10. Unsure if it'll work on other systems