/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 80031 (8.0.31)
 Source Host           : localhost:3306
 Source Schema         : labbooking

 Target Server Type    : MySQL
 Target Server Version : 80031 (8.0.31)
 File Encoding         : 65001

 Date: 23/12/2022 17:29:34
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for booking
-- ----------------------------
DROP TABLE IF EXISTS `booking`;
CREATE TABLE `booking`  (
  `teacher_no` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `lab_no` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime NULL DEFAULT NULL,
  `user` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`teacher_no`, `lab_no`, `start_time`) USING BTREE,
  INDEX `lab_no`(`lab_no` ASC) USING BTREE,
  CONSTRAINT `booking_ibfk_1` FOREIGN KEY (`teacher_no`) REFERENCES `teacher` (`no`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `booking_ibfk_2` FOREIGN KEY (`lab_no`) REFERENCES `lab` (`no`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of booking
-- ----------------------------
INSERT INTO `booking` VALUES ('10001', 'G101', '2022-12-23 15:40:00', '2022-12-23 16:40:00', 'a');
INSERT INTO `booking` VALUES ('10001', 'G101', '2022-12-23 17:00:00', '2022-12-23 18:00:00', 'b');

SET FOREIGN_KEY_CHECKS = 1;
