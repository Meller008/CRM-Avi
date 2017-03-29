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
-- Table structure for table `cut_mission_position`
--

DROP TABLE IF EXISTS `cut_mission_position`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cut_mission_position` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Cut_Mission_Id` int(11) NOT NULL,
  `Article_Parametr_Id` int(11) NOT NULL,
  `Material_Id` int(11) NOT NULL,
  `Value` smallint(5) unsigned DEFAULT NULL,
  `Value_Complete` smallint(5) unsigned DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `FK_C_M_P1_idx` (`Cut_Mission_Id`),
  KEY `FK_C_M_P2_idx` (`Article_Parametr_Id`),
  KEY `FK_C_M_P3_idx` (`Material_Id`),
  CONSTRAINT `FK_C_M_P1` FOREIGN KEY (`Cut_Mission_Id`) REFERENCES `cut_mission` (`Id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_C_M_P2` FOREIGN KEY (`Article_Parametr_Id`) REFERENCES `product_article_parametrs` (`Id`) ON UPDATE CASCADE,
  CONSTRAINT `FK_C_M_P3` FOREIGN KEY (`Material_Id`) REFERENCES `material_name` (`Id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cut_mission_position`
--

LOCK TABLES `cut_mission_position` WRITE;
/*!40000 ALTER TABLE `cut_mission_position` DISABLE KEYS */;
/*!40000 ALTER TABLE `cut_mission_position` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-03-29 15:22:00
