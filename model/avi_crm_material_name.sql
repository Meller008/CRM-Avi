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
-- Table structure for table `material_name`
--

DROP TABLE IF EXISTS `material_name`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `material_name` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(100) NOT NULL,
  `Information` text,
  `For_Beika` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`Id`),
  UNIQUE KEY `Name_UNIQUE` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `material_name`
--

LOCK TABLES `material_name` WRITE;
/*!40000 ALTER TABLE `material_name` DISABLE KEYS */;
INSERT INTO `material_name` VALUES (8,'Кулир с лайкрой 10% гладкокрашенный рулон','',0),(9,'Кулир белый','',0),(10,'Кулир гладкокрашенный','',0),(11,'Кулир гладкокрашенный Рулон','',1),(12,'Кулир КД меланж ассорти','',0),(13,'Кулир КД набивной','',0),(14,'Кулир набивной','',0),(15,'Кулир рулон реактив','',1),(17,'Кулир с лайкрой 10% белый рулон','',1),(19,'Кулир с лайкрой 10% набивка рулон','',0),(20,'Кулир с лайкрой 5% белый','',0),(21,'Кулир с лайкрой 5% г/крашенный','',0),(22,'Кулир с лайкрой 5% набивка','',0),(24,'Микрофибра','',0),(25,'Пике','',0),(26,'Рибана с лайкрой 5% белая','',0),(27,'Рибана х/б белая','',1),(28,'Рибана х/б г/крашенная Пе ','',0),(29,'Рибана х/б набивной','',0),(30,'Сток','',0),(31,'Термополотно','',0),(32,'Флис гладкокрашенный','',0),(33,'Флис набивной','',0),(34,'Футер г/крашенный пачка','',0),(35,'Футер набивной пачка','',0),(36,'Шифон','',0),(37,'Акрил','',0),(38,'Ассорти (Халатка+Г/кр. Март16)','',0),(39,'Атлас стрейч','',0),(40,'Велюр','',0),(41,'Висколин','',0),(42,'Интерлок белый Пе','',0),(43,'Интерлок г/крашенный Пе','',0),(44,'Интерлок набивной','',0),(45,'Кашкорсе','',0);
/*!40000 ALTER TABLE `material_name` ENABLE KEYS */;
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
