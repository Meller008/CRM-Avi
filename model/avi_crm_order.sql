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
-- Table structure for table `order`
--

DROP TABLE IF EXISTS `order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Client_Id` int(11) NOT NULL,
  `Clients_Vendor_Id` int(11) DEFAULT NULL,
  `Clients_Adress_Id` int(11) DEFAULT NULL,
  `Transport_Company_Id` int(11) DEFAULT NULL,
  `Date_Order` date NOT NULL,
  `Date_Shipment` date DEFAULT NULL,
  `Number_Order` varchar(11) DEFAULT NULL,
  `Number_Doc` smallint(6) unsigned NOT NULL,
  `Note` text,
  `Cut_Mission_Id` int(11) DEFAULT NULL,
  `Shipped` tinyint(1) NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `FK_OR_1_idx` (`Clients_Vendor_Id`),
  KEY `FK_OR_2_idx` (`Clients_Adress_Id`),
  KEY `FK_OR_3_idx` (`Transport_Company_Id`),
  KEY `FK_OR_4_idx` (`Client_Id`),
  KEY `FK_OR_5_idx` (`Cut_Mission_Id`),
  CONSTRAINT `FK_OR_1` FOREIGN KEY (`Clients_Vendor_Id`) REFERENCES `clients_vendor_number` (`Id`) ON UPDATE CASCADE,
  CONSTRAINT `FK_OR_2` FOREIGN KEY (`Clients_Adress_Id`) REFERENCES `clients_actual_address` (`Id`) ON UPDATE CASCADE,
  CONSTRAINT `FK_OR_3` FOREIGN KEY (`Transport_Company_Id`) REFERENCES `order_transport_company` (`Id`) ON UPDATE CASCADE,
  CONSTRAINT `FK_OR_4` FOREIGN KEY (`Client_Id`) REFERENCES `clients` (`Id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order`
--

LOCK TABLES `order` WRITE;
/*!40000 ALTER TABLE `order` DISABLE KEYS */;
/*!40000 ALTER TABLE `order` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-03-29 15:22:01
