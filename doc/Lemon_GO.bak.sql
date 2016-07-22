/*
SQLyog Ultimate v12.08 (32 bit)
MySQL - 5.5.45 : Database - Lemon_GO
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`Lemon_GO` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `Lemon_GO`;

/*Table structure for table `backup` */

DROP TABLE IF EXISTS `backup`;

CREATE TABLE `backup` (
  `backup_id` int(10) NOT NULL AUTO_INCREMENT,
  `backup_jobname` varchar(50) NOT NULL,
  `backup_ipaddr` varchar(15) NOT NULL,
  `ssh_port` int(5) NOT NULL,
  `backup_source` varchar(80) NOT NULL,
  `backup_destination` char(80) NOT NULL,
  `backup_shedule` varchar(20) DEFAULT NULL,
  `backup_owner` varchar(16) DEFAULT NULL,
  `created_time` datetime DEFAULT NULL,
  `last_runtime` datetime DEFAULT NULL,
  `backup_state` char(10) DEFAULT NULL,
  `backup_server` varchar(20) NOT NULL,
  PRIMARY KEY (`backup_id`)
) ENGINE=InnoDB AUTO_INCREMENT=99 DEFAULT CHARSET=utf8;

/*Data for the table `backup` */

insert  into `backup`(`backup_id`,`backup_jobname`,`backup_ipaddr`,`ssh_port`,`backup_source`,`backup_destination`,`backup_shedule`,`backup_owner`,`created_time`,`last_runtime`,`backup_state`,`backup_server`) values (3,'jboss','10.1.2.3',22,'/opt','/opt/backup','00 02 * * *','haha','2015-12-21 15:29:20','2016-04-22 16:15:00','sucess','backup_server_01'),(79,'nagios','1.1.1.2',10022,'/opt/jboss/','/opt/backup/jboss/','00 01 * * *','我被青','2016-04-06 17:11:46','2016-04-25 10:58:41','sucess','backup_server_01'),(84,'test','10.2.2.1',22,'/etc/named/','/opt/Backup/','00 01 12 * *','wawa','2016-07-06 13:45:51',NULL,NULL,'backup_server_02'),(95,'om-center','10.48.192.160',22,'/etc/ssh/','/opt/Backup/etc/ssh/','00 01 * * 2','mgcheng','2016-07-18 09:26:30','2016-07-19 17:03:36','Failed','om-center'),(98,'test-client.mgtest.com','10.48.192.205',22,'/tmp','/opt/Backup/test-client.mgtest.com_tmp','00 01 * * *','mgcheng','2016-07-19 17:39:02','2016-07-21 01:00:03','Failed','om-center');

/*Table structure for table `backup_server` */

DROP TABLE IF EXISTS `backup_server`;

CREATE TABLE `backup_server` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `server_name` varchar(30) DEFAULT NULL,
  `ipaddress` varchar(15) DEFAULT NULL,
  `backup_folder` varchar(20) DEFAULT NULL,
  `backup_user` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=35 DEFAULT CHARSET=utf8;

/*Data for the table `backup_server` */

insert  into `backup_server`(`id`,`server_name`,`ipaddress`,`backup_folder`,`backup_user`) values (1,'backup_server_01','10.2.2.2','/opt/Backup/','backup'),(2,'backup_server_02','192.1.2.1','/opt/Backup/','backup'),(3,'backup_server_03','10.2.1.2','/opt/Backup/','backup'),(34,'om-center','10.48.192.162','/opt/Backup','backup');

/*Table structure for table `roles` */

DROP TABLE IF EXISTS `roles`;

CREATE TABLE `roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role_name` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `role_name` (`role_name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

/*Data for the table `roles` */

insert  into `roles`(`id`,`role_name`) values (1,'Administrator'),(3,'Guest'),(2,'User');

/*Table structure for table `server` */

DROP TABLE IF EXISTS `server`;

CREATE TABLE `server` (
  `server_id` int(10) NOT NULL AUTO_INCREMENT,
  `server_hostname` varchar(50) NOT NULL,
  `server_ipaddr` varchar(15) DEFAULT '-.-.-.-',
  `server_os` varchar(20) DEFAULT NULL,
  `server_cpu` varchar(80) DEFAULT NULL,
  `server_memory` char(20) DEFAULT NULL,
  `server_model` varchar(40) DEFAULT NULL,
  `server_application` varchar(50) DEFAULT NULL,
  `server_owner` varchar(16) DEFAULT NULL,
  `server_location` varchar(16) DEFAULT NULL,
  `server_sn` varchar(16) DEFAULT NULL,
  `server_warranty` date DEFAULT NULL,
  `created_time` datetime DEFAULT NULL,
  `updated_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `server_remarks` varchar(120) DEFAULT NULL,
  PRIMARY KEY (`server_id`),
  UNIQUE KEY `server_hostname` (`server_hostname`),
  UNIQUE KEY `server_ipaddr` (`server_ipaddr`)
) ENGINE=InnoDB AUTO_INCREMENT=110 DEFAULT CHARSET=utf8;

/*Data for the table `server` */

insert  into `server`(`server_id`,`server_hostname`,`server_ipaddr`,`server_os`,`server_cpu`,`server_memory`,`server_model`,`server_application`,`server_owner`,`server_location`,`server_sn`,`server_warranty`,`created_time`,`updated_time`,`server_remarks`) values (108,'test-client','10.48.192.205','CentOS-6.7-x86_64','1 * Intel(R) Xeon(R) CPU E5-2609 0 @ 2.40GHz','1877','VMware',NULL,NULL,NULL,NULL,NULL,'2016-07-21 19:00:30',NULL,NULL),(109,'om-center','10.48.192.162','CentOS-6.8-x86_64','1 * Intel(R) Xeon(R) CPU E5-2609 0 @ 2.40GHz','980','VMware',NULL,NULL,NULL,NULL,NULL,'2016-07-21 19:00:30',NULL,NULL);

/*Table structure for table `users` */

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(64) DEFAULT NULL,
  `user_email` varchar(64) DEFAULT NULL,
  `password_hash` varchar(128) DEFAULT NULL,
  `created_time` datetime DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_users_email` (`user_email`),
  UNIQUE KEY `ix_users_user_name` (`user_name`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;

/*Data for the table `users` */

insert  into `users`(`id`,`user_name`,`user_email`,`password_hash`,`created_time`,`role_id`) values (1,'admin','admin@lemon.com','pbkdf2:sha1:1000$ISzcv13G$e60726cc7237be1cd9000f540a3d4681712cebb0','2016-06-15 17:50:44',1),(12,'gaga','gaga@lemon.com','pbkdf2:sha1:1000$TjYDpWcE$564293f5ddcc20848d78a0b870ae1972822bb345','2016-07-01 16:42:14',3),(13,'lala','lala@lemon.com','pbkdf2:sha1:1000$TvuGbBsq$95cc6a0f4177ae258a571c6ff02d9347c710b68a','2016-07-01 17:58:10',2);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
