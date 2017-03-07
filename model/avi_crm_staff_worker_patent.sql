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
-- Table structure for table `staff_worker_patent`
--

DROP TABLE IF EXISTS `staff_worker_patent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `staff_worker_patent` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Worker_Info_Id` int(11) NOT NULL,
  `Serial` varchar(4) NOT NULL,
  `Number` varchar(9) NOT NULL,
  `Additional_Number` varchar(10) NOT NULL,
  `Issued` varchar(38) NOT NULL,
  `Data_Issued` date NOT NULL,
  `Date_Ending` date NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `FK_S_W_P_1_idx` (`Worker_Info_Id`),
  CONSTRAINT `FK_S_W_P_1` FOREIGN KEY (`Worker_Info_Id`) REFERENCES `staff_worker_info` (`Id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff_worker_patent`
--

LOCK TABLES `staff_worker_patent` WRITE;
/*!40000 ALTER TABLE `staff_worker_patent` DISABLE KEYS */;
INSERT INTO `staff_worker_patent` VALUES (1,17,'','','','','2016-05-26','2016-05-26'),(3,27,'dfd','fdf','dfdfdf','dfdf','2016-05-26','2016-05-26'),(4,11,'88','99','00','00','2016-05-27','2016-05-27'),(5,32,'77','15464271','РК 1590585','ОВТМ УФМС РОССИИ ПО Г МОСКВЕ','2015-12-24','2016-06-18');
/*!40000 ALTER TABLE `staff_worker_patent` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-03-07 22:27:30
