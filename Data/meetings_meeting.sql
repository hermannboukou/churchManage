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

 Date: 10/10/2025 17:20:21
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for meetings_meeting
-- ----------------------------
DROP TABLE IF EXISTS `meetings_meeting`;
CREATE TABLE `meetings_meeting` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `infos` longtext,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of meetings_meeting
-- ----------------------------
BEGIN;
INSERT INTO `meetings_meeting` VALUES (1, 'Culte d\'adoration', 'Réunion de louange d\'adoration et d\'enseignement', '2025-02-12 09:54:02.523145', '2025-02-12 09:54:02.523193');
INSERT INTO `meetings_meeting` VALUES (2, 'Réunion de prière', 'Moment d\'intercession pour la communauté, la ville, le pays et les autorités', '2025-02-12 09:57:41.668289', '2025-02-12 09:57:41.668319');
INSERT INTO `meetings_meeting` VALUES (3, 'Étude biblique', 'Moment d\'étude biblique et d\'enseignement', '2025-02-12 09:59:20.589088', '2025-02-12 09:59:20.589133');
INSERT INTO `meetings_meeting` VALUES (4, 'Retraite jeûne et prière', 'Retraite jeûne et prière', '2025-02-12 10:00:52.529159', '2025-02-12 10:00:52.529185');
INSERT INTO `meetings_meeting` VALUES (5, 'Campagne d\'évangélisation', 'Campagne d\'évangélisation', '2025-02-12 10:02:02.126247', '2025-02-12 10:02:02.126291');
INSERT INTO `meetings_meeting` VALUES (6, 'Culte de Pentecôte', 'Culte de Pentecôte', '2025-02-12 10:04:01.531596', '2025-02-12 10:04:01.531647');
INSERT INTO `meetings_meeting` VALUES (7, 'Culte de la zone Est', 'Culte de la zone Est', '2025-02-12 10:05:04.959034', '2025-02-12 10:05:04.959086');
INSERT INTO `meetings_meeting` VALUES (8, 'Veillée de prière', 'Veillée de prière', '2025-03-24 13:10:14.237360', '2025-03-24 13:10:14.237392');
INSERT INTO `meetings_meeting` VALUES (9, 'Réveillon', '', '2025-03-24 13:10:24.118840', '2025-03-24 13:10:24.118895');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
