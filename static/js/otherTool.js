(function($){
	/*提示*/
	$.alt=function(str){
		$(".tip").html(str).css("display","block");
		var timer=window.setTimeout(function(){
			clearTimeout(timer);
			$(".tip").css("display","none");
		},3000);
	}
	$.altAuto=function(str){
		$.createConfirmBoxOK({"title":"系统提示","content":str});
//		$(".tip").html(str).css("display","block");
//		var timer=window.setTimeout(function(){
//			clearTimeout(timer);
//			$(".tip").css("display","none");
//		},3000);
	}
	
	/*
		数字输入框
	 */
	$.fn.isNumberBox=function(){
		$(this).keydown(function(event){
			if(bolKeyCodeNumber(event)) event.preventDefault();
		}).keyup(function(event){
			if(bolKeyCodeNumber(event)) return;
		});
	}
	/*
		判断是否输入数字
	 */
	function bolKeyCodeNumber(event){
		if((event.keyCode>=48&&event.keyCode<=57)||(event.keyCode>=96&&event.keyCode<=105)||event.keyCode==8)
			return false;
		return true;
	}
	
	/*汉字*/
	$.regTestChinese=function(text){
		var reg=/^[\u4e00-\u9fa5]+$/;
		return reg.test(text);
	}
	/*数字*/
	$.regTestNumber=function(text){
		var reg=/^[0-9]+$/;
		return reg.test(text);
	}
	
	function JSONLength(obj) {
		var size = 0, key;
		for (key in obj)if (obj.hasOwnProperty(key)) size++;
		return size;
	};
	$.JSONLength=JSONLength;
})($)
