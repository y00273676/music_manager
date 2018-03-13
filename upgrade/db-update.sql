

#207-04-01, 
ALTER table Record_Meta add column if not exists newscore varchar(32);
ALTER table ktvcloud_musicscore add column if not exists newscore varchar(32);

#207-04-20, Lizhe, need set id as auto_increment column
alter table ktvcloud_musicscore change id id int auto_increment;

#2017-04-27, by syi, diff for karaok db between 2017-0220 and 2017-0427
alter table addmedia modify column AddMedia_Size bigint;
update karaokversions set KaraokVersion_ver='5.0.0.70';
alter table medias add column if not exists media_light int not null default 0;

/* --自定义轮播 */
drop table if exists usermedias;
create table usermedias (
	Media_no varchar(10),
	Room_SerialNo varchar(30),
	Allday int,
	Begintime varchar(20),
	Endtime varchar(20)
);
/*流水影*/
drop table if exists cloud_musicshadow;
Create Table cloud_musicshadow (
	id integer not null auto_increment,
	Shadow_no integer comment '流水影编号',
	savepath varchar(200) comment '流水影视频路径',
	music_type varchar(50) comment '流水影类型',
	CreateTime datetime default CURRENT_TIMESTAMP comment '创建时间',
	primary key (id)
);


alter table carriers change Carrier_ID Carrier_ID integer not null AUTO_INCREMENT;
insert into carriers(Carrier_Name, Carrier_Description) values('WAV','WAV');
insert into carriers(Carrier_Name, Carrier_Description) values('LS','LS');
insert into carriers(Carrier_Name, Carrier_Description) values('LSS','LSS');


drop PROCEDURE if exists `sp_SetMediaIndex`;
DELIMITER //
CREATE PROCEDURE `sp_SetMediaIndex`()
BEGIN
	declare result int;
	declare id int;
	declare _err int default 0;  
	declare continue handler for sqlexception set _err=1;  	
	
	
	SET @STMT := CONCAT("select SettingInfo_Value into @changetime from systemsettinginfo where SettingInfo_Name = 'MeidasIndexCreateTime'");
	PREPARE STMT FROM @STMT;
	EXECUTE STMT;
	DEALLOCATE PREPARE STMT;

	IF @changetime is null THEN		
		call sp_createuniqueid('SystemSettingInfo','SettingInfo', @id);
		SET @STMT := CONCAT("INSERT	INTO	systemsettinginfo(SettingInfo_ID,SettingInfo_Name,SettingInfo_Value) VALUES (CAST(@id, VARCHAR),'MeidasIndexCreateTime',now())");
		PREPARE STMT FROM @STMT;
		EXECUTE STMT;
		DEALLOCATE PREPARE STMT;
		IF _err<>0 THEN
			set result = 1;
		END IF;
	ELSE
		SET @STMT := CONCAT("SELECT DATEDIFF(@changetime, now()) into @dtc");
		PREPARE STMT FROM @STMT;
		EXECUTE STMT;
		DEALLOCATE PREPARE STMT;
		
		IF @dtc <=0 THEN
			SET @STMT := CONCAT("select count(*) into @icount from meidasindex");
			PREPARE STMT FROM @STMT;
			EXECUTE STMT;
			DEALLOCATE PREPARE STMT;
			
			IF @icount <> 0
			THEN
				set result = 2;
			ELSE 
				SET @STMT := CONCAT("update systemsettinginfo set SettingInfo_Value = now() where SettingInfo_Name = 'MeidasIndexCreateTime'");
				PREPARE STMT FROM @STMT;
				EXECUTE STMT;
				DEALLOCATE PREPARE STMT;
				
				IF _err <> 0 THEN
						set result = 3;
				END IF;
			END IF;
		ELSE
			SET @STMT := CONCAT("update systemsettinginfo set SettingInfo_Value = @nowtime where SettingInfo_Name = 'MeidasIndexCreateTime'");
			PREPARE STMT FROM @STMT;
			EXECUTE STMT;
			DEALLOCATE PREPARE STMT;
			if _err<>0 THEN
				set result = 4;
			END IF;
		END IF;
	END IF;

	SET @STMT := CONCAT("delete from meidasindex");
	PREPARE STMT FROM @STMT;
	EXECUTE STMT;
	DEALLOCATE PREPARE STMT;
	COMMIT;
	
	SET @STMT := CONCAT("ALTER TABLE meidasindex AUTO_INCREMENT =1");
	PREPARE STMT FROM @STMT;
	EXECUTE STMT;
	DEALLOCATE PREPARE STMT;
	COMMIT;
	
	SET @STMT := CONCAT("INSERT INTO meidasindex(MeidasIndex_Media_ID) SELECT Media_ID FROM medias1 ",
			"where  Media_Name not like '%[0-9][A-B][0-9]%' ",
			"order by MediaManage_OrderCount desc,media_Name_length,Media_IsReserved5,Media_HeaderSoundSequence,Media_Name,Media_Sequence");
	
	PREPARE STMT FROM @STMT;
	EXECUTE STMT;
	DEALLOCATE PREPARE STMT;
	if _err<>0 THEN
		set result = 6;
	END IF;
END//
DELIMITER ;


