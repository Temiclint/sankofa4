-- phpMyAdmin SQL Dump
-- version 5.1.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 04, 2022 at 08:16 AM
-- Server version: 10.4.22-MariaDB
-- PHP Version: 7.4.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `amcl_2022`
--

-- --------------------------------------------------------

--
-- Table structure for table `amcl_states`
--

CREATE TABLE `amcl_states` (
  `state_id` int(5) NOT NULL,
  `state_statue` int(1) NOT NULL,
  `state_name` int(50) NOT NULL,
  `state_codedigit` int(5) NOT NULL,
  `state_codealpha` varchar(5) NOT NULL,
  `state_latitude` varchar(30) NOT NULL,
  `state_longitude` varchar(30) NOT NULL,
  `id_country` int(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `amcl_states`
--
ALTER TABLE `amcl_states`
  ADD PRIMARY KEY (`state_id`),
  ADD KEY `state_statue` (`state_statue`),
  ADD KEY `state_name` (`state_name`),
  ADD KEY `state_codedigit` (`state_codedigit`),
  ADD KEY `state_codealpha` (`state_codealpha`),
  ADD KEY `id_country` (`id_country`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `amcl_states`
--
ALTER TABLE `amcl_states`
  MODIFY `state_id` int(5) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
