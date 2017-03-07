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
-- Table structure for table `accessories_supply`
--

DROP TABLE IF EXISTS `accessories_supply`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accessories_supply` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Accessories_ProviderId` int(11) NOT NULL,
  `Data` date NOT NULL,
  `Note` text,
  PRIMARY KEY (`Id`),
  KEY `A_S_FK1_idx` (`Accessories_ProviderId`),
  CONSTRAINT `A_S_FK1` FOREIGN KEY (`Accessories_ProviderId`) REFERENCES `accessories_provider` (`Id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accessories_supply`
--

LOCK TABLES `accessories_supply` WRITE;
/*!40000 ALTER TABLE `accessories_supply` DISABLE KEYS */;
INSERT INTO `accessories_supply` VALUES (4,4,'2016-08-05','сч 5498 от 02.08.16, сумма 76459,20'),(5,5,'2016-06-01','нак 459 от 04.05.16, сумма 68300,00'),(6,6,'2016-09-01','сч 308 от 08.07.15, сумма 6700,00'),(7,7,'2016-08-12','Для баланса ярлыков'),(8,4,'2016-10-13','Test'),(11,8,'2016-12-27','test Pack 1'),(12,8,'2016-12-27','test Pack 2'),(13,8,'2016-12-27','test Pack 3'),(14,8,'2016-12-15','Тест для кроя'),(15,5,'2016-11-16','Тест'),(16,8,'2017-01-11','');
/*!40000 ALTER TABLE `accessories_supply` ENABLE KEYS */;
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
