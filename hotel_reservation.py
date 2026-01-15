import random
import mysql.connector
import getpass
from datetime import datetime, timedelta

print("\n" + "=" * 80)
print("**** HOTEL MANAGEMENT SYSTEM ****".center(80))
print("=" * 80)


class HotelManagementSystem:

    def __init__(self):
        self.connection = None
        self.cursor = None

    # ---------------- MYSQL CONNECTION ----------------
    def connect(self):
        host = "localhost"
        user = "root"
        password = getpass.getpass("Enter MySQL password: ")
        max_retries = 3
        for attempt in range(max_retries):
            try:
                self.connection = mysql.connector.connect(
                    host=host,
                    user=user,
                    password=password,
                    auth_plugin="mysql_native_password"
                )
                self.cursor = self.connection.cursor()
                try:
                    self.cursor.execute("CREATE DATABASE IF NOT EXISTS HMS")
                    self.connection.commit()
                except mysql.connector.Error as e:
                    print(f"Error creating database: {e}")
                self.connection.database = "HMS"
                try:
                    self.cursor.execute("DROP TABLE IF EXISTS ROOM_RENT")
                    self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS ROOM_RENT(
                        C_ID INT,
                        ROOM_NO INT,
                        DAYS INT,
                        RENT INT,
                        CHECK_IN_DATE DATE,
                        CHECK_OUT_DATE DATE
                    )
                    """)
                    self.cursor.execute("SHOW COLUMNS FROM ROOM_RENT LIKE 'CHECK_IN_DATE'")
                    if not self.cursor.fetchone():
                        self.cursor.execute("ALTER TABLE ROOM_RENT ADD COLUMN CHECK_IN_DATE DATE")
                    self.cursor.execute("SHOW COLUMNS FROM ROOM_RENT LIKE 'CHECK_OUT_DATE'")
                    if not self.cursor.fetchone():
                        self.cursor.execute("ALTER TABLE ROOM_RENT ADD COLUMN CHECK_OUT_DATE DATE")
                    self.connection.commit()
                except mysql.connector.Error as e:
                    print(f"Error creating/altering room rent table: {e}")
                    return
                print("Successfully connected to MySQL and HMS database.")
                return
            except mysql.connector.Error as e:
                print(f"Connection attempt {attempt+1} failed: {e}")
                if attempt < max_retries - 1:
                    print("Retrying...")
                else:
                    print("Failed to connect after retries.")
                    return

    # ---------------- CUSTOMER ----------------
    def create_customer(self):
        try:
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS C_DETAILS(
                C_ID INT PRIMARY KEY,
                NAME VARCHAR(50),
                ADDRESS VARCHAR(100),
                AGE INT,
                COUNTRY VARCHAR(30),
                PHONE VARCHAR(15),
                EMAIL VARCHAR(50)
            )
            """)
            self.cursor.execute("SHOW COLUMNS FROM C_DETAILS LIKE 'ID_TYPE'")
            if not self.cursor.fetchone():
                self.cursor.execute("ALTER TABLE C_DETAILS ADD COLUMN ID_TYPE VARCHAR(20)")
            self.cursor.execute("SHOW COLUMNS FROM C_DETAILS LIKE 'ID_NUMBER'")
            if not self.cursor.fetchone():
                self.cursor.execute("ALTER TABLE C_DETAILS ADD COLUMN ID_NUMBER VARCHAR(50)")
            self.connection.commit()
        except mysql.connector.Error as e:
            print(f"Error creating/altering table: {e}")
            return

        while True:
            cid = random.randint(1000, 9999)
            try:
                self.cursor.execute("SELECT 1 FROM C_DETAILS WHERE C_ID=%s", (cid,))
                if not self.cursor.fetchone():
                    break
            except mysql.connector.Error as e:
                print(f"Error checking C_ID uniqueness: {e}")
                return
        print(f"Generated unique Customer ID: {cid}")

        name = input("Enter customer name: ")
        address = input("Enter customer address: ")
        while True:
            try:
                age = int(input("Enter customer age: "))
                break
            except ValueError:
                print("Invalid input. Please enter a valid integer for age.")
        country = input("Enter customer country: ")
        while True:
            phone = input("Enter customer phone number: ")
            if phone.isdigit() and 10 <= len(phone) <= 15:
                break
            else:
                print("Phone number must be digits and 10-15 characters long.")
        email = input("Enter customer email: ")

        id_type = input("Enter ID type (Aadhar/Passport/Driving License): ").strip().title()
        while id_type not in ['Aadhar', 'Passport', 'Driving License']:
            print("Invalid ID type. Choose from Aadhar, Passport, Driving License.")
            id_type = input("Enter ID type (Aadhar/Passport/Driving License): ").strip().title()

        while True:
            id_number = input(f"Enter {id_type} number: ").strip()
            if not id_number:
                print("ID number cannot be empty.")
                continue
            if id_type == 'Aadhar':
                if not id_number.isdigit() or len(id_number) != 12:
                    print("Aadhar must be exactly 12 digits.")
                    continue
            elif id_type == 'Passport':
                if not id_number.isalnum() or len(id_number) < 6 or len(id_number) > 9:
                    print("Passport must be alphanumeric, 6-9 characters.")
                    continue
            elif id_type == 'Driving License':
                if not id_number.isalnum():
                    print("Driving License must be alphanumeric.")
                    continue
            break

        sql = "INSERT INTO C_DETAILS VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            self.cursor.execute(sql, (cid, name, address, age, country, phone, email, id_type, id_number))
            self.connection.commit()
            print(f"Customer '{name}' added successfully with ID {cid}!")
        except mysql.connector.Error as e:
            print(f"Error adding customer: {e}")

    def update_customer(self):
        while True:
            try:
                cid = int(input("Enter Customer ID to update: "))
                break
            except ValueError:
                print("Invalid input. Please enter a valid integer for Customer ID.")
        try:
            self.cursor.execute("SELECT * FROM C_DETAILS WHERE C_ID=%s", (cid,))
            data = self.cursor.fetchone()
        except mysql.connector.Error as e:
            print(f"Error fetching customer: {e}")
            return

        print(f"DEBUG: Fetched data length: {len(data)}")

        if not data:
            print(f"No customer found with ID {cid}")
            return

        print("Leave blank to keep current value")
        name = input(f"Enter new name [{data[1]}]: ") or data[1]
        address = input(f"Enter new address [{data[2]}]: ") or data[2]
        age_input = input(f"Enter new age [{data[3]}]: ")
        age = data[3]
        if age_input:
            while True:
                try:
                    age = int(age_input)
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid integer for age.")
                    age_input = input(f"Enter new age [{data[3]}]: ")
                    if not age_input:
                        age = data[3]
                        break
        country = input(f"Enter new country [{data[4]}]: ") or data[4]
        phone_input = input(f"Enter new phone [{data[5]}]: ")
        phone = data[5]
        if phone_input:
            while True:
                phone = phone_input
                if phone.isdigit() and 10 <= len(phone) <= 15:
                    break
                else:
                    print("Phone number must be digits and 10-15 characters long.")
                    phone_input = input(f"Enter new phone [{data[5]}]: ")
                    if not phone_input:
                        phone = data[5]
                        break
        email = input(f"Enter new email [{data[6]}]: ") or data[6]
        id_type_input = input(f"Enter new ID type [{data[7] if len(data) > 7 else 'Not set'}]: ")
        id_type = id_type_input or (data[7] if len(data) > 7 else 'Aadhar')
        if id_type_input:
            id_type = id_type.strip().title()
            while id_type not in ['Aadhar', 'Passport', 'Driving License']:
                print("Invalid ID type. Choose from Aadhar, Passport, Driving License.")
                id_type = input("Enter ID type (Aadhar/Passport/Driving License): ").strip().title()
        id_number = data[8] if len(data) > 8 else ''
        id_number_input = input(f"Enter new ID number [{data[8] if len(data) > 8 else 'Not set'}]: ")
        if id_number_input:
            while True:
                id_number = id_number_input.strip()
                if not id_number:
                    print("ID number cannot be empty.")
                    id_number_input = input(f"Enter new ID number [{data[8] if len(data) > 8 else 'Not set'}]: ")
                    if not id_number_input:
                        id_number = data[8] if len(data) > 8 else ''
                        break
                    continue
                if id_type == 'Aadhar':
                    if not id_number.isdigit() or len(id_number) != 12:
                        print("Aadhar must be exactly 12 digits.")
                        id_number_input = input(f"Enter new ID number [{data[8] if len(data) > 8 else 'Not set'}]: ")
                        if not id_number_input:
                            id_number = data[8] if len(data) > 8 else ''
                            break
                        continue
                elif id_type == 'Passport':
                    if not id_number.isalnum() or len(id_number) < 6 or len(id_number) > 9:
                        print("Passport must be alphanumeric, 6-9 characters.")
                        id_number_input = input(f"Enter new ID number [{data[8] if len(data) > 8 else 'Not set'}]: ")
                        if not id_number_input:
                            id_number = data[8] if len(data) > 8 else ''
                            break
                        continue
                elif id_type == 'Driving License':
                    if not id_number.isalnum():
                        print("Driving License must be alphanumeric.")
                        id_number_input = input(f"Enter new ID number [{data[8] if len(data) > 8 else 'Not set'}]: ")
                        if not id_number_input:
                            id_number = data[8] if len(data) > 8 else ''
                            break
                        continue
                break

        sql = """
        UPDATE C_DETAILS
        SET NAME=%s, ADDRESS=%s, AGE=%s, COUNTRY=%s, PHONE=%s, EMAIL=%s, ID_TYPE=%s, ID_NUMBER=%s
        WHERE C_ID=%s
        """
        try:
            self.cursor.execute(sql, (name, address, age, country, phone, email, id_type, id_number, cid))
            self.connection.commit()
            print(f"Customer '{name}' (ID: {cid}) updated successfully!")
        except mysql.connector.Error as e:
            print(f"Error updating customer: {e}")

    def delete_customer(self):
        while True:
            try:
                cid = int(input("Enter Customer ID to delete: "))
                break
            except ValueError:
                print("Invalid input. Please enter a valid integer for Customer ID.")
        try:
            self.cursor.execute("SELECT * FROM C_DETAILS WHERE C_ID=%s", (cid,))
            customer = self.cursor.fetchone()
            if not customer:
                print(f"No customer found with ID {cid}")
                return
        except mysql.connector.Error as e:
            print(f"Error checking customer: {e}")
            return

        print(f"DEBUG: Customer data length: {len(customer)}")

        print(f"Customer details: ID: {customer[0]}, Name: {customer[1]}, Address: {customer[2]}, Age: {customer[3]}, Country: {customer[4]}, Phone: {customer[5]}, Email: {customer[6]}, ID Type: {customer[7] if len(customer) > 7 else 'N/A'}, ID Number: {customer[8] if len(customer) > 8 else 'N/A'}")
        confirm = input("Are you sure you want to delete this customer? (yes/no): ").lower()
        if confirm == "yes":
            try:
                self.cursor.execute("DELETE FROM C_DETAILS WHERE C_ID=%s", (cid,))
                self.connection.commit()
                print(f"Customer '{customer[1]}' (ID: {cid}) deleted successfully!")
            except mysql.connector.Error as e:
                print(f"Error deleting customer: {e}")
        else:
            print("Deletion cancelled.")

    def show_customer(self):
        print("1. Show All Customers")
        print("2. Show Specific Customer")
        ch = input("Enter your choice (1 or 2): ")

        if ch == "1":
            try:
                self.cursor.execute("SELECT * FROM C_DETAILS")
                rows = self.cursor.fetchall()
                if not rows:
                    print("No customers found.")
                else:
                    print(f"DEBUG: All customers data lengths: {[len(r) for r in rows]}")
                    print("\n--- Customer List ---")
                    for r in rows:
                        print(f"ID: {r[0]}, Name: {r[1]}, Address: {r[2]}, Age: {r[3]}, Country: {r[4]}, Phone: {r[5]}, Email: {r[6]}, ID Type: {r[7] if len(r) > 7 else 'N/A'}, ID Number: {r[8] if len(r) > 8 else 'N/A'}")
                    print(f"\nTotal customers: {len(rows)}")
            except mysql.connector.Error as e:
                print(f"Error fetching customers: {e}")
        elif ch == "2":
            while True:
                try:
                    cid = int(input("Enter Customer ID: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid integer for Customer ID.")
            try:
                self.cursor.execute("SELECT * FROM C_DETAILS WHERE C_ID=%s", (cid,))
                r = self.cursor.fetchone()
                if r:
                    print(f"DEBUG: Specific customer data length: {len(r)}")
                    print("\n--- Customer Details ---")
                    print(f"ID: {r[0]}, Name: {r[1]}, Address: {r[2]}, Age: {r[3]}, Country: {r[4]}, Phone: {r[5]}, Email: {r[6]}, ID Type: {r[7] if len(r) > 7 else 'N/A'}, ID Number: {r[8] if len(r) > 8 else 'N/A'}")
                else:
                    print(f"No customer found with ID {cid}")
            except mysql.connector.Error as e:
                print(f"Error fetching customer: {e}")
        else:
            print("Invalid choice. Please select 1 or 2.")

    # ---------------- ROOMS ----------------
    def initialize_rooms(self):
        try:
            self.cursor.execute("DROP TABLE IF EXISTS ROOMS")
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS ROOMS(
                ROOM_NO INT PRIMARY KEY,
                STATUS VARCHAR(15),
                TYPE VARCHAR(10)
            )
            """)
            self.cursor.execute("SHOW COLUMNS FROM ROOMS LIKE 'TYPE'")
            if not self.cursor.fetchone():
                self.cursor.execute("ALTER TABLE ROOMS ADD COLUMN IF NOT EXISTS TYPE VARCHAR(10)")
        except mysql.connector.Error as e:
            print(f"Error creating/altering rooms table: {e}")
            return
        try:
            self.cursor.execute("DELETE FROM ROOMS")
            rooms = [(i, "AVAILABLE", "SINGLE" if i <= 2 else "DOUBLE") for i in range(1, 5)]
            self.cursor.executemany("INSERT INTO ROOMS VALUES (%s, %s, %s)", rooms)
            self.connection.commit()
        except mysql.connector.Error as e:
            print(f"Error initializing rooms: {e}")

    def book_room(self):

        while True:
            try:
                cid = int(input("Enter Customer ID for booking: "))
                if cid <= 0:
                    print("Customer ID must be a positive integer.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a valid integer for Customer ID.")
        room_type = input("Choose room type (single/double): ").upper()
        while room_type not in ['SINGLE', 'DOUBLE']:
            print("Invalid type. Choose 'single' or 'double'.")
            room_type = input("Choose room type (single/double): ").upper()

        while True:
            check_in_str = input("Enter check-in date (YYYY-MM-DD): ")
            try:
                check_in = datetime.strptime(check_in_str, '%Y-%m-%d').date()
                if check_in < datetime.now().date():
                    print("Check-in date cannot be in the past.")
                    continue
                break
            except ValueError:
                print("Invalid date format. Please enter in YYYY-MM-DD format.")

        while True:
            check_out_str = input("Enter check-out date (YYYY-MM-DD): ")
            try:
                check_out = datetime.strptime(check_out_str, '%Y-%m-%d').date()
                if check_out <= check_in:
                    print("Check-out date must be after check-in date.")
                    continue
                break
            except ValueError:
                print("Invalid date format. Please enter in YYYY-MM-DD format.")

        days = (check_out - check_in).days

        try:
            self.cursor.execute("SELECT ROOM_NO FROM ROOMS WHERE STATUS='AVAILABLE' AND TYPE=%s LIMIT 1", (room_type,))
            room = self.cursor.fetchone()
        except mysql.connector.Error as e:
            print(f"Error finding available room: {e}")
            return

        if not room:
            print(f"Sorry, no {room_type.lower()} rooms are currently available.")
            return

        room_no = room[0]
        rent = days * (2500 if room_type == 'SINGLE' else 3500)
        check_out = check_in + timedelta(days=days)

        try:
            self.cursor.execute(
                "INSERT INTO ROOM_RENT VALUES (%s,%s,%s,%s,%s,%s)",
                (cid, room_no, days, rent, check_in, check_out)
            )
            self.cursor.execute(
                "UPDATE ROOMS SET STATUS='BOOKED' WHERE ROOM_NO=%s",
                (room_no,)
            )
            self.connection.commit()
            print(f"Room {room_no} ({room_type.lower()}) booked successfully for Customer ID {cid}. Total rent: ₹{rent} for {days} days.")
        except mysql.connector.Error as e:
            print(f"Error booking room: {e}")

    # ---------------- BILL ----------------
    def total_bill(self):
        while True:
            try:
                cid = int(input("Enter Customer ID to calculate bill: "))
                break
            except ValueError:
                print("Invalid input. Please enter a valid integer for Customer ID.")

        try:
            self.cursor.execute("SELECT 1 FROM C_DETAILS WHERE C_ID=%s", (cid,))
            if not self.cursor.fetchone():
                print(f"Customer ID {cid} does not exist.")
                return
        except mysql.connector.Error as e:
            print(f"Error checking customer: {e}")
            return

        try:
            self.cursor.execute("SELECT RENT FROM ROOM_RENT WHERE C_ID=%s", (cid,))
            r = self.cursor.fetchone()
        except mysql.connector.Error as e:
            print(f"Error fetching room rent: {e}")
            r = None

        room_rent = r[0] if r else 0
        total = room_rent
        print(f"\n--- Bill Summary for Customer ID {cid} ---")
        print(f"Room Rent: ₹{room_rent}")
        if total == 0:
            print("No bills found for this customer.")
        print(f"Total Amount Due: ₹{total}")

    def admin_panel(self):
        while True:
            print("""
**** ADMIN PANEL ****
1. View all rooms
2. Update room status
3. Update room type
4. View booking logs
5. Checkout room
6. Reset all rooms to AVAILABLE
7. Add new room
8. Back to main menu
""")
            choice = input("Enter your choice (1-8): ")
            if choice not in ['1','2','3','4','5','6','7','8']:
                print("Invalid choice. Please select 1-8.")
                continue
            if choice == "1":
                try:
                    self.cursor.execute("""
                        SELECT ROOMS.ROOM_NO, ROOMS.TYPE, ROOMS.STATUS, ROOM_RENT.C_ID
                        FROM ROOMS LEFT JOIN ROOM_RENT ON ROOMS.ROOM_NO = ROOM_RENT.ROOM_NO AND ROOMS.STATUS = 'BOOKED'
                    """)
                    rooms = self.cursor.fetchall()
                    if not rooms:
                        print("No rooms found.")
                    else:
                        print("\n--- All Rooms ---")
                        print(f"{'Room No':<8} {'Type':<6} {'Status':<10} {'C_ID':<5}")
                        print("-" * 35)
                        for room in rooms:
                            c_id = room[3] if room[3] is not None else "N/A"
                            type_val = room[1] if room[1] else 'N/A'
                            status_val = room[2] if room[2] else 'N/A'
                            print(f"{room[0]:<8} {type_val:<6} {status_val:<10} {c_id:<5}")
                        print(f"\nTotal rooms: {len(rooms)}")
                except mysql.connector.Error as e:
                    print(f"Error fetching rooms: {e}")
            elif choice == "2":
                while True:
                    try:
                        room_no = int(input("Enter Room No: "))
                        break
                    except ValueError:
                        print("Invalid input. Please enter a valid integer for Room No.")
                status = input("Enter new status (AVAILABLE/BOOKED/OCCUPIED): ").upper()
                while status not in ['AVAILABLE', 'BOOKED', 'OCCUPIED']:
                    print("Invalid status. Choose from AVAILABLE, BOOKED, OCCUPIED.")
                    status = input("Enter new status (AVAILABLE/BOOKED/OCCUPIED): ").upper()
                if status == "AVAILABLE":
                    while True:
                        try:
                            cid = int(input("Enter Customer ID for checkout: "))
                            break
                        except ValueError:
                            print("Invalid input. Please enter a valid integer for Customer ID.")
                    try:
                        self.cursor.execute("SELECT * FROM ROOM_RENT WHERE C_ID=%s AND ROOM_NO=%s", (cid, room_no))
                        booking = self.cursor.fetchone()
                        if not booking:
                            print(f"No booking found for Customer ID {cid} and Room No {room_no}")
                            continue
                        print(f"Room number: {room_no}")
                        confirm = input("Confirm checkout (y/n): ").lower()
                        if confirm == "y":
                            self.cursor.execute("UPDATE ROOMS SET STATUS=%s WHERE ROOM_NO=%s", (status, room_no))
                            self.connection.commit()
                            print(f"Room {room_no} status updated to {status}")
                        else:
                            print("Checkout cancelled.")
                    except mysql.connector.Error as e:
                        if "Unknown column" in str(e):
                            print("Checkout verification failed due to database schema issues.")
                        else:
                            print(f"Error during checkout verification: {e}")
                else:
                    try:
                        self.cursor.execute("UPDATE ROOMS SET STATUS=%s WHERE ROOM_NO=%s", (status, room_no))
                        if self.cursor.rowcount == 0:
                            print(f"No room found with Room No {room_no}")
                        else:
                            self.connection.commit()
                            print(f"Room {room_no} status updated to {status}")
                    except mysql.connector.Error as e:
                        print(f"Error updating room status: {e}")
            elif choice == "3":
                # Update room type
                while True:
                    try:
                        room_no = int(input("Enter Room No: "))
                        break
                    except ValueError:
                        print("Invalid input. Please enter a valid integer for Room No.")
                new_type = input("Enter new type (SINGLE/DOUBLE): ").upper()
                while new_type not in ['SINGLE', 'DOUBLE']:
                    print("Invalid type. Choose from SINGLE or DOUBLE.")
                    new_type = input("Enter new type (SINGLE/DOUBLE): ").upper()
                try:
                    self.cursor.execute("SELECT 1 FROM ROOMS WHERE ROOM_NO=%s", (room_no,))
                    if not self.cursor.fetchone():
                        print(f"No room found with Room No {room_no}")
                    else:
                        self.cursor.execute("UPDATE ROOMS SET TYPE=%s WHERE ROOM_NO=%s", (new_type, room_no))
                        self.connection.commit()
                        print(f"Room {room_no} type updated to {new_type}")
                except mysql.connector.Error as e:
                    print(f"Error updating room type: {e}")
            elif choice == "4":
                # View booking logs
                self.cursor.execute("""
                    SELECT ROOM_RENT.C_ID, C_DETAILS.NAME, ROOMS.ROOM_NO, ROOMS.TYPE,
                           ROOM_RENT.CHECK_IN_DATE, ROOM_RENT.CHECK_OUT_DATE, ROOM_RENT.DAYS, ROOM_RENT.RENT
                    FROM ROOM_RENT
                    JOIN C_DETAILS ON ROOM_RENT.C_ID = C_DETAILS.C_ID
                    JOIN ROOMS ON ROOM_RENT.ROOM_NO = ROOMS.ROOM_NO
                    ORDER BY ROOM_RENT.CHECK_IN_DATE DESC
                """)
                logs = self.cursor.fetchall()
                if not logs:
                    print("No booking logs found.")
                else:
                    print("\n--- Booking Logs ---")
                    print(f"{'C_ID':<5} {'Customer Name':<20} {'Room No':<8} {'Type':<6} {'Check-In':<12} {'Check-Out':<12} {'Days':<5} {'Rent':<6}")
                    print("-" * 85)
                    for log in logs:
                        print(f"{log[0]:<5} {log[1]:<20} {log[2]:<8} {log[3]:<6} {str(log[4]):<12} {str(log[5]):<12} {log[6]:<5} {log[7]:<6}")
                    print(f"\nTotal logs: {len(logs)}")
            elif choice == "5":
                # Checkout room
                while True:
                    try:
                        cid = int(input("Enter Customer ID for checkout: "))
                        break
                    except ValueError:
                        print("Invalid input. Please enter a valid integer for Customer ID.")
                try:
                    self.cursor.execute("""
                        SELECT ROOM_NO FROM ROOMS
                        WHERE STATUS='BOOKED' AND ROOM_NO IN (SELECT ROOM_NO FROM ROOM_RENT WHERE C_ID=%s)
                    """, (cid,))
                    room = self.cursor.fetchone()
                    if not room:
                        print(f"No booked room found for Customer ID {cid}")
                    else:
                        room_no = room[0]
                        self.cursor.execute("UPDATE ROOMS SET STATUS='AVAILABLE' WHERE ROOM_NO=%s", (room_no,))
                        self.connection.commit()
                        print(f"Checkout successful. Room {room_no} is now available.")
                except mysql.connector.Error as e:
                    print(f"Error during checkout: {e}")
            elif choice == "6":
                try:
                    self.cursor.execute("UPDATE ROOMS SET STATUS='AVAILABLE'")
                    self.connection.commit()
                    print("All rooms have been reset to AVAILABLE status.")
                except mysql.connector.Error as e:
                    print(f"Error resetting rooms: {e}")
            elif choice == "7":
                room_type = input("Enter room type (single/double): ").upper()
                while room_type not in ['SINGLE', 'DOUBLE']:
                    print("Invalid type. Choose from 'single' or 'double'.")
                    room_type = input("Enter room type (single/double): ").upper()
                try:
                    self.cursor.execute("SELECT MAX(ROOM_NO) FROM ROOMS")
                    max_room = self.cursor.fetchone()[0]
                    next_room_no = max_room + 1 if max_room else 1
                    self.cursor.execute("INSERT INTO ROOMS (ROOM_NO, STATUS, TYPE) VALUES (%s, %s, %s)", (next_room_no, 'AVAILABLE', room_type))
                    self.connection.commit()
                    print(f"New room {next_room_no} ({room_type.lower()}) added successfully.")
                except mysql.connector.Error as e:
                    print(f"Error adding new room: {e}")
            elif choice == "8":
                break

    def close(self):
        try:
            self.cursor.close()
        except mysql.connector.Error as e:
            print(f"Error closing cursor: {e}")
        try:
            self.connection.close()
        except mysql.connector.Error as e:
            print(f"Error closing connection: {e}")
        print("Connection closed")


# ---------------- MAIN ----------------
if __name__ == "__main__":
    hms = HotelManagementSystem()
    hms.connect()
    hms.initialize_rooms()

    while True:
        try:
            print("""
**** MAIN MENU ****
1. Add Customer
2. Book Room
3. Calculate Total Amount
4. Update Customer Details
5. Delete Customer Details
6. Show Customer Details
7. Exit
8. Admin Panel
""")
            ch = input("Enter your choice (1-8): ")

            if ch == "1":
                hms.create_customer()
            elif ch == "2":
                hms.book_room()
            elif ch == "3":
                hms.total_bill()
            elif ch == "4":
                hms.update_customer()
            elif ch == "5":
                hms.delete_customer()
            elif ch == "6":
                hms.show_customer()
            elif ch == "7":
                hms.close()
                break
            elif ch == "8":
                hms.admin_panel()
            else:
                print("Invalid choice. Please select a number between 1 and 8.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Please try again.")
