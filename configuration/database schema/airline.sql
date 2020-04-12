-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Generation Time: Mar 30, 2020 at 12:36 PM
-- Server version: 5.7.26
-- PHP Version: 7.3.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `Airlines`
--

-- --------------------------------------------------------

--
-- Table structure for table `airline_info`
--

CREATE TABLE `airline_info` (
  `airlineID` varchar(128) NOT NULL PRIMARY KEY,
  `airlineName` varchar(128) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `airline_info`
--

INSERT INTO `airline_info` (`airlineID`, `airlineName`) VALUES
('3U', 'Sichuan Airlines'),
('4O', 'Interjet'),
('4U', 'Germanwings GmbH'),
('5D', 'Aerolitoral S.A. de C.V.'),
('5J', 'Cebu Pacific Air'),
('5X', 'UPS Airlines'),
('6E', 'Interglobe Aviation Ltd. dba Indigo'),
('9C', 'Spring Airlines Limited Corporation'),
('9E', 'Endeavor Air'),
('9W', 'Jet Airways'),
('AA', 'American Airlines'),
('AB', 'Air Berlin'),
('AC', 'Air Canada'),
('AD', 'Azul Brazilian Airlines'),
('AF', 'Air France'),
('AI', 'Air India'),
('AK', 'AirAsia Berhad dba AirAsia'),
('AM', 'Aeromexico'),
('AS', 'Alaska Airlines'),
('AV', 'AVIANCA'),
('AX', 'Trans States Airlines, LLC'),
('AZ', 'Alitalia'),
('B6', 'JetBlue'),
('BA', 'British Airways'),
('BE', 'flybe'),
('BR', 'EVA Air'),
('BY', 'Thomson Airways Limited'),
('CA', 'Air China Limited'),
('CI', 'China Airlines'),
('CM', 'COPA Airlines'),
('CP', 'Compass Airlines LLC'),
('CX', 'Cathay Pacific'),
('CZ', 'China Southern Airlines'),
('DL', 'Delta Air Lines'),
('DY', 'Norwegian Air Shuttle A.S.'),
('EK', 'Emirates'),
('ET', 'Ethiopian Airlines'),
('EY', 'Etihad Airways'),
('F9', 'Frontier Airlines, Inc.'),
('FM', 'Shanghai Airlines'),
('FR', 'Ryanair Ltd.'),
('FX', 'Federal Express'),
('G3', 'VRG Linhas Aereas S.A. - Grupo GOL'),
('G4', 'Allegiant Air LLC'),
('GA', 'Garuda'),
('GS', 'Tianjin Airlines'),
('HU', 'Hainan Airlines'),
('IB', 'IBERIA'),
('JD', 'Capital Airlines'),
('JJ', 'TAM Linhas Aereas'),
('JL', 'Japan Airlines'),
('JQ', 'Jetstar Airways Pty Limited'),
('JT', 'Lion Airlines'),
('KE', 'Korean Air'),
('KL', 'KLM'),
('LA', 'Lan Airlines'),
('LH', 'Lufthansa Cargo'),
('LS', 'Jet2.com Limited'),
('LX', 'SWISS'),
('MF', 'Xiamen Airlines'),
('MH', 'Malaysia Airlines'),
('MQ', 'Envoy Air Inc.'),
('MU', 'China Eastern'),
('NH', 'All Nippon Airways'),
('NK', 'Spirit Airlines'),
('OH', 'PSA Airlines'),
('OO', 'SkyWest Airlines'),
('OS', 'Austrian'),
('OZ', 'Asiana'),
('PC', 'Pegasus Airlines'),
('PR', 'Philippine Airlines'),
('QF', 'Qantas'),
('QK', 'Jazz Aviation LP'),
('QR', 'Qatar Airways'),
('RW', 'Republic Airlines'),
('S5', 'Shuttle America'),
('S7', 'S7 Airlines'),
('SC', 'Shandong Airlines'),
('SK', 'SAS'),
('SQ', 'SIA Cargo'),
('SU', 'Aeroflot'),
('SV', 'Saudi Arabian Airlines'),
('TG', 'Thai Airways International'),
('TK', 'THY - Turkish Airlines'),
('TP', 'TAP Portugal'),
('U2', 'Easyjet Airline Company Limited'),
('UA', 'United Airlines'),
('UT', 'UTair'),
('VA', 'Virgin Australia'),
('VN', 'Vietnam Airlines'),
('VX', 'Virgin America'),
('VY', 'Vueling'),
('W6', 'Wizz Air Hungary Ltd.'),
('WN', 'Southwest Airlines Co.'),
('WS', 'WestJet'),
('XE', 'Expressjet'),
('Y4', 'Volaris'),
('YV', 'Mesa Airlines, Inc.'),
('ZH', 'Shenzhen Airlines'),
('ZW', 'Air Wisconsin Airlines Corporation (AWAC)');

-- --------------------------------------------------------

--
-- Table structure for table `airport_info`
--

CREATE TABLE `airport_info` (
  `iataCode` varchar(128) NOT NULL PRIMARY KEY,
  `airportName` varchar(128) NOT NULL,
  `country` varchar(128) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `airport_info`
--

INSERT INTO `airport_info` (`iataCode`, `airportName`, `country`) VALUES
('ATL', 'Hartsfield-jackson Atlanta International Aiprot', 'Atlanta, Georgia'),
('BKK', 'Suvarnabhumi Airport', 'Bangkok'),
('DXB', 'Dubai International Airport', 'Dubai'),
('HKG', 'Hong Kong International Airport', 'Hong Kong'),
('HND', 'Tokyo Haneda Airport', 'Tokyo'),
('ICN', 'Seoul Incheon International Airport', 'Incheon'),
('LAS', 'McCarran International Airport', 'Las Vegas'),
('LHR', 'London Heathrow Airport', 'London'),
('PEK', 'Beijing Capital International Airport', 'Beijing'),
('PVG', 'Shanghai Pudong International Airport', 'Pudong, Shanghai'),
('SFO', 'San Francisco International Airport', 'San Francisco'),
('SIN', 'Singapore Changi Airport', 'Singapore'),
('SZX', 'Shenzhen Bao an International Airport', 'Shen Zhen');

-- --------------------------------------------------------

--
-- Table structure for table `flight_info`
--

CREATE TABLE `flight_info` (
  `flightId` int(11) NOT NULL PRIMARY KEY,
  `flightNumber` varchar(128) NOT NULL,
  `airlineId` varchar(128) NOT NULL,
  `origin` varchar(128) NOT NULL,
  `destination` varchar(128) NOT NULL,
  `outbound` varchar(128) NOT NULL,
  `inbound` varchar(128) DEFAULT NULL,
  `outbound_time` varchar(128) NOT NULL,
  `inbound_time` varchar(128) DEFAULT NULL,
  `flightDuration` int(128) NOT NULL,
  `seatsLeft` int(11) NOT NULL,
  `price` float(10,0) NOT NULL,
  `Class` varchar(128) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `flight_info`
--

INSERT INTO `flight_info` (`flightId`, `flightNumber`, `airlineId`, `origin`, `destination`, `outbound`, `inbound`, `outbound_time`, `inbound_time`, `flightDuration`, `seatsLeft`, `price`, `Class`) VALUES
(2, '720', 'SQ', 'ATL', 'BKK', '2020-03-20', '2020-04-14', '2020-03-20 16:25:00', '2020-04-14 20:10:00', 126600, 7, 548, 'Y'),
(3, '833', 'SQ', 'ATL', 'BKK', '2020-03-20', '2020-04-14', '2020-03-20 12:25:00', '2020-04-14 20:55:00', 115200, 9, 820, 'Y'),
(4, '721', 'SQ', 'ATL', 'HND', '2020-03-20', '2020-04-14', '2020-03-20 16:25:00', '2020-04-14 17:05:00', 123000, 7, 755, 'Y'),
(5, '722', 'SQ', 'ATL', 'PEK', '2020-03-20', '2020-04-14', '2020-03-20 16:25:00', '2020-04-14 16:35:00', 124500, 7, 952, 'Y'),
(6, '723', 'SQ', 'ATL', 'PVG', '2020-03-20', '2020-04-14', '2020-03-20 16:25:00', '2020-04-14 16:50:00', 123000, 4, 861, 'Y'),
(7, '724', 'SQ', 'ATL', 'SIN', '2020-03-20', '2020-04-14', '2020-03-20 16:25:00', '2020-04-14 09:25:00', 95100, 7, 592, 'Y'),
(8, '979', 'SQ', 'BKK', 'ATL', '2020-03-20', '2020-04-14', '2020-03-20 18:10:00', '2020-04-14 16:21:00', 185640, 6, 458, 'Y'),
(9, '981', 'SQ', 'BKK', 'DXB', '2020-03-20', '2020-04-14', '2020-03-20 21:10:00', '2020-04-14 20:00:00', 88500, 7, 450, 'Y'),
(10, '981', 'SQ', 'BKK', 'HKG', '2020-03-20', '2020-04-14', '2020-03-20 21:10:00', '2020-04-14 12:25:00', 51300, 9, 888, 'Y'),
(11, '979', 'SQ', 'BKK', 'HND', '2020-03-20', '2020-04-14', '2020-03-20 18:10:00', '2020-04-14 02:05:00', 36600, 9, 100, 'Y'),
(12, '981', 'SQ', 'BKK', 'LAS', '2020-03-20', '2020-04-14', '2020-03-20 21:10:00', '2020-04-14 18:50:00', 111480, 4, 235, 'Y'),
(13, '979', 'SQ', 'BKK', 'LHR', '2020-03-20', '2020-04-14', '2020-03-20 18:10:00', '2020-04-14 09:25:00', 67500, 9, 134, 'Y'),
(14, '983', 'SQ', 'BKK', 'PEK', '2020-03-20', '2020-04-14', '2020-03-20 21:10:00', '2020-04-14 00:05:00', 60600, 9, 152, 'Y'),
(15, '981', 'SQ', 'BKK', 'PVG', '2020-03-20', '2020-04-14', '2020-03-20 21:10:00', '2020-04-14 00:35:00', 59100, 9, 159, 'Y'),
(16, '975', 'SQ', 'BKK', 'SIN', '2020-03-20', '2020-04-14', '2020-03-20 12:15:00', '2020-04-14 07:10:00', 9000, 9, 431, 'Y'),
(17, '495', 'SQ', 'DXB', 'BKK', '2020-03-20', '2020-04-14', '2020-03-20 20:00:00', '2020-04-14 09:40:00', 56100, 7, 368, 'Y'),
(18, '496', 'SQ', 'DXB', 'HKG', '2020-03-20', '2020-04-14', '2020-03-20 20:00:00', '2020-04-14 09:05:00', 44700, 9, 473, 'Y'),
(19, '497', 'SQ', 'DXB', 'HND', '2020-03-20', '2020-04-14', '2020-03-20 20:00:00', '2020-04-14 02:05:00', 52500, 9, 446, 'Y'),
(20, '498', 'SQ', 'DXB', 'PEK', '2020-03-20', '2020-04-14', '2020-03-20 20:00:00', '2020-04-14 00:05:00', 54000, 7, 502, 'Y'),
(21, '499', 'SQ', 'DXB', 'PVG', '2020-03-20', '2020-04-14', '2020-03-20 20:00:00', '2020-04-14 08:05:00', 52500, 7, 505, 'Y'),
(22, '495', 'SQ', 'DXB', 'SIN', '2020-03-20', '2020-04-14', '2020-03-20 20:00:00', '2020-04-14 15:10:00', 26100, 7, 360, 'Y'),
(23, '861', 'SQ', 'HKG', 'ATL', '2020-03-20', '2020-04-14', '2020-03-20 15:50:00', '2020-04-14 16:21:00', 197940, 1, 150, 'Y'),
(24, '862', 'SQ', 'HKG', 'BKK', '2020-03-20', '2020-04-14', '2020-03-20 15:45:00', '2020-04-14 15:30:00', 64500, 9, 149, 'Y'),
(25, '863', 'SQ', 'HKG', 'DXB', '2020-03-20', '2020-04-14', '2020-03-20 15:40:00', '2020-04-14 20:00:00', 111600, 9, 492, 'Y'),
(26, '864', 'SQ', 'HKG', 'HND', '2020-03-20', '2020-04-14', '2020-03-20 15:45:00', '2020-04-14 02:05:00', 48900, 9, 489, 'Y'),
(27, '865', 'SQ', 'HKG', 'LAS', '2020-03-20', '2020-04-14', '2020-03-20 15:55:00', '2020-04-14 18:50:00', 114300, 1, 158, 'Y'),
(28, '866', 'SQ', 'HKG', 'LHR', '2020-03-20', '2020-04-14', '2020-03-20 16:45:00', '2020-04-14 11:25:00', 79800, 9, 219, 'Y'),
(29, '867', 'SQ', 'HKG', 'PEK', '2020-03-20', '2020-04-14', '2020-03-20 17:45:00', '2020-04-14 00:05:00', 83700, 9, 372, 'Y'),
(30, '868', 'SQ', 'HKG', 'PVG', '2020-03-20', '2020-04-14', '2020-03-20 18:45:00', '2020-04-14 08:05:00', 82200, 9, 372, 'Y'),
(31, '869', 'SQ', 'HKG', 'SFO', '2020-03-20', '2020-04-14', '2020-03-20 15:45:00', '2020-04-14 11:30:00', 71700, 4, 373, 'Y'),
(32, '863', 'SQ', 'HKG', 'SIN', '2020-03-20', '2020-04-14', '2020-03-20 14:10:00', '2020-04-14 07:25:00', 14400, 9, 156, 'Y'),
(33, '635', 'SQ', 'HND', 'BKK', '2020-03-20', '2020-04-14', '2020-03-20 22:50:00', '2020-04-14 09:40:00', 42600, 4, 321, 'Y'),
(34, '635', 'SQ', 'HND', 'DXB', '2020-03-20', '2020-04-14', '2020-03-20 22:50:00', '2020-04-14 20:00:00', 89700, 9, 675, 'Y'),
(35, '633', 'SQ', 'HND', 'LHR', '2020-03-20', '2020-04-14', '2020-03-20 16:40:00', '2020-04-14 09:25:00', 85200, 9, 499, 'Y'),
(36, '590', 'SQ', 'HND', 'SIN', '2020-03-20', '2020-04-14', '2020-03-20 00:30:00', '2020-04-14 08:00:00', 26700, 9, 317, 'Y'),
(37, '110', 'SQ', 'SIN', 'BKK', '2020-03-20', '2020-04-14', '2020-03-20 00:30:00', '2020-04-14 02:00:00', 34000, 1231, 250, 'Y'),
(38, '111', 'AF', 'SIN', 'BKK', '2020-03-20', '2020-04-14', '2020-03-20 01:30:00', '2020-04-14 03:30:00', 34000, 1231, 200, 'Y'),
(39, '112', 'AI', 'SIN', 'BKK', '2020-03-20', '2020-04-14', '2020-03-20 06:30:00', '2020-04-14 08:30:00', 34000, 1231, 150, 'Y'),
(40, '113', 'AS', 'SIN', 'BKK', '2020-03-20', '2020-04-14', '2020-03-20 10:30:00', '2020-04-14 12:30:00', 34000, 1231, 180, 'Y'),
(41, '114', 'SQ', 'SIN', 'BKK', '2020-03-20', '2020-04-14', '2020-03-20 12:30:00', '2020-04-14 14:30:00', 34000, 1231, 230, 'Y'),
(42, '115', 'SQ', 'SIN', 'BKK', '2020-03-20', '2020-04-14', '2020-03-20 14:30:00', '2020-04-14 16:30:00', 34000, 1231, 235, 'Y'),
(43, '800', 'SQ', 'SIN', 'ICN', '2020-03-20', '2020-04-14', '2020-03-20 14:30:00', '2020-04-14 22:30:00', 136000, 123, 750, 'Y'),
(44, '801', 'AF', 'SIN', 'ICN', '2020-03-20', '2020-04-14', '2020-03-20 15:30:00', '2020-04-14 23:30:00', 136000, 123, 600, 'Y'),
(45, '802', 'AI', 'SIN', 'ICN', '2020-03-20', '2020-04-14', '2020-03-20 10:30:00', '2020-04-14 18:30:00', 136000, 123, 800, 'Y'),
(46, '803', 'AS', 'SIN', 'ICN', '2020-03-20', '2020-04-14', '2020-03-20 11:30:00', '2020-04-14 19:30:00', 136000, 123, 550, 'Y'),
(47, '804', 'SQ', 'SIN', 'ICN', '2020-03-20', '2020-04-14', '2020-03-20 12:30:00', '2020-04-14 20:30:00', 136000, 123, 500, 'Y');




--
ALTER TABLE `flight_info`
  MODIFY `flightId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=43;
