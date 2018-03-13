(function($){
	var div=null;
	var ul1=null;
	var ul2=null;
	$.fn.messageBox=function(arr){
		if($(".messageBox").length>0){
			div=$(".messageBox");
			ul1=$(".messageBox").children("ul:eq(0)");
			ul2=$(".messageBox").children("ul:eq(1)");
		}else{
			div=$("<div></div>").addClass("messageBox");
			ul1=$("<ul></ul>");
			ul2=$("<ul></ul>");
			for(var i in arr){
				if(arr.hasOwnProperty(i)){
					var btn=arr[i];
					var b=$("<li>"+btn.text+"</li>");
					b.on("click",btn.click);
					ul1.append(b);
				}
			}
			div.append(ul1);
			div.append(ul2);
		}
		var offset=$(this).offset();
		var messageBoxWidth=$(this).width();
		var messageBoxHeight=$(this).height();
		var messageBoxTop=offset.top+messageBoxHeight+20;
		var messageBoxLeft=offset.left+messageBoxWidth-345;
		div.css("top",messageBoxTop+"px").css("left",messageBoxLeft+"px");
		
		$("body").on("click",function(){
			div.css("display","none");
		});
		div.off("click").on("click",function(e){
			e.stopPropagation();
		});
		div.css("display","none");
		$("body").append(div);
		$(this).off("click").on("click",function(e){
			e.stopPropagation();
			div.css("display","block")
		});
	}
	$.messageBoxPush=function(obj){
		var classUnRead="";
		if(obj.unRead==0)
			classUnRead="unRead";
		var li="";
		if($(".messageBox>ul:eq(1)>li[no='"+obj.id+"']").length==0)
			li=$("<li no=\""+obj.id+"\" class=\"messageState"+obj.state+" "+classUnRead+"\">"+obj.title+"<small>"+obj.time+"</small></li>").prependTo(ul2).data("obj",obj);
		$(".messageNum").html(ul2.children("li.unRead").length);
		return li;
	}
})($);
