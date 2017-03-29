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
-- Table structure for table `operations`
--

DROP TABLE IF EXISTS `operations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `operations` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Tree_Id` int(11) NOT NULL,
  `Name` varchar(100) NOT NULL,
  `Price` decimal(11,4) NOT NULL,
  `Sewing_Machine_Id` int(11) NOT NULL,
  `Note` text,
  PRIMARY KEY (`Id`),
  KEY `FK_OPER_1_idx` (`Tree_Id`),
  KEY `FK_OPER_2_idx` (`Sewing_Machine_Id`),
  CONSTRAINT `FK_OPER_1` FOREIGN KEY (`Tree_Id`) REFERENCES `operation_tree` (`Id`) ON UPDATE CASCADE,
  CONSTRAINT `FK_OPER_2` FOREIGN KEY (`Sewing_Machine_Id`) REFERENCES `sewing_machine` (`Id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `operations`
--

LOCK TABLES `operations` WRITE;
/*!40000 ALTER TABLE `operations` DISABLE KEYS */;
INSERT INTO `operations` VALUES (3,5,'Лв 50..1 Ластовица открытая жен. 42-50',0.9300,1,'ВТАЧАТЬ ОТКРЫТУЮ ДВОЙНУЮ ЛАСТОВИЦУ'),(4,5,'ТЖБэ 2 Окантовать ножки 42-50',1.2800,3,'ПРИТАЧАТЬ (ОКАНТОВАТЬ) ЭЛАСТИЧНУЮ ТЕСЬМУ ПО НОЖКАМ ТРУСОВ\n'),(5,5,'ТЖБэ 3 Боковой шов с закрепом',0.5400,1,'СТАЧАТЬ ОДИН БОКОВОЙ ШОВ С ЗАКРЕПОМ'),(6,5,'ТЖБэ 4 Окантовать верх 42-50',0.8900,3,'ПРИТАЧАТЬ (ОКАНТОВАТЬ) ЭЛАСТИЧНУЮ ТЕСЬМУ ПО ВЕРХНЕМУ СРЕЗУ'),(7,5,'ТЖБэ 5 Боковой шов с закрепами',0.6800,1,'СТАЧАТЬ ВТОРОЙ БОКОВОЙ ШОВ С ЗАКРЕПАМИ С ДВУХ СТОРОН'),(8,3,'уп ТЖБ-Э Трусы КД по 10 шт + этикетка',0.5100,4,'ВЫВЕРНУТЬ И СЛОЖИТЬ ПО 10 ШТ. + БУМАЖНЫЙ СТИКЕР'),(9,5,'Лв 56..1 Ластовица открытая жен. 52-56',0.9600,1,'ВТАЧАТЬ ОТКРЫТУЮ ДВОЙНУЮ ЛАСТОВИЦУ'),(10,5,'ТЖБэ 2 Окантовать ножки 52-56',1.4100,3,'ПРИТАЧАТЬ (ОКАНТОВАТЬ) ЭЛАСТИЧНУЮ ТЕСЬМУ ПО НОЖКАМ ТРУСОВ\n'),(11,5,'ТЖБэ 4 Окантовать верх 52-56',0.9300,3,'ПРИТАЧАТЬ (ОКАНТОВАТЬ) ЭЛАСТИЧНУЮ ТЕСЬМУ ПО ВЕРХНЕМУ СРЕЗУ');
/*!40000 ALTER TABLE `operations` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-03-29 15:21:44
