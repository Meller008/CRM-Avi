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
-- Table structure for table `material_supplyposition`
--

DROP TABLE IF EXISTS `material_supplyposition`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `material_supplyposition` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Material_SupplyId` int(11) NOT NULL,
  `Material_NameId` int(11) NOT NULL,
  `Weight` decimal(11,4) NOT NULL,
  `Price` decimal(11,4) NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `ForeginKey1_idx` (`Material_SupplyId`),
  KEY `ForeginKey2_idx` (`Material_NameId`),
  CONSTRAINT `M_S_P_FK1` FOREIGN KEY (`Material_SupplyId`) REFERENCES `material_supply` (`Id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `M_S_P_FK2` FOREIGN KEY (`Material_NameId`) REFERENCES `material_name` (`Id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `material_supplyposition`
--

LOCK TABLES `material_supplyposition` WRITE;
/*!40000 ALTER TABLE `material_supplyposition` DISABLE KEYS */;
INSERT INTO `material_supplyposition` VALUES (55,35,14,3832.6000,354.0000),(56,35,15,378.5000,388.0000),(57,36,10,47.4000,335.0000),(58,36,14,4140.9000,334.0000),(59,36,15,109.5000,380.0000),(60,36,20,25.4000,335.0000),(61,36,27,144.0000,315.0000),(62,36,28,213.6000,415.0000),(63,36,35,191.0000,348.0000);
/*!40000 ALTER TABLE `material_supplyposition` ENABLE KEYS */;
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
/*!50003 CREATE*/ /*!50017 DEFINER=`Meller`@`%`*/ /*!50003 TRIGGER `avi_crm`.`material_supplyposition_AFTER_INSERT` AFTER INSERT ON `material_supplyposition` FOR EACH ROW
BEGIN
	INSERT INTO material_balance SET Material_SupplyPositionId = NEW.Id, BalanceWeight = NEW.Weight;
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

-- Dump completed on 2017-03-07 22:27:31
