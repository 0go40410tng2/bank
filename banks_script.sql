-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: localhost    Database: bank_and_branches
-- ------------------------------------------------------
-- Server version	8.0.39

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `accounts`
--

DROP TABLE IF EXISTS `accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts` (
  `account_id` int NOT NULL,
  `account_type_code` int DEFAULT NULL,
  `customer_id` int DEFAULT NULL,
  `account_name` varchar(255) DEFAULT NULL,
  `date_opened` date DEFAULT NULL,
  `date_closed` date DEFAULT NULL,
  `current_balance` decimal(18,2) DEFAULT NULL,
  `other_account_details` text,
  PRIMARY KEY (`account_id`),
  KEY `account_type_code` (`account_type_code`),
  KEY `customer_id` (`customer_id`),
  CONSTRAINT `accounts_ibfk_1` FOREIGN KEY (`account_type_code`) REFERENCES `ref_account_types` (`account_type_code`),
  CONSTRAINT `accounts_ibfk_2` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts`
--

LOCK TABLES `accounts` WRITE;
/*!40000 ALTER TABLE `accounts` DISABLE KEYS */;
INSERT INTO `accounts` VALUES (1,1,1,'John\'s Current Account','2020-01-15',NULL,15000.00,'Primary account'),(2,2,2,'Acme Savings','2018-03-22',NULL,250000.00,'Business savings'),(3,3,3,'Jane\'s Fixed Deposit','2021-06-10',NULL,50000.00,NULL),(4,4,4,'Retail Account 1','2022-01-20',NULL,2000.00,NULL),(5,5,5,'Corporate Account 1','2019-11-13',NULL,1000000.00,'High value account'),(6,1,6,'Alice\'s Current Account','2021-08-05',NULL,8000.00,NULL);
/*!40000 ALTER TABLE `accounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers` (
  `customer_id` int NOT NULL,
  `customer_type_code` int DEFAULT NULL,
  `customer_name` varchar(255) DEFAULT NULL,
  `customer_phone` varchar(20) DEFAULT NULL,
  `customer_email` varchar(255) DEFAULT NULL,
  `date_became_customer` date DEFAULT NULL,
  `other_details` text,
  PRIMARY KEY (`customer_id`),
  KEY `customer_type_code` (`customer_type_code`),
  CONSTRAINT `customers_ibfk_1` FOREIGN KEY (`customer_type_code`) REFERENCES `ref_customer_types` (`customer_type_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES (1,1,'John Doe','1234567890','john.doe@example.com','2020-01-15','VIP customer'),(2,2,'Acme Corp','9876543210','info@acme.com','2018-03-22','Long-term partner'),(3,3,'Jane Smith','5555551234','jane.smith@example.com','2021-06-10',NULL),(4,4,'Retail User 1','4445556667','retail1@example.com','2022-01-20','Seasonal buyer'),(5,5,'Corporate User 1','7778889990','corporate1@example.com','2019-11-13','Preferred customer'),(6,1,'Alice Brown','1112223333','alice.brown@example.com','2021-08-05','Frequent buyer'),(7,3,'Bob Johnson','4445556666','bob.johnson@example.com','2020-09-10',NULL);
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `parties`
--

DROP TABLE IF EXISTS `parties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `parties` (
  `party_id` int NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `other_details` text,
  PRIMARY KEY (`party_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parties`
--

LOCK TABLES `parties` WRITE;
/*!40000 ALTER TABLE `parties` DISABLE KEYS */;
INSERT INTO `parties` VALUES (1,'Party A','1231231234','partyA@example.com','Business Partner'),(2,'Party B','2342342345','partyB@example.com','Supplier'),(3,'Party C','3453453456','partyC@example.com','Client'),(4,'Party D','4564564567','partyD@example.com','Investor'),(5,'Party E','5675675678','partyE@example.com','Affiliate'),(6,'Party F','6786786789','partyF@example.com','Distributor');
/*!40000 ALTER TABLE `parties` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ref_account_types`
--

DROP TABLE IF EXISTS `ref_account_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ref_account_types` (
  `account_type_code` int NOT NULL,
  `account_type_description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`account_type_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ref_account_types`
--

LOCK TABLES `ref_account_types` WRITE;
/*!40000 ALTER TABLE `ref_account_types` DISABLE KEYS */;
INSERT INTO `ref_account_types` VALUES (1,'Current'),(2,'Savings'),(3,'Deposit'),(4,'Business'),(5,'Premium');
/*!40000 ALTER TABLE `ref_account_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ref_customer_types`
--

DROP TABLE IF EXISTS `ref_customer_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ref_customer_types` (
  `customer_type_code` int NOT NULL,
  `customer_type_description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`customer_type_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ref_customer_types`
--

LOCK TABLES `ref_customer_types` WRITE;
/*!40000 ALTER TABLE `ref_customer_types` DISABLE KEYS */;
INSERT INTO `ref_customer_types` VALUES (1,'Administrator'),(2,'Organization'),(3,'Individual'),(4,'Retail'),(5,'Corporate');
/*!40000 ALTER TABLE `ref_customer_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ref_transaction_types`
--

DROP TABLE IF EXISTS `ref_transaction_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ref_transaction_types` (
  `transaction_type_code` int NOT NULL,
  `transaction_type_description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`transaction_type_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ref_transaction_types`
--

LOCK TABLES `ref_transaction_types` WRITE;
/*!40000 ALTER TABLE `ref_transaction_types` DISABLE KEYS */;
INSERT INTO `ref_transaction_types` VALUES (1,'Deposit'),(2,'Withdrawal'),(3,'Transfer'),(4,'Payment'),(5,'Fee');
/*!40000 ALTER TABLE `ref_transaction_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transaction_messages`
--

DROP TABLE IF EXISTS `transaction_messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transaction_messages` (
  `message_number` int NOT NULL,
  `account_id` int DEFAULT NULL,
  `counterparty_id` int DEFAULT NULL,
  `party_id` int DEFAULT NULL,
  `transaction_type_code` int DEFAULT NULL,
  `counterparty_role` varchar(255) DEFAULT NULL,
  `currency_code` varchar(10) DEFAULT NULL,
  `iban_number` varchar(34) DEFAULT NULL,
  `transaction_date` date DEFAULT NULL,
  `amount` decimal(18,2) DEFAULT NULL,
  `balance` decimal(18,2) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `party_role` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`message_number`),
  KEY `account_id` (`account_id`),
  KEY `counterparty_id` (`counterparty_id`),
  KEY `party_id` (`party_id`),
  KEY `transaction_type_code` (`transaction_type_code`),
  CONSTRAINT `transaction_messages_ibfk_1` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`account_id`),
  CONSTRAINT `transaction_messages_ibfk_2` FOREIGN KEY (`counterparty_id`) REFERENCES `parties` (`party_id`),
  CONSTRAINT `transaction_messages_ibfk_3` FOREIGN KEY (`party_id`) REFERENCES `parties` (`party_id`),
  CONSTRAINT `transaction_messages_ibfk_4` FOREIGN KEY (`transaction_type_code`) REFERENCES `ref_transaction_types` (`transaction_type_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transaction_messages`
--

LOCK TABLES `transaction_messages` WRITE;
/*!40000 ALTER TABLE `transaction_messages` DISABLE KEYS */;
INSERT INTO `transaction_messages` VALUES (1,1,2,3,1,'Sender','USD','US1234567890','2023-01-10',1000.00,14000.00,'New York','Payer'),(2,2,3,4,2,'Receiver','USD','US9876543210','2023-02-15',2000.00,248000.00,'San Francisco','Payee');
/*!40000 ALTER TABLE `transaction_messages` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-14 17:39:46
