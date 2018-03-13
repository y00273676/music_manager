(function($){
	$.fn.inputList=function(fn,width,addTop){
		var _this=$(this);
		var ul=$(".inputList");
		_this.off("input").on("input",function(){
			if(!!_this.val()){
				if(!!fn){
					fn(_this.val());
					ul.children("li").off("click").on("click",function(){
						_this.val($.trim($(this).html()));
					})
				}
				if(!$(ul).hasClass("active")){
					$(ul).addClass("active");
				}
			}else{
				if($(ul).hasClass("active"))
					$(ul).removeClass("active");
			}
		});
		_this.off("focus").on("focus",function(){
			if(!_this.val()){
				if($(ul).hasClass("active"))
					$(ul).removeClass("active");
			}
			var inputObj={};
			inputObj.x=_this.offset().left;
			inputObj.y=_this.offset().top;
			inputObj.w=_this.width();
			inputObj.h=_this.height();
			if(!!width){
				inputObj.w=width;
				inputObj.y+=addTop;
			}
			ul.css({"width":inputObj.w+"px","left":inputObj.x+"px","top":(inputObj.y+inputObj.h)+"px"});
		});
		document.onclick=function(){
			if($(ul).hasClass("active"))
				$(ul).removeClass("active");
		}
		document.onkeyup=function(e){
			if(e.keyCode==38){
				if($(ul).hasClass("active")){
					if($(".inputList>li.active").length==0)
						$(".inputList>li").last().addClass("active");
					else
						$(".inputList>li.active").removeClass("active").prev().addClass("active");
				}
			}else if(e.keyCode==40){
				if($(ul).hasClass("active")){
					if($(".inputList>li.active").length==0)
						$(".inputList>li").first().addClass("active");
					else
						$(".inputList>li.active").removeClass("active").next().addClass("active");
			
				}
			}else if(e.keyCode==13){
				if($(".inputList>li.active").length>0)
					$(".inputList>li.active").click();
				else
					$(ul).removeClass("active");
			}
		}
		var inputObj={};
		inputObj.x=_this.offset().left;
		inputObj.y=_this.offset().top;
		inputObj.w=_this.width();
		inputObj.h=_this.height();
		if(!!width){
			inputObj.w=width;
			inputObj.y+=addTop;
		}
		ul.css({"width":inputObj.w+"px","left":inputObj.x+"px","top":(inputObj.y+inputObj.h)+"px"});
	}
})($);
