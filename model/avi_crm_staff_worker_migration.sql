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
-- Table structure for table `staff_worker_migration`
--

DROP TABLE IF EXISTS `staff_worker_migration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `staff_worker_migration` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Worker_Info_Id` int(11) NOT NULL,
  `Serial` varchar(5) NOT NULL,
  `Number` varchar(8) NOT NULL,
  `KPP` varchar(15) NOT NULL,
  `Date_Validity_From` date NOT NULL,
  `Date_Validity_To` date NOT NULL,
  `Date_migration` date NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `FK_S_W_MI_1_idx` (`Worker_Info_Id`),
  CONSTRAINT `FK_S_W_MI_1` FOREIGN KEY (`Worker_Info_Id`) REFERENCES `staff_worker_info` (`Id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff_worker_migration`
--

LOCK TABLES `staff_worker_migration` WRITE;
/*!40000 ALTER TABLE `staff_worker_migration` DISABLE KEYS */;
INSERT INTO `staff_worker_migration` VALUES (3,25,'dfdf','dfdfd','dfdfdf','2016-05-26','2016-05-26','2015-12-01'),(4,26,'dfdf','dfdfd','dfdfdf','2016-05-26','2016-05-26','2015-12-01'),(5,27,'dfdf','dfdfd','dfdfdf','2016-05-26','2016-05-26','2015-12-01'),(6,11,'44','55','66','2016-05-27','2016-05-27','2015-12-01'),(8,32,'4521','2549947','Московский КПП','2016-05-31','2017-05-11','2015-12-01');
/*!40000 ALTER TABLE `staff_worker_migration` ENABLE KEYS */;
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
