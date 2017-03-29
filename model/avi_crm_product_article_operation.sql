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
-- Table structure for table `product_article_operation`
--

DROP TABLE IF EXISTS `product_article_operation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_article_operation` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Product_Article_Parametrs_Id` int(11) NOT NULL,
  `Operation_Id` int(11) NOT NULL,
  `Position` tinyint(4) NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `FK_P_A_O_FK_1_idx` (`Product_Article_Parametrs_Id`),
  KEY `FK_P_A_O_FK_2_idx` (`Operation_Id`),
  CONSTRAINT `FK_P_A_O_FK_1` FOREIGN KEY (`Product_Article_Parametrs_Id`) REFERENCES `product_article_parametrs` (`Id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_P_A_O_FK_2` FOREIGN KEY (`Operation_Id`) REFERENCES `operations` (`Id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=596 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_article_operation`
--

LOCK TABLES `product_article_operation` WRITE;
/*!40000 ALTER TABLE `product_article_operation` DISABLE KEYS */;
INSERT INTO `product_article_operation` VALUES (554,1,3,1),(555,1,4,2),(556,1,5,3),(557,1,6,4),(558,1,7,5),(559,1,8,6),(560,3,3,1),(561,3,4,2),(562,3,5,3),(563,3,6,4),(564,3,7,5),(565,3,8,6),(566,4,3,1),(567,4,4,2),(568,4,5,3),(569,4,6,4),(570,4,7,5),(571,4,8,6),(572,5,3,1),(573,5,4,2),(574,5,5,3),(575,5,6,4),(576,5,7,5),(577,5,8,6),(578,6,9,1),(579,6,10,2),(580,6,5,3),(581,6,11,4),(582,6,7,5),(583,6,8,6),(584,7,9,1),(585,7,10,2),(586,7,5,3),(587,7,11,4),(588,7,7,5),(589,7,8,6),(590,8,9,1),(591,8,10,2),(592,8,5,3),(593,8,11,4),(594,8,7,5),(595,8,8,6);
/*!40000 ALTER TABLE `product_article_operation` ENABLE KEYS */;
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
