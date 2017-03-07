CREATE DATABASE  IF NOT EXISTS `avi_crm` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `avi_crm`;
-- MySQL dump 10.13  Distrib 5.7.12, for Win64 (x86_64)
--
-- Host: localhost    Database: avi_crm
-- ------------------------------------------------------
-- Server version	5.7.17-log

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
-- Table structure for table `pay_worker`
--

DROP TABLE IF EXISTS `pay_worker`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pay_worker` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Worker_Id` int(11) NOT NULL,
  `Worker_Id_Insert` int(11) NOT NULL,
  `Reason_Id` int(11) NOT NULL,
  `Balance` decimal(11,4) NOT NULL,
  `Date_In_Pay` date NOT NULL,
  `Date_Input` date NOT NULL,
  `Note` varchar(150) DEFAULT NULL,
  `Pay` tinyint(1) NOT NULL,
  `Date_Pay` date DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `FK_P_W_1_idx` (`Worker_Id`),
  KEY `FK_P_W_2_idx` (`Worker_Id_Insert`),
  KEY `FK_P_W_3_idx` (`Reason_Id`),
  CONSTRAINT `FK_P_W_1` FOREIGN KEY (`Worker_Id`) REFERENCES `staff_worker_info` (`Id`) ON UPDATE CASCADE,
  CONSTRAINT `FK_P_W_2` FOREIGN KEY (`Worker_Id_Insert`) REFERENCES `staff_worker_info` (`Id`) ON UPDATE CASCADE,
  CONSTRAINT `FK_P_W_3` FOREIGN KEY (`Reason_Id`) REFERENCES `pay_reason` (`Id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pay_worker`
--

LOCK TABLES `pay_worker` WRITE;
/*!40000 ALTER TABLE `pay_worker` DISABLE KEYS */;
INSERT INTO `pay_worker` VALUES (10,11,32,1,150.0000,'2016-12-14','2017-01-12','',1,'2016-12-31'),(11,27,32,1,150.0000,'2016-12-20','2017-01-12','',1,'2016-12-31'),(12,11,32,2,-50.0000,'2016-12-23','2017-01-12','',1,'2016-12-31'),(13,34,32,2,-150.0000,'2016-12-07','2017-01-12','',1,'2016-12-31');
/*!40000 ALTER TABLE `pay_worker` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-03-07 22:27:31
