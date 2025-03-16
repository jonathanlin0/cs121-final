# Supermarket Data Analysis and Inventory Management System

## Overview
This application helps supermarket analysts and managers optimize inventory and track sales trends. It provides both a client-facing interface for data analysis and an admin interface for managing inventory and stock updates.

## Prerequisites
Before running the application, ensure you have the following:
- **Python 3.10** (This system was only tested on Python 3.10, and functionality is not guaranteed on other versions.)
- **MySQL Server**
- **Required Python Packages**: Install dependencies using:
  ```bash
  pip install -r requirements.txt
  ```
- **Dataset**: The data, which has been precleaned (from original Kaggle format)
  is in csv format in the data folder. No further data cleaning will be necessary


Since we are using CSV files for data import, enter MySQL with:
```bash
sudo mysql --local-infile=1
```

## Database Setup
To set up the database, run the following SQL commands in order:
```sql
drop database if exists final;
create database final;
use final;
source setup.sql;
source load-data.sql;
source setup-passwords.sql;
source grant-permissions.sql;
source setup-routines.sql
```


## Running the Application
### Admin Interface
To start the admin application, run:
```bash
python app_admin.py
```
Admin users can:
- Add new orders
- Add new products
- Delete old products

### Client Interface
To start the client application, run:
```bash
python app_client.py
```
Client users can:
- Query popular products
- Query popular aisles
- View customer order history

## Expected User Flow
1. A user (either admin or client) launches the application.
2. The system prompts for login credentials.
3. Upon successful authentication:
   - **Clients** can query supermarket sales data.
   - **Admins** can manage inventory.
4. The user selects an option from the menu and interacts accordingly.
5. The user can continue interacting or exit the system.

## Security & Permissions
- Clients have **read-only** access.
- Admins have **full control** over inventory and product modifications.
- Authentication is enforced before accessing any features.



