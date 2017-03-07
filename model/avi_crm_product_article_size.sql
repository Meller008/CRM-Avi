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
-- Table structure for table `product_article_size`
--

DROP TABLE IF EXISTS `product_article_size`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_article_size` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Article_Id` int(11) NOT NULL,
  `Size` varchar(7) NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `FK_P_A_S_1_idx` (`Article_Id`),
  CONSTRAINT `FK_P_A_S_1` FOREIGN KEY (`Article_Id`) REFERENCES `product_article` (`Id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=118 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_article_size`
--

LOCK TABLES `product_article_size` WRITE;
/*!40000 ALTER TABLE `product_article_size` DISABLE KEYS */;
INSERT INTO `product_article_size` VALUES (55,54,'22'),(56,54,'24'),(57,54,'26'),(58,54,'20'),(59,54,'28'),(61,56,'20'),(62,56,'22'),(63,56,'24'),(64,56,'26'),(65,56,'28'),(67,58,'26'),(68,58,'28'),(69,58,'30'),(70,58,'32'),(71,59,'34'),(72,59,'36'),(73,59,'38'),(74,59,'40'),(75,60,'34'),(76,60,'36'),(77,60,'38'),(78,60,'40'),(79,61,'26'),(80,61,'28'),(83,61,'30'),(84,61,'32'),(85,62,'26'),(86,62,'28'),(87,62,'30'),(88,62,'32'),(89,63,'26'),(90,63,'28'),(91,63,'30'),(92,63,'32'),(110,70,'34'),(111,70,'36'),(112,70,'38'),(113,70,'40'),(114,71,'26'),(115,71,'28'),(116,71,'30'),(117,71,'32');
/*!40000 ALTER TABLE `product_article_size` ENABLE KEYS */;
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
