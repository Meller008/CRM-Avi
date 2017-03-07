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
-- Table structure for table `product_article_warehouse`
--

DROP TABLE IF EXISTS `product_article_warehouse`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_article_warehouse` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Id_Article_Parametr` int(11) NOT NULL,
  `Value_In_Warehouse` int(11) NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `FK_P_W_1_idx` (`Id_Article_Parametr`),
  CONSTRAINT `FK_P_A_W_1` FOREIGN KEY (`Id_Article_Parametr`) REFERENCES `product_article_parametrs` (`Id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_article_warehouse`
--

LOCK TABLES `product_article_warehouse` WRITE;
/*!40000 ALTER TABLE `product_article_warehouse` DISABLE KEYS */;
INSERT INTO `product_article_warehouse` VALUES (1,139,1000),(2,48,880),(3,49,1050),(4,50,700),(5,51,780),(6,52,1000),(7,53,420),(8,54,370),(9,55,480),(10,56,380),(11,57,1160),(12,58,1150),(13,139,1000),(14,59,1150),(15,60,1000),(16,61,1000),(17,62,1170),(18,66,1000),(19,63,1000),(20,67,1000),(21,64,1168),(22,68,1000),(23,65,1000),(24,69,1000),(25,70,1000),(26,71,1000),(27,72,1000),(28,73,1000),(29,74,1000),(30,75,1000),(31,76,1000),(32,77,1000),(33,78,1000),(34,79,1000),(35,80,1000),(36,82,1000),(37,83,1000),(38,85,1000),(39,86,1000),(40,87,1000),(41,88,1000),(42,92,1000),(43,89,1000),(44,93,1000),(45,90,1000),(46,94,1000),(47,91,1000),(48,95,1000),(49,96,1000),(50,100,1000),(51,97,1000),(52,101,1000),(53,98,1000),(54,102,1000),(55,99,1000),(56,103,1000),(57,122,1000),(58,126,1000),(59,123,1000),(60,127,1000),(61,124,1000),(62,128,1000),(63,125,1000),(64,129,1000),(65,130,1000),(66,134,1000),(67,131,1000),(68,135,1000),(69,132,1000),(70,136,1000),(71,133,1000),(72,137,1000);
/*!40000 ALTER TABLE `product_article_warehouse` ENABLE KEYS */;
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
