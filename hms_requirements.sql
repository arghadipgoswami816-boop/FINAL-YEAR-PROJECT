-- HMS Database Setup SQL Dump
-- This file contains the complete MySQL database setup queries for the Hotel Management System (hs2.py)

-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS HMS;

-- Use the HMS database
USE HMS;

-- Create ROOM_RENT table
CREATE TABLE IF NOT EXISTS ROOM_RENT (
    C_ID INT,
    ROOM_NO INT,
    DAYS INT,
    RENT INT,
    CHECK_IN_DATE DATE,
    CHECK_OUT_DATE DATE
);

-- Create C_DETAILS table
CREATE TABLE IF NOT EXISTS C_DETAILS (
    C_ID INT PRIMARY KEY,
    NAME VARCHAR(50),
    ADDRESS VARCHAR(100),
    AGE INT,
    COUNTRY VARCHAR(30),
    PHONE VARCHAR(15),
    EMAIL VARCHAR(50),
    ID_TYPE VARCHAR(20),
    ID_NUMBER VARCHAR(50)
);

-- Create ROOMS table
CREATE TABLE IF NOT EXISTS ROOMS (
    ROOM_NO INT PRIMARY KEY,
    STATUS VARCHAR(15),
    TYPE VARCHAR(10)
);

-- Insert initial rooms data
INSERT INTO ROOMS (ROOM_NO, STATUS, TYPE) VALUES
(1, 'AVAILABLE', 'SINGLE'),
(2, 'AVAILABLE', 'SINGLE'),
(3, 'AVAILABLE', 'DOUBLE'),
(4, 'AVAILABLE', 'DOUBLE');
