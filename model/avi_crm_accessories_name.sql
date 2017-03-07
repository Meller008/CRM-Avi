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
-- Table structure for table `accessories_name`
--

DROP TABLE IF EXISTS `accessories_name`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accessories_name` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(100) NOT NULL,
  `Information` text,
  `For_Beika` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`Id`),
  UNIQUE KEY `Name_UNIQUE` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accessories_name`
--

LOCK TABLES `accessories_name` WRITE;
/*!40000 ALTER TABLE `accessories_name` DISABLE KEYS */;
INSERT INTO `accessories_name` VALUES (1,'Пуговицы большие','',0),(2,'Пуговицы маленькие','',0),(3,'Нитки маленькие','',0),(4,'Пуговица','',0),(5,'Резинка 15мм','',0),(6,'Тканевая бейка','',0),(7,'Резинка 25мм','',0),(8,'Нитка','',0),(9,'Резинка 8 мм','',0),(10,'Ярлык вшивной','',0),(11,'Резинка ажурная','',0),(12,'Пакет упаковочный с липучкой','',0),(13,'Ярлык бумажный \"TUsi\"','',0),(14,'Резинка ажурная для КД','',0),(15,'Аппликация малая','',0),(16,'Этикетка(Наклейка) КД','',0),(17,'Флажок \"TUsi\"','',0),(18,'Резинка приш. Широкая','',0),(19,'Бантик','',0),(20,'Вешалка детская','',0),(21,'Молния детская','',0),(22,'Молния взрослая','',0),(23,'Кольцо 8мм.','',0),(24,'Регулятор 8мм','',0),(25,'шитье 2','5см',0),(26,'Аппликация большая','',0),(27,'Пакет Слот','',0),(28,'лента атласная','',0),(29,'Вешалка бельевая (трусовая)','',0),(30,'шитье 5см','',0),(31,'Вкладыш картонный','',0),(32,'Бретели силиконовые ','',0),(33,'Кнопка малая ','',0),(34,'Гипюр','',0),(35,'пакет с кнопками','',0),(36,'Страз','',0),(37,'Люверс','',0),(38,'Резинка 40 мм','',0),(39,'шнур','',0),(40,'Кружево эластичное тонкое','',0),(41,'Аппликация прямая','',0),(42,'Флок триплированный','',0),(43,'Синтепон','',0),(44,'Кружево широкое 17 см.','',0),(45,'Сумочка мал.','',0),(46,'кант','',0),(47,'Глазки (пара)','',0),(48,'Коробочка сборная','',0),(49,'Флизелин','',0),(50,'Бейка','',1);
/*!40000 ALTER TABLE `accessories_name` ENABLE KEYS */;
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
