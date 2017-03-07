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
-- Table structure for table `clients_actual_address`
--

DROP TABLE IF EXISTS `clients_actual_address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clients_actual_address` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Client_Id` int(11) NOT NULL,
  `Name` varchar(45) NOT NULL,
  `Adres` text NOT NULL,
  `KPP` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `FK_C_A_ADD_1_idx` (`Client_Id`),
  CONSTRAINT `FK_C_A_ADD_1` FOREIGN KEY (`Client_Id`) REFERENCES `clients` (`Id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clients_actual_address`
--

LOCK TABLES `clients_actual_address` WRITE;
/*!40000 ALTER TABLE `clients_actual_address` DISABLE KEYS */;
INSERT INTO `clients_actual_address` VALUES (8,1,'ООО \"АШАН\" Белая Дача','ООО \"АШАН\" Белая Дача, Люберецкий р-н, г.Котельники, Яничкин проезд, 3',''),(9,1,'ООО \"АШАН\" г.Верхняя Пышма','ООО \"АШАН\" г.Верхняя Пышма, п.Залесье, Индустриальный проезд, 1, корп.1',''),(10,1,'ООО \"АШАН\" г.Ростов-на-Дону','ООО \"АШАН\" г.Ростов-на-Дону, Логопарк Дон, Аксайский р-н, х Большой Лог, Новочеркасское шоссе, 111',''),(11,1,'ООО \"АШАН\" г.Самара','ООО \"АШАН\" г.Самара, Московское шоссе (18 км), 27Б',''),(12,1,'ООО \"АШАН\" г.Санкт-Петербург, п.Шушары','ООО \"АШАН\" г.Санкт-Петербург, п.Шушары, Московское шоссе, д.177, корп.2, литера Б',''),(13,1,'ООО \"АШАН\" г.Санкт-Петербург, ФМ Парнас','ООО \"АШАН\" г.Санкт-Петербург, ФМ Парнас, 1-й Верхний пер., 12Б',''),(14,1,'ООО \"АШАН\" Новосибирский р-н','ООО \"АШАН\" Новосибирский р-н, с.Толмачево, Толмчевский с/с, о.п.3307 км, 16',''),(15,7,'Улан-Удэ, ул.Шумяцкого','670033 г.Улан-Удэ, ул.Шумяцкого , д.3А.',''),(16,7,'г.Иркутск, ул.Розы Люксембург','г.Иркутск, ул.Розы Люксембург, д.184','');
/*!40000 ALTER TABLE `clients_actual_address` ENABLE KEYS */;
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
