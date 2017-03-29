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
-- Table structure for table `operation_tree`
--

DROP TABLE IF EXISTS `operation_tree`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `operation_tree` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Parent_Id` int(11) NOT NULL,
  `Name` varchar(35) NOT NULL,
  `Position` tinyint(2) NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `operation_tree`
--

LOCK TABLES `operation_tree` WRITE;
/*!40000 ALTER TABLE `operation_tree` DISABLE KEYS */;
INSERT INTO `operation_tree` VALUES (3,0,'ОПЕРАЦИИ ОБЩИЕ',0),(4,0,'ТРУСЫ ЭКОНОМ',0),(5,4,'Женские',0),(6,4,'Девочка',0),(7,4,'Мальчик',0),(8,4,'Мужские',0),(9,0,'МАЙКИ, ФУТБ, КОМП. ЭКОНОМ',0),(10,9,'Женские',0),(11,9,'Девочка',0),(12,9,'Мальчик',0),(13,9,'Мужское',0),(14,0,'ОДЕЖДА ДЛЯ ДОМА ЭКОНОМ',0),(15,14,'Женское',0),(16,14,'Девочка',0),(17,14,'Мальчик',0),(18,14,'Мужское',0),(19,0,'ЯСЕЛЬКА ЭКОНОМ',0);
/*!40000 ALTER TABLE `operation_tree` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-03-29 15:22:01
