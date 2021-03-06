-- phpMyAdmin SQL Dump
-- version 5.0.4deb2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Dec 24, 2021 at 03:13 PM
-- Server version: 10.5.12-MariaDB-0+deb11u1
-- PHP Version: 7.4.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `esp_data`
--

-- --------------------------------------------------------

--
-- Table structure for table `MoonData`
--

CREATE TABLE `MoonData` (
  `id` int(6) UNSIGNED NOT NULL,
  `phase` varchar(30) NOT NULL,
  `illumination` float DEFAULT NULL,
  `age` float DEFAULT NULL,
  `diameter` float DEFAULT NULL,
  `reading_time` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `MoonData`
--

INSERT INTO `MoonData` (`id`, `phase`, `illumination`, `age`, `diameter`, `reading_time`) VALUES
(1, 'Waning Crescent', 0.08, 26.7508, 0.542111, '2021-12-01 22:00:02'),
(2, 'Waning Crescent', 0.05, 27.3186, 0.544158, '2021-12-02 10:00:02'),
(62, 'Waning Crescent', 0.03, 27.8933, 0.545822, '2021-12-02 22:00:02'),
(63, 'Waning Crescent', 0.01, 28.4734, 0.547064, '2021-12-03 10:00:02'),
(64, 'Dark Moon', 0, 29.0572, 0.547858, '2021-12-03 22:00:02'),
(65, 'New Moon', 0, 0.112387, 0.548187, '2021-12-04 10:00:02'),
(66, 'New Moon', 0.01, 0.69808, 0.548043, '2021-12-04 22:00:03'),
(67, 'New Moon', 0.02, 1.28182, 0.54743, '2021-12-05 10:00:02'),
(68, 'Waxing Crescent', 0.04, 1.86175, 0.546362, '2021-12-05 22:00:02'),
(69, 'Waxing Crescent', 0.07, 2.43627, 0.544862, '2021-12-06 10:00:03'),
(70, 'Waxing Crescent', 0.1, 3.0039, 0.542964, '2021-12-06 22:00:02'),
(71, 'Waxing Crescent', 0.14, 3.56349, 0.540708, '2021-12-07 10:00:02'),
(72, 'Waxing Crescent', 0.18, 4.11422, 0.538142, '2021-12-07 22:00:02'),
(73, 'Waxing Crescent', 0.23, 4.65552, 0.535315, '2021-12-08 10:00:02'),
(74, 'Waxing Crescent', 0.27, 5.18712, 0.532282, '2021-12-08 22:00:02'),
(75, 'Waxing Crescent', 0.33, 5.70904, 0.529099, '2021-12-09 10:00:02'),
(76, 'Waxing Crescent', 0.38, 6.22148, 0.52582, '2021-12-09 22:00:03'),
(77, 'Waxing Crescent', 0.43, 6.72487, 0.522497, '2021-12-10 10:00:02'),
(78, 'Waxing Crescent', 0.48, 7.21974, 0.519181, '2021-12-10 22:00:03'),
(79, '1st Quarter', 0.53, 7.70674, 0.515918, '2021-12-11 10:00:02'),
(80, 'Waxing Gibbous', 0.59, 8.18656, 0.51275, '2021-12-11 22:00:02'),
(81, 'Waxing Gibbous', 0.63, 8.65996, 0.509714, '2021-12-12 10:00:03'),
(82, 'Waxing Gibbous', 0.68, 9.12767, 0.506841, '2021-12-12 22:00:02'),
(83, 'Waxing Gibbous', 0.73, 9.59043, 0.50416, '2021-12-13 10:00:03'),
(84, 'Waxing Gibbous', 0.77, 10.0489, 0.501693, '2021-12-13 22:00:02'),
(85, 'Waxing Gibbous', 0.81, 10.5038, 0.499458, '2021-12-14 10:00:02'),
(86, 'Waxing Gibbous', 0.84, 10.9558, 0.497471, '2021-12-14 22:00:03'),
(87, 'Waxing Gibbous', 0.88, 11.4053, 0.495742, '2021-12-15 10:00:02'),
(88, 'Waxing Gibbous', 0.91, 11.853, 0.494281, '2021-12-15 22:00:03'),
(89, 'Waxing Gibbous', 0.93, 12.2992, 0.493094, '2021-12-16 10:00:02'),
(90, 'Waxing Gibbous', 0.95, 12.7445, 0.492184, '2021-12-16 22:00:03'),
(91, 'Waxing Gibbous', 0.97, 13.1891, 0.491556, '2021-12-17 10:00:02'),
(92, 'Waxing Gibbous', 0.99, 13.6335, 0.49121, '2021-12-17 22:00:02'),
(93, 'Waxing Gibbous', 0.99, 14.078, 0.491148, '2021-12-18 10:00:02'),
(94, 'Full Moon', 1, 14.5229, 0.491368, '2021-12-18 22:00:02'),
(95, 'Full Moon', 1, 14.9684, 0.491869, '2021-12-19 10:00:02'),
(96, 'Waning Gibbous', 1, 15.4149, 0.49265, '2021-12-19 22:00:02'),
(97, 'Waning Gibbous', 0.99, 15.8627, 0.493707, '2021-12-20 10:00:02'),
(98, 'Waning Gibbous', 0.97, 16.3119, 0.495036, '2021-12-20 22:00:02'),
(99, 'Waning Gibbous', 0.96, 16.763, 0.49663, '2021-12-21 10:00:02'),
(100, 'Waning Gibbous', 0.93, 17.2163, 0.498482, '2021-12-21 22:00:03'),
(101, 'Waning Gibbous', 0.91, 17.6721, 0.50058, '2021-12-22 10:00:02'),
(102, 'Waning Gibbous', 0.88, 18.1308, 0.502913, '2021-12-22 22:00:02'),
(103, 'Waning Gibbous', 0.84, 18.5927, 0.505462, '2021-12-23 10:00:03'),
(104, 'Waning Gibbous', 0.81, 19.0585, 0.508209, '2021-12-23 22:00:02'),
(105, 'Waning Gibbous', 0.76, 19.5285, 0.511129, '2021-12-24 10:00:02');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `MoonData`
--
ALTER TABLE `MoonData`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `MoonData`
--
ALTER TABLE `MoonData`
  MODIFY `id` int(6) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=106;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
