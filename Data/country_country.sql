/*
 Navicat Premium Data Transfer

 Source Server         : Local
 Source Server Type    : MySQL
 Source Server Version : 90100
 Source Host           : localhost:3306
 Source Schema         : tailwind

 Target Server Type    : MySQL
 Target Server Version : 90100
 File Encoding         : 65001

 Date: 10/10/2025 17:20:38
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for country_country
-- ----------------------------
DROP TABLE IF EXISTS `country_country`;
CREATE TABLE `country_country` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `code` varchar(2) NOT NULL,
  `phone_code` varchar(5) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of country_country
-- ----------------------------
BEGIN;
INSERT INTO `country_country` VALUES (1, 'Gabon', 'Gb', '+241', '2025-02-12 09:51:08.603589', '2025-10-10 08:54:33.728226');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
