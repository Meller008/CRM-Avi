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
-- Table structure for table `receiving_issuing_material`
--

DROP TABLE IF EXISTS `receiving_issuing_material`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `receiving_issuing_material` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Id_Suppli` int(11) DEFAULT NULL,
  `Id_Material_Name` int(11) NOT NULL,
  `Value` decimal(11,4) NOT NULL,
  `Note` varchar(75) DEFAULT NULL,
  `Date` datetime NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `FK_R_I_M_1_idx` (`Id_Suppli`),
  KEY `FK_R_I_M_2_idx` (`Id_Material_Name`),
  CONSTRAINT `FK_R_I_M_1` FOREIGN KEY (`Id_Suppli`) REFERENCES `material_supplyposition` (`Id`) ON UPDATE CASCADE,
  CONSTRAINT `FK_R_I_M_2` FOREIGN KEY (`Id_Material_Name`) REFERENCES `material_name` (`Id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `receiving_issuing_material`
--

LOCK TABLES `receiving_issuing_material` WRITE;
/*!40000 ALTER TABLE `receiving_issuing_material` DISABLE KEYS */;
/*!40000 ALTER TABLE `receiving_issuing_material` ENABLE KEYS */;
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
