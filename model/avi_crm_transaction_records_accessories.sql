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
-- Table structure for table `transaction_records_accessories`
--

DROP TABLE IF EXISTS `transaction_records_accessories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `transaction_records_accessories` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Supply_Balance_Id` int(11) NOT NULL,
  `Balance` decimal(11,4) NOT NULL,
  `Date` datetime NOT NULL,
  `Note` text,
  `Pack_Accessories_Id` int(11) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `FK_T_R_A_1_idx` (`Supply_Balance_Id`),
  CONSTRAINT `FK_T_R_A_1` FOREIGN KEY (`Supply_Balance_Id`) REFERENCES `accessories_balance` (`Id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=148 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transaction_records_accessories`
--

LOCK TABLES `transaction_records_accessories` WRITE;
/*!40000 ALTER TABLE `transaction_records_accessories` DISABLE KEYS */;
INSERT INTO `transaction_records_accessories` VALUES (21,7,-5709.6000,'2017-01-11 22:23:45','Крой №24 Пачка №1 - Добавление фурнитуры в пачку',9),(22,12,-40.0000,'2017-01-11 22:23:45','Крой №24 Пачка №1 - Добавление фурнитуры в пачку',10),(23,13,-80.0000,'2017-01-11 22:23:45','Крой №24 Пачка №1 - Добавление фурнитуры в пачку',10),(24,14,-96.0000,'2017-01-11 22:23:45','Крой №24 Пачка №1 - Добавление фурнитуры в пачку',10),(25,10,-90.0000,'2017-01-11 22:23:45','Крой №24 Пачка №1 - Добавление фурнитуры в пачку',11),(26,8,-18.0000,'2017-01-11 22:23:45','Крой №24 Пачка №1 - Добавление фурнитуры в пачку',12),(27,7,-6084.0000,'2017-01-11 22:24:20','Крой №24 Пачка №2 - Добавление фурнитуры в пачку',13),(28,8,-18.0000,'2017-01-11 22:24:20','Крой №24 Пачка №2 - Добавление фурнитуры в пачку',14),(29,14,-239.4000,'2017-01-11 22:24:20','Крой №24 Пачка №2 - Добавление фурнитуры в пачку',15),(30,10,-90.0000,'2017-01-11 22:24:20','Крой №24 Пачка №2 - Добавление фурнитуры в пачку',16),(31,7,-6679.8000,'2017-01-11 22:24:45','Крой №24 Пачка №3 - Добавление фурнитуры в пачку',17),(32,8,-18.0000,'2017-01-11 22:24:45','Крой №24 Пачка №3 - Добавление фурнитуры в пачку',18),(33,14,-261.0000,'2017-01-11 22:24:45','Крой №24 Пачка №3 - Добавление фурнитуры в пачку',19),(34,10,-90.0000,'2017-01-11 22:24:45','Крой №24 Пачка №3 - Добавление фурнитуры в пачку',20),(35,7,-7081.2000,'2017-01-11 22:25:14','Крой №24 Пачка №4 - Добавление фурнитуры в пачку',21),(36,8,-18.0000,'2017-01-11 22:25:14','Крой №24 Пачка №4 - Добавление фурнитуры в пачку',22),(37,14,-271.8000,'2017-01-11 22:25:14','Крой №24 Пачка №4 - Добавление фурнитуры в пачку',23),(38,10,-90.0000,'2017-01-11 22:25:14','Крой №24 Пачка №4 - Добавление фурнитуры в пачку',24),(39,7,-5709.6000,'2017-01-11 23:00:26','Крой №24 Пачка №5 - Добавление фурнитуры в пачку',25),(40,14,-181.8000,'2017-01-11 23:00:26','Крой №24 Пачка №5 - Добавление фурнитуры в пачку',26),(41,15,-34.2000,'2017-01-11 23:00:26','Крой №24 Пачка №5 - Добавление фурнитуры в пачку',26),(42,16,-180.0000,'2017-01-11 23:00:26','Крой №24 Пачка №5 - Добавление фурнитуры в пачку',27),(43,10,-90.0000,'2017-01-11 23:00:26','Крой №24 Пачка №5 - Добавление фурнитуры в пачку',28),(44,7,-6084.0000,'2017-01-11 23:00:53','Крой №24 Пачка №6 - Добавление фурнитуры в пачку',29),(45,15,-239.4000,'2017-01-11 23:00:53','Крой №24 Пачка №6 - Добавление фурнитуры в пачку',30),(46,16,-180.0000,'2017-01-11 23:00:53','Крой №24 Пачка №6 - Добавление фурнитуры в пачку',31),(47,10,-90.0000,'2017-01-11 23:00:53','Крой №24 Пачка №6 - Добавление фурнитуры в пачку',32),(48,7,-6679.8000,'2017-01-11 23:01:36','Крой №24 Пачка №7 - Добавление фурнитуры в пачку',33),(49,15,-261.0000,'2017-01-11 23:01:36','Крой №24 Пачка №7 - Добавление фурнитуры в пачку',34),(50,16,-180.0000,'2017-01-11 23:01:36','Крой №24 Пачка №7 - Добавление фурнитуры в пачку',35),(51,10,-90.0000,'2017-01-11 23:01:36','Крой №24 Пачка №7 - Добавление фурнитуры в пачку',36),(52,7,-6679.8000,'2017-01-11 23:01:57','Крой №24 Пачка №8 - Добавление фурнитуры в пачку',37),(53,15,-261.0000,'2017-01-11 23:01:57','Крой №24 Пачка №8 - Добавление фурнитуры в пачку',38),(54,16,-180.0000,'2017-01-11 23:01:57','Крой №24 Пачка №8 - Добавление фурнитуры в пачку',39),(55,10,-90.0000,'2017-01-11 23:01:57','Крой №24 Пачка №8 - Добавление фурнитуры в пачку',40),(56,17,-54.0000,'2017-01-11 23:14:59','Крой №25 Пачка №1 - Добавление фурнитуры в пачку',41),(57,7,-5475.0000,'2017-01-11 23:14:59','Крой №25 Пачка №1 - Добавление фурнитуры в пачку',42),(58,16,-150.0000,'2017-01-11 23:14:59','Крой №25 Пачка №1 - Добавление фурнитуры в пачку',43),(59,10,-75.0000,'2017-01-11 23:14:59','Крой №25 Пачка №1 - Добавление фурнитуры в пачку',44),(60,17,-57.0000,'2017-01-11 23:15:21','Крой №25 Пачка №2 - Добавление фурнитуры в пачку',45),(61,7,-5670.0000,'2017-01-11 23:15:21','Крой №25 Пачка №2 - Добавление фурнитуры в пачку',46),(62,16,-150.0000,'2017-01-11 23:15:21','Крой №25 Пачка №2 - Добавление фурнитуры в пачку',47),(63,10,-75.0000,'2017-01-11 23:15:21','Крой №25 Пачка №2 - Добавление фурнитуры в пачку',48),(64,17,-63.0000,'2017-01-11 23:16:00','Крой №25 Пачка №3 - Добавление фурнитуры в пачку',49),(65,7,-6090.0000,'2017-01-11 23:16:00','Крой №25 Пачка №3 - Добавление фурнитуры в пачку',50),(66,16,-150.0000,'2017-01-11 23:16:00','Крой №25 Пачка №3 - Добавление фурнитуры в пачку',51),(67,10,-75.0000,'2017-01-11 23:16:00','Крой №25 Пачка №3 - Добавление фурнитуры в пачку',52),(68,17,-70.5000,'2017-01-11 23:16:23','Крой №25 Пачка №4 - Добавление фурнитуры в пачку',53),(69,7,-6720.0000,'2017-01-11 23:16:23','Крой №25 Пачка №4 - Добавление фурнитуры в пачку',54),(70,16,-150.0000,'2017-01-11 23:16:23','Крой №25 Пачка №4 - Добавление фурнитуры в пачку',55),(71,10,-75.0000,'2017-01-11 23:16:23','Крой №25 Пачка №4 - Добавление фурнитуры в пачку',56),(72,7,-5392.4000,'2017-01-11 23:22:12','Крой №26 Пачка №1 - Добавление фурнитуры в пачку',57),(73,15,-204.0000,'2017-01-11 23:22:12','Крой №26 Пачка №1 - Добавление фурнитуры в пачку',58),(74,10,-85.0000,'2017-01-11 23:22:12','Крой №26 Пачка №1 - Добавление фурнитуры в пачку',59),(75,8,-17.0000,'2017-01-11 23:22:12','Крой №26 Пачка №1 - Добавление фурнитуры в пачку',60),(76,7,-5746.0000,'2017-01-11 23:22:35','Крой №26 Пачка №2 - Добавление фурнитуры в пачку',61),(77,8,-17.0000,'2017-01-11 23:22:35','Крой №26 Пачка №2 - Добавление фурнитуры в пачку',62),(78,15,-226.1000,'2017-01-11 23:22:35','Крой №26 Пачка №2 - Добавление фурнитуры в пачку',63),(79,10,-85.0000,'2017-01-11 23:22:35','Крой №26 Пачка №2 - Добавление фурнитуры в пачку',64),(80,7,-6308.7000,'2017-01-11 23:23:53','Крой №26 Пачка №3 - Добавление фурнитуры в пачку',65),(81,8,-17.0000,'2017-01-11 23:23:53','Крой №26 Пачка №3 - Добавление фурнитуры в пачку',66),(82,15,-246.5000,'2017-01-11 23:23:53','Крой №26 Пачка №3 - Добавление фурнитуры в пачку',67),(83,10,-85.0000,'2017-01-11 23:23:53','Крой №26 Пачка №3 - Добавление фурнитуры в пачку',68),(84,7,-6687.8000,'2017-01-11 23:24:30','Крой №26 Пачка №4 - Добавление фурнитуры в пачку',69),(85,8,-17.0000,'2017-01-11 23:24:30','Крой №26 Пачка №4 - Добавление фурнитуры в пачку',70),(86,15,-256.7000,'2017-01-11 23:24:30','Крой №26 Пачка №4 - Добавление фурнитуры в пачку',71),(87,10,-85.0000,'2017-01-11 23:24:30','Крой №26 Пачка №4 - Добавление фурнитуры в пачку',72),(88,7,-6608.0000,'2017-01-11 23:28:19','Крой №27 Пачка №1 - Добавление фурнитуры в пачку',73),(89,8,-16.0000,'2017-01-11 23:28:19','Крой №27 Пачка №1 - Добавление фурнитуры в пачку',74),(90,9,-480.0000,'2017-01-11 23:28:19','Крой №27 Пачка №1 - Добавление фурнитуры в пачку',75),(91,10,-160.0000,'2017-01-11 23:28:19','Крой №27 Пачка №1 - Добавление фурнитуры в пачку',76),(92,7,-6988.8000,'2017-01-11 23:28:52','Крой №27 Пачка №2 - Добавление фурнитуры в пачку',77),(93,8,-16.0000,'2017-01-11 23:28:52','Крой №27 Пачка №2 - Добавление фурнитуры в пачку',78),(94,9,-480.0000,'2017-01-11 23:28:52','Крой №27 Пачка №2 - Добавление фурнитуры в пачку',79),(95,10,-160.0000,'2017-01-11 23:28:52','Крой №27 Пачка №2 - Добавление фурнитуры в пачку',80),(96,7,-7392.0000,'2017-01-11 23:29:19','Крой №27 Пачка №3 - Добавление фурнитуры в пачку',81),(97,8,-16.0000,'2017-01-11 23:29:19','Крой №27 Пачка №3 - Добавление фурнитуры в пачку',82),(98,9,-480.0000,'2017-01-11 23:29:19','Крой №27 Пачка №3 - Добавление фурнитуры в пачку',83),(99,10,-160.0000,'2017-01-11 23:29:19','Крой №27 Пачка №3 - Добавление фурнитуры в пачку',84),(100,7,-7728.0000,'2017-01-11 23:29:41','Крой №27 Пачка №4 - Добавление фурнитуры в пачку',85),(101,8,-16.0000,'2017-01-11 23:29:41','Крой №27 Пачка №4 - Добавление фурнитуры в пачку',86),(102,9,-480.0000,'2017-01-11 23:29:41','Крой №27 Пачка №4 - Добавление фурнитуры в пачку',87),(103,10,-160.0000,'2017-01-11 23:29:41','Крой №27 Пачка №4 - Добавление фурнитуры в пачку',88),(104,7,-7728.0000,'2017-01-11 23:30:01','Крой №27 Пачка №5 - Добавление фурнитуры в пачку',89),(105,8,-16.0000,'2017-01-11 23:30:01','Крой №27 Пачка №5 - Добавление фурнитуры в пачку',90),(106,9,-480.0000,'2017-01-11 23:30:01','Крой №27 Пачка №5 - Добавление фурнитуры в пачку',91),(107,10,-160.0000,'2017-01-11 23:30:01','Крой №27 Пачка №5 - Добавление фурнитуры в пачку',92),(108,7,-6608.0000,'2017-01-11 23:30:26','Крой №27 Пачка №6 - Добавление фурнитуры в пачку',93),(109,8,-16.0000,'2017-01-11 23:30:26','Крой №27 Пачка №6 - Добавление фурнитуры в пачку',94),(110,9,-480.0000,'2017-01-11 23:30:26','Крой №27 Пачка №6 - Добавление фурнитуры в пачку',95),(111,10,-160.0000,'2017-01-11 23:30:26','Крой №27 Пачка №6 - Добавление фурнитуры в пачку',96),(112,7,-6988.8000,'2017-01-11 23:30:43','Крой №27 Пачка №7 - Добавление фурнитуры в пачку',97),(113,8,-16.0000,'2017-01-11 23:30:43','Крой №27 Пачка №7 - Добавление фурнитуры в пачку',98),(114,9,-480.0000,'2017-01-11 23:30:43','Крой №27 Пачка №7 - Добавление фурнитуры в пачку',99),(115,10,-160.0000,'2017-01-11 23:30:43','Крой №27 Пачка №7 - Добавление фурнитуры в пачку',100),(116,7,-7392.0000,'2017-01-11 23:30:58','Крой №27 Пачка №8 - Добавление фурнитуры в пачку',101),(117,8,-16.0000,'2017-01-11 23:30:58','Крой №27 Пачка №8 - Добавление фурнитуры в пачку',102),(118,9,-480.0000,'2017-01-11 23:30:58','Крой №27 Пачка №8 - Добавление фурнитуры в пачку',103),(119,10,-160.0000,'2017-01-11 23:30:58','Крой №27 Пачка №8 - Добавление фурнитуры в пачку',104),(120,7,-7728.0000,'2017-01-11 23:31:17','Крой №27 Пачка №9 - Добавление фурнитуры в пачку',105),(121,8,-16.0000,'2017-01-11 23:31:17','Крой №27 Пачка №9 - Добавление фурнитуры в пачку',106),(122,9,-480.0000,'2017-01-11 23:31:17','Крой №27 Пачка №9 - Добавление фурнитуры в пачку',107),(123,10,-160.0000,'2017-01-11 23:31:17','Крой №27 Пачка №9 - Добавление фурнитуры в пачку',108),(124,7,-7728.0000,'2017-01-11 23:31:34','Крой №27 Пачка №10 - Добавление фурнитуры в пачку',109),(125,8,-16.0000,'2017-01-11 23:31:34','Крой №27 Пачка №10 - Добавление фурнитуры в пачку',110),(126,9,-480.0000,'2017-01-11 23:31:34','Крой №27 Пачка №10 - Добавление фурнитуры в пачку',111),(127,10,-160.0000,'2017-01-11 23:31:34','Крой №27 Пачка №10 - Добавление фурнитуры в пачку',112),(128,7,206.5000,'2017-01-18 15:58:02','Крой №27 Пачка №1 - Уменьшение фурнитуры в пачке',73),(129,8,0.5000,'2017-01-18 15:58:02','Крой №27 Пачка №1 - Уменьшение фурнитуры в пачке',74),(130,9,15.0000,'2017-01-18 15:58:02','Крой №27 Пачка №1 - Уменьшение фурнитуры в пачке',75),(131,10,5.0000,'2017-01-18 15:58:02','Крой №27 Пачка №1 - Уменьшение фурнитуры в пачке',76),(132,7,-5392.4000,'2017-01-18 15:58:34','Крой №26 Пачка №5 - Добавление фурнитуры в пачку',113),(133,15,-204.0000,'2017-01-18 15:58:34','Крой №26 Пачка №5 - Добавление фурнитуры в пачку',114),(134,10,-85.0000,'2017-01-18 15:58:34','Крой №26 Пачка №5 - Добавление фурнитуры в пачку',115),(135,8,-17.0000,'2017-01-18 15:58:34','Крой №26 Пачка №5 - Добавление фурнитуры в пачку',116),(136,7,5392.4000,'2017-01-18 16:00:59','Крой №26 Пачка №5 - Удаление пачки',113),(137,15,204.0000,'2017-01-18 16:00:59','Крой №26 Пачка №5 - Удаление пачки',114),(138,10,85.0000,'2017-01-18 16:00:59','Крой №26 Пачка №5 - Удаление пачки',115),(139,8,17.0000,'2017-01-18 16:00:59','Крой №26 Пачка №5 - Удаление пачки',116),(140,7,82.6000,'2017-01-23 13:11:45','Крой №27 Пачка №1 - Уменьшение фурнитуры в пачке',73),(141,8,0.2000,'2017-01-23 13:11:45','Крой №27 Пачка №1 - Уменьшение фурнитуры в пачке',74),(142,9,6.0000,'2017-01-23 13:11:45','Крой №27 Пачка №1 - Уменьшение фурнитуры в пачке',75),(143,10,2.0000,'2017-01-23 13:11:45','Крой №27 Пачка №1 - Уменьшение фурнитуры в пачке',76),(144,7,74.2200,'2017-02-05 03:44:52','26/3 - Уменьшение фурнитуры в пачке',65),(145,8,0.2000,'2017-02-05 03:44:52','26/3 - Уменьшение фурнитуры в пачке',66),(146,15,2.9000,'2017-02-05 03:44:52','26/3 - Уменьшение фурнитуры в пачке',67),(147,10,1.0000,'2017-02-05 03:44:52','26/3 - Уменьшение фурнитуры в пачке',68);
/*!40000 ALTER TABLE `transaction_records_accessories` ENABLE KEYS */;
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
