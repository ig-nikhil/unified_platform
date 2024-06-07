-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 07, 2024 at 12:05 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `project_dis`
--

-- --------------------------------------------------------

--
-- Table structure for table `customers`
--

CREATE TABLE `customers` (
  `CustomerID` int(11) NOT NULL,
  `CustomerName` varchar(100) NOT NULL,
  `ContactNumber` varchar(20) DEFAULT NULL,
  `Email` varchar(100) NOT NULL,
  `Address` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customers`
--

INSERT INTO `customers` (`CustomerID`, `CustomerName`, `ContactNumber`, `Email`, `Address`) VALUES
(1, 'Divya Kapoor', '9876543219', 'divya.kapoor@gmail.com', '808 Brown Street, Jaipur, Rajasthan, India'),
(2, 'Alok Khanna', '9876543220', 'alok.khanna@gmail.com', '909 Maroon Drive, Lucknow, Uttar Pradesh, India'),
(3, 'Neha Trivedi', '9876543221', 'neha.trivedi@gmail.com', '1010 Gray Avenue, Kanpur, Uttar Pradesh, India'),
(4, 'Vikram Mehra', '9876543222', 'vikram.mehra@gmail.com', '1111 Cyan Lane, Nagpur, Maharashtra, India'),
(5, 'Anjali Desai', '9876543223', 'anjali.desai@gmail.com', '1212 Aqua Street, Patna, Bihar, India'),
(6, 'Prakash Singh', '9876543224', 'prakash.singh@gmail.com', '1313 Beige Road, Indore, Madhya Pradesh, India'),
(7, 'Deepak Sharma', '9876543225', 'deepak.sharma@gmail.com', '1414 Tan Drive, Bhopal, Madhya Pradesh, India'),
(8, 'Kavita Nair', '9876543226', 'kavita.nair@gmail.com', '1515 Gold Avenue, Ludhiana, Punjab, India'),
(9, 'Suresh Menon', '9876543227', 'suresh.menon@gmail.com', '1616 Silver Lane, Agra, Uttar Pradesh, India'),
(10, 'Anita Iyer', '9876543228', 'anita.iyer@gmail.com', '1717 Bronze Street, Varanasi, Uttar Pradesh, India'),
(11, 'Rajeev Kapoor', '9876543229', 'rajeev.kapoor@gmail.com', '1818 Ivory Road, Allahabad, Uttar Pradesh, India'),
(12, 'Meera Reddy', '9876543230', 'meera.reddy@gmail.com', '1919 Copper Drive, Ranchi, Jharkhand, India'),
(13, 'Manoj Choudhary', '9876543231', 'manoj.choudhary@gmail.com', '2020 Brass Avenue, Coimbatore, Tamil Nadu, India'),
(14, 'Nisha Mehra', '9876543232', 'nisha.mehra@gmail.com', '2121 Platinum Lane, Kochi, Kerala, India'),
(15, 'Rahul Sinha', '9876543233', 'rahul.sinha@gmail.com', '2222 Steel Street, Visakhapatnam, Andhra Pradesh, India'),
(16, 'Pooja Mehta', '9876543234', 'pooja.mehta@gmail.com', '2323 Pearl Road, Mysore, Karnataka, India'),
(17, 'Vinod Gupta', '9876543235', 'vinod.gupta@gmail.com', '2424 Diamond Drive, Guwahati, Assam, India'),
(18, 'Kiran Joshi', '9876543236', 'kiran.joshi@gmail.com', '2525 Ruby Avenue, Shimla, Himachal Pradesh, India'),
(19, 'Shalini Patel', '9876543237', 'shalini.patel@gmail.com', '2626 Sapphire Lane, Dehradun, Uttarakhand, India'),
(20, 'Arun Khatri', '9876543238', 'arun.khatri@gmail.com', '2727 Emerald Street, Gandhinagar, Gujarat, India'),
(30, 'ram sharma', '9898989898', 'sharma@gmail.com', 'Patel Nagar'),
(31, 'rudra', '07970888043', 'rudra@gmail.com', 'hdgdh');

-- --------------------------------------------------------

--
-- Table structure for table `employees`
--

CREATE TABLE `employees` (
  `EmployeeID` int(11) NOT NULL,
  `FirstName` varchar(50) NOT NULL,
  `LastName` varchar(50) NOT NULL,
  `DateOfBirth` date DEFAULT NULL,
  `Gender` enum('Male','Female','Other') DEFAULT NULL,
  `Department` varchar(50) DEFAULT NULL,
  `Position` varchar(50) DEFAULT NULL,
  `Salary` decimal(10,2) DEFAULT NULL,
  `Password` varchar(50) NOT NULL,
  `Email` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `employees`
--

INSERT INTO `employees` (`EmployeeID`, `FirstName`, `LastName`, `DateOfBirth`, `Gender`, `Department`, `Position`, `Salary`, `Password`, `Email`) VALUES
(1, 'Rishabh', 'Yadav', '2003-05-24', 'Male', 'Sales', 'Manager', 500000.00, '1625', 'rishabh@gmail.com'),
(2, 'kartik', 'kumar', '1990-07-25', 'Female', 'HR', 'employee', 35000.00, 'password2', 'kartik@gmail.com'),
(4, 'Priya', 'Patel', '1995-04-20', 'Female', 'Finance', 'employee', 40000.00, 'password4', 'priya.patel@gmail.com'),
(5, 'Alok', 'Singh', '1988-09-05', 'Male', 'Production', 'employee', 45000.00, 'password5', 'alok.singh@gmail.com'),
(6, 'Anjali', 'Gupta', '1983-01-30', 'Female', 'Production', 'Manager', 55000.00, 'password6', 'anjali.gupta@gmail.com'),
(7, 'Ravi', 'Verma', '1992-06-18', 'Male', 'Sales', 'employee', 38000.00, 'password7', 'ravi.verma@gmail.com'),
(8, 'Nisha', 'Reddy', '1987-12-03', 'Female', 'Marketing', 'employee', 32000.00, 'password8', 'nisha.reddy@gmail.com'),
(9, 'Sanjay', 'Joshi', '1975-08-12', 'Male', 'HR', 'employee', 52000.00, 'password9', 'sanjay.joshi@gmail.com'),
(10, 'Meera', 'Menon', '1998-02-28', 'Female', 'Sales', 'employee', 25000.00, 'password10', 'meera.menon@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `OrderID` int(11) NOT NULL,
  `OrderDate` date DEFAULT NULL,
  `CustomerID` int(11) DEFAULT NULL,
  `ProductID` int(11) DEFAULT NULL,
  `Quantity` int(11) DEFAULT NULL,
  `TotalAmount` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`OrderID`, `OrderDate`, `CustomerID`, `ProductID`, `Quantity`, `TotalAmount`) VALUES
(1, '2024-04-01', 1, 1, 2, 150000.00),
(2, '2024-04-02', 2, 2, 1, 75000.00),
(3, '2024-04-03', 3, 3, 3, 225000.00),
(4, '2024-04-04', 4, 4, 1, 50000.00),
(5, '2024-04-05', 5, 5, 2, 120000.00),
(6, '2024-04-06', 6, 6, 1, 70000.00),
(7, '2024-04-07', 7, 7, 4, 320000.00),
(8, '2024-04-08', 8, 1, 3, 225000.00),
(9, '2024-04-09', 9, 2, 2, 150000.00),
(10, '2024-04-10', 10, 3, 1, 75000.00),
(11, '2024-04-11', 11, 4, 3, 150000.00),
(12, '2024-04-12', 12, 5, 1, 60000.00),
(13, '2024-04-13', 13, 6, 2, 140000.00),
(14, '2024-04-14', 14, 7, 1, 80000.00),
(15, '2024-04-15', 15, 1, 4, 300000.00),
(16, '2024-04-16', 16, 2, 2, 150000.00),
(17, '2024-04-17', 17, 3, 1, 90000.00),
(18, '2024-04-18', 18, 4, 2, 100000.00),
(19, '2024-04-19', 19, 5, 3, 180000.00),
(20, '2024-04-20', 20, 6, 1, 70000.00),
(21, '2024-04-02', 3, 1, 7, 1200.00),
(22, '2024-04-02', 3, 1, 7, 1200.00),
(23, '2024-04-02', 3, 1, 7, 1200.00),
(54, '2024-07-07', 7, 7, 7, 7.00),
(55, '2024-04-06', 6, 6, 6, 6.00),
(56, '2024-04-24', 6, 1, 7, 200000.00),
(57, '2024-04-26', 19, 12, 100, 200000.00),
(58, '2024-04-26', 3, 1, 100, 12345.00),
(59, '2024-04-26', 3, 1, 10, 10000.00);

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `ProductID` int(11) NOT NULL,
  `ProductName` varchar(100) NOT NULL,
  `Category` varchar(50) DEFAULT NULL,
  `QuantityInStock` int(11) DEFAULT NULL,
  `UnitPrice` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`ProductID`, `ProductName`, `Category`, `QuantityInStock`, `UnitPrice`) VALUES
(1, ' Butter', 'Dairy', 100, 250.00),
(2, ' Milk', 'Dairy', 200, 40.00),
(3, ' Cheese', 'Dairy', 150, 180.00),
(4, ' Ice Cream', 'Dairy', 120, 150.00),
(5, ' Ghee', 'Dairy', 80, 300.00),
(6, ' Yogurt', 'Dairy', 100, 30.00),
(7, ' Paneer', 'Dairy', 80, 200.00),
(8, 'dahi', 'dairy', 20, 100.00),
(9, 'amul butter', 'dairy', 0, 4.00),
(10, 'amul butter', 'dairy', 0, 4.00),
(11, 'amul butter', 'dairy', 0, 4.00),
(12, 'milk shake', 'dairy', 30, 60.00),
(13, 'pani puri', 'fast food', 100, 10.00),
(14, 'butter biscuit', 'biscuit', 70, 10.00),
(15, 'chasni', 'sweet dish', 100, 12.00),
(16, 'pani puri', 'fast food', 20, 10.00),
(17, 'amul butter', 'dairy', 10, 90.00);

-- --------------------------------------------------------

--
-- Table structure for table `suppliers`
--

CREATE TABLE `suppliers` (
  `SupplierID` int(11) NOT NULL,
  `SupplierName` varchar(100) NOT NULL,
  `ContactNumber` varchar(20) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `Address` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `suppliers`
--

INSERT INTO `suppliers` (`SupplierID`, `SupplierName`, `ContactNumber`, `Email`, `Address`) VALUES
(1, 'Amul Dairy', '9876543210', 'contact@amuldairy.com', '123 Main Street, Mumbai, Maharashtra, India'),
(2, 'Mother Dairy', '9876543211', 'contact@motherdairy.com', '456 Sarojini nagar, New Delhi, India'),
(3, 'Nestle', '9876543212', 'contact@nestle.com', '789 Oak Street, Bangalore, Karnataka, India'),
(4, 'Britannia Industries', '9876543213', 'contact@britannia.com', '101 sonagachi, Kolkata, West Bengal, India'),
(5, 'Parle Agro', '9876543214', 'contact@parleagro.com', '202 Rajni Street, Chennai, Tamil Nadu, India');

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE `transactions` (
  `TransactionID` int(11) NOT NULL,
  `TransactionDate` date DEFAULT NULL,
  `ProductID` int(11) DEFAULT NULL,
  `TransactionType` enum('Inbound','Outbound') DEFAULT NULL,
  `Quantity` int(11) DEFAULT NULL,
  `Remarks` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `transactions`
--

INSERT INTO `transactions` (`TransactionID`, `TransactionDate`, `ProductID`, `TransactionType`, `Quantity`, `Remarks`) VALUES
(1, '2024-04-01', 1, 'Outbound', 5, 'Sold to customer A'),
(2, '2024-04-03', 2, 'Outbound', 3, 'Sold to customer B'),
(3, '2024-04-05', 3, 'Inbound', 10, 'Received from supplier X'),
(4, '2024-04-08', 1, 'Outbound', 2, 'Sold to customer C'),
(5, '2024-04-10', 4, 'Inbound', 7, 'Received from supplier Y'),
(6, '2024-04-12', 2, 'Outbound', 4, 'Sold to customer D'),
(7, '2024-04-15', 5, 'Inbound', 6, 'Received from supplier Z'),
(8, '2024-04-18', 3, 'Outbound', 1, 'Sold to customer E'),
(9, '2024-04-20', 6, 'Inbound', 8, 'Received from supplier W'),
(10, '2024-04-22', 4, 'Outbound', 3, 'Sold to customer F');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`CustomerID`),
  ADD UNIQUE KEY `Email` (`Email`);

--
-- Indexes for table `employees`
--
ALTER TABLE `employees`
  ADD PRIMARY KEY (`EmployeeID`),
  ADD UNIQUE KEY `Email` (`Email`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`OrderID`),
  ADD KEY `CustomerID` (`CustomerID`),
  ADD KEY `ProductID` (`ProductID`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`ProductID`);

--
-- Indexes for table `suppliers`
--
ALTER TABLE `suppliers`
  ADD PRIMARY KEY (`SupplierID`);

--
-- Indexes for table `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`TransactionID`),
  ADD KEY `ProductID` (`ProductID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `customers`
--
ALTER TABLE `customers`
  MODIFY `CustomerID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT for table `employees`
--
ALTER TABLE `employees`
  MODIFY `EmployeeID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `OrderID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=60;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `ProductID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `suppliers`
--
ALTER TABLE `suppliers`
  MODIFY `SupplierID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `transactions`
--
ALTER TABLE `transactions`
  MODIFY `TransactionID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`CustomerID`) REFERENCES `customers` (`CustomerID`),
  ADD CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`ProductID`) REFERENCES `products` (`ProductID`);

--
-- Constraints for table `transactions`
--
ALTER TABLE `transactions`
  ADD CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`ProductID`) REFERENCES `products` (`ProductID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
