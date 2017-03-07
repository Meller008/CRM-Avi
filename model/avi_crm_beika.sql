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
-- Table structure for table `beika`
--

DROP TABLE IF EXISTS `beika`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `beika` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Material_Id` int(11) NOT NULL,
  `Accessories_Id` int(11) NOT NULL,
  `Worker_Id` int(11) NOT NULL,
  `Date` date NOT NULL,
  `Value` decimal(11,4) NOT NULL,
  `Finished` tinyint(1) NOT NULL,
  `Supply_Id` int(11) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `FK_B_1_idx` (`Material_Id`),
  KEY `FK_B_2_idx` (`Accessories_Id`),
  KEY `FK_B_3_idx` (`Worker_Id`),
  KEY `FK_B_4_idx` (`Supply_Id`),
  CONSTRAINT `FK_B_1` FOREIGN KEY (`Material_Id`) REFERENCES `material_name` (`Id`) ON UPDATE CASCADE,
  CONSTRAINT `FK_B_2` FOREIGN KEY (`Accessories_Id`) REFERENCES `accessories_name` (`Id`) ON UPDATE CASCADE,
  CONSTRAINT `FK_B_3` FOREIGN KEY (`Worker_Id`) REFERENCES `staff_worker_info` (`Id`) ON UPDATE CASCADE,
  CONSTRAINT `FK_B_4` FOREIGN KEY (`Supply_Id`) REFERENCES `accessories_supply` (`Id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `beika`
--

LOCK TABLES `beika` WRITE;
/*!40000 ALTER TABLE `beika` DISABLE KEYS */;
INSERT INTO `beika` VALUES (1,15,50,32,'2017-01-29',5.0000,0,NULL),(4,15,50,11,'2017-01-10',8.1500,0,NULL);
/*!40000 ALTER TABLE `beika` ENABLE KEYS */;
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
