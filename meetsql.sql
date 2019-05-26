-- MySQL dump 10.13  Distrib 5.7.26, for Linux (x86_64)
--
-- Host: localhost    Database: MEET
-- ------------------------------------------------------
-- Server version	5.7.26-0ubuntu0.18.04.1

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
-- Table structure for table `Attendee`
--

DROP TABLE IF EXISTS `Attendee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Attendee` (
  `attendee_id` int(11) NOT NULL AUTO_INCREMENT,
  `event_id` int(11) DEFAULT NULL,
  `user_name` varchar(100) DEFAULT NULL,
  `attending` tinyint(1) DEFAULT NULL,
  `group_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`attendee_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Attendee`
--

LOCK TABLES `Attendee` WRITE;
/*!40000 ALTER TABLE `Attendee` DISABLE KEYS */;
INSERT INTO `Attendee` VALUES (2,NULL,'jason@email.com',1,11),(4,3,'jason@email.com',0,NULL),(7,NULL,'admin@email.com',1,2),(9,NULL,'jason@email.com',1,12),(10,1,'jason@email.com',0,NULL),(11,NULL,'jason@email.com',0,2),(15,11,'anricojason@gmail.com',1,NULL),(16,NULL,'anricojason@gmail.com',1,12);
/*!40000 ALTER TABLE `Attendee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Events`
--

DROP TABLE IF EXISTS `Events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Events` (
  `event_id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `description` varchar(100) DEFAULT NULL,
  `date_time` varchar(100) DEFAULT NULL,
  `starttime` time DEFAULT NULL,
  `endtime` time DEFAULT NULL,
  `attendees` int(11) DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  `creator` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`event_id`,`group_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Events`
--

LOCK TABLES `Events` WRITE;
/*!40000 ALTER TABLE `Events` DISABLE KEYS */;
INSERT INTO `Events` VALUES (1,12,'event','this is a new event to test if this is committed into the db','2019-04-28',NULL,NULL,NULL,NULL,NULL),(3,2,'DATA','hello this is a new event to see if joining events and attendees works in dash','2019-05-26','22:00:00','02:00:00',NULL,'Morill 221',NULL),(4,10,'TIME','description','2019-04-28','14:00:00','15:00:00',NULL,'Morill 221',NULL),(9,10,'EVENTP2','hello!','2019-05-31','13:00:00','17:00:00',NULL,'The Classroom',NULL),(11,33,'Event time','this is a description','2019-05-26','22:00:00','12:00:00',NULL,'LOCATION','jason@email.com');
/*!40000 ALTER TABLE `Events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Follower`
--

DROP TABLE IF EXISTS `Follower`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Follower` (
  `follower_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `user_name` varchar(100) DEFAULT NULL,
  `following` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`follower_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Follower`
--

LOCK TABLES `Follower` WRITE;
/*!40000 ALTER TABLE `Follower` DISABLE KEYS */;
INSERT INTO `Follower` VALUES (1,1,'jason@email.com',1),(3,1,'anricojason@gmail.com',1);
/*!40000 ALTER TABLE `Follower` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `GroupComments`
--

DROP TABLE IF EXISTS `GroupComments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `GroupComments` (
  `comment_id` int(11) NOT NULL AUTO_INCREMENT,
  `event_id` int(11) DEFAULT NULL,
  `group_id` int(11) DEFAULT NULL,
  `creator_id` int(11) DEFAULT NULL,
  `approp_flag` tinyint(1) DEFAULT NULL,
  `content` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`comment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `GroupComments`
--

LOCK TABLES `GroupComments` WRITE;
/*!40000 ALTER TABLE `GroupComments` DISABLE KEYS */;
/*!40000 ALTER TABLE `GroupComments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Groups_table`
--

DROP TABLE IF EXISTS `Groups_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Groups_table` (
  `group_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `tag` varchar(45) DEFAULT NULL,
  `num_members` int(11) DEFAULT NULL,
  `group_img_path` blob,
  `creator` varchar(100) DEFAULT NULL,
  `createdate` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `group_description` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`group_id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Groups_table`
--

LOCK TABLES `Groups_table` WRITE;
/*!40000 ALTER TABLE `Groups_table` DISABLE KEYS */;
INSERT INTO `Groups_table` VALUES (2,'Blog Test','group',NULL,'','jason@email.com','2019-05-01 02:35:58','edit group'),(11,'Group name ','tags',NULL,_binary 'test.png','jason@email.com','2019-04-04 20:23:41',NULL),(12,'Notification Test','groupmeet',NULL,'','jason@email.com','2019-05-15 14:47:46','Notifcation'),(32,'Hello','t',NULL,_binary 'test.png','jason@email.com','2019-05-15 00:32:42','vbcvbvbb');
/*!40000 ALTER TABLE `Groups_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Messages`
--

DROP TABLE IF EXISTS `Messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Messages` (
  `message_id` int(11) NOT NULL AUTO_INCREMENT,
  `body` varchar(400) DEFAULT NULL,
  `author` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`message_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Messages`
--

LOCK TABLES `Messages` WRITE;
/*!40000 ALTER TABLE `Messages` DISABLE KEYS */;
/*!40000 ALTER TABLE `Messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Notification`
--

DROP TABLE IF EXISTS `Notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Notification` (
  `notify_id` int(11) NOT NULL AUTO_INCREMENT,
  `event_id` int(11) DEFAULT NULL,
  `group_id` int(11) DEFAULT NULL,
  `change_summary` varchar(100) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`notify_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Notification`
--

LOCK TABLES `Notification` WRITE;
/*!40000 ALTER TABLE `Notification` DISABLE KEYS */;
/*!40000 ALTER TABLE `Notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Posts`
--

DROP TABLE IF EXISTS `Posts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Posts` (
  `post_id` int(11) NOT NULL AUTO_INCREMENT,
  `body` varchar(250) DEFAULT NULL,
  `author` varchar(100) DEFAULT NULL,
  `date_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`post_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Posts`
--

LOCK TABLES `Posts` WRITE;
/*!40000 ALTER TABLE `Posts` DISABLE KEYS */;
INSERT INTO `Posts` VALUES (1,'This is a blog post','jason@email.com','2019-05-13 04:09:44',NULL),(2,'This is another test','jason@email.com','2019-05-13 04:24:41',1),(3,'New Post','jason@email.com','2019-05-14 20:18:53',1);
/*!40000 ALTER TABLE `Posts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Security`
--

DROP TABLE IF EXISTS `Security`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Security` (
  `sec_event_id` int(11) NOT NULL AUTO_INCREMENT,
  `date_time` datetime DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `method_used` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`sec_event_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Security`
--

LOCK TABLES `Security` WRITE;
/*!40000 ALTER TABLE `Security` DISABLE KEYS */;
/*!40000 ALTER TABLE `Security` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `User`
--

DROP TABLE IF EXISTS `User`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `User` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `community_violations` smallint(6) DEFAULT NULL,
  `profile_pic_path` varchar(100) DEFAULT NULL,
  `followers` int(11) DEFAULT NULL,
  `role` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User`
--

LOCK TABLES `User` WRITE;
/*!40000 ALTER TABLE `User` DISABLE KEYS */;
INSERT INTO `User` VALUES (1,'Jason','Anrico','jason@email.com','$5$rounds=535000$h8GZA26eHpQfVjfp$BdceZCWsgkC7tMg0GSrjx8/Qg8Ts.cYxCGXBpiGcD9C',NULL,NULL,NULL,'user'),(2,'Jay','Hey','anricojason@gmail.com','$5$rounds=535000$1ZxG3fBKG9BAcppS$TAEHsFlsylF8Ul2jtWORVfv0UmFB6xdeJSpnSvKtfc0',NULL,NULL,NULL,'user'),(5,'Admin','Admin','admin@email.com','$5$rounds=535000$OKb8FePccqvmCqG8$G3puVg59AhdZDBly781oyqJktRvwg6I5q7ngurSAcW/',NULL,NULL,NULL,'admin'),(6,'New','Admin','admin2@email.com','$5$rounds=535000$PzL9FYMnaSMP8ZbT$evWlY4Zis6vMfYZqjVtzUj6BSUe5LXdl4WyE4xSSdW8',NULL,NULL,NULL,'admin');
/*!40000 ALTER TABLE `User` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-05-15 14:36:12
