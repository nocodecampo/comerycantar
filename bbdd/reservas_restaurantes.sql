CREATE DATABASE  IF NOT EXISTS `reservas_restaurantes` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `reservas_restaurantes`;
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: reservas_restaurantes
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.32-MariaDB

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
-- Table structure for table `clientes`
--

DROP TABLE IF EXISTS `clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clientes` (
  `cliente_id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `telefono` varchar(15) DEFAULT NULL,
  `password_hash` varchar(255) NOT NULL,
  `fecha_registro` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`cliente_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes`
--

LOCK TABLES `clientes` WRITE;
/*!40000 ALTER TABLE `clientes` DISABLE KEYS */;
INSERT INTO `clientes` VALUES (1,'Carlos Pérez','carlos@email.com','600123456','hashedpassword3','2025-03-11 17:18:50'),(2,'Laura Gómez','laura@email.com','612345678','hashedpassword4','2025-03-11 17:18:50');
/*!40000 ALTER TABLE `clientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estados_reserva`
--

DROP TABLE IF EXISTS `estados_reserva`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estados_reserva` (
  `estado_id` int(11) NOT NULL AUTO_INCREMENT,
  `estado_nombre` enum('activa','cancelada','pasada') NOT NULL,
  PRIMARY KEY (`estado_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estados_reserva`
--

LOCK TABLES `estados_reserva` WRITE;
/*!40000 ALTER TABLE `estados_reserva` DISABLE KEYS */;
INSERT INTO `estados_reserva` VALUES (1,'activa'),(2,'cancelada'),(3,'pasada');
/*!40000 ALTER TABLE `estados_reserva` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `horarios`
--

DROP TABLE IF EXISTS `horarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `horarios` (
  `horario_id` int(11) NOT NULL AUTO_INCREMENT,
  `hora` time NOT NULL,
  PRIMARY KEY (`horario_id`),
  UNIQUE KEY `hora` (`hora`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `horarios`
--

LOCK TABLES `horarios` WRITE;
/*!40000 ALTER TABLE `horarios` DISABLE KEYS */;
INSERT INTO `horarios` VALUES (1,'13:00:00'),(2,'14:00:00'),(3,'15:00:00'),(4,'20:00:00'),(5,'21:00:00'),(6,'22:00:00');
/*!40000 ALTER TABLE `horarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mesas`
--

DROP TABLE IF EXISTS `mesas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mesas` (
  `mesa_id` int(11) NOT NULL AUTO_INCREMENT,
  `restaurante_id` int(11) NOT NULL,
  `capacidad` int(11) NOT NULL,
  `estado` enum('disponible','ocupada') DEFAULT 'disponible',
  PRIMARY KEY (`mesa_id`),
  KEY `restaurante_id` (`restaurante_id`),
  CONSTRAINT `mesas_ibfk_1` FOREIGN KEY (`restaurante_id`) REFERENCES `restaurantes` (`restaurante_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mesas`
--

LOCK TABLES `mesas` WRITE;
/*!40000 ALTER TABLE `mesas` DISABLE KEYS */;
INSERT INTO `mesas` VALUES (1,1,4,'disponible'),(2,1,2,'disponible'),(3,2,6,'disponible'),(4,2,4,'disponible');
/*!40000 ALTER TABLE `mesas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reservas`
--

DROP TABLE IF EXISTS `reservas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reservas` (
  `reserva_id` int(11) NOT NULL AUTO_INCREMENT,
  `cliente_id` int(11) NOT NULL,
  `restaurante_id` int(11) NOT NULL,
  `mesa_id` int(11) NOT NULL,
  `estado_id` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `horario_id` int(11) NOT NULL,
  `num_personas` int(11) NOT NULL,
  PRIMARY KEY (`reserva_id`),
  UNIQUE KEY `unique_reserva` (`mesa_id`,`fecha`,`horario_id`),
  KEY `cliente_id` (`cliente_id`),
  KEY `restaurante_id` (`restaurante_id`),
  KEY `estado_id` (`estado_id`),
  KEY `horario_id` (`horario_id`),
  CONSTRAINT `reservas_ibfk_1` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`cliente_id`) ON DELETE CASCADE,
  CONSTRAINT `reservas_ibfk_2` FOREIGN KEY (`restaurante_id`) REFERENCES `restaurantes` (`restaurante_id`) ON DELETE CASCADE,
  CONSTRAINT `reservas_ibfk_3` FOREIGN KEY (`mesa_id`) REFERENCES `mesas` (`mesa_id`) ON DELETE CASCADE,
  CONSTRAINT `reservas_ibfk_4` FOREIGN KEY (`estado_id`) REFERENCES `estados_reserva` (`estado_id`),
  CONSTRAINT `reservas_ibfk_5` FOREIGN KEY (`horario_id`) REFERENCES `horarios` (`horario_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reservas`
--

LOCK TABLES `reservas` WRITE;
/*!40000 ALTER TABLE `reservas` DISABLE KEYS */;
INSERT INTO `reservas` VALUES (1,1,1,1,1,'2024-06-15',1,4),(2,2,2,3,1,'2024-06-16',5,2);
/*!40000 ALTER TABLE `reservas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `restaurantes`
--

DROP TABLE IF EXISTS `restaurantes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `restaurantes` (
  `restaurante_id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `telefono` varchar(15) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `ciudad` varchar(100) DEFAULT NULL,
  `password_hash` varchar(255) NOT NULL,
  `fecha_registro` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`restaurante_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `restaurantes`
--

LOCK TABLES `restaurantes` WRITE;
/*!40000 ALTER TABLE `restaurantes` DISABLE KEYS */;
INSERT INTO `restaurantes` VALUES (1,'Restaurante Central','central@email.com','123456789','Calle Mayor 10','Madrid','hashedpassword1','2025-03-11 17:16:12'),(2,'Bistro 360','bistro360@email.com','987654321','Avenida Sol 5','Barcelona','hashedpassword2','2025-03-11 17:16:12');
/*!40000 ALTER TABLE `restaurantes` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

