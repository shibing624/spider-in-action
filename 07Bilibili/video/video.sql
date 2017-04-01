# mysql
use bilibili;
CREATE TABLE `video` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `av` int(11) DEFAULT NULL,
  `cid` int(11) DEFAULT NULL,
  `title` varchar(150) DEFAULT NULL,
  `tminfo` varchar(45) DEFAULT NULL,
  `time` varchar(45) DEFAULT NULL,
  `click` int(11) DEFAULT NULL,
  `danmu` int(11) DEFAULT NULL,
  `coins` int(11) DEFAULT NULL,
  `favourites` int(11) DEFAULT NULL,
  `duration` varchar(45) DEFAULT NULL,
  `mid` int(11) DEFAULT NULL,
  `name` varchar(45) DEFAULT NULL,
  `article` int(11) DEFAULT NULL,
  `fans` int(11) DEFAULT NULL,
  `tag1` varchar(45) DEFAULT NULL,
  `tag2` varchar(45) DEFAULT NULL,
  `tag3` varchar(45) DEFAULT NULL,
  `common` int(11) DEFAULT NULL,
  `honor_click` int(11) DEFAULT NULL,
  `honor_coins` int(11) DEFAULT NULL,
  `honor_favourites` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
