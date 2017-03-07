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
-- Table structure for table `staff_worker_info`
--

DROP TABLE IF EXISTS `staff_worker_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `staff_worker_info` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `First_Name` varchar(40) NOT NULL,
  `Last_Name` varchar(40) NOT NULL,
  `Middle_Name` varchar(40) DEFAULT NULL,
  `Sex` varchar(1) NOT NULL,
  `Date_Birth` date NOT NULL,
  `Date_Recruitment` date NOT NULL,
  `Leave` int(1) NOT NULL,
  `Date_Leave` date DEFAULT NULL,
  `Country_Id` int(11) NOT NULL,
  `Phone` varchar(17) DEFAULT NULL,
  `Address` varchar(80) DEFAULT NULL,
  `Position_Id` int(11) NOT NULL,
  `INN` varchar(13) DEFAULT NULL,
  `SNILS` varchar(12) DEFAULT NULL,
  `Note` tinytext,
  `Birthplace` varchar(78) NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `FK_S_W_I_1_idx` (`Country_Id`),
  KEY `FK_S_W_I_2_idx` (`Position_Id`),
  CONSTRAINT `FK_S_W_I_1` FOREIGN KEY (`Country_Id`) REFERENCES `staff_country` (`Id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FK_S_W_I_2` FOREIGN KEY (`Position_Id`) REFERENCES `staff_position` (`Id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff_worker_info`
--

LOCK TABLES `staff_worker_info` WRITE;
/*!40000 ALTER TABLE `staff_worker_info` DISABLE KEYS */;
INSERT INTO `staff_worker_info` VALUES (11,'Имя 4','Фамилия 4','44','F','2016-05-05','2016-01-06',0,'2016-05-07',5,'55','66',4,'77','88','999\n999','fgfdgfd'),(12,'Имя 3','Фамилия 3','44','F','2016-05-05','2016-01-25',0,'2016-05-07',5,'55','66',4,'77','88','999\n999','2626'),(16,'Имя 2 ','Фамилия 2','','F','2016-05-26','2016-03-03',0,'2016-06-08',5,'','',8,'','','',''),(17,'Имя 1','Фамилия 1','','F','2016-05-26','2016-03-26',0,'2016-05-26',5,'','',8,'','','','123'),(19,'Имя 5','Фамилия 5','','F','2016-05-26','2016-07-26',0,'2016-05-26',5,'','',4,'','','',''),(20,'Имя 6','Фамилия 6','','F','2016-05-26','2014-05-26',0,'2014-05-26',5,'','',4,'','','','вава'),(22,'Имя 7','Фамилия 7','','F','2016-05-26','2016-10-26',0,'2016-05-26',5,'','',4,'','','',''),(23,'Имя 8','Фамилия 8','','F','2016-05-26','2016-10-09',0,'2016-05-26',5,'','',4,'','','',''),(24,'Имя 9','Фамилия 9','','F','2016-05-26','2016-12-26',0,'2016-05-26',5,'','',4,'','','',''),(25,'Имя 10','Фамилия 10','','F','2016-05-26','2016-12-26',0,'2016-05-26',5,'','',4,'','','',''),(26,'Имя 11','Фамилия 11','','F','2016-05-26','2015-01-26',0,'2016-05-26',5,'','',4,'','','',''),(27,'Имя 12','Фамилия 12','','F','2016-05-26','2015-03-26',0,'2016-05-26',5,'','',4,'','','',''),(28,'Имя 13','Фамилия 13','','F','2016-05-26','2015-05-26',0,'2016-05-26',5,'','',4,'','','',''),(29,'Имя 14','Фамилия 14','','F','2016-05-26','2015-08-26',0,'2017-05-26',5,'','',4,'','','',''),(30,'Имя 15','Фамилия 15','','F','2016-05-26','2015-11-26',0,'2016-05-26',5,'','',4,'','','',''),(31,'Имя 16','Фамилия 16','','F','2016-05-26','2016-05-26',0,'2016-05-26',5,'','',4,'','','',''),(32,'Александр','Рублев','Александрович','M','1993-10-10','2016-01-18',0,'2016-05-31',8,'89163961668','Филевский бульвар д41 к41',4,'123456789','173773169985','Директор нового цеха\nМолод\nКрасив )','г. Москва'),(34,'Имя17','Фамилия 17','','F','2016-06-09','2014-06-09',0,'2014-06-09',5,'','',4,'','','','trtrt');
/*!40000 ALTER TABLE `staff_worker_info` ENABLE KEYS */;
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
