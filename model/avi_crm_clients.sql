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
-- Table structure for table `clients`
--

DROP TABLE IF EXISTS `clients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clients` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(35) NOT NULL,
  `Legal_Address` text,
  `Actual_Address` text,
  `INN` varchar(15) DEFAULT NULL,
  `KPP` varchar(15) DEFAULT NULL,
  `OGRN` varchar(15) DEFAULT NULL,
  `Account` varchar(25) DEFAULT NULL,
  `Bank` text,
  `corres_Account` varchar(25) DEFAULT NULL,
  `BIK` varchar(12) DEFAULT NULL,
  `Contact_Person` varchar(45) DEFAULT NULL,
  `Phone` varchar(15) DEFAULT NULL,
  `Mail` varchar(45) DEFAULT NULL,
  `Note` text,
  `No_Nds` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `Name_UNIQUE` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clients`
--

LOCK TABLES `clients` WRITE;
/*!40000 ALTER TABLE `clients` DISABLE KEYS */;
INSERT INTO `clients` VALUES (1,'ООО \"АШАН\"','141014, Московская облась, Мытищинский р-н, г.Мытищи, шоссе Осташковское, 1','141014, Московская облась, Мытищинский р-н, г.Мытищи, шоссе Осташковское, 1','7703270067','509950001','','40702810000000100268','ООО \"Эйч-Эс-Би-Си Банк\"','30101810400000000351','044525351','','','','',1),(7,'ИП Шагдарова И.В.','295022, РФ, Республика Крым,г.Симферополь,пр-т Победы, д.211Д, кв.19','670033 г.Улан-Удэ, ул.Шумяцкого , д.3А.','032500432033','','','40802810609160104387','В Бурятском ОСБ №8601 г.Улан -Удэ','30101810400000000604','048142604','','','','',0);
/*!40000 ALTER TABLE `clients` ENABLE KEYS */;
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
