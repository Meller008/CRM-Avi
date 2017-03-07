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
-- Table structure for table `transaction_records_rest`
--

DROP TABLE IF EXISTS `transaction_records_rest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `transaction_records_rest` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Cut_Id` int(11) DEFAULT NULL,
  `Date` date NOT NULL,
  `Balance` decimal(11,4) NOT NULL,
  `Note` varchar(255) NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `FK_T_R_R_1_idx` (`Cut_Id`),
  CONSTRAINT `FK_T_R_R_1` FOREIGN KEY (`Cut_Id`) REFERENCES `cut` (`Id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transaction_records_rest`
--

LOCK TABLES `transaction_records_rest` WRITE;
/*!40000 ALTER TABLE `transaction_records_rest` DISABLE KEYS */;
INSERT INTO `transaction_records_rest` VALUES (1,27,'2017-01-29',5.0000,'27 - Увеличение обрези в крое'),(2,27,'2017-01-30',-5.0000,'27 - Уменьшение обрези в крое'),(3,27,'2017-01-30',5.0000,'27 - Увеличение обрези в крое'),(4,27,'2017-01-30',-5.0000,'27 - Уменьшение обрези в крое'),(5,27,'2017-01-30',5.0000,'27 - Увеличение обрези в крое'),(6,27,'2017-01-30',-5.0000,'27 - Уменьшение обрези в крое'),(7,NULL,'2017-01-30',50.0000,'28 - Увеличение обрези в крое'),(8,NULL,'2017-01-30',50.0000,'29 - Увеличение обрези в крое'),(9,NULL,'2017-01-30',50.0000,'29 - Удаление кроя'),(10,27,'2017-01-31',0.5484,'27 - Увеличение обрези в крое'),(11,25,'2017-01-31',0.8545,'25 - Увеличение обрези в крое'),(12,NULL,'2017-01-31',-1.0000,'Test 1'),(13,NULL,'2017-01-31',1.0000,'T'),(14,NULL,'2017-01-31',1.0000,''),(15,NULL,'2017-01-31',1.0000,''),(16,NULL,'2017-01-31',1.0000,''),(17,NULL,'2017-01-31',-1.4029,''),(18,NULL,'2017-01-31',-1.0000,'');
/*!40000 ALTER TABLE `transaction_records_rest` ENABLE KEYS */;
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
