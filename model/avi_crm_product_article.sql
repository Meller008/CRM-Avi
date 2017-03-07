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
-- Table structure for table `product_article`
--

DROP TABLE IF EXISTS `product_article`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_article` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Article` varchar(12) NOT NULL,
  `Name` varchar(60) DEFAULT NULL,
  `Tree_Id` int(11) NOT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `Article_UNIQUE` (`Article`),
  KEY `FK_P_A_1_idx` (`Tree_Id`),
  CONSTRAINT `FK_P_A_1` FOREIGN KEY (`Tree_Id`) REFERENCES `product_tree` (`Id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=72 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_article`
--

LOCK TABLES `product_article` WRITE;
/*!40000 ALTER TABLE `product_article` DISABLE KEYS */;
INSERT INTO `product_article` VALUES (54,'7515f','Кофточка ясельная',10),(56,'7515','Кофточка ясельная',10),(58,'7127','Боксеры для мальчика',11),(59,'7002','Майка д/дев. на резинке',11),(60,'7142','Майка детская белая широк. брет.',11),(61,'7135','Майка д/дев.(набивная)',11),(62,'7143','Майка для мальчика (с набивкой)',11),(63,'7122','Трусы для девочки (набивка)',11),(70,'7121','Трусы для дев. пришивн.',11),(71,'7113','Трусы для мальчика плавки',11);
/*!40000 ALTER TABLE `product_article` ENABLE KEYS */;
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
