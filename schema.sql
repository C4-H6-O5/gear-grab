-- DATABASE SCHEMA SCRIPT for LensLocker
-- Context: Focus BatStateU Camera Club Inventory
-- This file is read and executed by db_setup.py

-- ==========================================
-- 1. CLEANUP
-- ==========================================
DROP TABLE IF EXISTS Borrowings;
DROP TABLE IF EXISTS Inventory_Items;
DROP TABLE IF EXISTS Equipment_Models;
DROP TABLE IF EXISTS Members;
DROP TABLE IF EXISTS Categories;

-- ==========================================
-- 2. TABLE CREATION
-- ==========================================

CREATE TABLE Categories (
    CategoryID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    MaxLoanDays INTEGER DEFAULT 3
);

CREATE TABLE Equipment_Models (
    ModelID INTEGER PRIMARY KEY AUTOINCREMENT,
    CategoryID INTEGER,
    Name TEXT NOT NULL,
    ReplacementCost REAL,
    FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
);

CREATE TABLE Inventory_Items (
    AssetTag TEXT PRIMARY KEY,
    ModelID INTEGER,
    Status TEXT CHECK(Status IN ('Available', 'Borrowed', 'Internal', 'Maintenance', 'Lost')) DEFAULT 'Available',
    PurchaseDate TEXT,
    FOREIGN KEY (ModelID) REFERENCES Equipment_Models(ModelID)
);

CREATE TABLE Members (
    MemberID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Email TEXT UNIQUE,
    PhoneNumber TEXT,
    IsOfficer BOOLEAN DEFAULT 0
);

CREATE TABLE Borrowings (
    BorrowID INTEGER PRIMARY KEY AUTOINCREMENT,
    MemberID INTEGER,
    AssetTag TEXT,
    DateOut DATETIME DEFAULT CURRENT_TIMESTAMP,
    DueDate DATETIME,
    DateReturned DATETIME,
    ReturnCondition TEXT,
    PaymentStatus TEXT DEFAULT 'N/A', -- Can be 'N/A', 'Unpaid', 'Paid'
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID),
    FOREIGN KEY (AssetTag) REFERENCES Inventory_Items(AssetTag)
);

-- ==========================================
-- 3. DATA INSERTION (Based on "Gear Grab" Poster)
-- ==========================================

-- --- A. CATEGORIES ---
INSERT INTO Categories (Name, MaxLoanDays) VALUES ('Camera Body', 3);          -- ID 1
INSERT INTO Categories (Name, MaxLoanDays) VALUES ('Camera Lens', 3);          -- ID 2
INSERT INTO Categories (Name, MaxLoanDays) VALUES ('Lighting', 1);             -- ID 3
INSERT INTO Categories (Name, MaxLoanDays) VALUES ('Tripods & Support', 3);    -- ID 4
INSERT INTO Categories (Name, MaxLoanDays) VALUES ('Audio & Microphones', 3);  -- ID 5
INSERT INTO Categories (Name, MaxLoanDays) VALUES ('Drones', 1);               -- ID 6
INSERT INTO Categories (Name, MaxLoanDays) VALUES ('Stabilizers & Gimbals', 2);-- ID 7
INSERT INTO Categories (Name, MaxLoanDays) VALUES ('Studio Accessories', 3);   -- ID 8 (Misc)

-- --- B. EQUIPMENT MODELS (The Catalog) ---

-- 1. Camera Bodies
INSERT INTO Equipment_Models (CategoryID, Name, ReplacementCost) VALUES (1, 'Sony ZV-E10', 35000.00);
INSERT INTO Equipment_Models (CategoryID, Name, ReplacementCost) VALUES (1, 'Sony A6400', 45000.00);
INSERT INTO Equipment_Models (CategoryID, Name, ReplacementCost) VALUES (1, 'Canon EOS M50 Mark II', 30000.00); -- (Filler)

-- 2. Camera Lenses
INSERT INTO Equipment_Models (CategoryID, Name, ReplacementCost) VALUES (2, 'Sony E PZ 16-50mm Kit Lens', 8000.00);
INSERT INTO Equipment_Models (CategoryID, Name, ReplacementCost) VALUES (2, 'Sigma 16mm f/1.4 DC DN', 19000.00); -- (Filler)
INSERT INTO Equipment_Models (CategoryID, Name, ReplacementCost) VALUES (2, 'Sony E 50mm f/1.8 OSS', 12000.00); -- (Filler)

-- 3. Lighting
INSERT INTO Equipment_Models (CategoryID, Name, ReplacementCost) VALUES (3, 'Godox SL60II Bi-Color', 8500.00);
INSERT INTO Equipment_Models (CategoryID, Name, ReplacementCost) VALUES (3, 'Godox Strobe 200W', 6000.00);
INSERT INTO Equipment_Models (CategoryID, Name, ReplacementCost) VALUES (3, 'Maia 50x70cm Softbox', 1500.00);
INSERT INTO Equipment_Models (CategoryID, Name, ReplacementCost) VALUES (3, 'Continuous Light 105W', 1200.00); -- From "2 105Watt Light"

-- 4. Tripods
INSERT INTO Equipment_Models (CategoryID, Name, ReplacementCost) VALUES (4, 'Yunteng Video Tripod', 1500.00);
INSERT INTO Equipment_Models (CategoryID, Name, ReplacementCost) VALUES (4, 'Manfrotto Compact Action', 4000.00); -- (Filler)

-- 5. Audio
INSERT INTO Equipment_Models (CategoryID, Name, ReplacementCost) VALUES (5, 'DJI Mic Mini Wireless', 15000.00);
INSERT INTO Equipment_Models (CategoryID, Name, ReplacementCost) VALUES (5, 'Rode VideoMicro', 3000.00); -- (Filler)

-- 6. Drones
INSERT INTO Equipment_Models (CategoryID, Name, ReplacementCost) VALUES (6, 'DJI Mini 2', 25000.00);
INSERT INTO Equipment_Models (CategoryID, Name, ReplacementCost) VALUES (6, 'DJI Mini 3 Pro', 40000.00); -- (Filler)

-- 7. Stabilizers
INSERT INTO Equipment_Models (CategoryID, Name, ReplacementCost) VALUES (7, 'DJI Ronin SC', 18000.00);
INSERT INTO Equipment_Models (CategoryID, Name, ReplacementCost) VALUES (7, 'Zhiyun Crane M2', 12000.00); -- (Filler)

-- 8. Misc / Studio Accessories
INSERT INTO Equipment_Models (CategoryID, Name, ReplacementCost) VALUES (8, 'Extension Cord (10m)', 500.00);
INSERT INTO Equipment_Models (CategoryID, Name, ReplacementCost) VALUES (8, 'Green Screen Backdrop', 1000.00);

-- --- C. INVENTORY ITEMS (Physical Units) ---

-- Drones
INSERT INTO Inventory_Items (AssetTag, ModelID, Status, PurchaseDate) VALUES ('DRONE-01', (SELECT ModelID FROM Equipment_Models WHERE Name='DJI Mini 2'), 'Available', '2023-05-10');
INSERT INTO Inventory_Items (AssetTag, ModelID, Status, PurchaseDate) VALUES ('DRONE-02', (SELECT ModelID FROM Equipment_Models WHERE Name='DJI Mini 3 Pro'), 'Maintenance', '2023-09-12');

-- Cameras
INSERT INTO Inventory_Items (AssetTag, ModelID, Status, PurchaseDate) VALUES ('CAM-01', (SELECT ModelID FROM Equipment_Models WHERE Name='Sony ZV-E10'), 'Available', '2023-01-15');
INSERT INTO Inventory_Items (AssetTag, ModelID, Status, PurchaseDate) VALUES ('CAM-02', (SELECT ModelID FROM Equipment_Models WHERE Name='Sony A6400'), 'Borrowed', '2023-02-20');
INSERT INTO Inventory_Items (AssetTag, ModelID, Status, PurchaseDate) VALUES ('CAM-03', (SELECT ModelID FROM Equipment_Models WHERE Name='Canon EOS M50 Mark II'), 'Available', '2023-06-01');

-- Lenses
INSERT INTO Inventory_Items (AssetTag, ModelID, Status, PurchaseDate) VALUES ('LENS-01', (SELECT ModelID FROM Equipment_Models WHERE Name='Sigma 16mm f/1.4 DC DN'), 'Available', '2023-03-10');
INSERT INTO Inventory_Items (AssetTag, ModelID, Status, PurchaseDate) VALUES ('LENS-02', (SELECT ModelID FROM Equipment_Models WHERE Name='Sony E 50mm f/1.8 OSS'), 'Available', '2023-03-10');

-- Lighting (Poster says "2 105Watt Light", so we add two)
INSERT INTO Inventory_Items (AssetTag, ModelID, Status, PurchaseDate) VALUES ('LIGHT-01', (SELECT ModelID FROM Equipment_Models WHERE Name='Godox SL60II Bi-Color'), 'Available', '2023-11-05');
INSERT INTO Inventory_Items (AssetTag, ModelID, Status, PurchaseDate) VALUES ('LIGHT-02', (SELECT ModelID FROM Equipment_Models WHERE Name='Godox Strobe 200W'), 'Internal', '2023-11-05');
INSERT INTO Inventory_Items (AssetTag, ModelID, Status, PurchaseDate) VALUES ('LIGHT-03', (SELECT ModelID FROM Equipment_Models WHERE Name='Continuous Light 105W'), 'Available', '2023-10-01');
INSERT INTO Inventory_Items (AssetTag, ModelID, Status, PurchaseDate) VALUES ('LIGHT-04', (SELECT ModelID FROM Equipment_Models WHERE Name='Continuous Light 105W'), 'Available', '2023-10-01');
INSERT INTO Inventory_Items (AssetTag, ModelID, Status, PurchaseDate) VALUES ('MOD-01', (SELECT ModelID FROM Equipment_Models WHERE Name='Maia 50x70cm Softbox'), 'Available', '2023-10-01');

-- Tripods (Poster says "3 Tripod")
INSERT INTO Inventory_Items (AssetTag, ModelID, Status, PurchaseDate) VALUES ('TRIPOD-01', (SELECT ModelID FROM Equipment_Models WHERE Name='Yunteng Video Tripod'), 'Available', '2023-08-15');
INSERT INTO Inventory_Items (AssetTag, ModelID, Status, PurchaseDate) VALUES ('TRIPOD-02', (SELECT ModelID FROM Equipment_Models WHERE Name='Yunteng Video Tripod'), 'Available', '2023-08-15');
INSERT INTO Inventory_Items (AssetTag, ModelID, Status, PurchaseDate) VALUES ('TRIPOD-03', (SELECT ModelID FROM Equipment_Models WHERE Name='Yunteng Video Tripod'), 'Lost', '2023-08-15');

-- Audio
INSERT INTO Inventory_Items (AssetTag, ModelID, Status, PurchaseDate) VALUES ('MIC-01', (SELECT ModelID FROM Equipment_Models WHERE Name='DJI Mic Mini Wireless'), 'Available', '2024-01-10');
INSERT INTO Inventory_Items (AssetTag, ModelID, Status, PurchaseDate) VALUES ('MIC-02', (SELECT ModelID FROM Equipment_Models WHERE Name='Rode VideoMicro'), 'Available', '2023-12-05');

-- Gimbal
INSERT INTO Inventory_Items (AssetTag, ModelID, Status, PurchaseDate) VALUES ('GIMBAL-01', (SELECT ModelID FROM Equipment_Models WHERE Name='DJI Ronin SC'), 'Available', '2023-07-20');

-- Misc
INSERT INTO Inventory_Items (AssetTag, ModelID, Status, PurchaseDate) VALUES ('MISC-01', (SELECT ModelID FROM Equipment_Models WHERE Name='Extension Cord (10m)'), 'Available', '2023-05-05');

-- --- D. MEMBERS ---
INSERT INTO Members (Name, Email, PhoneNumber, IsOfficer) VALUES ('John Doe', 'john@school.edu', '0912-345-6789', 0);
INSERT INTO Members (Name, Email, PhoneNumber, IsOfficer) VALUES ('Justine Ronquillo', 'justine@school.edu', '0998-765-4321', 1); -- Based on Poster!
INSERT INTO Members (Name, Email, PhoneNumber, IsOfficer) VALUES ('Mike Hoarder', 'mike@school.edu', '0917-111-2222', 0);