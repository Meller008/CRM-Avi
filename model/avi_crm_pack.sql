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
-- Table structure for table `pack`
--

DROP TABLE IF EXISTS `pack`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pack` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Article_Parametr_Id` int(11) NOT NULL,
  `Cut_Id` int(11) NOT NULL,
  `Order_Id` int(11) DEFAULT NULL,
  `Number` tinyint(4) NOT NULL,
  `Value_Pieces` smallint(6) NOT NULL,
  `Value_Damage` smallint(6) NOT NULL DEFAULT '0',
  `Weight` decimal(11,4) NOT NULL,
  `Note` text,
  `Size` varchar(5) DEFAULT NULL,
  `Client_Id` int(11) DEFAULT NULL,
  `Date_Make` date DEFAULT NULL,
  `Date_Coplete` date DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `FK_PACK_1_idx` (`Article_Parametr_Id`),
  KEY `FK_PACK_2_idx` (`Cut_Id`),
  KEY `FK_PACK_4_idx` (`Client_Id`),
  KEY `FK_PACK_5_idx` (`Order_Id`),
  CONSTRAINT `FK_PACK_1` FOREIGN KEY (`Article_Parametr_Id`) REFERENCES `product_article_parametrs` (`Id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FK_PACK_2` FOREIGN KEY (`Cut_Id`) REFERENCES `cut` (`Id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FK_PACK_4` FOREIGN KEY (`Client_Id`) REFERENCES `clients` (`Id`) ON UPDATE CASCADE,
  CONSTRAINT `FK_PACK_5` FOREIGN KEY (`Order_Id`) REFERENCES `order` (`Id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pack`
--

LOCK TABLES `pack` WRITE;
/*!40000 ALTER TABLE `pack` DISABLE KEYS */;
/*!40000 ALTER TABLE `pack` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-03-29 15:22:02
