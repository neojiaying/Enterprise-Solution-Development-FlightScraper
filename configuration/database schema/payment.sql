-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Generation Time: Mar 30, 2020 at 12:47 PM
-- Server version: 5.7.26
-- PHP Version: 7.3.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `Payment`
--

-- --------------------------------------------------------

--
-- Table structure for table `payment_info`
--

CREATE TABLE `payment_info` (
  `paymentID` int(11) NOT NULL,
  `bookingID` int(11) NOT NULL,
  `email` varchar(128) NOT NULL,
  `billing_address` varchar(268) NOT NULL,
  `country` varchar(128) NOT NULL,
  `zip` int(128) NOT NULL,
  `total_cost` int(11) NOT NULL,
  `name_on_card` varchar(128) DEFAULT NULL,
  `card_number` varchar(128) DEFAULT NULL,
  `exp_date` varchar(128) DEFAULT NULL,
  `cvv` varchar(128) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `payment_info`
--

--
-- Indexes for dumped tables
--

--
-- Indexes for table `payment_info`
--
ALTER TABLE `payment_info`
  ADD PRIMARY KEY (`paymentID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `payment_info`
--
ALTER TABLE `payment_info`
  MODIFY `paymentID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;
