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
-- Table structure for table `staff_worker_registraton`
--

DROP TABLE IF EXISTS `staff_worker_registraton`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `staff_worker_registraton` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Worker_Info_id` int(11) NOT NULL,
  `Address` varchar(90) NOT NULL,
  `Date_Registration` date DEFAULT NULL,
  `Date_Validity_From` date DEFAULT NULL,
  `Date_Validity_To` date DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `FK_S_W_RE_1_idx` (`Worker_Info_id`),
  CONSTRAINT `FK_S_W_RE_1` FOREIGN KEY (`Worker_Info_id`) REFERENCES `staff_worker_info` (`Id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff_worker_registraton`
--

LOCK TABLES `staff_worker_registraton` WRITE;
/*!40000 ALTER TABLE `staff_worker_registraton` DISABLE KEYS */;
INSERT INTO `staff_worker_registraton` VALUES (1,2,'Кутузовский проезд 16, строение 15','2017-03-23','2016-10-08','2017-04-26'),(4,3,'Кутузовский проезд 16, строение15','2017-03-13','2017-03-10','2017-06-07'),(5,4,'Кутузовский проезд 16, строение 15','2017-02-28','2017-02-23','2017-05-23'),(6,6,'Кутузовский проезд 16, строение 15','2017-01-17','2017-03-26','2017-03-29'),(7,1,'Филевский бульвар, дом 40, кв.157','1998-10-13','1998-10-13','1998-10-13');
/*!40000 ALTER TABLE `staff_worker_registraton` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-03-29 15:21:45
