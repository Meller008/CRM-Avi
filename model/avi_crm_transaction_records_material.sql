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
-- Table structure for table `transaction_records_material`
--

DROP TABLE IF EXISTS `transaction_records_material`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `transaction_records_material` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Supply_Balance_Id` int(11) NOT NULL,
  `Balance` decimal(11,4) NOT NULL,
  `Date` datetime NOT NULL,
  `Note` text,
  `Cut_Material_Id` int(11) DEFAULT NULL,
  `Beika_Id` int(11) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `FK_T_R_M_1_idx` (`Supply_Balance_Id`),
  KEY `FK_T_R_M_2_idx` (`Beika_Id`),
  CONSTRAINT `FK_T_R_M_1` FOREIGN KEY (`Supply_Balance_Id`) REFERENCES `material_balance` (`Id`) ON UPDATE CASCADE,
  CONSTRAINT `FK_T_R_M_2` FOREIGN KEY (`Beika_Id`) REFERENCES `beika` (`Id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transaction_records_material`
--

LOCK TABLES `transaction_records_material` WRITE;
/*!40000 ALTER TABLE `transaction_records_material` DISABLE KEYS */;
INSERT INTO `transaction_records_material` VALUES (1,55,-15.0000,'2017-01-11 22:23:45','Крой №24 Пачка №1 - Новая пачка в крое',24,NULL),(2,55,-14.5000,'2017-01-11 22:24:20','Крой №24 Пачка №2 - Новая пачка в крое',24,NULL),(3,55,-12.0000,'2017-01-11 22:24:45','Крой №24 Пачка №3 - Новая пачка в крое',24,NULL),(4,55,-12.2500,'2017-01-11 22:25:14','Крой №24 Пачка №4 - Новая пачка в крое',24,NULL),(5,55,-25.0000,'2017-01-11 22:26:06','Крой №24 - Увеличение обрези в крое',24,NULL),(6,55,-18.5400,'2017-01-11 23:00:26','Крой №24 Пачка №5 - Новая пачка в крое',24,NULL),(7,55,-11.9958,'2017-01-11 23:00:53','Крой №24 Пачка №6 - Новая пачка в крое',24,NULL),(8,55,-15.2240,'2017-01-11 23:01:36','Крой №24 Пачка №7 - Новая пачка в крое',24,NULL),(9,55,-16.2500,'2017-01-11 23:01:57','Крой №24 Пачка №8 - Новая пачка в крое',24,NULL),(10,56,-10.2500,'2017-01-11 23:14:59','Крой №25 Пачка №1 - Новая пачка в крое',25,NULL),(11,56,-11.3500,'2017-01-11 23:15:21','Крой №25 Пачка №2 - Новая пачка в крое',25,NULL),(12,56,-9.9580,'2017-01-11 23:16:00','Крой №25 Пачка №3 - Новая пачка в крое',25,NULL),(13,56,-12.2540,'2017-01-11 23:16:23','Крой №25 Пачка №4 - Новая пачка в крое',25,NULL),(14,56,-15.0000,'2017-01-11 23:16:25','Крой №25 - Увеличение обрези в крое',25,NULL),(15,55,-14.2500,'2017-01-11 23:22:12','Крой №26 Пачка №1 - Новая пачка в крое',26,NULL),(16,55,-14.9580,'2017-01-11 23:22:35','Крой №26 Пачка №2 - Новая пачка в крое',26,NULL),(17,55,-13.5000,'2017-01-11 23:23:53','Крой №26 Пачка №3 - Новая пачка в крое',26,NULL),(18,55,-13.5400,'2017-01-11 23:24:30','Крой №26 Пачка №4 - Новая пачка в крое',26,NULL),(19,55,-15.0000,'2017-01-11 23:24:31','Крой №26 - Увеличение обрези в крое',26,NULL),(20,62,-12.2500,'2017-01-11 23:28:19','Крой №27 Пачка №1 - Новая пачка в крое',27,NULL),(21,62,-10.2500,'2017-01-11 23:28:52','Крой №27 Пачка №2 - Новая пачка в крое',27,NULL),(22,62,-9.2540,'2017-01-11 23:29:19','Крой №27 Пачка №3 - Новая пачка в крое',27,NULL),(23,62,-10.2540,'2017-01-11 23:29:41','Крой №27 Пачка №4 - Новая пачка в крое',27,NULL),(24,62,-9.9980,'2017-01-11 23:30:01','Крой №27 Пачка №5 - Новая пачка в крое',27,NULL),(25,62,-11.2510,'2017-01-11 23:30:26','Крой №27 Пачка №6 - Новая пачка в крое',27,NULL),(26,62,-11.2540,'2017-01-11 23:30:43','Крой №27 Пачка №7 - Новая пачка в крое',27,NULL),(27,62,-9.2540,'2017-01-11 23:30:58','Крой №27 Пачка №8 - Новая пачка в крое',27,NULL),(28,62,-11.2250,'2017-01-11 23:31:17','Крой №27 Пачка №9 - Новая пачка в крое',27,NULL),(29,62,-11.2540,'2017-01-11 23:31:34','Крой №27 Пачка №10 - Новая пачка в крое',27,NULL),(30,62,-25.0000,'2017-01-11 23:31:35','Крой №27 - Увеличение обрези в крое',27,NULL),(31,55,-20.0000,'2017-01-18 15:58:34','Крой №26 Пачка №5 - Новая пачка в крое',26,NULL),(32,55,20.0000,'2017-01-18 16:00:59','Крой №26 Пачка №5 - Удаление пачки из кроя',26,NULL),(35,56,-5.0000,'2017-01-29 18:35:53','На нарезку бейки №1',NULL,1),(36,56,5.0000,'2017-01-29 20:15:59','Отмена нарезки бейки №1',NULL,1),(37,62,-5.0000,'2017-01-30 23:02:39','27 - Увеличение обрези в крое',27,NULL),(38,62,5.0000,'2017-01-30 23:02:52','27 - Уменьшение обрези в крое',27,NULL),(39,62,-5.0000,'2017-01-30 23:04:06','27 - Увеличение обрези в крое',27,NULL),(40,62,5.0000,'2017-01-30 23:04:12','27 - Уменьшение обрези в крое',27,NULL),(41,62,-5.0000,'2017-01-30 23:04:38','27 - Увеличение обрези в крое',27,NULL),(42,62,5.0000,'2017-01-30 23:04:41','27 - Уменьшение обрези в крое',27,NULL),(43,55,-50.0000,'2017-01-30 23:05:03','28 - Увеличение обрези в крое',28,NULL),(46,55,50.0000,'2017-01-30 23:15:53','28 - Возврат ткани из за удаления кроя',28,NULL),(47,55,-50.0000,'2017-01-30 23:18:11','29 - Увеличение обрези в крое',29,NULL),(48,55,50.0000,'2017-01-30 23:18:19','29 - Возврат ткани из за удаления кроя',29,NULL),(49,62,-0.5484,'2017-01-31 03:17:16','27 - Увеличение обрези в крое',27,NULL),(50,56,-0.8545,'2017-01-31 03:17:22','25 - Увеличение обрези в крое',25,NULL);
/*!40000 ALTER TABLE `transaction_records_material` ENABLE KEYS */;
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
