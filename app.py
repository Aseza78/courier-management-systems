import tkinter as tk
from tkinter import ttk, messagebox
import database



# LOGIN DETAILS

USERNAME = "admin"
PASSWORD = "admin123"

username_entry = None
password_entry = None
login_window = None



# SHOW TABLE

def show_table(title, table_name, columns):

    data_window = tk.Toplevel(window)
    data_window.title(title)
    data_window.geometry("1100x650")

    heading = tk.Label(
        data_window,
        text=title,
        font=("Arial", 20, "bold")
    )
    heading.pack(pady=10)

    input_frame = tk.Frame(data_window)
    input_frame.pack(pady=5)

    entries = {}

    for index, column in enumerate(columns):

        label = tk.Label(
            input_frame,
            text=column + ":"
        )

        label.grid(
            row=index,
            column=0,
            padx=10,
            pady=3,
            sticky="e"
        )

        entry = tk.Entry(
            input_frame,
            width=35
        )

        entry.grid(
            row=index,
            column=1,
            padx=10,
            pady=3
        )

        entries[column] = entry

    
    # TABLE
    

    table_frame = tk.Frame(data_window)

    table_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

    table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    for column in columns:

        table.heading(
            column,
            text=column
        )

        table.column(
            column,
            width=150
        )

    table.pack(
        fill="both",
        expand=True
    )

    
    # LOAD DATA
    
    def load_data():

        for item in table.get_children():
            table.delete(item)

        cursor = database.connection.cursor()

        try:

            cursor.execute(
                f"SELECT * FROM {table_name}"
            )

            records = cursor.fetchall()

            for record in records:

                table.insert(
                    "",
                    "end",
                    values=record
                )

        except Exception as error:

            messagebox.showerror(
                "Database Error",
                str(error)
            )

        finally:

            cursor.close()

    
    # CLEAR FIELDS
    

    def clear_fields():

        for entry in entries.values():

            entry.delete(
                0,
                tk.END
            )

        table.selection_remove(
            table.selection()
        )


    # SELECT RECORD
    # ========================================================

    def select_record(event):

        selected = table.focus()

        if selected == "":
            return

        record = table.item(
            selected,
            "values"
        )

        clear_fields()

        for index, column in enumerate(columns):

            entries[column].insert(
                0,
                record[index]
            )

    table.bind(
        "<ButtonRelease-1>",
        select_record
    )

    # ========================================================
    # ADD RECORD
    # ========================================================

    def add_record():

        values = []

        for column in columns:

            value = entries[column].get().strip()

            if value == "":

                messagebox.showwarning(
                    "Missing Information",
                    "Please fill in all fields."
                )

                return

            values.append(value)

        cursor = database.connection.cursor()

        try:

            column_names = ", ".join(columns)

            placeholders = ", ".join(
                ["%s"] * len(columns)
            )

            query = f"""
                INSERT INTO {table_name}
                ({column_names})
                VALUES ({placeholders})
            """

            cursor.execute(
                query,
                tuple(values)
            )

            database.connection.commit()

            messagebox.showinfo(
                "Success",
                "Record added successfully."
            )

            clear_fields()
            load_data()

            update_dashboard()

        except Exception as error:

            database.connection.rollback()

            messagebox.showerror(
                "Database Error",
                str(error)
            )

        finally:

            cursor.close()

    # ========================================================
    # UPDATE RECORD
    # ========================================================

    def update_record():

        primary_key = columns[0]

        primary_key_value = entries[primary_key].get().strip()

        if primary_key_value == "":

            messagebox.showwarning(
                "No Record Selected",
                "Please click on an existing record first."
            )

            return

        values = []

        for column in columns:

            value = entries[column].get().strip()

            if value == "":

                messagebox.showwarning(
                    "Missing Information",
                    "Please fill in all fields."
                )

                return

            values.append(value)

        set_part = ", ".join(
            f"{column} = %s"
            for column in columns[1:]
        )

        query = f"""
            UPDATE {table_name}
            SET {set_part}
            WHERE {primary_key} = %s
        """

        update_values = values[1:]

        update_values.append(
            primary_key_value
        )

        cursor = database.connection.cursor()

        try:

            cursor.execute(
                query,
                tuple(update_values)
            )

            database.connection.commit()

            messagebox.showinfo(
                "Success",
                "Record updated successfully."
            )

            clear_fields()
            load_data()

            update_dashboard()

        except Exception as error:

            database.connection.rollback()

            messagebox.showerror(
                "Database Error",
                str(error)
            )

        finally:

            cursor.close()

    # ========================================================
    # DELETE RECORD
    # ========================================================

    def delete_record():

        primary_key = columns[0]

        primary_key_value = entries[primary_key].get().strip()

        if primary_key_value == "":

            messagebox.showwarning(
                "No Record Selected",
                "Please click on the record you want to delete."
            )

            return

        answer = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this record?"
        )

        if not answer:
            return

        query = f"""
            DELETE FROM {table_name}
            WHERE {primary_key} = %s
        """

        cursor = database.connection.cursor()

        try:

            cursor.execute(
                query,
                (primary_key_value,)
            )

            database.connection.commit()

            messagebox.showinfo(
                "Success",
                "Record deleted successfully."
            )

            clear_fields()
            load_data()

            update_dashboard()

        except Exception as error:

            database.connection.rollback()

            messagebox.showerror(
                "Database Error",
                str(error)
            )

        finally:

            cursor.close()

    # ========================================================
    # BUTTONS
    # ========================================================

    button_frame = tk.Frame(data_window)

    button_frame.pack(
        pady=10
    )

    tk.Button(
        button_frame,
        text="Add",
        width=15,
        command=add_record
    ).grid(
        row=0,
        column=0,
        padx=5
    )

    tk.Button(
        button_frame,
        text="Update",
        width=15,
        command=update_record
    ).grid(
        row=0,
        column=1,
        padx=5
    )

    tk.Button(
        button_frame,
        text="Delete",
        width=15,
        command=delete_record
    ).grid(
        row=0,
        column=2,
        padx=5
    )

    tk.Button(
        button_frame,
        text="Clear",
        width=15,
        command=clear_fields
    ).grid(
        row=0,
        column=3,
        padx=5
    )

    tk.Button(
        button_frame,
        text="Refresh",
        width=15,
        command=load_data
    ).grid(
        row=0,
        column=4,
        padx=5
    )

    load_data()


# ============================================================
# CUSTOMERS
# ============================================================

def show_customers():

    show_table(
        "Customers",
        "Customer",
        (
            "CustomerID",
            "FirstName",
            "LastName",
            "Phone",
            "Email"
        )
    )


# ============================================================
# DRIVERS
# ============================================================

def show_drivers():

    show_table(
        "Drivers",
        "Driver",
        (
            "DriverID",
            "FirstName",
            "LastName",
            "Phone",
            "LicenceNumber"
        )
    )


# ============================================================
# ORDERS
# ============================================================

def show_orders():

    show_table(
        "Orders",
        "Orders",
        (
            "OrderID",
            "CustomerID",
            "OrderDate",
            "OrderStatus",
            "TotalAmount",
            "PickupAddress",
            "DestinationAddress"
        )
    )


# ============================================================
# PACKAGES
# ============================================================

def show_packages():

    show_table(
        "Packages",
        "Package",
        (
            "PackageID",
            "OrderID",
            "TrackingNumber",
            "Description",
            "Weight",
            "PackageType"
        )
    )


# ============================================================
# PAYMENTS
# ============================================================

def show_payments():

    show_table(
        "Payments",
        "Payment",
        (
            "PaymentID",
            "OrderID",
            "PaymentDate",
            "Amount",
            "PaymentMethod",
            "PaymentStatus"
        )
    )


# ============================================================
# DELIVERIES
# ============================================================

def show_deliveries():

    show_table(
        "Deliveries",
        "Delivery",
        (
            "DeliveryID",
            "OrderID",
            "DriverID",
            "DeliveryDate",
            "DeliveryStatus"
        )
    )


# ============================================================
# TRACKING
# ============================================================

def show_tracking():

    show_table(
        "Tracking",
        "Tracking",
        (
            "TrackingID",
            "PackageID",
            "Status",
            "Location",
            "UpdateDateTime"
        )
    )


# ============================================================
# RETURNS
# ============================================================

def show_returns():

    show_table(
        "Returns",
        "Returns",
        (
            "ReturnID",
            "PackageID",
            "ReturnDate",
            "ReturnReason",
            "ReturnStatus"
        )
    )


# ============================================================
# REPORT WINDOW
# ============================================================

def create_report_window(title, columns, query):

    report_window = tk.Toplevel(window)

    report_window.title(title)

    report_window.geometry("1100x600")

    report_window.configure(
        bg=background_colour
    )

    heading = tk.Label(
        report_window,
        text=title,
        font=("Arial", 20, "bold"),
        bg=background_colour,
        fg=text_colour
    )

    heading.pack(
        pady=20
    )

    frame = tk.Frame(
        report_window,
        bg=card_colour,
        bd=1,
        relief="solid"
    )

    frame.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=10
    )

    table = ttk.Treeview(
        frame,
        columns=columns,
        show="headings"
    )

    for column in columns:

        table.heading(
            column,
            text=column
        )

        table.column(
            column,
            width=180
        )

    table.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=15
    )

    cursor = database.connection.cursor()

    try:

        cursor.execute(query)

        records = cursor.fetchall()

        for record in records:

            table.insert(
                "",
                "end",
                values=record
            )

    except Exception as error:

        messagebox.showerror(
            "Report Error",
            str(error)
        )

    finally:

        cursor.close()


# ============================================================
# REPORTS
# ============================================================

def show_reports():

    reports_window = tk.Toplevel(window)

    reports_window.title(
        "Reports"
    )

    reports_window.geometry(
        "700x550"
    )

    reports_window.configure(
        bg=background_colour
    )

    heading = tk.Label(
        reports_window,
        text="Reports",
        font=("Arial", 22, "bold"),
        bg=background_colour,
        fg=text_colour
    )

    heading.pack(
        pady=(30, 10)
    )

    subtitle = tk.Label(
        reports_window,
        text="Select a report to view",
        font=("Arial", 11),
        bg=background_colour,
        fg=secondary_text
    )

    subtitle.pack(
        pady=(0, 25)
    )

    # ========================================================
    # CUSTOMER REPORT
    # ========================================================

    tk.Button(
        reports_window,
        text="Customer Orders Report",
        width=30,
        height=2,
        font=("Arial", 11),
        command=lambda: create_report_window(
            "Customer Orders Report",
            (
                "CustomerID",
                "FirstName",
                "LastName",
                "OrderID",
                "OrderStatus",
                "TotalAmount"
            ),
            """
            SELECT
                Customer.CustomerID,
                Customer.FirstName,
                Customer.LastName,
                Orders.OrderID,
                Orders.OrderStatus,
                Orders.TotalAmount
            FROM Customer
            LEFT JOIN Orders
                ON Customer.CustomerID = Orders.CustomerID
            ORDER BY Customer.CustomerID
            """
        )
    ).pack(
        pady=8
    )

    # ========================================================
    # ORDER REPORT
    # ========================================================

    tk.Button(
        reports_window,
        text="Order Report",
        width=30,
        height=2,
        font=("Arial", 11),
        command=lambda: create_report_window(
            "Order Report",
            (
                "OrderID",
                "CustomerID",
                "OrderDate",
                "OrderStatus",
                "TotalAmount",
                "PickupAddress",
                "DestinationAddress"
            ),
            """
            SELECT
                OrderID,
                CustomerID,
                OrderDate,
                OrderStatus,
                TotalAmount,
                PickupAddress,
                DestinationAddress
            FROM Orders
            ORDER BY OrderDate DESC
            """
        )
    ).pack(
        pady=8
    )

    # ========================================================
    # DELIVERY REPORT
    # ========================================================

    tk.Button(
        reports_window,
        text="Delivery Report",
        width=30,
        height=2,
        font=("Arial", 11),
        command=lambda: create_report_window(
            "Delivery Report",
            (
                "DeliveryID",
                "OrderID",
                "DriverID",
                "DeliveryDate",
                "DeliveryStatus"
            ),
            """
            SELECT
                DeliveryID,
                OrderID,
                DriverID,
                DeliveryDate,
                DeliveryStatus
            FROM Delivery
            ORDER BY DeliveryDate DESC
            """
        )
    ).pack(
        pady=8
    )

    # ========================================================
    # PAYMENT REPORT
    # ========================================================

    tk.Button(
        reports_window,
        text="Payment Report",
        width=30,
        height=2,
        font=("Arial", 11),
        command=lambda: create_report_window(
            "Payment Report",
            (
                "PaymentID",
                "OrderID",
                "PaymentDate",
                "Amount",
                "PaymentMethod",
                "PaymentStatus"
            ),
            """
            SELECT
                PaymentID,
                OrderID,
                PaymentDate,
                Amount,
                PaymentMethod,
                PaymentStatus
            FROM Payment
            ORDER BY PaymentDate DESC
            """
        )
    ).pack(
        pady=8
    )


# ============================================================
# DASHBOARD DATABASE FUNCTIONS
# ============================================================

def get_count(table_name):

    cursor = database.connection.cursor()

    try:

        cursor.execute(
            f"SELECT COUNT(*) FROM {table_name}"
        )

        result = cursor.fetchone()

        return result[0]

    except Exception:

        return 0

    finally:

        cursor.close()


def get_recent_orders():

    cursor = database.connection.cursor()

    try:

        cursor.execute(
            """
            SELECT
                OrderID,
                OrderStatus,
                TotalAmount
            FROM Orders
            ORDER BY OrderDate DESC
            LIMIT 5
            """
        )

        return cursor.fetchall()

    except Exception:

        return []

    finally:

        cursor.close()


# ============================================================
# UPDATE DASHBOARD
# ============================================================

def update_dashboard():

    customer_count.config(
        text=str(
            get_count("Customer")
        )
    )

    order_count.config(
        text=str(
            get_count("Orders")
        )
    )

    package_count.config(
        text=str(
            get_count("Package")
        )
    )

    delivery_count.config(
        text=str(
            get_count("Delivery")
        )
    )

    for item in recent_orders_table.get_children():

        recent_orders_table.delete(item)

    recent_orders = get_recent_orders()

    for order in recent_orders:

        recent_orders_table.insert(
            "",
            "end",
            values=(
                order[0],
                order[1],
                f"R{order[2]}"
            )
        )


# ============================================================
# MAIN WINDOW
# ============================================================

window = tk.Tk()

window.title(
    "Courier Management System"
)

window.geometry(
    "1200x700"
)

window.minsize(
    1000,
    600
)


# ============================================================
# COLOURS
# ============================================================

background_colour = "#F4F6F8"

sidebar_colour = "#FFFFFF"

header_colour = "#FFFFFF"

card_colour = "#FFFFFF"

text_colour = "#1F2937"

secondary_text = "#6B7280"

button_colour = "#FFFFFF"


window.configure(
    bg=background_colour
)


# ============================================================
# HEADER
# ============================================================

header = tk.Frame(
    window,
    bg=header_colour,
    height=70
)

header.pack(
    side="top",
    fill="x"
)

header.pack_propagate(
    False
)


system_name = tk.Label(
    header,
    text="COURIER MANAGEMENT SYSTEM",
    font=("Arial", 20, "bold"),
    bg=header_colour,
    fg=text_colour
)

system_name.pack(
    side="left",
    padx=25
)


admin_label = tk.Label(
    header,
    text="Admin",
    font=("Arial", 12),
    bg=header_colour,
    fg=secondary_text
)

admin_label.pack(
    side="right",
    padx=30
)


# ============================================================
# BODY
# ============================================================

body = tk.Frame(
    window,
    bg=background_colour
)

body.pack(
    fill="both",
    expand=True
)


# ============================================================
# SIDEBAR
# ============================================================

sidebar = tk.Frame(
    body,
    bg=sidebar_colour,
    width=220
)

sidebar.pack(
    side="left",
    fill="y"
)

sidebar.pack_propagate(
    False
)


menu_label = tk.Label(
    sidebar,
    text="MENU",
    font=("Arial", 10, "bold"),
    bg=sidebar_colour,
    fg=secondary_text
)

menu_label.pack(
    anchor="w",
    padx=25,
    pady=(25, 10)
)


# ============================================================
# SIDEBAR BUTTON FUNCTION
# ============================================================

def create_sidebar_button(text, command):

    button = tk.Button(
        sidebar,
        text=text,
        font=("Arial", 11),
        anchor="w",
        width=22,
        height=2,
        relief="flat",
        bd=0,
        bg=button_colour,
        fg=text_colour,
        activebackground="#E9EEF5",
        activeforeground=text_colour,
        command=command,
        cursor="hand2"
    )

    button.pack(
        fill="x",
        padx=12,
        pady=2
    )

    return button


# ============================================================
# SIDEBAR BUTTONS
# ============================================================

create_sidebar_button(
    "Customers",
    show_customers
)

create_sidebar_button(
    "Drivers",
    show_drivers
)

create_sidebar_button(
    "Orders",
    show_orders
)

create_sidebar_button(
    "Packages",
    show_packages
)

create_sidebar_button(
    "Payments",
    show_payments
)

create_sidebar_button(
    "Deliveries",
    show_deliveries
)

create_sidebar_button(
    "Tracking",
    show_tracking
)

create_sidebar_button(
    "Returns",
    show_returns
)

create_sidebar_button(
    "Reports",
    show_reports
)


# ============================================================
# DASHBOARD AREA
# ============================================================

dashboard = tk.Frame(
    body,
    bg=background_colour
)

dashboard.pack(
    side="left",
    fill="both",
    expand=True,
    padx=30,
    pady=25
)


dashboard_title = tk.Label(
    dashboard,
    text="Dashboard Overview",
    font=("Arial", 22, "bold"),
    bg=background_colour,
    fg=text_colour
)

dashboard_title.pack(
    anchor="w",
    pady=(0, 20)
)


# ============================================================
# SUMMARY CARDS
# ============================================================

cards_frame = tk.Frame(
    dashboard,
    bg=background_colour
)

cards_frame.pack(
    fill="x"
)


def create_card(parent, title):

    card = tk.Frame(
        parent,
        bg=card_colour,
        bd=1,
        relief="solid",
        width=200,
        height=120
    )

    card.pack_propagate(
        False
    )

    title_label = tk.Label(
        card,
        text=title,
        font=("Arial", 11),
        bg=card_colour,
        fg=secondary_text
    )

    title_label.pack(
        anchor="w",
        padx=18,
        pady=(18, 5)
    )

    count_label = tk.Label(
        card,
        text="0",
        font=("Arial", 26, "bold"),
        bg=card_colour,
        fg=text_colour
    )

    count_label.pack(
        anchor="w",
        padx=18
    )

    return card, count_label


customer_card, customer_count = create_card(
    cards_frame,
    "Customers"
)

customer_card.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(0, 10)
)


order_card, order_count = create_card(
    cards_frame,
    "Orders"
)

order_card.pack(
    side="left",
    fill="x",
    expand=True,
    padx=10
)


package_card, package_count = create_card(
    cards_frame,
    "Packages"
)

package_card.pack(
    side="left",
    fill="x",
    expand=True,
    padx=10
)


delivery_card, delivery_count = create_card(
    cards_frame,
    "Deliveries"
)

delivery_card.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(10, 0)
)



# RECENT ORDERS


lower_frame = tk.Frame(
    dashboard,
    bg=background_colour
)

lower_frame.pack(
    fill="both",
    expand=True,
    pady=(25, 0)
)


recent_orders_card = tk.Frame(
    lower_frame,
    bg=card_colour,
    bd=1,
    relief="solid"
)

recent_orders_card.pack(
    fill="both",
    expand=True
)


recent_orders_title = tk.Label(
    recent_orders_card,
    text="Recent Orders",
    font=("Arial", 15, "bold"),
    bg=card_colour,
    fg=text_colour
)

recent_orders_title.pack(
    anchor="w",
    padx=20,
    pady=(18, 10)
)


recent_orders_table = ttk.Treeview(
    recent_orders_card,
    columns=(
        "OrderID",
        "Status",
        "Amount"
    ),
    show="headings",
    height=8
)


recent_orders_table.heading(
    "OrderID",
    text="Order ID"
)

recent_orders_table.heading(
    "Status",
    text="Status"
)

recent_orders_table.heading(
    "Amount",
    text="Amount"
)


recent_orders_table.column(
    "OrderID",
    width=150
)

recent_orders_table.column(
    "Status",
    width=200
)

recent_orders_table.column(
    "Amount",
    width=150
)


recent_orders_table.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=(0, 20)
)


# LOGIN FUNCTION


def login():

    username = username_entry.get().strip()

    password = password_entry.get()

    if username == USERNAME and password == PASSWORD:

        login_window.destroy()

        window.deiconify()

        update_dashboard()

    else:

        messagebox.showerror(
            "Login Failed",
            "Invalid username or password."
        )


# LOGIN WINDOW


login_window = tk.Toplevel(window)

login_window.title(
    "Login - Courier Management System"
)

login_window.geometry(
    "450x400"
)

login_window.resizable(
    False,
    False
)

login_window.configure(
    bg=background_colour
)


window.withdraw()


login_title = tk.Label(
    login_window,
    text="COURIER MANAGEMENT SYSTEM",
    font=("Arial", 20, "bold"),
    bg=background_colour,
    fg=text_colour
)

login_title.pack(
    pady=(50, 10)
)


login_subtitle = tk.Label(
    login_window,
    text="Administrator Login",
    font=("Arial", 12),
    bg=background_colour,
    fg=secondary_text
)

login_subtitle.pack(
    pady=(0, 30)
)


username_label = tk.Label(
    login_window,
    text="Username",
    font=("Arial", 11),
    bg=background_colour,
    fg=text_colour
)

username_label.pack(
    anchor="w",
    padx=70
)


username_entry = tk.Entry(
    login_window,
    width=35,
    font=("Arial", 11)
)

username_entry.pack(
    pady=(5, 15)
)


password_label = tk.Label(
    login_window,
    text="Password",
    font=("Arial", 11),
    bg=background_colour,
    fg=text_colour
)

password_label.pack(
    anchor="w",
    padx=70
)


password_entry = tk.Entry(
    login_window,
    width=35,
    font=("Arial", 11),
    show="*"
)

password_entry.pack(
    pady=(5, 25)
)


login_button = tk.Button(
    login_window,
    text="LOGIN",
    width=20,
    height=2,
    font=("Arial", 11, "bold"),
    bg="#1F2937",
    fg="white",
    activebackground="#374151",
    activeforeground="white",
    command=login,
    cursor="hand2"
)

login_button.pack()


password_entry.bind(
    "<Return>",
    lambda event: login()
)


# CLOSE APPLICATION


def close_application():

    window.destroy()


login_window.protocol(
    "WM_DELETE_WINDOW",
    close_application
)



# START APPLICATION


window.mainloop()