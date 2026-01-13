# 🏨 Hotel Management System (Python + MySQL)

A **console-based Hotel Management System** built using **Python** and **MySQL**, designed to handle customer records, room bookings, restaurant billing, and total bill calculation efficiently.

This project is ideal for **college projects**, **database learning**, and **Python beginners** who want to understand how Python integrates with MySQL in a real-world application.

---

## ✨ Features

✅ Customer Management  
- Add new customers  
- Update customer details  
- Delete customer records  
- View all or specific customer details  

✅ Room Management  
- Automatically initializes hotel rooms  
- Tracks room availability (Available / Booked)  
- Allows room booking with rent calculation  

✅ Restaurant Module  
- Place food orders  
- Automatically calculates restaurant bill  

✅ Billing System  
- Calculates **total bill** (Room Rent + Restaurant Bill)  

✅ Database Powered  
- Uses **MySQL** for persistent data storage  
- Automatically creates required tables  

---

## 🛠️ Technologies Used

- **Python 3**
- **MySQL**
- **mysql-connector-python**
- Object-Oriented Programming (OOP)

---

## 🗃️ Database Structure

**Database Name:** `HMS`

### Tables Used:
- `C_DETAILS` → Stores customer information  
- `ROOMS` → Stores room numbers and availability  
- `ROOM_RENT` → Stores room booking details  
- `RESTAURANT` → Stores restaurant bills  

---

## ⚙️ Installation & Setup

### 1️⃣ Install Required Package
```bash
pip install mysql-connector-python
