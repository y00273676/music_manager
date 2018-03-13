--use mysql;
--drop database if exists karaok;
--create database karaok character set utf8;
use karaok;

set names utf8;
/*
SET character_set_client='utf8';  
SET character_set_connection='utf8';  
SET character_set_results='utf8'; 
set character_set_database='utf8';
set character_set_server='utf8';
show variables like "%char%";
*/

--服务器信息表
drop table if exists servers;
CREATE TABLE `servers` (
  `server_id` int primary key default 1 comment '服务器编号',
  `server_grpid` int not null default 1 comment '1，主组（常唱组）； 2,从组（非常唱组）',
  `server_name` varchar(64) NOT NULL comment '服务器名称',
  `server_ip` varchar(16) NOT NULL comment '服务器名称',
  `server_weight` tinyint NOT NULL default 9 comment '服务器权重',
  `server_addtime` datetime not null default CURRENT_TIMESTAMP comment '服务器添加时间',
  UNIQUE KEY `server_ip` (`server_ip`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
insert into `servers`(server_id, server_grpid, server_name, server_ip, server_weight) values(1, 1, '201', '192.168.1.201', 9);

drop table if exists carriers;
CREATE TABLE `carriers` (
      `carrier_id` int primary key AUTO_INCREMENT comment '媒体格式id',
      `carrier_name` varchar(64) DEFAULT NULL comment '媒体格式名称',
      `carrier_desc` varchar(256) DEFAULT NULL comment '媒体格式说明'
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

INSERT INTO `carriers` VALUES (2,'DVD','DVD'),(3,'MPEG1','MPEG1'),(4,'MPEG2','MPEG2'),(5,'SVCD','SVCD'),(6,'MP3','MP3'),(7,'WAV','WAV'),(8,'LS','LS'),(9,'LSS','LSS'),(10,'WAV','WAV');

--语言信息表
drop table if exists langs;
CREATE TABLE `langs` (
  `lang_id` int(11) primary key comment 'id',
  `lang_name` varchar(200) DEFAULT NULL comment '语言名称',
  `lang_des` varchar(255) DEFAULT NULL comment '语言说明',
  UNIQUE KEY `lang_name` (`lang_name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

INSERT INTO `langs` VALUES (2,'国语','国语'),(3,'粤语','粤语'),(4,'闽南语','闽南语'),(5,'英语','英语'),(6,'日语','日语'),(7,'韩语','韩语'),(8,'其它','其它');

--歌曲文件信息表--
/*用于更新文件路径使用，查询的时候不参与联表查询。*/
drop table if exists mediafiles;
CREATE TABLE `mediafiles` (
  `media_no` int primary key comment '歌曲编号',
  `media_svrgroup` tinyint not null DEFAULT 1 comment '文件所在服务器组：1-主组，2-从组',
  `media_file` varchar(256) DEFAULT NULL comment '文件路径（文件名）'
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

/*用于更新歌曲高潮信息，加歌时用，查询的时候不参与联表查询。*/
drop table if exists mediaclimax;
CREATE TABLE `mediaclimax` (
  `media_no` int primary key comment '歌曲编号',
  `media_climaxinfo` varchar(256) DEFAULT NULL comment '歌曲高潮信息'
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--歌曲信息表
drop table if exists medias;
CREATE TABLE `medias` (
  `media_no` int primary key comment '歌曲编号',
  `media_name` varchar(256) NOT NULL comment '歌曲名称',
  `media_namelen` tinyint NOT NULL comment '歌曲名称长度',
  `media_langtype` tinyint DEFAULT NULL comment '(歌曲语言类型) 用于显示歌曲信息,字幕时选择字库文件.0: 中文,1韩文,2日文',
  `media_langid` int DEFAULT NULL comment '歌曲语言ID',
  `media_lang` varchar(64) DEFAULT NULL comment '歌曲语言',
  `media_tag1` varchar(128) DEFAULT NULL comment '歌曲3D分类',
  `media_tag2` varchar(128) DEFAULT NULL comment '歌曲3D分类',
  `media_actname1` varchar(128) DEFAULT NULL comment '歌星名字1',
  `media_actname2` varchar(128) DEFAULT NULL comment '歌星名字2',
  `media_actname3` varchar(128) DEFAULT NULL comment '歌星名字3',
  `media_actname4` varchar(128) DEFAULT NULL comment '歌星名字4',
  `media_carria` varchar(32) DEFAULT NULL comment '歌曲载体类型（DVD，MP3等）',
  `media_yuan` tinyint DEFAULT NULL comment '原唱',
  `media_ban` tinyint DEFAULT NULL comment '伴唱',
  `media_svrgroup` tinyint not null DEFAULT 1 comment '文件所在服务器组：1-主组，2-从组',
  `media_file` varchar(256) DEFAULT NULL comment '文件路径（文件名）',
  `media_style` tinyint DEFAULT NULL comment '视频风格类型: 0-MV 1-现场版 2-流水影',
  `media_audio` varchar(32) DEFAULT NULL comment '音频类型（mpeg）',
  `media_volume` tinyint(4) DEFAULT NULL comment '音量',
  `media_jp` varchar(128) DEFAULT NULL comment '简拼',
  `media_py` varchar(256) DEFAULT NULL comment '拼音',
  `media_strok` tinyint DEFAULT NULL comment '笔画数',
  `media_stroks` varchar(128) DEFAULT NULL comment '笔划序列',
  `media_lyric` varchar(512) DEFAULT NULL comment '歌词,用于搜吧搜索',
  `media_isnew` tinyint DEFAULT NULL comment '是否新歌',
  `media_clickm` int DEFAULT 0 comment '月点击量',
  `media_clickw` int DEFAULT 0 comment '周点击量',
  `media_click` int DEFAULT 0 comment '总点击量',
  `media_type` tinyint NOT NULL default 1 comment '类型，1: 歌曲|2: 广告|3: 电影',
  `media_stars` tinyint not null DEFAULT 0 comment 'star_level, 歌曲热度设定',
  `media_actno1` int DEFAULT NULL comment '歌星1 编号',
  `media_actno2` int DEFAULT NULL comment '歌星2 编号',
  `media_actno3` int DEFAULT NULL comment '歌星3 编号',
  `media_actno4` int DEFAULT NULL comment '歌星4 编号',
  `media_dafen` tinyint not null DEFAULT 0 comment '该歌曲是否支持打分',
  `media_climax` tinyint not null DEFAULT 0 comment '该歌曲是否有高潮信息',
  `media_climaxinfo` varchar(256) comment '该歌曲高潮信息',
  `media_yinyi` tinyint not null DEFAULT 0 comment '该歌曲是否有音译信息',
  `media_light` int not null DEFAULT 0 comment '灯光设置',
  `media_newadd` tinyint not null DEFAULT 0 comment '用于清除空纪录',
  index `medias_media_name`(media_name),
  index `medias_media_namelen`(media_namelen),
  index `medias_media_langid`(media_langid),
  index `medias_media_tag1`(media_tag1),
  index `medias_media_tag2`(media_tag2),
  index `medias_media_strok`(media_strok),
  index `medias_media_actorno1`(media_actno1),
  index `medias_media_actorno2`(media_actno2),
  index `medias_media_actorno3`(media_actno3),
  index `medias_media_actorno4`(media_actno4),
  FULLTEXT `FK_media_name`(`media_name`),
  FULLTEXT `FK_media_jp`(`media_jp`),
  FULLTEXT `FK_media_stroks`(`media_stroks`),
  FULLTEXT `FK_media_all`(`media_name`,`media_actname1`,`media_actname2`,`media_actname3`,`media_actname4`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*
  FULLTEXT (`media_name`) WITH PARSER ngram,
  FULLTEXT (`media_jp`) WITH PARSER ngram,
  FULLTEXT (`media_name`,`media_jp`,`media_actname1`,`media_actname2`,`media_actname3`,`media_actname4`) WITH PARSER ngram
  */

--歌星信息表
drop table if exists actors;
CREATE TABLE `actors` (
  `actor_no` int not null primary key comment '歌星编号',
  `actor_name` varchar(128) NOT NULL comment '歌星名称',
  `actor_des` varchar(256) NOT NULL comment '歌星名称',
  `actor_typeid` int NOT NULL comment '歌星类别id',
  `actor_type` varchar(64) NOT NULL comment '歌星类别',
  `actor_py` varchar(128) NOT NULL comment '歌星全拼',
  `actor_jp` varchar(64) NOT NULL comment '歌星简拼',
  `actor_click` int DEFAULT 0 comment '点击量',
  `actor_clickw` int DEFAULT 0 comment '周点击量',
  `actor_clickm` int DEFAULT 0 comment '月点击量',
  `actor_newadd` tinyint DEFAULT 0 comment '批处理时的标记',
  FULLTEXT `actor_name`(`actor_name`),
  FULLTEXT `actor_jp`(`actor_jp`),
  FULLTEXT `actor_name_jp`(`actor_name`,`actor_jp`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `mediatypes`;
CREATE TABLE `mediatypes` (
  `MediaType_ID` int(11) NOT NULL,
  `MediaType_Name` varchar(128) DEFAULT NULL,
  `MediaType_Description` varchar(255) DEFAULT NULL,
  `MediaType_IsMovie` int(11) DEFAULT NULL,
  `MediaType_IsKaraok` int(11) DEFAULT NULL,
  `MediaType_IsAds` int(11) DEFAULT NULL,
  `MediaType_NewTypeID` int(11) DEFAULT NULL,
  PRIMARY KEY (`MediaType_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

INSERT INTO `mediatypes` VALUES (1,'男女对唱','男女对唱',1,1,0,500007),(2,'校园民谣','校园民谣',0,1,0,500003),
(3,'欢乐庆典','欢乐庆典',0,1,0,500013),(4,'歌颂祖国','歌颂祖国',0,1,0,500014),(5,'戏曲片段','戏曲片段',0,1,0,500004),
(6,'民歌传唱','民歌传唱',0,1,0,500008),(7,'草原歌曲','草原歌曲',0,1,0,500017),(8,'经典老歌','经典老歌',0,1,0,500011),
(9,'影视金曲','影视金曲',0,1,0,500002),(10,'disco','disco',0,1,0,500018),(11,'友谊万岁','友谊万岁',0,1,0,500001),
(12,'军旅歌曲','军旅歌曲',0,1,0,500010),(13,'网络歌曲','网络歌曲',0,1,0,500005),(14,'儿童歌曲','儿童歌曲',0,1,0,500015),
(15,'纯音乐','纯音乐',0,1,0,500016),(101,'心碎伤感','心碎伤感',0,1,0,500006),(102,'经典翻唱','经典翻唱',0,1,0,500012),
(103,'甜蜜幸福','甜蜜幸福',0,1,0,500019),(104,'寂寞空灵','寂寞空灵',0,1,0,500021),(105,'异国风情','异国风情',0,1,0,500020),
(106,'高清歌曲','高清歌曲',0,1,0,500009),(241,'民歌悠扬','民歌悠扬',0,1,0,500048),(240,'雷石专属','雷石专属',0,1,0,500024),
(239,'我是歌手','我是歌手',0,1,0,500027),(238,'中国新声代','中国新声代',0,1,0,500065),(237,'蒙面歌王','蒙面歌王',0,1,0,500064),
(236,'最美和声','最美和声',0,1,0,500032),(235,'神了歌曲','神了歌曲',0,1,0,500052),(234,'雷客专属','雷客专属',0,1,0,500024),
(233,'中国好声音','中国好声音',0,1,0,500029),(232,'中国好歌曲','中国好歌曲',0,1,0,500035),(231,'视听盛宴','视听盛宴',0,1,0,500053),
(230,'一曲成名','一曲成名',0,1,0,500057),(229,'音译','音译',0,1,0,500061),(228,'男高音','男高音',0,1,0,500062),
(227,'卫视歌曲','卫视歌曲',0,1,0,500067),(226,'跨界歌王','跨界歌王',0,1,0,500073),(225,'蒙面唱将猜猜猜','蒙面唱将猜猜猜',0,1,0,500086),
(224,'王者归来','王者归来',0,1,0,500087),(223,'歌手','歌手',0,1,0,500088),(222,'安静','安静',0,1,0,500038),
(221,'萌动童声','萌动童声',0,1,0,500047),(156,'谁是大擂主','谁是大擂主',0,1,0,500026),(157,'全能星战','全能星战',0,1,0,500025),
(158,'中国梦之声','中国梦之声',0,1,0,500030),(159,'我为歌狂','我为歌狂',0,1,0,500028),(219,'民族歌曲','民族歌曲',0,1,0,500085),
(220,'水墨丹青','水墨丹青',0,1,0,500054),(214,'民乐悠扬','民乐悠扬',0,1,0,500048),(215,'梨园国粹','梨园国粹',0,1,0,500045),
(216,'恋爱','恋爱',0,1,0,500040),(217,'囧味青春','囧味青春',0,1,0,500046),(218,'伤感','伤感',0,1,0,500041),
(213,'纯粹音乐','纯粹音乐',0,1,0,500050),(200,'最美夕阳红','最美夕阳红',0,1,0,500089),(212,'影音动漫','影音动漫',0,1,0,500058),
(201,'劲嗨','劲嗨',0,1,0,500066),(202,'红歌嘹亮','红歌嘹亮',0,1,0,500059),(203,'天籁和鸣','天籁和鸣',0,1,0,500055),
(204,'神了个曲','神了个曲',0,1,0,500052),(205,'雕刻时光','雕刻时光',1,1,0,500044),(206,'宣泄','宣泄',0,1,0,500043),
(207,'快乐','快乐',0,1,0,500039),(208,'南亚情怀','南亚情怀',0,1,0,500070),(209,'日韩风尚','日韩风尚',0,1,0,500051),
(210,'欧美风情','欧美风情',0,1,0,500049),(211,'思念','思念',0,1,0,500042),(196,'空耳','空耳',0,1,0,500084),
(197,'交谊舞曲','交谊舞曲',0,1,0,500072),(198,'盖世英雄','盖世英雄',0,1,0,500083),(199,'中国新歌声','中国新歌声',0,1,0,500082);

---Cloud Music------
drop table if exists cloud_musicinfo;
CREATE TABLE if not exists cloud_musicinfo (
   music_no int not null primary key COMMENT '歌曲编号唯一',
   music_name varchar(128) COMMENT '歌曲名称',
   music_singer varchar(256) COMMENT '歌星',
   music_3d1 varchar(20) COMMENT '3d分类',
   music_3d2 varchar(20) COMMENT '3d分类2',
   music_downloadcount int COMMENT '歌曲线上下载次数',
   music_ishd tinyint COMMENT '是否高清',
   music_isnew tinyint COMMENT '是否新歌',
   music_isoften tinyint COMMENT '是否常唱',
   music_isreplace tinyint COMMENT '是否替换',
   music_state tinyint COMMENT '是否使用',
   music_lastver varchar(20) COMMENT '版本号',
   music_lang varchar(20) COMMENT '语言',
   music_type1 varchar(20) COMMENT '普通分类',
   music_type2 varchar(20) COMMENT '普通分类2',
   music_status int COMMENT '歌曲状态 0：未下载 1：替换 2：已下载 3：待添加', 
   music_lastverdate datetime COMMENT '更新时间',
   music_unixtime bigint COMMENT '更新时间戳',
   index cloud_musicinfo_music_no (music_no)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

drop table if exists cloud_downlog;
CREATE TABLE if not exists cloud_downlog(
    down_id integer primary key not null auto_increment COMMENT 'id',   
    down_gid varchar(32) comment '下载任务gid',
    music_no varchar(20) COMMENT '歌曲编号', 
    music_caption varchar(256) COMMENT '歌曲名称', 
    music_singer varchar(256) COMMENT '歌星',  
    music_lang varchar(16) COMMENT '语言',  
    music_theme varchar(16) COMMENT '分类',       
    music_ver float COMMENT '版本',         
    music_verdate datetime COMMENT '版本最后更新时间',     
    down_path varchar(256) COMMENT '下载路径',  
    down_url varchar(256) COMMENT '下载url',       
    file_size bigint COMMENT '文件大小',   
    down_stime datetime COMMENT '添加下载列表时间',        
    down_etime datetime COMMENT '下载完成时间',       
    down_status tinyint comment '下载状态, 下载完成状态:0-正在下载，1-下载完成，2-已暂停，3-下载失败',
    music_addtime datetime COMMENT '成功加歌时间',        
    music_hot varchar(50) COMMENT '热度',       
    music_replace tinyint COMMENT '是否替换',           
    music_type varchar(32) COMMENT '歌曲类型',           
    down_type tinyint COMMENT '歌曲下载触发类型, 0:实时下载,1:云端强推,2:手动下载,',           
    file_md5 varchar(50) COMMENT '',
    file_type varchar(10) COMMENT '文件类型',
    movie_type tinyint COMMENT '电影类型 0 片花 1 正片'
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


/*
DROP TABLE IF EXISTS `mediatags`;
CREATE TABLE `mediatags` (
  `tag_id` int(11) primary key auto_increment comment 'id',
  `tag_name` varchar(20) DEFAULT NULL comment '3D分类名称',
  `tag_desc` varchar(255) DEFAULT NULL comment '3D分类描述',
  `tag_x` int(11) DEFAULT NULL comment '横版X位置',
  `tag_y` int(11) DEFAULT NULL comment '横版Y位置',
  `tag_width` int(11) DEFAULT NULL comment '横版宽度',
  `tag_height` int(11) DEFAULT NULL comment '横版高度',
  `tag_pic` varchar(255) DEFAULT NULL comment '横版图片',
  `tag_verx` int(11) DEFAULT NULL comment '竖版X位置',
  `tag_very` int(11) DEFAULT NULL comment '竖版Y位置',
  `tag_verwidth` int(11) DEFAULT NULL comment '竖版宽',
  `tag_verheight` int(11) DEFAULT NULL comment '竖版高度',
  `tag_verpic` varchar(255) DEFAULT NULL comment '竖版图片',
  `tag_datatype` int(11) DEFAULT NULL comment '分类编号',
  `tag_datatime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `tag_light` int(11) DEFAULT NULL comment '分类使用的灯光类型',
  PRIMARY KEY (`MediaType_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `medianewtypes`;
CREATE TABLE `medianewtypes` (
  `MediaType_ID` int(11) NOT NULL,
  `MediaType_Name` varchar(20) DEFAULT NULL,
  `MediaType_Desc` varchar(255) DEFAULT NULL,
  `MediaType_X` int(11) DEFAULT NULL,
  `MediaType_Y` int(11) DEFAULT NULL,
  `MediaType_Width` int(11) DEFAULT NULL,
  `MediaType_Height` int(11) DEFAULT NULL,
  `MediaType_Pic` varchar(255) DEFAULT NULL,
  `MediaType_VerX` int(11) DEFAULT NULL,
  `MediaType_VerY` int(11) DEFAULT NULL,
  `MediaType_VerWidth` int(11) DEFAULT NULL,
  `MediaType_VerHeight` int(11) DEFAULT NULL,
  `MediaType_VerPic` varchar(255) DEFAULT NULL,
  `MediaType_DataType` int(11) DEFAULT NULL,
  `MediaType_DataTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `MediaType_Light` int(11) DEFAULT NULL,
  PRIMARY KEY (`MediaType_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `medianewtypes` VALUES (1,'男女对唱','男女对唱',60,107,284,144,'男女对唱20131122103904.png',0,0,0,0,'',500007,'2015-07-01 17:00:09',8),(2,'校园民谣','校园民谣',644,128,138,252,'校园民谣20131122103904.png',0,0,0,0,'',500003,'2015-07-01 17:00:04',2),(3,'经典翻唱','经典翻唱',790,128,138,122,'经典翻唱20131122103904.png',0,0,0,0,'',500012,'1989-12-31 16:00:00',1),(4,'欢乐庆典','欢乐庆典',936,128,138,122,'欢乐庆典20131122103904.png',0,0,0,0,'',500013,'2015-07-01 17:00:25',1),(5,'歌颂祖国','歌颂祖国',60,258,138,122,'歌颂祖国20131122103905.png',0,0,0,0,'',500014,'2015-07-01 17:00:26',4),(6,'戏曲片段','戏曲片段',206,258,138,122,'戏曲片段20131122103905.png',0,0,0,0,'',500004,'2015-09-12 19:05:26',4),(7,'经典老歌','经典老歌',936,258,138,122,'经典老歌20131122103905.png',44,129,246,160,'sbfl_经典老歌.png',500011,'2015-07-01 17:00:22',8),(8,'纯音乐','纯音乐',1082,388,138,122,'纯音乐20131122103907.png',0,0,0,0,'',500016,'2015-09-12 19:04:01',6),(9,'儿童歌曲','儿童歌曲',790,388,284,122,'儿童歌曲20131122103907.png',0,0,0,0,'',500015,'2015-07-01 17:00:27',4),(10,'军旅歌曲','军旅歌曲',498,388,138,122,'军旅歌曲20131122103908.png',0,0,0,0,'',500010,'2015-07-01 17:00:14',4),(11,'友谊万岁','友谊万岁',352,388,138,122,'友谊万岁20131122103908.png',0,0,0,0,'',500001,'1989-12-31 16:00:00',6),(12,'影视金曲','影视金曲',60,388,138,122,'影视金曲20131122103908.png',0,0,0,0,'',500002,'2015-11-29 17:25:39',2),(13,'心碎伤感','心碎伤感',1082,128,138,122,'心碎伤感20131122103909.png',0,0,0,0,'',500006,'2015-07-01 17:00:07',5),(14,'民歌传唱','民歌传唱',498,258,138,122,'民歌传唱20131122103909.png',0,0,0,0,'',500008,'2015-07-01 17:00:11',4),(15,'高清歌曲','高清歌曲',352,258,138,122,'高清歌曲20131122103910.png',0,0,0,0,'',500009,'2015-07-01 17:00:13',1),(16,'网络歌曲','网络歌曲',644,388,138,122,'网络歌曲20131122103910.png',0,0,0,0,'',500005,'2015-10-15 23:58:49',8),(17,'草原歌曲','草原歌曲',790,258,138,122,'草原歌曲20131122103911.png',0,0,0,0,'',500017,'2015-07-01 17:00:30',1),(18,'disco','disco',206,388,138,122,'DISCO20131122103911.png',965,415,122,122,'sbfl_disco.png',500018,'2016-03-06 17:57:37',3),(19,'甜蜜幸福','甜蜜幸福',352,128,138,122,'甜蜜幸福20131122103911.png',0,0,0,0,'',500019,'2015-07-01 17:00:33',6),(20,'异国风情','异国风情',498,128,138,122,'异国风情20131122103913.png',0,0,0,0,'',500020,'2015-12-27 23:41:05',7),(21,'寂寞空灵','寂寞空灵',1082,258,138,122,'寂寞空灵20131122103913.png',0,0,0,0,'',500021,'2015-07-01 17:00:43',5),(22,'我是歌手','我是歌手',NULL,NULL,NULL,NULL,NULL,567,415,122,122,'sbfl_我是歌手.png',500027,'2016-03-06 17:42:22',1),(23,'谁是大擂主','谁是大擂主',NULL,NULL,NULL,NULL,NULL,0,0,0,0,'',500026,'2015-03-05 17:33:34',0),(24,'全能星战','全能星战',NULL,NULL,NULL,NULL,NULL,0,0,0,0,'',500025,'2015-03-05 17:33:34',0),(25,'中国梦之声','中国梦之声',NULL,NULL,NULL,NULL,NULL,0,0,0,0,'',500030,'2015-07-01 17:00:48',0),(26,'中国最强音','中国最强音',NULL,NULL,NULL,NULL,NULL,0,0,0,0,'',500031,'2015-07-01 17:00:49',1),(27,'我为歌狂','我为歌狂',NULL,NULL,NULL,NULL,NULL,0,0,0,0,'',500028,'2015-07-01 17:00:45',0),(28,'最美和声','最美和声',NULL,NULL,NULL,NULL,NULL,319,167,122,122,'sbfl_最美和声.png',500032,'2015-08-02 17:40:38',1),(29,'雷石专属','雷石专属',NULL,NULL,NULL,NULL,NULL,168,415,122,122,'sbfl_雷石专属.png',500024,'1989-12-31 16:00:00',1),(30,'中国好声音','中国好声音',NULL,NULL,NULL,NULL,NULL,319,291,370,122,'sbfl_中国好声音.png',500029,'2015-11-08 21:22:08',1),(31,'快乐男声','快乐男声',NULL,NULL,NULL,NULL,NULL,0,0,0,0,'',500033,'2015-03-05 19:46:21',1),(32,'伤感','伤感',NULL,NULL,NULL,NULL,NULL,44,814,122,122,'sbfl_伤感.png',500041,'2016-03-06 18:06:37',5),(33,'安静','安静',NULL,NULL,NULL,NULL,NULL,44,690,122,122,'sbfl_安静.png',500038,'2016-03-06 18:07:25',2),(34,'神了歌曲','神了歌曲',NULL,NULL,NULL,NULL,NULL,841,415,122,122,'sbfl_神了歌曲.png',500052,'1989-12-31 16:00:00',8),(35,'欧美风情','欧美风情',NULL,NULL,NULL,NULL,NULL,717,415,122,122,'sbfl_欧美风情.png',500049,'1989-12-31 16:00:00',7),(36,'日韩风尚','日韩风尚',NULL,NULL,NULL,NULL,NULL,717,291,122,122,'sbfl_日韩风尚.png',500051,'1989-12-31 16:00:00',1),(37,'南亚情怀','南亚情怀',NULL,NULL,NULL,NULL,NULL,841,167,122,122,'sbfl_南亚情怀.png',500070,'1989-12-31 16:00:00',7),(38,'影音动漫','影音动漫',NULL,NULL,NULL,NULL,NULL,717,167,122,122,'sbfl_影音动漫.png',500058,'1989-12-31 16:00:00',1),(39,'萌动童声','萌动童声',NULL,NULL,NULL,NULL,NULL,965,167,122,122,'sbfl_萌动童声.png',500047,'1989-12-31 16:00:00',2),(40,'囧味青春','囧味青春',NULL,NULL,NULL,NULL,NULL,841,291,246,122,'sbfl_囧味青春.png',500046,'1989-12-31 16:00:00',8),(41,'中国好歌曲','中国好歌曲',NULL,NULL,NULL,NULL,NULL,443,167,122,122,'sbfl_中国好歌曲.png',500035,'1989-12-31 16:00:00',1),(42,'蒙面歌王','蒙面歌王',NULL,NULL,NULL,NULL,NULL,567,167,122,122,'sbfl_蒙面歌王.png',500064,'1989-12-31 16:00:00',1),(43,'卫视歌曲','卫视歌曲',NULL,NULL,NULL,NULL,NULL,319,415,122,122,'sbfl_卫视歌曲.png',500067,'2015-12-10 21:58:23',1),(44,'音译','音译',NULL,NULL,NULL,NULL,NULL,168,291,122,122,'sbfl_音译.png',500061,'1989-12-31 16:00:00',8),(45,'男高音','男高音',NULL,NULL,NULL,NULL,NULL,44,415,122,122,'sbfl_男高音.png',500062,'1989-12-31 16:00:00',6),(46,'劲嗨','劲嗨',NULL,NULL,NULL,NULL,NULL,44,291,122,122,'sbfl_劲嗨.png',500066,'2016-03-06 17:54:05',3),(47,'思念','思念',NULL,NULL,NULL,NULL,NULL,44,566,122,122,'sbfl_思念.png',500042,'1989-12-31 16:00:00',7),(48,'宣泄','宣泄',NULL,NULL,NULL,NULL,NULL,168,566,122,122,'sbfl_宣泄.png',500043,'1989-12-31 16:00:00',4),(49,'水墨丹青','水墨丹青',NULL,NULL,NULL,NULL,NULL,567,814,122,122,'sbfl_水墨丹青.png',500054,'1989-12-31 16:00:00',2),(50,'视听盛宴','视听盛宴',NULL,NULL,NULL,NULL,NULL,567,566,122,122,'sbfl_视听盛宴.png',500053,'2016-03-06 18:00:56',1),(51,'一曲成名','一曲成名',NULL,NULL,NULL,NULL,NULL,319,690,122,122,'sbfl_一曲成名.png',500057,'1989-12-31 16:00:00',1),(52,'恋爱','恋爱',NULL,NULL,NULL,NULL,NULL,168,814,122,122,'sbfl_恋爱.png',500040,'1989-12-31 16:00:00',6),(53,'快乐','快乐',NULL,NULL,NULL,NULL,NULL,168,690,122,122,'sbfl_快乐.png',500039,'1989-12-31 16:00:00',8),(54,'天籁和鸣','天籁和鸣',NULL,NULL,NULL,NULL,NULL,443,566,122,122,'sbfl_天籁和鸣.png',500055,'1989-12-31 16:00:00',8),(55,'红歌嘹亮','红歌嘹亮',NULL,NULL,NULL,NULL,NULL,443,690,122,122,'sbfl_红歌嘹亮.png',500059,'1989-12-31 16:00:00',4),(56,'雕刻时光','雕刻时光',NULL,NULL,NULL,NULL,NULL,443,814,122,122,'sbfl_雕刻时光.png',500044,'1989-12-31 16:00:00',8),(57,'梨园国粹','梨园国粹',NULL,NULL,NULL,NULL,NULL,319,566,122,122,'sbfl_梨园国粹.png',500045,'1989-12-31 16:00:00',6),(58,'民歌悠扬','民歌悠扬',NULL,NULL,NULL,NULL,NULL,319,814,122,122,'sbfl_民歌悠扬.png',500048,'2016-03-06 18:04:53',4),(59,'纯粹音乐','纯粹音乐',NULL,NULL,NULL,NULL,NULL,567,690,122,122,'sbfl_纯粹音乐.png',500050,'1989-12-31 16:00:00',6),(60,'中国之星','中国之星',NULL,NULL,NULL,NULL,NULL,443,415,122,122,'sbfl_中国之星.png',500069,'1989-12-31 16:00:00',1);
*/


--房台信息表
drop table if exists rooms;
CREATE TABLE `rooms` (
  `room_mac` varchar(32) primary key comment '房台MAC',
  `room_no` varchar(32) not null comment '房台编号',
  `room_name` varchar(256) not null comment '房台名称',
  `room_type` tinyint not null default 3 comment '房台类型, 小包，中包，大包',
  `room_ip` varchar(16) not null default '' comment '房台IP',
  `room_mask` varchar(16) default null comment '房台IP Netmask',
  `room_gw` varchar(16) default null comment '房台IP 网关',
  `room_dns` varchar(32) default null comment '房台IP DNS',
  `room_stbtype` tinyint not null default 1 comment '机顶盒类型，主机顶盒，从机顶盒，门牌机等等',
  `room_svr` varchar(20) not null comment '服务器IP',
  `room_recordsvr` varchar(20) comment '录音服务器IP',
  `room_skin` int default null comment '默认皮肤ID',
  `room_theme` int default null comment '默认模板ID',
  `room_profile` text default null comment 'DHCP ini文件中其他设置项',
  `room_state` tinyint default 0 comment '房间状态：0:关台（空闲）， 1：开台（使用中）',
  UNIQUE index `room_rip` (`room_ip`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--insert into rooms(room_mac, room_no, room_name, room_type, room_ip, room_mask, room_gw, room_dns, room_stbtype, room_svr, room_recordsvr, room_theme, room_profile) values('5254006aefd6', '101', '北海厅', 3, '192.168.1.101', '255.255.255.0', '192.168.1.1', '192.168.1.1', 1, '192.168.1.201', '192.168.1.201', 1, '');

--点歌曲表
drop table if exists playlist;
CREATE TABLE `playlist` (
  `room_ip` varchar(32) not null comment '房台IP',
  `media_no` int not null comment '歌曲编号',
  `addtime` datetime not null default CURRENT_TIMESTAMP comment '添加时间',
  `status` tinyint not null comment '点唱状态， 0：未唱， 1,正唱，2，已唱'
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


--收藏
drop table if exists favorites;
CREATE TABLE `favorites` (
  `phone_num` varchar(18) not null comment '用户手机号',
  `media_no` int not null comment '歌曲编号',
  primary key (`phone_num`, `media_no`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--轮播歌曲表
/*无论设置哪种轮播类型，只需要把相应的歌曲信息导入到此表就行*/
drop table if exists autoplay;
CREATE TABLE `autoplay` (
  `media_no` int primary key comment '歌曲编号',
  `media_svrgrp` int comment '服务器组ID',
  `media_file` varchar(256)  comment '文件路径'
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--配置信息表:systemsettinginfo
drop table if exists config;
CREATE TABLE `config` (
  `config_id` int primary key auto_increment comment '配置项ID',
  `config_name` varchar(64) not null comment '配置项名称',
  `config_value` varchar(128) not null default '' comment '配置项的值',
  `config_desc` varchar(512) not null default '' comment '配置项说明, 初始添加时设定，用于页面回显说明，不允许修改',
  UNIQUE KEY `config_config_name` (`config_name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

insert into config(config_name, config_value, config_desc) values 
('ktv_name', '您的公司名称', '公司名称'),
('ktv_salutatoty', '北京雷客天地科技有限公司欢迎您！电话：010-64424996', '开台滚动字幕'),
('ktv_statime', '60', '字幕停留时间'),
('karaok_ver', '5.0.0.76', '系统版本'),
('transfer_ip', '192.168.1.201', '中转服务器IP'),
('transfer_ip_ex', '127.0.0.1', '中转服务器外网IP'),
('erpsvr_ip', '192.168.1.201', 'ERP服务器IP'),
('erpsvr_name', 'erpserver', 'ERP服务器名称'),
('erpdb_name', '', 'ERP数据库用户名'),
('erpdb_passwd', '', 'ERP数据库密码'),
('SSID','', 'WIFI名称'), ('SSID_Pwd','', 'WIFI密码'),
('CloudMusic_uname','', '云端帐号用户名'),
('CloudMusic_passwd','', '云端帐号密码'),
('CloudMusic_realdown','1', '是否启用实时下载'),
('90横版-2.0','modules/90plus_56AF41C9BC66B78ED11A5FA6B84FF84C', '默认90后V2横版模板'),
('90竖版-2.0','modules/90plus_F3DD3F4EBBAA12163830AD79CA728297', '默认90后V2竖版模板'),
('CanSing_ayways','1', '不开台就能点歌'),
('Loop_play','2', '轮播类型'),
('control_disco','0', '是否启用迪曲控制'),
('passwd_disco','', '迪曲控制密码'),
('control_orderdrink','0', '是否启用酒水控制'),
('passwd_orderdrink','', '酒水控制密码'),
('default_netmask','', '子网掩码'),
('default_skin','', '默认皮肤'),
('theme_update','0', '模板强制更新'),
('climax_update','0', '歌曲高潮信息更新时间'),
('CloudMusic_Update','0', '歌曲更新时间'),
('CloudMusic_type','2', '云端歌曲库类型'),
('NewSong_Update','0', '歌曲空记录更新时间'),
('clouddownsvr_ip','192.168.1.201', '实时下载服务器IP')
;

drop table if exists actortypes;
CREATE TABLE `actortypes` (
  `actortype_id` int primary key NOT NULL,
  `actortype_name` varchar(128) not NULL,
  `actortype_des` varchar(256) DEFAULT NULL,
  `actortype_ismovie` int DEFAULT 0,
  `actortype_iskaraok` int DEFAULT 1
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

INSERT INTO `actortypes` VALUES (1,'大陆男歌星','大陆男歌星',0,1),(2,'大陆女歌星','大陆女歌星',0,1),(3,'港台男歌星','港台男歌星',0,1),(4,'港台女歌星','港台女歌星',0,1),(5,'外国歌星','外国歌星',0,1),(6,'中国组合','中国组合',0,1),(7,'外国组合','外国组合',0,1),(8,'影星','影星',1,0);

--消息、提示消息、日志信息表
drop table if exists mesgs;
CREATE TABLE `mesgs` (
  `mesg_id` int primary key AUTO_INCREMENT,
  `mesg_ip` varchar(20) DEFAULT NULL comment '消息来源IP',
  `mesg_app` varchar(80) DEFAULT NULL comment '消息来源应用',
  `mesg_title` varchar(80) DEFAULT NULL comment '消息标题',
  `mesg_content` varchar(500) DEFAULT NULL comment '消息内容',
  `mesg_time` datetime DEFAULT NULL comment '消息时间',
  `mesg_level` tinyint not null DEFAULT 7 comment '消息级别（参考Linux Kernel Log Level)：0:emergency(系统已经不可用）, 1:alert（必须马上处理的问题）, 2:critical（很严重的错误情况）, 3:error（错误）, 4:warnning（警告，系统可能存在问题）, 5: notice（提请注意）, 6:info（信息）, 7:debug（调试信息）',
  `mesg_flag` tinyint DEFAULT 1 comment '消息状态 0:新消息  1:已经读'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--皮肤信息表
drop table if exists skins;
CREATE TABLE `skins` (
  `skin_id` int primary key AUTO_INCREMENT comment '皮肤编号',
  `skin_name` varchar(64) not null comment '皮肤名称',
  `skin_desc` varchar(256) comment '说明文字',
  `skin_file` varchar(256) comment '皮肤包路径',
  `skin_unpath` varchar(256) comment '解压路径',
  `skin_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP comment '添加时间',
  index `skins_skin_name` (`skin_name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
insert into skins ( skin_name, skin_desc) values( '90后V2', '90后V2');

--模板信息
DROP TABLE IF EXISTS `ktvmodule_ver`;
CREATE TABLE `ktvmodule_ver` (
      `id` int(11) NOT NULL,
      `name` varchar(256) DEFAULT NULL COMMENT '名称',
      `addtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      `fileurl` varchar(256) DEFAULT NULL COMMENT '文件路径',
      `unpath` varchar(256) DEFAULT NULL COMMENT '解压路径 ',
      `version` varchar(32) DEFAULT NULL COMMENT '版本',
      `isuse` int(11) DEFAULT NULL COMMENT '是否正在使用 1 是 0否',
      `needun` int(11) DEFAULT NULL COMMENT '状态 0：需要解压 1：解压成功 2：导入完成',
      `desc` varchar(1024) DEFAULT NULL COMMENT '描述',
      `msgtime` int(11) DEFAULT NULL COMMENT '提示间隔时间  分钟',
      `isshow` tinyint(1) DEFAULT NULL COMMENT '是否强制提示',
      `bagtype` int(11) DEFAULT NULL COMMENT '1:横版  2：竖版',
      `isdefault` tinyint(1) DEFAULT NULL COMMENT '是否默认模版',
      `revision` decimal(20,0) DEFAULT NULL,
      `vertype` int(11) DEFAULT NULL COMMENT '版本类型 1、全部刷新 0、部分刷新',
      PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

INSERT INTO `ktvmodule_ver` VALUES (3,'6.1主题皮肤','2017-08-14 10:23:53','','/opt/thunder/www/modules/90plus_cbf55578f97add87908b0ed410048160/','1.0.0.17',1,2,'20170726-雷客-6.1主题皮肤',60,0,1,0,1000000000000000017,1),
(4,'青春不毕业','2017-08-14 10:23:53','','/opt/thunder/www/modules/90plus_1d273cc897ecedae0ec460b3d4ee2978/','1.0.0.18',1,2,'20170726-雷客-青春不毕业',60,0,1,0,1000000000000000018,1),
(1,'固定模板V2','2017-05-05 02:27:04','C:\\thunder\\apache\\htdocs\\modules\\56AF41C9BC66B78ED11A5FA6B84FF84C.zip','/opt/thunder/www/modules/90plus_56AF41C9BC66B78ED11A5FA6B84FF84C','1.0.0.0',1,2,'90Plus 横版模块包',60,0,1,1,1000000000000000000,1),
(2,'固定竖版模板V2','2017-08-14 10:09:38','C:\\thunder\\apache\\htdocs\\modules\\F3DD3F4EBBAA12163830AD79CA728297.zip','/opt/thunder/www/modules/90plus_F3DD3F4EBBAA12163830AD79CA728297','1.0.0.0',1,2,'90Plus 竖版模块包',60,0,2,1,1000000000000000000,1);

--子模板-换肤模板
DROP TABLE IF EXISTS `themes`;
CREATE TABLE `themes` (
  `theme_id` int(11) primary key auto_increment NOT NULL,
  `theme_name` varchar(64) DEFAULT NULL COMMENT '模板名称',
  `theme_desc` varchar(512) DEFAULT NULL COMMENT '模板描述',
  `theme_path` varchar(256) DEFAULT NULL COMMENT '模板路径',
  `theme_unpath` varchar(256) DEFAULT NULL COMMENT '模板解压后的目录',
  `theme_type` tinyint DEFAULT NULL COMMENT '模板类型 0：自由主题  1、特定主题 ',
  `theme_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `theme_author` varchar(16) DEFAULT NULL COMMENT '设计者',
  `theme_state` tinyint DEFAULT NULL,
  `theme_bagtype` tinyint DEFAULT NULL COMMENT '模板包类型 1：横版 2 竖版'
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

INSERT INTO `themes` VALUES (49,'雷客-6.1主题皮肤','色彩与音乐碰撞，放飞那份最初的梦想，“我和我骄傲的倔强，我在风中大声的唱”，带上真挚的自己唱翻童年。你的奥特曼开始打小怪兽了吗？宠物>小精灵都长大了吗？暑期《西游记》即将开播了吗？致童年！我的精彩我做主！', '/data/download/themes/d522ab0ff68fc3e27988a7a7ea54841b.zip','/opt/thunder/www/themes/htheme_d522ab0ff68fc3e27988a7a7ea54841b',0,'2017-07-26 06:42:26','牛冬阳',1,1),
(50,'雷客-青春不毕业','炎炎夏日，又是一年毕业季，用全世界标记的足迹，来致敬我们终将逝去的青春，不忘初心，最后任性一次，毕业旅行走起来，带上小伙伴和傲娇的青春，世界那么大，我们一起疯！','/data/download/themes/90a937bd2d57404cb5a405bc2f3b8eaf.zip','/opt/thunder/www/themes/htheme_90a937bd2d57404cb5a405bc2f3b8eaf',0,'2017-07-26 06:43:12','安祖慧',1,1);

DROP TABLE IF EXISTS `staffs`;
CREATE TABLE `staffs` (
  `Staff_ID` int(11) primary key auto_increment,
  `Staff_SerialNo` varchar(200) DEFAULT NULL,
  `Staff_Password` varchar(128) default NULL,
  `Staff_RealName` varchar(200) DEFAULT NULL,
  `Staff_Rank_ID` int(11) DEFAULT NULL,
  `Staff_Branch_ID` int(11) DEFAULT NULL,
  `Staff_Description` varchar(255) DEFAULT NULL,
  `Staff_Gender` int(11) DEFAULT NULL,
  `Staff_Birthday` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `Staff_IdentityCardNo` varchar(18) DEFAULT NULL,
  `Staff_OfficePhone` varchar(30) DEFAULT NULL,
  `Staff_HomePhone` varchar(30) DEFAULT NULL,
  `Staff_MailAddress` varchar(100) DEFAULT NULL,
  `Staff_EMailAddress` varchar(60) DEFAULT NULL,
  `Staff_ICCardNo` varchar(100) DEFAULT NULL,
  `Staff_Enable` char(1) DEFAULT NULL,
  `Staff_Finger1` varchar(19) DEFAULT NULL,
  `Staff_Finger2` varchar(19) DEFAULT NULL,
  `OnlyUpperFee` decimal(19,2) DEFAULT NULL,
  `PeriodOfTimeUpperFee` decimal(19,2) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
INSERT INTO `staffs` VALUES (1,'admin','admin','系统管理员',5,1,NULL,0,'2016-10-11 11:32:33',NULL,NULL,NULL,NULL,NULL,NULL,'Y',NULL,NULL,0.00,0.00);

Create Table if not exists cloud_musicshadow (
    id integer not null primary key auto_increment,
    shadow_no integer not null comment '流水影编号',
    savepath varchar(200) not null comment '流水影视频路径',
    music_type varchar(50) comment '流水影类型',
    CreateTime datetime default CURRENT_TIMESTAMP comment '创建时间'
)ENGINE=MyISAM DEFAULT CHARSET=utf8;

--录音信息表
drop table if exists record;
CREATE TABLE `record` (
      `Record_Name` varchar(255) NOT NULL COMMENT '录音文件名',
      `Record_IP` varchar(15) NOT NULL COMMENT '房间IP地址',
      `Record_VideoType` varchar(10) DEFAULT NULL COMMENT '录音视频格式',
      `Record_AudioType` varchar(10) DEFAULT NULL COMMENT '录音音频格式',
      `Record_Volume` int(11) DEFAULT NULL COMMENT '音量',
      `Record_Original` int(11) DEFAULT NULL COMMENT '原唱',
      `Record_Accompany` int(11) DEFAULT NULL COMMENT '伴唱',
      `Record_AudioStatus` int(11) DEFAULT NULL,
      `Record_VideoURL` varchar(256) DEFAULT NULL COMMENT '视频URL',
      `Record_Type` int(11) DEFAULT NULL,
      `Record_UserID` int(11) DEFAULT NULL COMMENT '用户ID',
      `Record_UpLoadFlag` int(11) DEFAULT NULL COMMENT '上传标记',
      `Record_Uuid` longtext COMMENT 'uuid',
      `Record_AddTime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '添加时间',
      PRIMARY KEY (`Record_Name`,`Record_IP`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


--录音信息表--transfer_vod用，不能确保dbass与Transfer_vod的写表顺序，保留了不同的表
--长期来看，应该合表，Dbass与Transfer_vod做兼容，或者前端按固定的顺序调用。
--暂时保留（为减少代码改动）-2017-11-01
drop table if exists record_info;
create table record_info(
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(128) NOT NULL DEFAULT '' COMMENT '录音歌曲名字',
    `room_ip` varchar(32) NOT NULL DEFAULT '' COMMENT '房间IP',
    `media_no` varchar(32) NOT NULL DEFAULT '' COMMENT '歌曲编号',
    `score` varchar(32) NOT NULL DEFAULT '' COMMENT '录音评分',
    `calorie` varchar(32) NOT NULL DEFAULT '' COMMENT '录音评分',
    `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
)ENGINE=MyISAM DEFAULT CHARSET=utf8;

--原来的ktvmodule_classdata表
drop table if exists `module_medias`;
CREATE TABLE `module_medias` (
      `moduleid` int(11) DEFAULT NULL COMMENT '模板中的分类id',
      `media_no` int(11) DEFAULT NULL COMMENT '歌曲编号'
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--本地点播历史表。用于统计月排行，周排行。
drop table if exists mediahistory;
CREATE TABLE `mediahistory` (
  `media_no`  int NOT NULL COMMENT '歌曲编号' ,
  `addtime`  datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '添加时间' 
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

drop table if exists tmp;
CREATE TABLE `tmp` (
  `media_no`  int NOT NULL COMMENT '歌曲编号' ,
  `status`   int NOT NULL DEFAULT 0  
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

drop table if exists YouHuiPictureInfos;
CREATE TABLE `YouHuiPictureInfos` (
  `YouHuiPictureInfo_FileName` varchar(255) not NULL COMMENT '优惠图片名称',
  `YouHuiPictureInfo_Path` varchar(255) DEFAULT NULL COMMENT '优惠图片路径'
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

drop table if exists versionhistory;
CREATE TABLE `versionhistory` (
  `VersionHistory_ID` smallint(8) unsigned NOT NULL AUTO_INCREMENT,
  `VersionHistory_ver` varchar(20) DEFAULT NULL,
  `VersionHistory_Type` smallint(8) DEFAULT NULL,
  `VersionHistory_Result` smallint(8) DEFAULT NULL,
  `VersionHistory_RegisterTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`VersionHistory_ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

drop table if exists wechat_useroperation;
CREATE TABLE `wechat_useroperation` (
  `id` varchar(60) NOT NULL,
  `roomip` varchar(100) NOT NULL,
  `userid` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

drop table if exists medias_allowdel;
CREATE TABLE `medias_allowdel` (
      `media_no` int(11) primary key COMMENT '歌曲编号'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

drop table if exists medias_deleted;
CREATE TABLE `medias_deleted` (
      `media_no` int(11) NOT NULL COMMENT '歌曲编号',
      `media_file` varchar(256) CHARACTER SET utf8 DEFAULT NULL COMMENT '文件路径（文件名）',
      `media_deltime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
