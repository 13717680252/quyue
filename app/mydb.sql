-- MySQL dump 10.13  Distrib 5.7.9, for Win64 (x86_64)
--
-- Host: localhost    Database: yue
-- ------------------------------------------------------
-- Server version	5.7.9-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `t_activity`
--

DROP TABLE IF EXISTS `t_activity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_activity` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `publisher` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `description` varchar(1000) NOT NULL,
  `create_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `start_date` datetime NOT NULL,
  `end_date` datetime NOT NULL,
  `min_num` int(11) NOT NULL DEFAULT '0',
  `max_num` int(11) NOT NULL DEFAULT '0',
  `cur_num` int(11) NOT NULL DEFAULT '0',
  `join_ids` text NOT NULL,
  `is_expired` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `tags` varchar(1000) NOT NULL DEFAULT '',
  `is_canceled` tinyint(3) unsigned NOT NULL,
  `cancel_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `name_2` (`name`),
  KEY `fk_ac_gid_idx` (`group_id`),
  KEY `fk_ac_user_idx` (`publisher`),
  CONSTRAINT `fk_ac_gid` FOREIGN KEY (`group_id`) REFERENCES `t_group` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `fk_ac_user` FOREIGN KEY (`publisher`) REFERENCES `t_user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_activity`
--

LOCK TABLES `t_activity` WRITE;
/*!40000 ALTER TABLE `t_activity` DISABLE KEYS */;
INSERT INTO `t_activity` VALUES (2,'新活动',22,2,'a description','2017-05-10 14:24:06','2017-05-10 14:24:06','2017-05-10 14:24:06',2,10,3,'',0,'聚餐,交友',0,NULL),(4,'新活动2',22,2,'a description','2017-05-10 14:25:32','2017-05-10 14:25:32','2017-05-10 14:25:32',2,10,3,'',0,'聚餐,交友',0,NULL),(5,'新活动3',22,2,'a description','2017-05-10 14:26:02','2017-05-10 14:26:03','2017-05-10 14:26:03',2,10,3,'',0,'聚餐,交友',0,NULL),(6,'新活动4',22,2,'a description','2017-05-24 10:02:11','2017-06-01 21:00:00','2017-05-31 21:00:00',2,10,1,'22',0,'聚餐,交友',0,NULL),(7,'新活动5',22,2,'a description','2017-05-24 10:02:11','2017-06-01 21:00:00','2017-05-31 21:00:00',2,10,1,'22,23',0,'聚餐,交友',0,NULL),(8,'新活动6',22,2,'a description','2017-05-24 10:02:11','2017-06-01 21:00:00','2017-05-31 21:00:00',2,10,1,'22',0,'聚餐,交友',0,NULL),(9,'新活动8',22,2,'a description','2017-06-05 16:47:44','2017-06-09 21:00:00','2017-05-31 21:00:00',2,10,1,'22,22',0,'爆菊,编程',0,NULL),(10,'新活动9',22,2,'a description','2017-06-05 16:47:44','2017-06-09 21:00:00','2017-05-31 21:00:00',2,10,1,'',0,'日狗,交大',0,NULL),(11,'新活动11',22,2,'a description','2017-06-05 16:47:44','2017-06-09 21:00:00','2017-05-31 21:00:00',2,10,1,'',0,'智障,四道口',0,NULL),(12,'新活动12',22,2,'a description','2017-06-10 14:16:45','2017-06-20 21:00:00','2017-06-16 21:00:00',2,10,3,'22,24',0,'爆菊,编程',0,NULL),(13,'新活动13',22,2,'a description','2017-06-10 14:16:45','2017-06-20 21:00:00','2017-06-16 21:00:00',2,10,3,'22,23',0,'日狗,交大',0,NULL),(14,'新活动14',22,2,'a description','2017-06-10 14:16:45','2017-06-20 21:00:00','2017-06-16 21:00:00',2,10,4,'22,23,24',0,'交大,四道口',0,NULL),(15,'新活动16',24,2,'a description','2017-06-10 18:21:45','2017-06-20 21:00:00','2017-06-16 21:00:00',2,10,2,'22',0,'爆菊,编程',0,NULL),(16,'新活动17',24,2,'a description','2017-06-10 18:21:45','2017-06-20 21:00:00','2017-06-16 21:00:00',2,10,2,'22',0,'爆菊,口交',0,NULL),(17,'新活动18',24,2,'a description','2017-06-10 18:21:45','2017-06-20 21:00:00','2017-06-16 21:00:00',2,10,1,'',0,'爆菊,四道口',0,NULL),(18,'新活动20',24,2,'a description','2017-06-10 18:38:28','2017-06-20 21:00:00','2017-06-16 21:00:00',2,10,1,'',0,'交大,编程',0,NULL),(19,'新活动21',24,2,'a description','2017-06-10 18:38:28','2017-06-20 21:00:00','2017-06-16 21:00:00',2,10,1,'',0,'交大,口交',0,NULL),(20,'新活动22',24,2,'a description','2017-06-10 18:38:28','2017-06-20 21:00:00','2017-06-16 21:00:00',2,10,1,'',0,'爆菊,四道口',0,NULL);
/*!40000 ALTER TABLE `t_activity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_chat`
--

DROP TABLE IF EXISTS `t_chat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_chat` (
  `get_id` int(11) NOT NULL,
  `send_id` int(11) NOT NULL,
  `chat_info` varchar(100) NOT NULL,
  `chat_data` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `is_notify` int(11) DEFAULT '0',
  `is_clear` int(11) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_chat`
--

LOCK TABLES `t_chat` WRITE;
/*!40000 ALTER TABLE `t_chat` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_chat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_comment_activity`
--

DROP TABLE IF EXISTS `t_comment_activity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_comment_activity` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `activity_id` bigint(20) NOT NULL,
  `comment_user_id` int(11) NOT NULL,
  `level` tinyint(3) unsigned NOT NULL,
  `content` varchar(100) DEFAULT NULL,
  `create_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `is_deleted` tinyint(4) NOT NULL DEFAULT '0',
  `delelte_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_ca_act_idx` (`activity_id`),
  KEY `fk_ca_user_idx` (`comment_user_id`),
  CONSTRAINT `fk_ca_act` FOREIGN KEY (`activity_id`) REFERENCES `t_activity` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `fk_ca_user` FOREIGN KEY (`comment_user_id`) REFERENCES `t_user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_comment_activity`
--

LOCK TABLES `t_comment_activity` WRITE;
/*!40000 ALTER TABLE `t_comment_activity` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_comment_activity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_commnet_people`
--

DROP TABLE IF EXISTS `t_commnet_people`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_commnet_people` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `activity_id` bigint(20) NOT NULL,
  `comment_user_id` int(11) NOT NULL,
  `commented_user_id` int(11) NOT NULL,
  `level` tinyint(3) unsigned NOT NULL,
  `content` varchar(100) NOT NULL,
  `create_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `is_deleted` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `delete_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_act_idx` (`activity_id`),
  KEY `fk_cmp_user1_idx` (`comment_user_id`),
  KEY `fk_cmp_user2_idx` (`commented_user_id`),
  CONSTRAINT `fk_act` FOREIGN KEY (`activity_id`) REFERENCES `t_activity` (`id`) ON DELETE NO ACTION ON UPDATE CASCADE,
  CONSTRAINT `fk_cmp_user1` FOREIGN KEY (`comment_user_id`) REFERENCES `t_user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_cmp_user2` FOREIGN KEY (`commented_user_id`) REFERENCES `t_user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_commnet_people`
--

LOCK TABLES `t_commnet_people` WRITE;
/*!40000 ALTER TABLE `t_commnet_people` DISABLE KEYS */;
INSERT INTO `t_commnet_people` VALUES (1,7,22,23,3,'dwadadada','2017-06-10 15:19:24',0,NULL),(2,7,22,23,3,'dwadadada','2017-06-10 15:21:01',0,NULL);
/*!40000 ALTER TABLE `t_commnet_people` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_group`
--

DROP TABLE IF EXISTS `t_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `type` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `description` varchar(1000) NOT NULL,
  `create_date` date NOT NULL,
  `attention_count` int(11) NOT NULL DEFAULT '0',
  `activetity_count` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `name_2` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_group`
--

LOCK TABLES `t_group` WRITE;
/*!40000 ALTER TABLE `t_group` DISABLE KEYS */;
INSERT INTO `t_group` VALUES (2,'篮球',0,'系统自定义组','2017-04-01',1,15),(3,'足球',0,'','2017-04-01',1,0),(4,'网球',0,'','2017-04-01',0,0),(5,'跑步',0,'','2017-04-01',0,0),(6,'攀岩',0,'','2017-04-01',0,0),(7,'自行车',0,'','2017-04-01',0,0),(8,'乒乓球',0,'','2017-04-01',0,0),(9,'健身',0,'','2017-04-01',0,0),(10,'羽毛球',0,'','2017-04-01',0,0),(11,'游泳',0,'','2017-04-01',0,0),(12,'棒球',0,'','2017-04-01',0,0),(13,'太极拳',0,'','2017-04-01',0,0),(14,'吉他',1,'','2017-04-01',0,0),(15,'绘画',1,'','2017-04-01',0,0),(16,'扬琴',1,'','2017-04-01',0,0),(17,'古筝',1,'','2017-04-01',0,0),(18,'诗歌',1,'','2017-04-01',0,0),(19,'舞蹈',1,'','2017-04-01',0,0),(20,'歌曲',1,'','2017-04-01',0,0),(21,'书法',1,'','2017-04-01',0,0),(22,'电影',1,'','2017-04-01',0,0),(23,'小说',1,'','2017-04-01',0,0),(24,'自习',2,'','2017-04-01',0,0),(25,'实验',2,'','2017-04-01',0,0),(27,'辩论会',2,'','2017-04-01',0,0),(28,'书友会',2,'','2017-04-01',0,0),(29,'摄影',1,'','2017-04-01',0,0),(30,'表演',1,'','2017-04-01',0,0),(31,'数学建模',2,'','2017-04-01',0,0),(32,'宣讲会',2,'','2017-04-01',0,0),(33,'新软攀峰',2,'','2017-04-01',0,0),(34,'英语写作',2,'','2017-04-01',0,0),(35,'程序设计',2,'','2017-04-01',0,0),(36,'机械设计',2,'','2017-04-01',0,0),(37,'建筑结构设计',2,'','2017-04-01',0,0),(38,'图书漂流',2,'','2017-04-01',0,0);
/*!40000 ALTER TABLE `t_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_pic_url`
--

DROP TABLE IF EXISTS `t_pic_url`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_pic_url` (
  `pic_id` bigint(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(1000) NOT NULL,
  PRIMARY KEY (`pic_id`),
  UNIQUE KEY `url` (`url`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_pic_url`
--

LOCK TABLES `t_pic_url` WRITE;
/*!40000 ALTER TABLE `t_pic_url` DISABLE KEYS */;
INSERT INTO `t_pic_url` VALUES (15,'D:\\yue_server\\path\\10.png'),(7,'D:\\yue_server\\path\\2.png'),(8,'D:\\yue_server\\path\\3.png'),(9,'D:\\yue_server\\path\\4.png'),(10,'D:\\yue_server\\path\\5.png'),(11,'D:\\yue_server\\path\\6.png'),(12,'D:\\yue_server\\path\\7.png'),(13,'D:\\yue_server\\path\\8.png'),(14,'D:\\yue_server\\path\\9.png'),(4,'D:\\yue_server\\path\\button8.png'),(6,'D:\\yue_server\\path\\button9.png');
/*!40000 ALTER TABLE `t_pic_url` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_user`
--

DROP TABLE IF EXISTS `t_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(12) NOT NULL,
  `password` varchar(16) NOT NULL,
  `mail` varchar(321) NOT NULL,
  `phone` varchar(12) NOT NULL,
  `stu_id` varchar(16) NOT NULL,
  `college` varchar(32) NOT NULL,
  `profession` varchar(16) NOT NULL,
  `sex` char(1) NOT NULL,
  `birthdate` date NOT NULL,
  `friends` varchar(1000) NOT NULL DEFAULT '',
  `credit` int(11) NOT NULL DEFAULT '10',
  `active_value` int(11) NOT NULL DEFAULT '0',
  `avatar` bigint(20) DEFAULT NULL,
  `is_activated` char(1) NOT NULL DEFAULT 'y' COMMENT '''y'' for yes and ''n'' for no',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `mail` (`mail`),
  KEY `name_2` (`name`),
  KEY `mail_2` (`mail`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_user`
--

LOCK TABLES `t_user` WRITE;
/*!40000 ALTER TABLE `t_user` DISABLE KEYS */;
INSERT INTO `t_user` VALUES (1,'fdsaf','123456','123@qq.com','123456','14301002','北交大','xx','m','1995-05-22','',10,0,NULL,'y'),(4,'fsx','123456','1234@qq.com','123456','14301002','北交大','xx','m','1995-05-22','',10,0,NULL,'y'),(8,'fsxx','123456','12345@qq.com','123456','14301002','北交大','xx','m','1995-05-22','',10,0,NULL,'y'),(13,'fad','123456','1253@qq.com','123456','123456','123456','xxx','m','1996-01-01','',10,0,NULL,'y'),(14,'fxad','123456','12753@qq.com','123456','123456','123456','xxx','m','1996-01-01','',10,0,NULL,'y'),(15,'f9ad','123456','127653@qq.com','123456','123456','123456','xxx','m','1996-01-01','',10,0,NULL,'y'),(16,'f9a6d','123456','1299653@qq.com','123456','123456','123456','xxx','m','1996-01-01','',10,0,NULL,'y'),(17,'f9x6d','123456','99653@qq.com','123456','123456','北交大','xxx','m','1996-01-01','',10,0,NULL,'y'),(18,'f9x5d','123456','9653@qq.com','123456','123456','北交大','xxx','m','1996-01-01','',10,0,NULL,'y'),(19,'f95d','123456','653@qq.com','123456','123456','北交大','xxx','m','1996-01-01','',10,0,NULL,'y'),(20,'f5d','123456','53@qq.com','123456','123456','北交大','xxx','m','1996-01-01','',10,0,NULL,'y'),(21,'f5d8','123456','153@qq.com','123456','123456','北交大','xxx','m','1996-01-01','',10,0,NULL,'n'),(22,'wangtianran','123456','1271369334@qq.com','1008600','14301020','北交大','xxx','m','1996-01-01','24,23,24,23',10,0,4,'n'),(23,'tianyang','123456','98745@qq.com','12345678911','564154','学生','学生','m','1995-01-01','22,22',25,0,-1,'n'),(24,'yuhang','123456','1619965461@qq.com','18522797953','454681','bjtu','学生','m','1995-01-01','22,22',10,0,-1,'n');
/*!40000 ALTER TABLE `t_user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-06-10 19:11:45
