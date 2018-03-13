/**
 * 右击菜单 -bzy
 * @param {Object} json
 * {
 *	 "data":[{
 *		"text":"删除目录",
 *		"id":"aaa",
 * 		"class":"ccc",
 *		"click":function(){}
 *	 }]
 * }
 */
(function($){
	var cuActiveLi=null;
	$.fn.contextmenu=function(json,fn){
		var div=document.createElement("div");
		var ul=document.createElement("ul");
		var menuJson=json.data;
	
		var $this=$(this);
		if($this.next().hasClass("supplement_contextmenu")){
			$this.next().remove();
		}
		for(var i in menuJson){
			var li=document.createElement("li");
			li.id=menuJson[i].id;
			li.className=menuJson[i].class;
			li.innerHTML=menuJson[i].text;
			$(li).data("ti",i);
			li.onclick=function(){
				var func=menuJson[$(this).data("ti")].click;
				func.call(cuActiveLi[0]);
			}
			ul.appendChild(li);
		}
		div.className="supplement_contextmenu";
		div.appendChild(ul);
	
		$this.after($(div));
		$this.bind("contextmenu",function(e){
			return false;
		});
		$(document).mouseup(function(){
			$(".supplement_contextmenu:visible").css("display","none");
		});
		$this.mouseup(function(e){
			var $th=$(this);
			
			//***--追加--***
			
			var body=$th.parentsUntil(".tableDiv");
			var offset=body.offset();
			var bodyTop=offset.top-96;
			var bodyLeft=offset.left;
			
			//***--项目追加--***
			
			window.setTimeout(function(){
				var menu=$th.next()[0];
				if (e.button==2){
					$(".supplement_contextmenu:visible").css("display","none");
					var epageY=e.pageY-bodyTop;
					if(e.pageY>($(window).height()-menuJson.length*30)){
						epageY-=(menuJson.length*30);
					}
					with(menu.style){
						top=epageY+"px";
						left=(e.pageX-bodyLeft)+"px";
						display="block";
					}
					cuActiveLi=$th;
					if(!!fn)
						fn.call($th[0]);
				}else{
					with(menu.style){
						display="none";
					}
					$(".supplement_contextmenu:visible").css("display","none");
				}
			},50);
		});
	}
})($);