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
-- Table structure for table `accessories_supplyposition`
--

DROP TABLE IF EXISTS `accessories_supplyposition`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accessories_supplyposition` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Accessories_SupplyId` int(11) NOT NULL,
  `Accessories_NameId` int(11) NOT NULL,
  `Value` decimal(11,4) NOT NULL,
  `Price` decimal(11,4) NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `A_S_FK1_idx` (`Accessories_SupplyId`),
  KEY `A_S_FK2_idx` (`Accessories_NameId`),
  CONSTRAINT `A_S_FK_1` FOREIGN KEY (`Accessories_SupplyId`) REFERENCES `accessories_supply` (`Id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `A_S_FK_2` FOREIGN KEY (`Accessories_NameId`) REFERENCES `accessories_name` (`Id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accessories_supplyposition`
--

LOCK TABLES `accessories_supplyposition` WRITE;
/*!40000 ALTER TABLE `accessories_supplyposition` DISABLE KEYS */;
INSERT INTO `accessories_supplyposition` VALUES (7,4,8,7140000.0000,0.0107),(8,5,12,40000.0000,1.7075),(9,6,4,100000.0000,0.0670),(10,7,10,1000000.0000,0.1800),(11,8,8,500000.0000,0.0108),(14,11,11,40.0000,1.5500),(15,12,11,80.0000,1.6000),(16,13,11,1050.0000,1.5000),(17,14,11,20000.0000,1.7500),(18,15,16,100000.0000,0.1750),(19,16,5,255000.0000,7.5650);
/*!40000 ALTER TABLE `accessories_supplyposition` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`Meller`@`%`*/ /*!50003 TRIGGER `avi_crm`.`accessories_supplyposition_AFTER_INSERT` AFTER INSERT ON `accessories_supplyposition` FOR EACH ROW
BEGIN
	INSERT INTO accessories_balance SET Accessories_SupplyPositionId = NEW.Id, BalanceValue = NEW.Value;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-03-07 22:27:30
