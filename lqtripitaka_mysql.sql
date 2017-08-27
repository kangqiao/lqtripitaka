# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 5.7.17)
# Database: lqtripitaka
# Generation Time: 2017-08-27 13:25:31 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table auth_group
# ------------------------------------------------------------

DROP TABLE IF EXISTS `auth_group`;

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table auth_group_permissions
# ------------------------------------------------------------

DROP TABLE IF EXISTS `auth_group_permissions`;

CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table auth_permission
# ------------------------------------------------------------

DROP TABLE IF EXISTS `auth_permission`;

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=93 DEFAULT CHARSET=utf8;



# Dump of table auth_user
# ------------------------------------------------------------

DROP TABLE IF EXISTS `auth_user`;

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;



# Dump of table auth_user_groups
# ------------------------------------------------------------

DROP TABLE IF EXISTS `auth_user_groups`;

CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table auth_user_user_permissions
# ------------------------------------------------------------

DROP TABLE IF EXISTS `auth_user_user_permissions`;

CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table core_accessrecord
# ------------------------------------------------------------

DROP TABLE IF EXISTS `core_accessrecord`;

CREATE TABLE `core_accessrecord` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `user_count` int(11) NOT NULL,
  `view_count` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table core_lqsutra
# ------------------------------------------------------------

DROP TABLE IF EXISTS `core_lqsutra`;

CREATE TABLE `core_lqsutra` (
  `id` char(32) NOT NULL,
  `code` varchar(64) NOT NULL,
  `name` varchar(256) NOT NULL,
  `remark` longtext,
  `roll_count` int(11) DEFAULT NULL,
  `translator_id` char(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `core_lqsutra_translator_id_d14cc955_fk_core_translator_id` (`translator_id`),
  KEY `core_lqsutra_name_99780f0d` (`name`),
  CONSTRAINT `core_lqsutra_translator_id_d14cc955_fk_core_translator_id` FOREIGN KEY (`translator_id`) REFERENCES `core_translator` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table core_normname
# ------------------------------------------------------------

DROP TABLE IF EXISTS `core_normname`;

CREATE TABLE `core_normname` (
  `id` char(32) NOT NULL,
  `name` varchar(64) NOT NULL,
  `type` varchar(8) NOT NULL,
  `remark` longtext,
  PRIMARY KEY (`id`),
  KEY `core_normname_name_2d9ded81` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table core_normnamemap
# ------------------------------------------------------------

DROP TABLE IF EXISTS `core_normnamemap`;

CREATE TABLE `core_normnamemap` (
  `id` char(32) NOT NULL,
  `type` varchar(8) NOT NULL,
  `name` varchar(64) NOT NULL,
  `remark` longtext,
  `norm_name_id` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_normnamemap_norm_name_id_f568746b_fk_core_normname_id` (`norm_name_id`),
  KEY `core_normnamemap_name_5164b808` (`name`),
  CONSTRAINT `core_normnamemap_norm_name_id_f568746b_fk_core_normname_id` FOREIGN KEY (`norm_name_id`) REFERENCES `core_normname` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table core_page
# ------------------------------------------------------------

DROP TABLE IF EXISTS `core_page`;

CREATE TABLE `core_page` (
  `id` char(32) NOT NULL,
  `code` varchar(64) NOT NULL,
  `name` varchar(64) NOT NULL,
  `type` varchar(8) NOT NULL,
  `series` varchar(64) DEFAULT NULL,
  `volume` varchar(64) DEFAULT NULL,
  `sutra` varchar(64) DEFAULT NULL,
  `pre_page` varchar(64) DEFAULT NULL,
  `next_page` varchar(64) DEFAULT NULL,
  `roll_id` char(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `core_page_roll_id_e9714047_fk_core_roll_id` (`roll_id`),
  KEY `core_page_series_6bc12c24` (`series`),
  KEY `core_page_sutra_b77244ff` (`sutra`),
  KEY `core_page_volume_91b3fe33` (`volume`),
  CONSTRAINT `core_page_roll_id_e9714047_fk_core_roll_id` FOREIGN KEY (`roll_id`) REFERENCES `core_roll` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table core_pageresource
# ------------------------------------------------------------

DROP TABLE IF EXISTS `core_pageresource`;

CREATE TABLE `core_pageresource` (
  `id` char(32) NOT NULL,
  `type` varchar(8) NOT NULL,
  `source` varchar(8) NOT NULL,
  `resource` varchar(100) NOT NULL,
  `page_id` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_pageresource_page_id_b4179094_fk_core_page_id` (`page_id`),
  KEY `core_pageresource_source_34a9c1aa` (`source`),
  KEY `core_pageresource_type_c699e846` (`type`),
  CONSTRAINT `core_pageresource_page_id_b4179094_fk_core_page_id` FOREIGN KEY (`page_id`) REFERENCES `core_page` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table core_roll
# ------------------------------------------------------------

DROP TABLE IF EXISTS `core_roll`;

CREATE TABLE `core_roll` (
  `id` char(32) NOT NULL,
  `code` varchar(64) NOT NULL,
  `name` varchar(64) NOT NULL,
  `type` varchar(16) NOT NULL,
  `page_count` int(11) DEFAULT NULL,
  `start_volume` varchar(64) DEFAULT NULL,
  `end_volume` varchar(64) DEFAULT NULL,
  `start_page` varchar(64) DEFAULT NULL,
  `end_page` varchar(64) DEFAULT NULL,
  `qianziwen` varchar(8) DEFAULT NULL,
  `remark` longtext,
  `series_id` char(32) DEFAULT NULL,
  `sutra_id` char(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `core_roll_series_id_439211d5_fk_core_series_id` (`series_id`),
  KEY `core_roll_sutra_id_f09dc575_fk_core_sutra_id` (`sutra_id`),
  KEY `core_roll_type_ac227dde` (`type`),
  CONSTRAINT `core_roll_series_id_439211d5_fk_core_series_id` FOREIGN KEY (`series_id`) REFERENCES `core_series` (`id`),
  CONSTRAINT `core_roll_sutra_id_f09dc575_fk_core_sutra_id` FOREIGN KEY (`sutra_id`) REFERENCES `core_sutra` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table core_series
# ------------------------------------------------------------

DROP TABLE IF EXISTS `core_series`;

CREATE TABLE `core_series` (
  `id` char(32) NOT NULL,
  `code` varchar(64) NOT NULL,
  `name` varchar(64) NOT NULL,
  `type` varchar(2) NOT NULL,
  `volume_count` int(11) DEFAULT NULL,
  `sutra_count` int(11) DEFAULT NULL,
  `roll_count` int(11) DEFAULT NULL,
  `page_count` int(11) DEFAULT NULL,
  `word_count` int(11) DEFAULT NULL,
  `dynasty` varchar(64) DEFAULT NULL,
  `historic_site` varchar(64) DEFAULT NULL,
  `library_site` varchar(64) DEFAULT NULL,
  `book_reservation` varchar(64) DEFAULT NULL,
  `publish_name` varchar(64) DEFAULT NULL,
  `publish_date` date DEFAULT NULL,
  `publish_edition` smallint(6) DEFAULT NULL,
  `publish_prints` smallint(6) DEFAULT NULL,
  `publish_ISBN` varchar(64) DEFAULT NULL,
  `remark` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table core_sutra
# ------------------------------------------------------------

DROP TABLE IF EXISTS `core_sutra`;

CREATE TABLE `core_sutra` (
  `id` char(32) NOT NULL,
  `code` varchar(64) NOT NULL,
  `name` varchar(64) NOT NULL,
  `type` varchar(2) NOT NULL,
  `clazz` varchar(64) DEFAULT NULL,
  `dynasty` varchar(64) DEFAULT NULL,
  `historic_site` varchar(64) DEFAULT NULL,
  `roll_count` int(11) DEFAULT NULL,
  `page_count` int(11) DEFAULT NULL,
  `start_volume` varchar(64) DEFAULT NULL,
  `end_volume` varchar(64) DEFAULT NULL,
  `start_page` varchar(64) DEFAULT NULL,
  `end_page` varchar(64) DEFAULT NULL,
  `qianziwen` varchar(8) DEFAULT NULL,
  `resource` varchar(100) DEFAULT NULL,
  `remark` longtext,
  `lqsutra_id` char(32) DEFAULT NULL,
  `series_id` char(32) DEFAULT NULL,
  `translator_id` char(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `core_sutra_series_id_62f05234_fk_core_series_id` (`series_id`),
  KEY `core_sutra_translator_id_d55eb245_fk_core_translator_id` (`translator_id`),
  KEY `core_sutra_lqsutra_id_977ded90_fk` (`lqsutra_id`),
  KEY `core_sutra_type_255d4500` (`type`),
  CONSTRAINT `core_sutra_lqsutra_id_977ded90_fk` FOREIGN KEY (`lqsutra_id`) REFERENCES `core_lqsutra` (`id`),
  CONSTRAINT `core_sutra_series_id_62f05234_fk_core_series_id` FOREIGN KEY (`series_id`) REFERENCES `core_series` (`id`),
  CONSTRAINT `core_sutra_translator_id_d55eb245_fk_core_translator_id` FOREIGN KEY (`translator_id`) REFERENCES `core_translator` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table core_translator
# ------------------------------------------------------------

DROP TABLE IF EXISTS `core_translator`;

CREATE TABLE `core_translator` (
  `id` char(32) NOT NULL,
  `name` varchar(256) NOT NULL,
  `type` varchar(2) NOT NULL,
  `remark` longtext,
  PRIMARY KEY (`id`),
  KEY `core_translator_name_6c74417e` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table core_volume
# ------------------------------------------------------------

DROP TABLE IF EXISTS `core_volume`;

CREATE TABLE `core_volume` (
  `id` char(32) NOT NULL,
  `code` varchar(64) NOT NULL,
  `name` varchar(64) NOT NULL,
  `page_count` int(11) DEFAULT NULL,
  `start_page` varchar(64) DEFAULT NULL,
  `end_page` varchar(64) DEFAULT NULL,
  `resource` varchar(100) DEFAULT NULL,
  `remark` longtext,
  `series_id` char(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `core_volume_series_id_94c6ff67_fk_core_series_id` (`series_id`),
  CONSTRAINT `core_volume_series_id_94c6ff67_fk_core_series_id` FOREIGN KEY (`series_id`) REFERENCES `core_series` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table django_admin_log
# ------------------------------------------------------------

DROP TABLE IF EXISTS `django_admin_log`;

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;



# Dump of table django_content_type
# ------------------------------------------------------------

DROP TABLE IF EXISTS `django_content_type`;

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;



# Dump of table django_migrations
# ------------------------------------------------------------

DROP TABLE IF EXISTS `django_migrations`;

CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8;



# Dump of table django_session
# ------------------------------------------------------------

DROP TABLE IF EXISTS `django_session`;

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table reversion_revision
# ------------------------------------------------------------

DROP TABLE IF EXISTS `reversion_revision`;

CREATE TABLE `reversion_revision` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_created` datetime(6) NOT NULL,
  `comment` longtext NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `reversion_revision_user_id_17095f45_fk_auth_user_id` (`user_id`),
  KEY `reversion_revision_date_created_96f7c20c` (`date_created`),
  CONSTRAINT `reversion_revision_user_id_17095f45_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;



# Dump of table reversion_version
# ------------------------------------------------------------

DROP TABLE IF EXISTS `reversion_version`;

CREATE TABLE `reversion_version` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `object_id` varchar(191) NOT NULL,
  `format` varchar(255) NOT NULL,
  `serialized_data` longtext NOT NULL,
  `object_repr` longtext NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `revision_id` int(11) NOT NULL,
  `db` varchar(191) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `reversion_version_db_content_type_id_objec_b2c54f65_uniq` (`db`,`content_type_id`,`object_id`,`revision_id`),
  KEY `reversion_version_content_type_id_7d0ff25c_fk_django_co` (`content_type_id`),
  KEY `reversion_version_revision_id_af9f6a9d_fk_reversion_revision_id` (`revision_id`),
  CONSTRAINT `reversion_version_content_type_id_7d0ff25c_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `reversion_version_revision_id_af9f6a9d_fk_reversion_revision_id` FOREIGN KEY (`revision_id`) REFERENCES `reversion_revision` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;



# Dump of table xadmin_bookmark
# ------------------------------------------------------------

DROP TABLE IF EXISTS `xadmin_bookmark`;

CREATE TABLE `xadmin_bookmark` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(128) NOT NULL,
  `url_name` varchar(64) NOT NULL,
  `query` varchar(1000) NOT NULL,
  `is_share` tinyint(1) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `xadmin_bookmark_content_type_id_60941679_fk_django_co` (`content_type_id`),
  KEY `xadmin_bookmark_user_id_42d307fc_fk_auth_user_id` (`user_id`),
  CONSTRAINT `xadmin_bookmark_content_type_id_60941679_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `xadmin_bookmark_user_id_42d307fc_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table xadmin_log
# ------------------------------------------------------------

DROP TABLE IF EXISTS `xadmin_log`;

CREATE TABLE `xadmin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `ip_addr` char(39) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` varchar(32) NOT NULL,
  `message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `xadmin_log_content_type_id_2a6cb852_fk_django_content_type_id` (`content_type_id`),
  KEY `xadmin_log_user_id_bb16a176_fk_auth_user_id` (`user_id`),
  CONSTRAINT `xadmin_log_content_type_id_2a6cb852_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `xadmin_log_user_id_bb16a176_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;



# Dump of table xadmin_usersettings
# ------------------------------------------------------------

DROP TABLE IF EXISTS `xadmin_usersettings`;

CREATE TABLE `xadmin_usersettings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `key` varchar(256) NOT NULL,
  `value` longtext NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `xadmin_usersettings_user_id_edeabe4a_fk_auth_user_id` (`user_id`),
  CONSTRAINT `xadmin_usersettings_user_id_edeabe4a_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;



# Dump of table xadmin_userwidget
# ------------------------------------------------------------

DROP TABLE IF EXISTS `xadmin_userwidget`;

CREATE TABLE `xadmin_userwidget` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `page_id` varchar(256) NOT NULL,
  `widget_type` varchar(50) NOT NULL,
  `value` longtext NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `xadmin_userwidget_user_id_c159233a_fk_auth_user_id` (`user_id`),
  CONSTRAINT `xadmin_userwidget_user_id_c159233a_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
