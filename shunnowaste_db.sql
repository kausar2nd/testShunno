-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 24, 2025 at 07:09 AM
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
-- Database: `shunnowaste_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `admin_id` int(11) NOT NULL,
  `admin_email` varchar(20) NOT NULL,
  `admin_password` varchar(20) NOT NULL,
  `admin_created` date NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`admin_id`, `admin_email`, `admin_password`, `admin_created`) VALUES
(1, 'k@a.c', '123', '2024-12-13'),
(2, 'admin@test.com', '1234', '2024-12-13');

-- --------------------------------------------------------

--
-- Table structure for table `company`
--

CREATE TABLE `company` (
  `company_id` int(11) NOT NULL,
  `company_name` varchar(40) NOT NULL,
  `company_email` varchar(20) NOT NULL,
  `company_password` varchar(20) NOT NULL,
  `company_location` varchar(30) NOT NULL,
  `company_joining_date` date NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `company`
--

INSERT INTO `company` (`company_id`, `company_name`, `company_email`, `company_password`, `company_location`, `company_joining_date`) VALUES
(2, 'ChiP wire connedted', 'b@g.c', '123', 'Dhaka, Bangladesh', '2024-12-07'),
(3, 'TechCorp', 'info@techcorp.com', 'pass123', 'Silicon Valley', '2024-12-09'),
(4, 'MediCare', 'contact@medicare.com', 'pass456', 'New York', '2024-12-09'),
(5, 'EcoGreen', 'support@ecogreen.com', 'pass789', 'Texas', '2024-12-09'),
(6, 'EduWise', 'hello@eduwise.com', 'pass321', 'Florida', '2024-12-09'),
(7, 'Foodies', 'info@foodies.com', 'pass654', 'Washington', '2024-12-09'),
(8, 'AutoDrive', 'sales@autodrive.com', 'pass987', 'Michigan', '2024-12-09'),
(9, 'BuildSmart', 'team@buildsmart.com', 'pass159', 'Ohio', '2024-12-09'),
(10, 'SkyHigh', 'reach@skyhigh.com', 'pass753', 'Colorado', '2024-12-09'),
(11, 'NextGen', 'info@nextgen.com', 'pass852', 'Arizona', '2024-12-09'),
(12, 'BrightFuture', 'hello@brightfuture.c', 'pass951', 'Nevada', '2024-12-09'),
(13, 'test2', 'm@n.c', '123', 'ubn', '2024-12-13'),
(14, 'jobair', 'jobairhossain123@gma', 'mkbj@', 'Hazaribagh', '2025-04-23'),
(15, 'jobair', 'ab@g.com', '1122', 'Hazaribagh', '2025-04-23');

-- --------------------------------------------------------

--
-- Table structure for table `company_history`
--

CREATE TABLE `company_history` (
  `company_history_id` int(10) NOT NULL,
  `company_id` int(11) NOT NULL,
  `company_history_date` date NOT NULL DEFAULT current_timestamp(),
  `plastic_bottles` int(11) DEFAULT NULL,
  `cardboards` int(11) DEFAULT NULL,
  `glasses` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `company_history`
--

INSERT INTO `company_history` (`company_history_id`, `company_id`, `company_history_date`, `plastic_bottles`, `cardboards`, `glasses`) VALUES
(8, 2, '2025-03-14', 3, 3, 3),
(9, 2, '2025-04-23', 9, 5, 1),
(10, 15, '2025-04-23', 5, 2, 1);

-- --------------------------------------------------------

--
-- Table structure for table `storage`
--

CREATE TABLE `storage` (
  `plastic` int(11) DEFAULT 0,
  `cardboard` int(11) DEFAULT 0,
  `glass` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `storage`
--

INSERT INTO `storage` (`plastic`, `cardboard`, `glass`) VALUES
(69, 77, 49);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `user_id` int(11) NOT NULL,
  `user_name` varchar(20) NOT NULL,
  `user_email` varchar(30) NOT NULL,
  `user_password` varchar(20) NOT NULL,
  `user_location` varchar(20) NOT NULL,
  `user_points` int(11) DEFAULT NULL,
  `user_joining_date` date NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`user_id`, `user_name`, `user_email`, `user_password`, `user_location`, `user_points`, `user_joining_date`) VALUES
(15, 'Emran Khan musa', 'a@g.com', '123', 'Mohammadpur', 15, '2024-12-01'),
(16, 'John Doe', 'john1@example.com', 'pass123', 'New York', 0, '2024-12-09'),
(17, 'Jane Smith', 'jane2@example.com', 'pass456', 'Los Angeles', 0, '2024-12-09'),
(18, 'Alice Brown', 'alice3@example.com', 'pass789', 'Chicago', 0, '2024-12-09'),
(19, 'Bob White', 'bob4@example.com', 'pass321', 'Houston', 0, '2024-12-09'),
(20, 'Charlie Black', 'charlie5@example.com', 'pass654', 'Miami', 0, '2024-12-09'),
(21, 'Diana Grey', 'diana6@example.com', 'pass987', 'Seattle', 39, '2024-12-09'),
(22, 'Eve Green', 'eve7@example.com', 'pass159', 'San Francisco', 0, '2024-12-09'),
(23, 'Frank Blue', 'frank8@example.com', 'pass753', 'Austin', 0, '2024-12-09'),
(24, 'Grace Red', 'grace9@example.com', 'pass852', 'Boston', 0, '2024-12-09'),
(25, 'Hank Yellow', 'hank10@example.com', 'pass951', 'Denver', 0, '2024-12-09'),
(26, 'zodiac', 'q@w.c', '1234', 'unknown', 0, '2024-12-13'),
(27, 'Regan', 'brg@mail.com', 'reganoss', 'Farmgate', NULL, '2025-03-14'),
(28, 'jobair', 'ab@g.com', '1234', 'Hazaribagh', NULL, '2025-04-23'),
(29, 'Shadid', 'shadid@gmail.com', 'Shadid@196', 'Dahar, Nawabganj', NULL, '2025-04-23');

-- --------------------------------------------------------

--
-- Table structure for table `user_history`
--

CREATE TABLE `user_history` (
  `user_history_id` int(10) NOT NULL,
  `user_id` int(11) NOT NULL,
  `user_history_date` date NOT NULL DEFAULT current_timestamp(),
  `user_history_branch` varchar(20) DEFAULT NULL,
  `plastic_bottles` int(11) DEFAULT NULL,
  `cardboards` int(11) DEFAULT NULL,
  `glasses` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_history`
--

INSERT INTO `user_history` (`user_history_id`, `user_id`, `user_history_date`, `user_history_branch`, `plastic_bottles`, `cardboards`, `glasses`) VALUES
(18, 15, '2025-03-13', 'Mohammadpur', 1, 1, 1),
(19, 15, '2025-03-13', 'Dhanmondi', 5, 6, 6),
(20, 15, '2025-03-13', 'Dhanmondi', 2, 3, 4),
(21, 27, '2025-03-14', 'Mohammadpur', 3, 3, 3),
(22, 15, '2025-03-14', 'Dhanmondi', 1, 1, 1),
(23, 15, '2025-04-23', 'Mirpur - 10', 6, 8, 2),
(27, 21, '2025-04-23', 'Uttara', 5, 2, 9);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`admin_id`);

--
-- Indexes for table `company`
--
ALTER TABLE `company`
  ADD PRIMARY KEY (`company_id`);

--
-- Indexes for table `company_history`
--
ALTER TABLE `company_history`
  ADD PRIMARY KEY (`company_history_id`),
  ADD KEY `company_id` (`company_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`user_id`);

--
-- Indexes for table `user_history`
--
ALTER TABLE `user_history`
  ADD PRIMARY KEY (`user_history_id`),
  ADD KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `admin_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `company`
--
ALTER TABLE `company`
  MODIFY `company_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `company_history`
--
ALTER TABLE `company_history`
  MODIFY `company_history_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT for table `user_history`
--
ALTER TABLE `user_history`
  MODIFY `user_history_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `company_history`
--
ALTER TABLE `company_history`
  ADD CONSTRAINT `company_history_ibfk_1` FOREIGN KEY (`company_id`) REFERENCES `company` (`company_id`) ON DELETE CASCADE;

--
-- Constraints for table `user_history`
--
ALTER TABLE `user_history`
  ADD CONSTRAINT `user_history_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
