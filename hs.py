import random
import mysql.connector
from datetime import datetime

width = 100
print("**** HOTEL MANAGEMENT SYSTEM ****".center(width))


class HotelManagementSystem:

    def __init__(self):
        self.connection = None
        self.cursor = None

    # ---------- MYSQL CONNECTION ----------
    def connect_to_mysql(self, password):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password=password,
                auth_plugin="mysql_native_password"
            )
            self.cursor = self.connection.cursor()
            self.cursor.execute("CREATE DATABASE IF NOT EXISTS HMS")
            self.connection.commit()
            print("Connected to MySQL successfully!")
            return True
        except mysql.connector.Error as e:
            print("MySQL Error:", e)
            return False

    def use_database(self, password):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=password,
            database="HMS",
            auth_plugin="mysql_native_password"
        )
        self.cursor = self.connection.cursor()

    # ---------- CUSTOMER ----------
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

    # ---------- ROOMS ----------
    def initialize_rooms(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS ROOMS(
            ROOM_NO INT PRIMARY KEY,
            CATEGORY VARCHAR(20),
            STATUS VARCHAR(15) DEFAULT 'AVAILABLE'
        )
        """)

        self.cursor.execute("SELECT COUNT(*) FROM ROOMS")
        if self.cursor.fetchone()[0] == 0:
            rooms = []
            rooms += [(i, 'Ultra Luxury') for i in range(1, 6)]
            rooms += [(i, 'Luxury') for i in range(6, 16)]
            rooms += [(i, 'Elite') for i in range(16, 36)]
            rooms += [(i, 'Economy') for i in range(36, 53)]
            self.cursor.executemany("INSERT INTO ROOMS VALUES (%s,%s,'AVAILABLE')", rooms)
            self.connection.commit()
            print("Rooms initialized!")

    # ---------- ROOM RENT ----------
    def book_room(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS ROOM_RENT(
            C_ID INT,
            ROOMNO INT,
            DAYS INT,
            RENT INT
        )
        """)

        cid = int(input("Enter CID: "))
        days = int(input("Number of days: "))

        self.cursor.execute("SELECT ROOM_NO FROM ROOMS WHERE STATUS='AVAILABLE'")
        rooms = self.cursor.fetchall()

        if not rooms:
            print("No rooms available!")
            return

        room_no = rooms[0][0]
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

    # ---------- RESTAURANT ----------
    def restaurant(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS RESTAURANT(
            CID INT,
            BILL INT
        )
        """)

        cid = int(input("CID: "))
        qty = int(input("Quantity of meals (₹300 each): "))
        bill = qty * 300

        self.cursor.execute("INSERT INTO RESTAURANT VALUES (%s,%s)", (cid, bill))
        self.connection.commit()
        print("Food Bill = ₹", bill)

    # ---------- TOTAL ----------
    def calculate_total(self):
        cid = int(input("CID: "))

        self.cursor.execute("SELECT RENT FROM ROOM_RENT WHERE C_ID=%s", (cid,))
        room = self.cursor.fetchone()

        self.cursor.execute("SELECT BILL FROM RESTAURANT WHERE CID=%s", (cid,))
        food = self.cursor.fetchone()

        total = (room[0] if room else 0) + (food[0] if food else 0)
        print("Total Bill = ₹", total)

    # ---------- CLOSE ----------
    def close(self):
        self.cursor.close()
        self.connection.close()
        print("Connection closed.")


# ---------- MAIN ----------
if __name__ == "__main__":
    hms = HotelManagementSystem()
    pwd = input("Enter MySQL Password: ")

    if hms.connect_to_mysql(pwd):
        hms.use_database(pwd)
        hms.initialize_rooms()

        while True:
            print("""
1. Add Customer
2. Book Room
3. Restaurant
4. Total Bill
5. Exit
""")
            ch = input("Choice: ")

            if ch == '1':
                hms.create_customer()
            elif ch == '2':
                hms.book_room()
            elif ch == '3':
                hms.restaurant()
            elif ch == '4':
                hms.calculate_total()
            elif ch == '5':
                hms.close()
                break
            else:
                print("Invalid choice")
