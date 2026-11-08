# Courier Management System

A university group database project designed to organise courier-service operations, from customer delivery requests through parcel tracking and final delivery.

## Project overview

The project proposes a centralised database and a desktop GUI prototype to manage customers, drivers, orders, packages, payments, deliveries, tracking updates and returns.

The project report identifies common problems with manual records, spreadsheets and phone calls, including difficult record-keeping, data errors, duplicated information and limited oversight.

## Main features

- Customer and driver records
- Order and package management
- Payment records
- Delivery and driver assignment records
- Parcel tracking by status, location and update time
- Return records
- GUI prototype with add, update, delete, clear and refresh actions

## Database design

The MySQL database is named `courierManagement` and contains these tables:

1. `Customer`
2. `Driver`
3. `Orders`
4. `Package`
5. `Payment`
6. `Delivery`
7. `Tracking`
8. `Returns`

The SQL script defines primary keys and foreign-key relationships between related tables and inserts sample records for demonstration.

## Technologies

- MySQL
- Python
- `mysql-connector-python`
- Tkinter (`tkinter` and `ttk`) for the desktop interface

## Repository structure

```text
courier-management-system/
├── README.md
├── database/
│   └── courier_management.sql
├── app/
│   ├── app.py
│   └── database.py
├── docs/
│   └── PROJECT_NOTES.md
├── requirements.txt
└── .gitignore
```

## Setup

### 1. Create the database

Open MySQL Workbench or a MySQL client and run:

```sql
SOURCE database/courier_management.sql;
```

Alternatively, open the SQL file and execute its contents in MySQL Workbench.

### 2. Install Python dependency

```bash
pip install -r requirements.txt
```

### 3. Configure database connection

Set these environment variables before running the application:

- `DB_HOST` (default: `localhost`)
- `DB_USER` (default: `root`)
- `DB_PASSWORD` (your own local MySQL password)
- `DB_NAME` (default: `courierManagement`)

Do not commit passwords, API keys or other secrets to GitHub.

### 4. Run the prototype

From the repository root:

```bash
python app/app.py
```

The GUI code uses a local MySQL connection. Ensure MySQL is running and the database has been created first.

## Important project notes

- The supplied prototype imports `database`, so `app/database.py` is included to provide that connection module.
- The original connection file contained a plaintext password. It has deliberately not been copied into this public-ready package; use your own local environment variable instead.
- The GUI's login credentials are hard-coded in the supplied prototype (`admin` / `admin123`). This is only suitable as a classroom demonstration, not a secure production login. Change or remove these credentials before any real deployment.
- The project report and presentation identify this as group work. Credit all group members appropriately and confirm permission before publishing group materials.
- The report describes vehicle assignment, but the SQL schema supplied in the ZIP does not include a `Vehicle` table. This README describes the implemented schema rather than claiming a vehicle table exists.
- Test the project locally before describing it as fully operational.

## Learning outcomes

This project demonstrates relational database design, primary and foreign keys, SQL table creation and data insertion, sample data retrieval, Python-to-MySQL connectivity, and a Tkinter CRUD interface.

## References

The original report lists the following learning/reference resources:
- GeeksforGeeks SQL Tutorial: https://www.geeksforgeeks.org/sql/sql-tutorial/
- The Courier Guy: https://thecourierguy.co.za/
- GitHub courier project reference: https://github.com/vesk4000/Couriers

This is an academic project and is not affiliated with The Courier Guy.
