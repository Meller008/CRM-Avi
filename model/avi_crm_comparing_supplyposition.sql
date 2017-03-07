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
-- Table structure for table `comparing_supplyposition`
--

DROP TABLE IF EXISTS `comparing_supplyposition`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comparing_supplyposition` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Material_SupplyId` int(11) DEFAULT NULL,
  `Accessories_SupplyId` int(11) DEFAULT NULL,
  `Comparing_NameId` int(11) NOT NULL,
  `Value` decimal(11,4) NOT NULL,
  `Price` decimal(11,4) NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `ForeginKey2_idx` (`Comparing_NameId`),
  KEY `C_S_P_FK1_idx` (`Material_SupplyId`),
  KEY `C_S_P_FK3_idx` (`Accessories_SupplyId`),
  CONSTRAINT `C_S_P_FK1` FOREIGN KEY (`Material_SupplyId`) REFERENCES `material_supply` (`Id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `C_S_P_FK2` FOREIGN KEY (`Comparing_NameId`) REFERENCES `comparing_name` (`Id`) ON UPDATE CASCADE,
  CONSTRAINT `C_S_P_FK3` FOREIGN KEY (`Accessories_SupplyId`) REFERENCES `accessories_supply` (`Id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comparing_supplyposition`
--

LOCK TABLES `comparing_supplyposition` WRITE;
/*!40000 ALTER TABLE `comparing_supplyposition` DISABLE KEYS */;
INSERT INTO `comparing_supplyposition` VALUES (1,35,NULL,3,1.0000,5000.0000),(2,35,NULL,4,2.0000,1000.0000);
/*!40000 ALTER TABLE `comparing_supplyposition` ENABLE KEYS */;
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
