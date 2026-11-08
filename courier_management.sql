CREATE DATABASE courierManagement;

USE courierManagement;

CREATE TABLE Customer (
    CustomerID VARCHAR(10) PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Phone VARCHAR(20),
    Email VARCHAR(100)
);

CREATE TABLE Driver (
    DriverID VARCHAR(10) PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Phone VARCHAR(20),
    LicenceNumber VARCHAR(20)
);

CREATE TABLE Orders (
    OrderID VARCHAR(10) PRIMARY KEY,
    CustomerID VARCHAR(10),
    OrderDate DATE,
    OrderStatus VARCHAR(30),
    TotalAmount DECIMAL(10,2),
    PickupAddress VARCHAR(150),
    DestinationAddress VARCHAR(150),
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
);

CREATE TABLE Package (
    PackageID VARCHAR(10) PRIMARY KEY,
    OrderID VARCHAR(10),
    TrackingNumber VARCHAR(20),
    Description VARCHAR(100),
    Weight DECIMAL(5,2),
    PackageType VARCHAR(30),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
);

CREATE TABLE Payment (
    PaymentID VARCHAR(10) PRIMARY KEY,
    OrderID VARCHAR(10),
    PaymentDate DATE,
    Amount DECIMAL(10,2),
    PaymentMethod VARCHAR(30),
    PaymentStatus VARCHAR(30),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
);

CREATE TABLE Delivery (
    DeliveryID VARCHAR(10) PRIMARY KEY,
    OrderID VARCHAR(10),
    DriverID VARCHAR(10),
    DeliveryDate DATE,
    DeliveryStatus VARCHAR(30),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (DriverID) REFERENCES Driver(DriverID)
);

CREATE TABLE Tracking (
    TrackingID VARCHAR(10) PRIMARY KEY,
    PackageID VARCHAR(10),
    Status VARCHAR(30),
    Location VARCHAR(50),
    UpdateDateTime DATETIME,
    FOREIGN KEY (PackageID) REFERENCES Package(PackageID)
);

CREATE TABLE Returns (
    ReturnID VARCHAR(10) PRIMARY KEY,
    PackageID VARCHAR(10),
    ReturnDate DATE,
    ReturnReason VARCHAR(100),
    ReturnStatus VARCHAR(30),
    FOREIGN KEY (PackageID) REFERENCES Package(PackageID)
);

INSERT INTO Customer (CustomerID, FirstName, LastName, Phone, Email)
VALUES
('C001', 'Lerato', 'Mokwena', '0713426433', 'leratomo15@gmail.com'),
('C002', 'Sipho', 'Nkosi', '0835477781', 'sipho45@gmail.com');

INSERT INTO Driver (DriverID, FirstName, LastName, Phone, LicenceNumber)
VALUES
('D001', 'Thabo', 'Moloi', '0723456287', 'DL001'),
('D002', 'Naledi', 'Molefe', '0798675321', 'DL002');

INSERT INTO Orders (OrderID, CustomerID, OrderDate, OrderStatus, TotalAmount, PickupAddress, DestinationAddress
)
VALUES
('O001', 'C001', '2026-09-10', 'Pending', 500.00, '23 Main St', '45 Church Rd'),
('O002', 'C002', '2026-09-12', 'Confirmed', 350.00, '74 Evergreen St', '14 North Rd');

INSERT INTO Package (PackageID, OrderID, TrackingNumber, Description, Weight, PackageType)
VALUES
('P001', 'O001', 'TR001', 'Shoes', 2.00, 'Standard'),
('P002', 'O002', 'TR002', 'Clothing', 1.50, 'Express');

INSERT INTO Payment (PaymentID, OrderID, PaymentDate, Amount, PaymentMethod, PaymentStatus)
VALUES
('PAY001', 'O001', '2026-09-10', 500.00, 'Card', 'Paid'),
('PAY002', 'O002', '2026-09-12', 350.00, 'Card', 'Paid');

INSERT INTO Delivery (DeliveryID, OrderID, DriverID, DeliveryDate, DeliveryStatus
)
VALUES
('DEL001', 'O001', 'D001', '2026-09-11', 'In Transit'),
('DEL002', 'O002', 'D002', '2026-09-13', 'Delivered');

INSERT INTO Tracking (TrackingID, PackageID, Status, Location, UpdateDateTime)
VALUES
('T001', 'P001', 'In Transit', 'Kimberley', '2026-09-10 14:30:00'),
('T002', 'P002', 'Delivered', 'Bloemfontein', '2026-09-12 16:00:00');

INSERT INTO Returns (ReturnID, PackageID, ReturnDate, ReturnReason, ReturnStatus)
VALUES
('R001', 'P001', '2026-09-13', 'Customer request', 'Pending'),
('R002', 'P002', '2026-09-14', 'Damaged package', 'Approved');

SHOW TABLES;

SELECT * FROM Customer;
SELECT * FROM Driver;
SELECT * FROM Orders;
SELECT * FROM Package;
SELECT * FROM Payment;
SELECT * FROM Delivery;
SELECT * FROM Tracking;
SELECT * FROM Returns;

SELECT DATABASE();

SHOW TABLES;

SELECT COUNT(*) AS PackageRows FROM Package;
SELECT COUNT(*) AS PaymentRows FROM Payment;
SELECT COUNT(*) AS DeliveryRows FROM Delivery;
SELECT COUNT(*) AS TrackingRows FROM Tracking;
SELECT COUNT(*) AS ReturnsRows FROM Returns;

USE courierManagement;

INSERT INTO Package
(PackageID, OrderID, TrackingNumber, Description, Weight, PackageType)
VALUES
('P001', 'O001', 'TR001', 'Shoes', 2.00, 'Standard'),
('P002', 'O002', 'TR002', 'Clothing', 1.50, 'Express');

SELECT * FROM Package;
USE courierManagement;

INSERT INTO Payment
(PaymentID, OrderID, PaymentDate, Amount, PaymentMethod, PaymentStatus)
VALUES
('PAY001', 'O001', '2026-09-10', 500.00, 'Card', 'Paid'),
('PAY002', 'O002', '2026-09-12', 350.00, 'Card', 'Paid');

SELECT * FROM Payment;
USE courierManagement;

INSERT INTO Delivery
(DeliveryID, OrderID, DriverID, DeliveryDate, DeliveryStatus)
VALUES
('DEL001', 'O001', 'D001', '2026-09-11', 'In Transit'),
('DEL002', 'O002', 'D002', '2026-09-13', 'Delivered');

SELECT * FROM Delivery;
USE courierManagement;

INSERT INTO Tracking
(TrackingID, PackageID, Status, Location, UpdateDateTime)
VALUES
('T001', 'P001', 'In Transit', 'Kimberley', '2026-09-10 14:30:00'),
('T002', 'P002', 'Delivered', 'Bloemfontein', '2026-09-12 16:00:00');

SELECT * FROM Tracking;

USE courierManagement;

INSERT INTO Returns
(ReturnID, PackageID, ReturnDate, ReturnReason, ReturnStatus)
VALUES
('R001', 'P001', '2026-09-13', 'Customer request', 'Pending'),
('R002', 'P002', '2026-09-14', 'Damaged package', 'Approved');

SELECT * FROM Returns;

