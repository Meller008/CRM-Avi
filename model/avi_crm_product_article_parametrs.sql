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
-- Table structure for table `product_article_parametrs`
--

DROP TABLE IF EXISTS `product_article_parametrs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_article_parametrs` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Product_Article_Size_Id` int(11) NOT NULL,
  `Name` varchar(30) NOT NULL,
  `Client_Name` varchar(45) DEFAULT NULL,
  `Barcode` varchar(15) DEFAULT NULL,
  `Client_code` varchar(15) DEFAULT NULL,
  `In_On_Place` mediumint(9) DEFAULT NULL,
  `Price` decimal(11,4) DEFAULT NULL,
  `Product_Note` text,
  `Cut_Note` text,
  `Show` tinyint(4) NOT NULL,
  `NDS` tinyint(3) unsigned DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `FK_P_A_PA_1_idx` (`Product_Article_Size_Id`),
  CONSTRAINT `FK_P_A_PA_1` FOREIGN KEY (`Product_Article_Size_Id`) REFERENCES `product_article_size` (`Id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_article_parametrs`
--

LOCK TABLES `product_article_parametrs` WRITE;
/*!40000 ALTER TABLE `product_article_parametrs` DISABLE KEYS */;
INSERT INTO `product_article_parametrs` VALUES (1,1,'Ашан КД','КД/СЛИПЫ ЖЕНСКИЕ Р.44 БЕЛЫЕ','4690363023967','854643',60,20.2724,'БЕЛЫЕ тр. жен. пришивная резинка везде строго ажур 7мм.,  ласт. открытая, ярлык в верх','бикини низкие женские, кулир  белый',1,18),(2,1,'Эконом',NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,NULL),(3,2,'Ашан КД','КД/СЛИПЫ ЖЕНСКИЕ Р.46 БЕЛЫЕ','4690363023974','854647',60,20.2724,'БЕЛЫЕ тр. жен. пришивная резинка везде строго ажур 7мм.,  ласт. открытая, ярлык в верх','бикини низкие женские, кулир  белый',1,18),(4,3,'Ашан КД','КД/СЛИПЫ ЖЕНСКИЕ Р.48 БЕЛЫЕ','4690363023981','854648',60,20.2724,'БЕЛЫЕ тр. жен. пришивная резинка везде строго ажур 7мм.,  ласт. открытая, ярлык в верх','бикини низкие женские, кулир  белый',1,18),(5,4,'Ашан КД','КД/СЛИПЫ ЖЕНСКИЕ Р.50 БЕЛЫЕ','4690363023998','854651',60,20.2724,'БЕЛЫЕ тр. жен. пришивная резинка везде строго ажур 7мм.,  ласт. открытая, ярлык в верх','бикини низкие женские, кулир  белый',1,18),(6,5,'Ашан КД','КД/СЛИПЫ ЖЕНСКИЕ Р.52 БЕЛЫЕ','4690363024001','854653',60,20.2724,'БЕЛЫЕ тр. жен. пришивная резинка везде строго ажур 7мм.,  ласт. открытая, ярлык в верх','бикини низкие женские, кулир  белый',1,18),(7,6,'Ашан КД','КД/СЛИПЫ ЖЕНСКИЕ Р.54 БЕЛЫЕ','4690363024018','854654',60,20.2724,'БЕЛЫЕ тр. жен. пришивная резинка везде строго ажур 7мм.,  ласт. открытая, ярлык в верх','бикини низкие женские, кулир  белый',1,18),(8,7,'Ашан КД','КД/СЛИПЫ ЖЕНСКИЕ Р.56 БЕЛЫЕ','4690363024025','854655',60,20.2724,'БЕЛЫЕ тр. жен. пришивная резинка везде строго ажур 7мм.,  ласт. открытая, ярлык в верх','бикини низкие женские, кулир  белый',1,18);
/*!40000 ALTER TABLE `product_article_parametrs` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-03-29 15:21:45
