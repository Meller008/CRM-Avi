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
-- Table structure for table `staff_worker_passport`
--

DROP TABLE IF EXISTS `staff_worker_passport`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `staff_worker_passport` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Worker_Info_Id` int(11) NOT NULL,
  `Series` varchar(6) DEFAULT NULL,
  `Number` varchar(12) NOT NULL,
  `Issued` varchar(40) NOT NULL,
  `Data_Issued` date NOT NULL,
  `Date_Ending` date NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `FK_S_W_PA_1_idx` (`Worker_Info_Id`),
  CONSTRAINT `FK_S_W_PA_1` FOREIGN KEY (`Worker_Info_Id`) REFERENCES `staff_worker_info` (`Id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff_worker_passport`
--

LOCK TABLES `staff_worker_passport` WRITE;
/*!40000 ALTER TABLE `staff_worker_passport` DISABLE KEYS */;
INSERT INTO `staff_worker_passport` VALUES (3,24,'434','3434','34343','2016-05-26','2016-05-26'),(5,11,'11','22','33','2016-05-27','2016-05-27'),(6,32,'4513','330668','УФМС РОССИИ ЗАО ФИЛЕВСКИЙ ПАРК','2011-10-29','2036-10-29'),(8,12,'22','33','44','2016-06-09','2016-06-10');
/*!40000 ALTER TABLE `staff_worker_passport` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-03-07 22:27:32
