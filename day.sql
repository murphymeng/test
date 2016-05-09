-- phpMyAdmin SQL Dump
-- version 4.1.14
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: May 09, 2016 at 04:51 PM
-- Server version: 5.6.17
-- PHP Version: 5.5.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `stock`
--

-- --------------------------------------------------------

--
-- Table structure for table `day`
--

CREATE TABLE IF NOT EXISTS `test` (
  `id` int(11) NOT NULL,
  `symbol` varchar(55) NOT NULL,
  `open` decimal(10,2) NOT NULL,
  `high` decimal(10,2) NOT NULL,
  `close` decimal(10,2) NOT NULL,
  `low` decimal(10,2) NOT NULL,
  `volume` decimal(12,0) NOT NULL,
  `volume_rate` decimal(10,2) NOT NULL,
  `chg` decimal(10,2) NOT NULL,
  `percent` decimal(10,2) NOT NULL,
  `turnrate` decimal(10,2) NOT NULL,
  `ma5` decimal(10,2) NOT NULL,
  `ma10` decimal(10,2) NOT NULL,
  `ma20` decimal(10,2) NOT NULL,
  `ma30` decimal(10,2) NOT NULL,
  `dif` decimal(10,2) NOT NULL,
  `dea` decimal(10,2) NOT NULL,
  `macd` float NOT NULL,
  `time` date NOT NULL,
  `newhigh30` tinyint(1) NOT NULL,
  `newhigh60` tinyint(1) NOT NULL,
  `newhigh120` tinyint(1) NOT NULL,
  `r_newhigh30` tinyint(1) NOT NULL,
  `high_day` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`symbol`,`time`),
  KEY `time` (`time`),
  KEY `symbol` (`symbol`),
  KEY `symbol_2` (`symbol`),
  KEY `time_2` (`time`),
  KEY `newhigh30` (`newhigh30`),
  KEY `macd` (`macd`),
  KEY `percent` (`percent`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
