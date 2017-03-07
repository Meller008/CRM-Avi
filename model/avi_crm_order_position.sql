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
-- Table structure for table `order_position`
--

DROP TABLE IF EXISTS `order_position`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order_position` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Order_Id` int(11) NOT NULL,
  `Product_Article_Parametr_Id` int(11) NOT NULL,
  `Price` decimal(11,4) NOT NULL,
  `NDS` tinyint(3) unsigned NOT NULL,
  `Value` int(11) NOT NULL,
  `In_On_Place` mediumint(9) NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `FK_O_PO_1_idx` (`Order_Id`),
  KEY `FK_O_PO_2_idx` (`Product_Article_Parametr_Id`),
  CONSTRAINT `FK_O_PO_1` FOREIGN KEY (`Order_Id`) REFERENCES `order` (`Id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_O_PO_2` FOREIGN KEY (`Product_Article_Parametr_Id`) REFERENCES `product_article_parametrs` (`Id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=109 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_position`
--

LOCK TABLES `order_position` WRITE;
/*!40000 ALTER TABLE `order_position` DISABLE KEYS */;
INSERT INTO `order_position` VALUES (4,4,53,50.9000,10,580,0),(5,4,54,50.9000,10,790,0),(6,4,55,58.7000,10,680,0),(7,4,56,58.7000,10,620,0),(9,4,51,53.4000,10,220,0),(10,4,48,53.4000,10,120,0),(11,4,49,61.2000,10,110,0),(12,4,50,61.2000,10,300,0),(14,5,58,24.5000,10,420,60),(15,5,59,24.5000,10,300,60),(16,5,60,24.5000,10,660,60),(17,5,61,24.5000,10,480,60),(18,5,66,32.9700,10,144,24),(19,5,67,32.9700,10,96,24),(20,5,68,32.9700,10,72,24),(21,5,69,32.9700,10,48,60),(22,5,82,24.3800,10,300,60),(23,5,83,24.3800,10,180,60),(24,5,87,24.3800,10,300,60),(25,5,92,25.3000,10,180,60),(26,5,93,25.3000,10,240,60),(27,5,94,25.3000,10,240,60),(28,5,95,25.3000,10,180,60),(29,5,71,35.1000,10,240,60),(30,5,73,35.1000,10,60,60),(31,5,75,35.1000,10,60,60),(32,5,77,35.1000,10,120,60),(33,5,100,14.2100,10,600,60),(34,5,101,14.2100,10,540,60),(35,5,102,14.2100,10,420,60),(36,5,103,14.2100,10,480,60),(37,5,134,14.6000,10,420,60),(38,5,135,14.6000,10,600,60),(39,5,136,14.6000,10,420,60),(40,5,137,14.6000,10,660,60),(41,6,66,32.9700,10,48,24),(42,6,63,36.0900,10,48,24),(43,6,64,36.0900,10,24,24),(44,6,87,24.3800,10,60,60),(45,6,82,24.3800,10,60,60),(46,6,92,25.3000,10,120,60),(47,6,93,25.3000,10,60,60),(48,6,94,25.3000,10,120,60),(49,6,95,25.3000,10,60,60),(50,6,71,35.1000,10,60,60),(51,6,73,35.1000,10,120,60),(52,6,77,35.1000,10,60,60),(53,6,100,14.7700,10,480,60),(54,6,101,14.7700,10,600,60),(55,6,102,14.7700,10,240,60),(56,6,103,14.7700,10,420,60),(57,7,66,32.9700,10,768,24),(58,7,67,32.9700,10,768,24),(59,7,69,32.9700,10,384,24),(60,7,82,24.3800,10,1920,60),(61,7,83,24.3800,10,1920,60),(62,7,87,24.3800,10,1920,60),(63,7,92,25.3000,10,1920,60),(64,7,93,25.3000,10,1920,60),(65,7,94,25.3000,10,2880,60),(66,7,95,25.3000,10,2880,60),(67,7,71,35.1000,10,960,60),(68,7,73,35.1000,10,1440,60),(69,7,75,35.1000,10,1440,60),(70,7,77,35.1000,10,1440,60),(71,7,100,14.2100,10,7560,60),(72,7,101,14.2100,10,8400,60),(73,7,102,14.2100,10,6720,60),(74,7,103,14.2100,10,6720,60),(75,7,126,15.4500,10,3360,60),(76,7,127,15.4500,10,3360,60),(77,7,128,15.4500,10,3360,60),(78,7,129,15.4500,10,2520,60),(79,7,134,14.6000,10,1920,60),(80,7,135,14.6000,10,1920,60),(81,7,136,14.6000,10,2880,60),(82,7,137,14.6000,10,1920,60),(83,7,100,14.2100,10,1,60),(93,7,66,32.9700,10,1,24),(98,7,66,32.9700,10,1,24),(99,7,66,32.9700,10,1,24),(100,7,66,32.9700,10,1,24),(101,7,66,32.9700,10,1,24),(105,7,66,32.9700,10,1,24),(106,7,58,24.5000,10,1,60),(107,7,66,32.9700,10,1,24),(108,5,64,38.1818,10,2000,0);
/*!40000 ALTER TABLE `order_position` ENABLE KEYS */;
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
