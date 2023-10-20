-- MySQL dump 10.13  Distrib 8.0.34, for Linux (x86_64)
--
-- Host: localhost    Database: FurnitureStore
-- ------------------------------------------------------
-- Server version	8.0.34-0ubuntu0.22.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Client`
--

DROP TABLE IF EXISTS `Client`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Client` (
  `ID` smallint NOT NULL AUTO_INCREMENT,
  `Name` varchar(60) DEFAULT NULL,
  `PhoneNumber` varchar(15) DEFAULT NULL,
  `BillingAddress` varchar(80) NOT NULL,
  `MailingAddress` varchar(80) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Client`
--

LOCK TABLES `Client` WRITE;
/*!40000 ALTER TABLE `Client` DISABLE KEYS */;
INSERT INTO `Client` VALUES (1,'Jane Doe','123-123-1234','123 Road rd. City, ST, Zip','123 Road rd. City, ST, Zip'),(2,'John Doe','123-122-4434','123 Road rd. City, ST, Zip','123 Road rd. City, ST, Zip'),(3,'Terra Moar','111-222-3333','122 Street st. City, ST, Zip','122 Street st. City, ST, Zip'),(4,'Stella King','111-333-444','124 Lane ln. City, ST, Zip','124 Lane ln. City, ST, Zip');
/*!40000 ALTER TABLE `Client` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Color`
--

DROP TABLE IF EXISTS `Color`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Color` (
  `ID` smallint unsigned NOT NULL AUTO_INCREMENT,
  `Color` char(3) NOT NULL,
  `ItemID` smallint unsigned NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `ItemID` (`ItemID`),
  CONSTRAINT `Color_ibfk_1` FOREIGN KEY (`ItemID`) REFERENCES `Furniture` (`ItemID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Color`
--

LOCK TABLES `Color` WRITE;
/*!40000 ALTER TABLE `Color` DISABLE KEYS */;
INSERT INTO `Color` VALUES (1,'BRN',1),(2,'BLK',1),(3,'GRY',2),(4,'BLU',3),(5,'RED',4);
/*!40000 ALTER TABLE `Color` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Discount`
--

DROP TABLE IF EXISTS `Discount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Discount` (
  `Code` varchar(10) NOT NULL,
  `StartDate` datetime NOT NULL,
  `EndDate` datetime NOT NULL,
  `Discount` tinyint unsigned DEFAULT NULL,
  PRIMARY KEY (`Code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Discount`
--

LOCK TABLES `Discount` WRITE;
/*!40000 ALTER TABLE `Discount` DISABLE KEYS */;
INSERT INTO `Discount` VALUES ('BUY1GET2L','2023-01-02 00:00:00','2023-01-10 00:00:00',50),('NEWYEAR50','2022-12-02 00:00:00','2023-01-02 00:00:00',50);
/*!40000 ALTER TABLE `Discount` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Furniture`
--

DROP TABLE IF EXISTS `Furniture`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Furniture` (
  `ItemID` smallint unsigned NOT NULL AUTO_INCREMENT,
  `FurnitureType` char(1) NOT NULL,
  `Dimensions` varchar(20) DEFAULT NULL,
  `Weight` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`ItemID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Furniture`
--

LOCK TABLES `Furniture` WRITE;
/*!40000 ALTER TABLE `Furniture` DISABLE KEYS */;
INSERT INTO `Furniture` VALUES (1,'S','20 x 20 x 33',15.00),(2,'L','21 x 11.75 x 8',2.00),(3,'L','34 x 24.25 x 123',5.50),(4,'S','64 x 64 x 53',50.00);
/*!40000 ALTER TABLE `Furniture` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Invoice`
--

DROP TABLE IF EXISTS `Invoice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Invoice` (
  `ID` smallint NOT NULL AUTO_INCREMENT,
  `DateTime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ClientID` smallint DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `ClientID` (`ClientID`),
  CONSTRAINT `Invoice_ibfk_1` FOREIGN KEY (`ClientID`) REFERENCES `Client` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Invoice`
--

LOCK TABLES `Invoice` WRITE;
/*!40000 ALTER TABLE `Invoice` DISABLE KEYS */;
INSERT INTO `Invoice` VALUES (1,'2023-01-01 15:06:03',4),(2,'2023-01-03 17:47:00',4),(3,'2023-01-04 12:47:02',1),(4,'2023-01-04 12:47:02',2);
/*!40000 ALTER TABLE `Invoice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Lighting`
--

DROP TABLE IF EXISTS `Lighting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Lighting` (
  `ItemID` smallint unsigned NOT NULL,
  `Wattage` smallint unsigned NOT NULL,
  `Dimmable` tinyint(1) NOT NULL DEFAULT '0',
  `Strobe` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`ItemID`),
  CONSTRAINT `Lighting_ibfk_1` FOREIGN KEY (`ItemID`) REFERENCES `Furniture` (`ItemID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Lighting`
--

LOCK TABLES `Lighting` WRITE;
/*!40000 ALTER TABLE `Lighting` DISABLE KEYS */;
INSERT INTO `Lighting` VALUES (2,60,0,0),(3,350,1,0);
/*!40000 ALTER TABLE `Lighting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `LineItem`
--

DROP TABLE IF EXISTS `LineItem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `LineItem` (
  `LineNumber` int unsigned NOT NULL AUTO_INCREMENT,
  `InvoiceID` smallint NOT NULL,
  `ItemID` smallint unsigned NOT NULL,
  `Quantity` tinyint unsigned NOT NULL,
  `Price` smallint unsigned DEFAULT NULL,
  `DiscountCode` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`LineNumber`),
  KEY `InvoiceID` (`InvoiceID`),
  KEY `ItemID` (`ItemID`),
  KEY `fk_DiscountCode` (`DiscountCode`),
  CONSTRAINT `fk_DiscountCode` FOREIGN KEY (`DiscountCode`) REFERENCES `Discount` (`Code`) ON UPDATE CASCADE,
  CONSTRAINT `LineItem_ibfk_1` FOREIGN KEY (`InvoiceID`) REFERENCES `Invoice` (`ID`),
  CONSTRAINT `LineItem_ibfk_2` FOREIGN KEY (`ItemID`) REFERENCES `Furniture` (`ItemID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `LineItem`
--

LOCK TABLES `LineItem` WRITE;
/*!40000 ALTER TABLE `LineItem` DISABLE KEYS */;
INSERT INTO `LineItem` VALUES (1,1,2,2,5,'NEWYEAR50'),(2,1,3,1,10,'NEWYEAR50'),(3,2,1,1,25,NULL),(4,3,2,1,5,NULL),(5,4,4,1,45,NULL),(6,4,3,2,40,'BUY1GET2L'),(7,4,1,1,25,NULL);
/*!40000 ALTER TABLE `LineItem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Material`
--

DROP TABLE IF EXISTS `Material`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Material` (
  `ID` smallint unsigned NOT NULL AUTO_INCREMENT,
  `Material` varchar(40) DEFAULT NULL,
  `ItemID` smallint unsigned NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `ItemID` (`ItemID`),
  CONSTRAINT `Material_ibfk_1` FOREIGN KEY (`ItemID`) REFERENCES `Furniture` (`ItemID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Material`
--

LOCK TABLES `Material` WRITE;
/*!40000 ALTER TABLE `Material` DISABLE KEYS */;
INSERT INTO `Material` VALUES (1,'Oak Wood',1),(2,'Faux Leather',1),(3,'Stainless Steel',2),(4,'Stainless Steel',3),(5,'Polyester',4),(6,'Polystyrene Beans',4);
/*!40000 ALTER TABLE `Material` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Seating`
--

DROP TABLE IF EXISTS `Seating`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Seating` (
  `ItemID` smallint unsigned NOT NULL,
  `Outdoor` tinyint(1) NOT NULL DEFAULT '0',
  `Rocking` tinyint(1) NOT NULL DEFAULT '0',
  `Reclinable` tinyint(1) NOT NULL DEFAULT '0',
  `WeightCap` smallint unsigned NOT NULL,
  PRIMARY KEY (`ItemID`),
  CONSTRAINT `Seating_ibfk_1` FOREIGN KEY (`ItemID`) REFERENCES `Furniture` (`ItemID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Seating`
--

LOCK TABLES `Seating` WRITE;
/*!40000 ALTER TABLE `Seating` DISABLE KEYS */;
INSERT INTO `Seating` VALUES (1,0,0,0,250),(4,0,0,0,200);
/*!40000 ALTER TABLE `Seating` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-10-20 21:11:42
