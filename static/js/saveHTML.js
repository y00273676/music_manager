(function($){
	var db=null;
	function saveHTMLInit(){
		/*
			构建本地数据库
		 */
		db=openDatabase("data","1.0","存储",200*1024);  //kb
		/*
			建表
		 */
		if(db){
			db.transaction( function(tx) {
				tx.executeSql(
					"create table if not exists HTML (id integer primary key AUTOINCREMENT,name VARCHAR(50), content TEXT)",
					[],
					function(tx,result){},
					function(tx, error){ console.error('创建表失败:' + error.message);
				});
			});
		}
	}
	
	/*
		插入数据
	 */
	function addHTML(key,value){
		db.transaction( function(tx) {
			tx.executeSql(
				"insert into HTML (name, content) values(?, ?)",
				[key,value],
				function(tx,result){},
				function(tx, error){ console.error('添加失败' + error.message);
				});
		});
	}
	/*
		修改数据
	 */
	function updateHTML(key,value){
		db.transaction( function(tx) {
			tx.executeSql(
				"update HTML set content=? where name=?",
				[value,key],
				function(tx,result){},
				function(tx, error){ console.error('添加失败:' + error.message);
				});
		});
	}
	/*
		查询数据
	 */
	function getHTML(name,fn){
		var sql="select content from HTML where name='"+name+"'";
		db.transaction( function(tx) {
			tx.executeSql(
				sql,
				[],
				function(tx,result){
					if(fn)
						if(result.rows.length>0)
							fn(result.rows.item(0)['content']);
						else
							fn(null);
				},
				function(tx, error){ console.error('查询失败:' + error.message);
				});
		});
	}
	/*
		删除数据
	 */
	function deleteHTML(name){
		db.transaction( function(tx) {
			var arr=[];
			var sql="delete from HTML";
			if(name) {
				arr.push(name);
				sql+=" where name=?"
			}
			tx.executeSql(
				sql,
				arr,
				function(tx,result){},
				function(tx, error){ alert('删除失败:' + error.message);
				});
		});
	}
	$.saveHTMLInit=saveHTMLInit;
	$.addHTML=addHTML;
	$.updateHTML=updateHTML;
	$.getHTML=getHTML;
	$.deleteHTML=deleteHTML;
})($);
