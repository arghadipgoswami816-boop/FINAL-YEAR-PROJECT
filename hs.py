import random
import mysql.connector

print("\n" + "**** HOTEL MANAGEMENT SYSTEM ****".center(80))


class HotelManagementSystem:

    def __init__(self):
        self.connection = None
        self.cursor = None

    # ---------------- MYSQL CONNECTION ----------------
    def connect(self, password):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=password,
            auth_plugin="mysql_native_password"
        )
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS HMS")
        self.connection.commit()
        self.connection.database = "HMS"
        print("Connected to MySQL & HMS database")

    # ---------------- CUSTOMER ----------------
    def create_customer(self):
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

        cid = random.randint(1000, 9999)
        print("Customer ID:", cid)

        name = input("Name: ")
        address = input("Address: ")
        age = int(input("Age: "))
        country = input("Country: ")
        phone = input("Phone: ")
        email = input("Email: ")

        sql = "INSERT INTO C_DETAILS VALUES (%s,%s,%s,%s,%s,%s,%s)"
        self.cursor.execute(sql, (cid, name, address, age, country, phone, email))
        self.connection.commit()
        print("Customer added successfully!")

    def update_customer(self):
        cid = int(input("Enter CID to update: "))
        self.cursor.execute("SELECT * FROM C_DETAILS WHERE C_ID=%s", (cid,))
        data = self.cursor.fetchone()

        if not data:
            print("Customer not found")
            return

        print("Leave blank to keep old value")
        name = input(f"Name [{data[1]}]: ") or data[1]
        address = input(f"Address [{data[2]}]: ") or data[2]
        age = input(f"Age [{data[3]}]: ") or data[3]
        country = input(f"Country [{data[4]}]: ") or data[4]
        phone = input(f"Phone [{data[5]}]: ") or data[5]
        email = input(f"Email [{data[6]}]: ") or data[6]

        sql = """
        UPDATE C_DETAILS
        SET NAME=%s, ADDRESS=%s, AGE=%s, COUNTRY=%s, PHONE=%s, EMAIL=%s
        WHERE C_ID=%s
        """
        self.cursor.execute(sql, (name, address, age, country, phone, email, cid))
        self.connection.commit()
        print("Customer updated successfully!")

    def delete_customer(self):
        cid = int(input("Enter CID to delete: "))
        self.cursor.execute("SELECT * FROM C_DETAILS WHERE C_ID=%s", (cid,))
        if not self.cursor.fetchone():
            print("Customer not found")
            return

        confirm = input("Are you sure? (yes/no): ").lower()
        if confirm == "yes":
            self.cursor.execute("DELETE FROM C_DETAILS WHERE C_ID=%s", (cid,))
            self.connection.commit()
            print("Customer deleted successfully")
        else:
            print("Deletion cancelled")

    def show_customer(self):
        print("1. Show All Customers")
        print("2. Show Specific Customer")
        ch = input("Choice: ")

        if ch == "1":
            self.cursor.execute("SELECT * FROM C_DETAILS")
            rows = self.cursor.fetchall()
            for r in rows:
                print(r)
        elif ch == "2":
            cid = int(input("Enter CID: "))
            self.cursor.execute("SELECT * FROM C_DETAILS WHERE C_ID=%s", (cid,))
            r = self.cursor.fetchone()
            if r:
                print(r)
            else:
                print("Customer not found")

    # ---------------- ROOMS ----------------
    def initialize_rooms(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS ROOMS(
            ROOM_NO INT PRIMARY KEY,
            STATUS VARCHAR(15)
        )
        """)
        self.cursor.execute("SELECT COUNT(*) FROM ROOMS")
        if self.cursor.fetchone()[0] == 0:
            rooms = [(i, "AVAILABLE") for i in range(1, 41)]
            self.cursor.executemany("INSERT INTO ROOMS VALUES (%s,%s)", rooms)
            self.connection.commit()

    def book_room(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS ROOM_RENT(
            C_ID INT,
            ROOM_NO INT,
            DAYS INT,
            RENT INT
        )
        """)

        cid = int(input("Enter CID: "))
        days = int(input("Number of days: "))

        self.cursor.execute("SELECT ROOM_NO FROM ROOMS WHERE STATUS='AVAILABLE' LIMIT 1")
        room = self.cursor.fetchone()

        if not room:
            print("No rooms available")
            return

        room_no = room[0]
        rent = days * 3000

        self.cursor.execute(
            "INSERT INTO ROOM_RENT VALUES (%s,%s,%s,%s)",
            (cid, room_no, days, rent)
        )
        self.cursor.execute(
            "UPDATE ROOMS SET STATUS='BOOKED' WHERE ROOM_NO=%s",
            (room_no,)
        )
        self.connection.commit()
        print(f"Room {room_no} booked. Rent = ₹{rent}")

    # ---------------- RESTAURANT ----------------
    def restaurant(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS RESTAURANT(
            CID INT,
            BILL INT
        )
        """)

        cid = int(input("Enter CID: "))
        qty = int(input("Meals quantity (₹300 each): "))
        bill = qty * 300

        self.cursor.execute("INSERT INTO RESTAURANT VALUES (%s,%s)", (cid, bill))
        self.connection.commit()
        print("Food Bill = ₹", bill)

    # ---------------- BILL ----------------
    def total_bill(self):
        cid = int(input("Enter CID: "))

        self.cursor.execute("SELECT RENT FROM ROOM_RENT WHERE C_ID=%s", (cid,))
        r = self.cursor.fetchone()

        self.cursor.execute("SELECT BILL FROM RESTAURANT WHERE CID=%s", (cid,))
        f = self.cursor.fetchone()

        total = (r[0] if r else 0) + (f[0] if f else 0)
        print("Total Bill = ₹", total)

    def close(self):
        self.cursor.close()
        self.connection.close()
        print("Connection closed")


# ---------------- MAIN ----------------
if __name__ == "__main__":
    hms = HotelManagementSystem()
    pwd = input("Enter MySQL Password: ")
    hms.connect(pwd)
    hms.initialize_rooms()

    while True:
        print("""
1. Add Customer
2. Book Room
3. Restaurant
4. Calculate Total Amount
5. Update Customer Details
6. Delete Customer Details
7. Show Customer Details
8. Exit
""")
        ch = input("Enter choice: ")

        if ch == "1":
            hms.create_customer()
        elif ch == "2":
            hms.book_room()
        elif ch == "3":
            hms.restaurant()
        elif ch == "4":
            hms.total_bill()
        elif ch == "5":
            hms.update_customer() 
        elif ch == "6":
            hms.delete_customer()
        elif ch == "7":
            hms.show_customer()
        elif ch == "8":
            hms.close()
            break
        else:
            print("Invalid choice")
