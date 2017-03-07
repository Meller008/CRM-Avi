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
-- Table structure for table `staff_worker_doc_number`
--

DROP TABLE IF EXISTS `staff_worker_doc_number`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `staff_worker_doc_number` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Worker_Info_Id` int(11) NOT NULL,
  `Name` varchar(15) NOT NULL,
  `Number` int(11) NOT NULL,
  `Date` date NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `FK_S_W_D_N_1_idx` (`Worker_Info_Id`),
  CONSTRAINT `FK_S_W_D_N_1` FOREIGN KEY (`Worker_Info_Id`) REFERENCES `staff_worker_info` (`Id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff_worker_doc_number`
--

LOCK TABLES `staff_worker_doc_number` WRITE;
/*!40000 ALTER TABLE `staff_worker_doc_number` DISABLE KEYS */;
INSERT INTO `staff_worker_doc_number` VALUES (1,32,'труд.дог.',1,'2015-06-06'),(2,32,'труд.дог.',2,'2015-06-06'),(3,32,'труд.дог.',3,'2015-06-06'),(4,32,'труд.дог.',1,'2016-06-06'),(5,32,'труд.дог.',2,'2016-06-06'),(6,32,'труд.дог.',3,'2016-06-06'),(7,32,'труд.дог.',4,'2016-06-06'),(8,32,'труд.дог.',5,'2016-06-06'),(9,32,'труд.дог.',6,'2016-06-06'),(10,32,'труд.дог.',7,'2016-06-06'),(11,32,'труд.дог.',8,'2016-06-06'),(12,32,'труд.дог.',9,'2016-06-06'),(13,32,'труд.дог.',10,'2016-06-06'),(14,32,'труд.дог.',10,'2016-06-06'),(15,32,'труд.дог.',10,'2016-06-06'),(16,32,'труд.дог.',10,'2016-06-06'),(17,32,'труд.дог.',10,'2016-06-06'),(18,32,'труд.дог.',10,'2016-06-06'),(19,32,'труд.дог.',10,'2016-06-06'),(20,32,'труд.дог.',10,'2016-06-06'),(21,32,'труд.дог.',10,'2016-06-06'),(22,32,'труд.дог.',10,'2016-06-06'),(23,32,'труд.дог.',10,'2016-06-06'),(24,32,'труд.дог.',10,'2016-06-06'),(25,32,'труд.дог.',10,'2016-06-06'),(26,32,'труд.дог.',10,'2016-06-06'),(27,32,'труд.дог.',11,'2016-06-06'),(28,32,'труд.дог.',12,'2016-06-06'),(29,32,'труд.дог.',13,'2016-06-06'),(30,32,'труд.дог.',14,'2016-06-06'),(31,32,'труд.дог.',15,'2016-06-06'),(32,32,'труд.дог.',16,'2016-06-06'),(34,32,'труд.дог.',17,'2016-06-06'),(35,32,'труд.дог.',18,'2016-06-06'),(36,32,'труд.дог.',19,'2016-06-06'),(37,32,'труд.дог.',20,'2016-06-06'),(38,32,'труд.дог.',1,'2017-06-06'),(39,32,'труд.дог.',21,'2016-06-07'),(40,32,'труд.дог.',22,'2016-06-07'),(41,32,'труд.дог.',23,'2016-06-07'),(42,32,'труд.дог.',24,'2016-06-08'),(43,32,'труд.дог.',25,'2016-06-08'),(44,32,'труд.дог.',26,'2016-06-08');
/*!40000 ALTER TABLE `staff_worker_doc_number` ENABLE KEYS */;
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
