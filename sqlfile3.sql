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

USE `note_app`;

/*Table structure for table `note` */

DROP TABLE IF EXISTS `note`;

CREATE TABLE `note` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` text NOT NULL,
  `user_id` int(11) NOT NULL,
  `doodle` text DEFAULT NULL,
  `notebook_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `notebook_id` (`notebook_id`),
  CONSTRAINT `note_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `note_ibfk_2` FOREIGN KEY (`notebook_id`) REFERENCES `notebook` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=104 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `note` */

insert  into `note`(`id`,`content`,`user_id`,`doodle`,`notebook_id`) values (103,'Ini harusnya tanda tangan saya',1,'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABf4AAAEsCAYAAACSQKKDAAAgAElEQVR4Xu3dCbx253gvfqfUrI6ahxBzS6ggZk7MUyglURJDzNXiX2NU/I9zpCVqKEoNGaipkqh5pnLUUIIoidZUMRPUMZdGnetXa9Xjyd773WvvZ1jD9/58rs969rPXs9Z1f+/1vsl7rfXc9387i0aAAAECBAgQIECAAAECBAgQIECAAAECBAiMRuC/jaYnOkKAAAECBAgQIECAAAECBAgQIECAAAECBAicReHfRUCAAAECBAgQIECAAAECBAgQIECAAAECBEYkoPA/osHUFQIECBAgQIAAAQIECBAgQIAAAQIECBAgoPDvGiBAgAABAgQIECBAgAABAgQIECBAgAABAiMSUPgf0WDqCgECBAgQIECAAAECBAgQIECAAAECBAgQUPh3DRAgQIAAAQIECBAgQIAAAQIECBAgQIAAgREJKPyPaDB1hQABAgQIECBAgAABAgQIECBAgAABAgQIKPy7BggQIECAAAECBAgQIECAAAECBAgQIECAwIgEFP5HNJi6QoAAAQIECBAgQIAAAQIECBAgQIAAAQIEFP5dAwQIECBAgAABAgQIECBAgAABAgQIECBAYEQCCv8jGkxdIUCAAAECBAgQIECAAAECBAgQIECAAAECCv+uAQIECBAgQIAAAQIECBAgQIAAAQIECBAgMCIBhf8RDaauECBAgAABAgQIECBAgAABAgQIECBAgAABhX/XAAECBAgQIECAAAECBAgQIECAAAECBAgQGJGAwv+IBlNXCBAgQIAAAQIECBAgQIAAAQIECBAgQICAwr9rgAABAgQIECBAgAABAgQIECBAgAABAgQIjEhA4X9Eg6krBAgQIECAAAECBAgQIECAAAECBAgQIEBA4d81QIAAAQIECBAgQIAAAQIECBAgQIAAAQIERiSg8D+iwdQVAgQIECBAgAABAgQIECBAgAABAgQIECCg8O8aIECAAAECBAgQIECAAAECBAgQIECAAAECIxJQ+B/RYOoKAQIECBAgQIAAAQIECBAgQIAAAQIECBBQ+HcNECBAgAABAgQIECBAgAABAgQIECBAgACBEQko/I9oMHWFAAECBAgQIECAAAECBAgQIECAAAECBAgo/LsGCBAgQIAAAQIECBAgQIAAAQIECBAgQIDAiAQU/kc0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0OcJrE9gnzr1ByrOW/GEiiPWl4ozEyBAgAABAgQIECBAgAABAgQIECDQFwGF/76MhDwIdBc4uj5y34qXVxzS/eM+QYAAAQIECBAgQIAAAQIECBAgQIDAGAUU/sc4qvo0BYEnVycPq3hdRab7OWMKndZHAgQIECBAgAABAgQIECBAgAABAgT2LKDwv2cjexDom8D+ldC7m6RuWtsT+5agfAgQIECAAAECBAgQIECAAAECBAgQWJ+Awv/67J2ZwE4FnloffHTFUyoet9OD+BwBAgQIECBAgAABAgQIECBAgAABAuMUUPgf57jq1fgFblFdfOf4u6mHBAgQIECAAAECBAgQIECAAAECBAh0FVD47ypmfwIECBAgQIAAAQIECBAgQIAAAQIECBAg0GMBhf8eD47UCBAgQIAAAQIECBAgQIAAAQIECBAgQIBAVwGF/65i9idAgAABAgQIECBAgAABAgQIECBAgAABAj0WUPjv8eBIjQABAgQIECBAgAABAgQIECBAgAABAgQIdBVQ+O8qZn8CBAgQIECAAAECBAgQIECAAAECBAgQINBjAYX/Hg+O1AgQIECAAAECBAgQIECAAAECBAgQIECAQFcBhf+uYvYnQIAAAQIECBAgQIAAAQIECBAgQIAAAQI9FlD47/HgSI0AAQIECBAgQIAAAQIECBAgQIAAAQIECHQVUPjvKmZ/AgQIECBAgAABAgQIECBAgAABAgQIECDQYwGF/x4PjtQIECBAgAABAgQIECBAgAABAgQIECBAgEBXAYX/rmL2J0CAAAECBAgQIECAAAECBAgQIECAAAECPRZQ+O/x4EiNAAECBAgQIECAAAECBAgQIECAAAECBAh0FVD47ypmfwIECBAgQIAAAQIECBAgQIAAAQIECBAg0GMBhf8eD47UCBAgQIAAAQIECBAgQIAAAQIECBAgQIBAVwGF/65i9idAgAABAgQIECBAgAABAgQIECBAgAABAj0WUPjv8eBIjQABAgQIECBAgAABAgQIECBAgAABAgQIdBVQ+O8qZn8CBAgQIECAAAECBAgQIECAAAECBAgQINBjAYX/Hg+O1AgQIECAAAECBAgQIECAAAECBAgQIECAQFcBhf+uYvYnQIAAAQIECBAgQIAAAQIECBAgQIAAAQI9FlD47/HgSI0AAQIECBAgQIAAAQIECBAgQIAAAQIECHQVUPjvKmZ/AgQIECBAgAABAgQIECBAgAABAgQIECDQYwGF/x4PjtQIECBAgAABAgQIECBAgAABAgQIECBAgEBXAYX/rmL2J0CAAAECBAgQIECAAAECBAgQIECAAAECPRZQ+O/x4EiNAAECBAgQIECAAAECBAgQIECAAAECBAh0FVD47ypmfwIECBAgQIAAAQIECBAgQIAAAQIECBAg0GMBhf8eD47UCBAgQIAAAQIECBAgQIAAAQIECBAgQIBAVwGF/65i9idAgAABAgQIECBAgAABAgQIECBAgAABAj0WUPjv8eBIjQABAgQIECBAgAABAgQIECBAgAABAgQIdBVQ+O8qZn8CBAgQIECAAAECBAgQIECAAAECBAgQINBjAYX/Hg+O1AgQIECAAAECBAgQIECAAAECBAgQIECAQFcBhf+uYvYnQIAAAQIECBAgQIAAAQIECBAgQIAAAQI9FlD47/HgSI0AAQIECBAgQIAAAQIECBAgQIAAAQIECHQVUPjvKmZ/AgQIECBAgAABAgQIECBAgAABAgQIECDQYwGF/x4PjtQIECBAgAABAgQIECBAgAABAgQIECBAgEBXAYX/rmL2J0CAAAECBAgQIECAAAECBAgQIECAAAECPRZQ+O/x4EiNAAECBAgQIECAAAECBAgQIECAAAECBAh0FVD47ypmfwIECBAgQIAAAQIECBAgQIAAAQIECBAg0GMBhf8eD47UCBAgQIAAAQIECBAgQIAAAQIECBAgQIBAVwGF/65i9idAgAABAgQIECBAgAABAgQIECBAgAABAj0WUPjv8eBIjQABAgQIECBAgAABAgQIECBAgAABAgQIdBVQ+O8qZn8CBAgQIECAAAECBAgQIECAAAECBAgQINBjAYX/Hg+O1AgQIECAAAECBAgQIECAAAECBAgQIECAQFcBhf+uYvYnQIAAAQIECBAgQIAAAQIECBAgQIAAAQI9FlD47/HgSI0AAQIECBAgQIAAAQIECBAgQIAAAQIECHQVUPjvKmZ/AgQIECBAgAABAgQIECBAgAABAgQIECDQYwGF/x4PjtQIECBAgAABAgQIECBAgAABAgQIECBAgEBXAYX/rmL2J0CAAAECBAgQIECAAAECBAgQIECAAAECPRZQ+O/x4EiNAAECBAgQIECAAAECBAgQIECAAAECBAh0FVD47ypmfwIECBAgQIAAAQIECBAgQIAAAQIECBAg0GMBhf8eD47UCBAgQIAAAQIECBAgQIAAAQIECBAgQIBAVwGF/65i9idAgAABAgQIECBAgAABAgQIECBAgAABAj0WUPjv8eBIjQABAgQIECBAgAABAgQIECBAgAABAgQIdBVQ+O8qZn8CBAgQIECAAAECBAgQIECAAAECBAgQINBjAYX/Hg+O1AgQIECAAAECBAgQIECAAAECBAgQIECAQFcBhf+uYvYnQIAAAQIECBAgQIAAAQIECBAgQIAAAQI9FlD47/HgSI0AAQIECBAgQIAAAQIECBAgQIAAAQIECHQVUPjvKmZ/AgQIECBAgAABAgQIECBAgAABAgQIECDQYwGF/x4PjtQIECBAgAABAgQIECBAgAABAgQIECBAgEBXAYX/rmL2J0CAAAECBAgQIECAAAECBAgQIECAAAECPRZQ+O/x4EiNAAECBAgQIECAAAECBAgQIECAAAECBAh0FVD47ypmfwIECBAgQIAAAQIECBAgQIAAAQIECBAg0GMBhf8eD47UCBAgQIAAAQIECBAgQIAAAQIECBAgQIBAVwGF/65i9idAgAABAgQIECBAgAABAgQIECBAgAABAj0WUPjv8eBIjQABAgQIECBAgAABAgQIECBAgAABAgQIdBVQ+O8qZn8CBAgQIECAAAECBAgQIECAAAECBAgQINBjAYX/Hg+O1AgQIECAAAECBAgQIECAAAECBAgQIECAQFcBhf+uYvYnQIAAAQIECBAgQIAAAQIECBAgQIAAAQI9FlD47/HgSI0AAQIECBAgQIAAAQIECBAgQIAAAQIECHQVUPjvKmZ/AgQIECBAgAABAgQIECBAgAABAgQIECDQYwGF/x4PjtQIECBAgAABAgQIECBAgAABAgQIECBAgEBXAYX/rmL2J0CAAAECBAgQIECAAAECBAgQIECAAAECPRZQ+O/x4EiNAAECBAgQIECAAAECBAgQIECAAAECBAh0FVD47ypmfwIECBAgQIAAAQIECBAgQIAAAQIECBAg0GMBhf8eD47UCBAgQIAAAQIECBAgQIAAAQIECBAgQIBAVwGF/65i9idAgAABAgQIECBAgAABAgQIECBAgAABAj0WUPjv8eBIjQABAgQIECBAgAABAgQIECBAgAABAgQIdBVQ+O8qZn8CBAgQIECAAAECBAgQIECAAAECBAgQINBjAYX/Hg+O1AgQIECAAAECBAgQIECAAAECBAgQIECAQFcBhf+uYvYnQIAAAQIECBAgQIAAAQIECBAgQIAAAQI9FlD47/HgSI0AAQIECBAgQIAAAQIECBAgQIAAAQIECHQVUPjvKmZ/AgQIECBAgAABAgQIECBAgAABAgQIECDQYwGF/x4PjtQIECBAgAABAgQIECBAgAABAgQIECBAgEBXAYX/rmL2J0CAAAECBAgQIECAAAECBAgQIECAAAECPRZQ+O/x4EiNAAECBAgQIECAAAECBAgQIECAAAECBAh0FVD47ypmfwIECBAgQIAAAQIECBAgQIAAAQIECBAg0GMBhf8eD47UCBAgQIAAAQIECBAgQIAAAQIECBAgQIBAVwGF/65i9idAgAABAgQIECBAgAABAgQIECBAgAABAj0WUPjv8eBIjQABAgQIECBAgAABAgQIECBAgAABAgQIdBVQ+O8qZn8CBAgQIECAAAECBAgQIECAAAECBAgQINBjAYX/Hg+O1AgQIECAAAECBAgQIECAAAECBAgQIECAQFcBhf+uYvYnQIAAAQIECBAgQIAAAQIECBAgQIAAAQI9FlD47/HgSI0AAQIECBAgQIAAAQIECBAgQIAAAQIECHQVUPjvKmZ/AgQIECBAgAABAgQIECBAgAABAgQIECDQYwGF/x4PjtQIECBAgAABAgQIECBAgAABAgQIECBAgEBXAYX/rmL2J0CAAAECBAgQIECAAAECBAgQIECAAAECPRZQ+O/x4EiNAAECBAgQIECAAAECBAgQIECAAAECBAh0FVD47ypmfwIECBAgQIAAAQIECBAgQIAAAQIECBAg0GOB/wcH3EK0gb4F3QAAAABJRU5ErkJggg==',5);

/*Table structure for table `notebook` */

DROP TABLE IF EXISTS `notebook`;

CREATE TABLE `notebook` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `notebook_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `notebook` */

insert  into `notebook`(`id`,`title`,`user_id`) values (5,'Hai',1),(6,'Halo',1),(7,'Hai',1);

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `user` */

insert  into `user`(`id`,`username`,`password`) values (1,'rayza','pbkdf2:sha256:600000$g8flYpPkxXaaxyBp$74b628d5dc72cc549ede0767c3a001a3bf058aed0177664238db17783eeb4809'),(2,'jmk','pbkdf2:sha256:1000000$xxUx7tuboLK3CYa6$8b157a04c190fef0695de14a1f31708bce462e3f8b3b9eb7bab3783bc1b5ecec'),(3,'akugila','pbkdf2:sha256:1000000$PExF0aju9zgYlj75$dc3661f4a1cb3d48f583049e9b40742516a663d9f3a6df1ca17a0c61231191d9');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;