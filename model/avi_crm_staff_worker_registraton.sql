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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff_worker_registraton`
--

LOCK TABLES `staff_worker_registraton` WRITE;
/*!40000 ALTER TABLE `staff_worker_registraton` DISABLE KEYS */;
INSERT INTO `staff_worker_registraton` VALUES (1,16,'sdsadasd','2016-05-26','2016-05-26','2016-05-26'),(2,26,'dfdfdf','2016-05-25','2016-05-26','2016-05-27'),(3,27,'dfdfdf','2016-05-26','2016-05-26','2016-05-26'),(4,11,'77','2016-05-27','2016-05-27','2016-07-07'),(5,32,'Москва Кутузовский проезд дом 16 строение 15','2015-12-04','2002-08-08','2016-05-31');
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

-- Dump completed on 2017-03-07 22:27:29
