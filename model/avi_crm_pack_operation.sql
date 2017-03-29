CREATE DATABASE  IF NOT EXISTS `avi_crm` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `avi_crm`;
-- MySQL dump 10.13  Distrib 5.7.12, for Win64 (x86_64)
--
-- Host: 192.168.1.2    Database: avi_crm
-- ------------------------------------------------------
-- Server version	5.7.13-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `pack_operation`
--

DROP TABLE IF EXISTS `pack_operation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pack_operation` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Pack_Id` int(11) NOT NULL,
  `Operation_id` int(11) DEFAULT NULL,
  `Worker_Id` int(11) DEFAULT NULL,
  `Position` tinyint(2) DEFAULT NULL,
  `Name` varchar(65) NOT NULL,
  `Date_make` date DEFAULT NULL,
  `Date_Input` datetime DEFAULT NULL,
  `Value` int(11) DEFAULT NULL,
  `Price` decimal(11,4) DEFAULT NULL,
  `Pay` tinyint(1) NOT NULL,
  `Date_Pay` date DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `FK_P_O_1_idx` (`Pack_Id`),
  KEY `FK_P_O_1_idx1` (`Operation_id`),
  KEY `FK_P_O_2_idx` (`Worker_Id`),
  CONSTRAINT `FK_P_O_1` FOREIGN KEY (`Pack_Id`) REFERENCES `pack` (`Id`) ON UPDATE CASCADE,
  CONSTRAINT `FK_P_O_2` FOREIGN KEY (`Operation_id`) REFERENCES `operations` (`Id`) ON UPDATE CASCADE,
  CONSTRAINT `FK_P_O_3` FOREIGN KEY (`Worker_Id`) REFERENCES `staff_worker_info` (`Id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pack_operation`
--

LOCK TABLES `pack_operation` WRITE;
/*!40000 ALTER TABLE `pack_operation` DISABLE KEYS */;
/*!40000 ALTER TABLE `pack_operation` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-03-29 15:22:02
