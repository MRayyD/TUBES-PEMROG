/*
SQLyog Enterprise - MySQL GUI v8.05 
MySQL - 5.5.5-10.4.32-MariaDB : Database - note_app
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`note_app` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;

/*Data for the table `note` */

insert  into `note`(`id`,`content`,`user_id`,`doodle`,`notebook_id`) values (70,'sdgfsgdfd',1,'',5);

/*Data for the table `notebook` */

insert  into `notebook`(`id`,`title`,`content`,`user_id`) values (5,'Hai',NULL,1),(6,'Halo',NULL,1);

/*Data for the table `user` */

insert  into `user`(`id`,`username`,`password`) values (1,'rayza','pbkdf2:sha256:600000$g8flYpPkxXaaxyBp$74b628d5dc72cc549ede0767c3a001a3bf058aed0177664238db17783eeb4809');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
