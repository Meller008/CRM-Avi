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
-- Table structure for table `staff_worker_info`
--

DROP TABLE IF EXISTS `staff_worker_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `staff_worker_info` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `First_Name` varchar(40) NOT NULL,
  `Last_Name` varchar(40) NOT NULL,
  `Middle_Name` varchar(40) DEFAULT NULL,
  `Sex` varchar(1) NOT NULL,
  `Date_Birth` date NOT NULL,
  `Date_Recruitment` date NOT NULL,
  `Leave` int(1) NOT NULL,
  `Date_Leave` date DEFAULT NULL,
  `Country_Id` int(11) NOT NULL,
  `Phone` varchar(17) DEFAULT NULL,
  `Address` varchar(80) DEFAULT NULL,
  `Position_Id` int(11) NOT NULL,
  `INN` varchar(13) DEFAULT NULL,
  `SNILS` varchar(12) DEFAULT NULL,
  `Note` tinytext,
  `Birthplace` varchar(78) NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `FK_S_W_I_1_idx` (`Country_Id`),
  KEY `FK_S_W_I_2_idx` (`Position_Id`),
  CONSTRAINT `FK_S_W_I_1` FOREIGN KEY (`Country_Id`) REFERENCES `staff_country` (`Id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FK_S_W_I_2` FOREIGN KEY (`Position_Id`) REFERENCES `staff_position` (`Id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 COMMENT='Основная информация работника';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff_worker_info`
--

LOCK TABLES `staff_worker_info` WRITE;
/*!40000 ALTER TABLE `staff_worker_info` DISABLE KEYS */;
INSERT INTO `staff_worker_info` VALUES (1,'Наталья','Ширяева','Александровна','F','1972-06-17','2005-08-29',0,'2017-03-27',1,'','',1,'773005579077','06403544232','','Украина Днепропетровск'),(2,'Барон','Ходжаев','Собирович','M','1983-08-31','2016-11-07',0,'2017-03-27',2,'','Кутузовский проезд 16, строение 15',2,'775111594610','','','Узбекистан'),(3,'Нургуль ','Асанова','','F','1974-01-19','2017-03-13',0,'2017-03-27',3,'','Кутузовский проезд 16, строение 15',3,'','','','республика Кыргызстан'),(4,'Мухаббат ','Каюмова','','F','1977-08-09','2017-03-27',0,'2017-03-27',4,'','Кутузовский проезд 16, строение 15',4,'770176035970','','','Таджикистан'),(5,'Александр','Рублев','Александрович','M','1993-10-10','2016-03-10',0,'2017-03-28',1,'','',5,'','','','Новый Уренгой , Тюменская обл.'),(6,'Елена','Радько','Евгеньевна','F','1967-11-18','2014-09-17',0,'2017-03-28',5,'','Кутузовский проезд 16 строение 15, до 14.04.17',6,'771563338205','','','Украина'),(7,'Анна ','Радько','Сергеевна','F','1985-01-22','2015-04-17',1,'2017-03-13',5,'','Филевский бульвар, дом 40, кв.157',7,'773014499043','','','Украина');
/*!40000 ALTER TABLE `staff_worker_info` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-03-29 15:21:58
