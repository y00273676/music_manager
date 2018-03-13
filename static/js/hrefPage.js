(function($){
	var isOpenSaveHTML=true;
	var sudu=0.25;
	
	function preLoadPage(href){
		$.getHTML(href,function(html){
			if(!html) {
				loadHTML(href);
			}
		});
	}
	$.preLoadPage=preLoadPage;
	
	function hrefPage(url,indexView,fn){
		var hrefArrStr=indexView.attr("hrefArr");
		if(!hrefArrStr)
			hrefArr=new Array();
		else
			hrefArr=$.parseJSON(hrefArrStr);
		var hrefStr="";
		if(hrefArr.length>1)
			hrefStr=hrefArr[hrefArr.length-2];
		if(hrefStr==url){
			$.getHTML(url,function(html){
				if((!html||html==null||html=="null"||html=="undefined")||!isOpenSaveHTML) {
					loadHTML(url,function(str){
						html=str;
						changePage(html,1,indexView,fn);
					});
				}else{
					changePage(html,1,indexView,fn);
				}
				hrefArr.pop();
			});
		}else{
			hrefArr.push(url);
			$.getHTML(url,function(html){
				if((!html||html==null||html=="null"||html=="undefined")||!isOpenSaveHTML) {
					loadHTML(url,function(str){
						html=str;
						changePage(html,-1,indexView,fn);
					});
				}else{
					changePage(html,-1,indexView,fn);
				}
			});
		}
	}
	$.hrefPage=hrefPage;
	function toBack(indexView,fn){
		var hrefArrStr=indexView.attr("hrefArr");
		if(!hrefArrStr)
			hrefArr=new Array();
		else
			hrefArr=$.parseJSON(hrefArrStr);
		var hrefStr="";
		if(hrefArr.length>1)
			hrefStr=hrefArr[hrefArr.length-2];
		hrefPage(hrefStr,indexView,fn);
	}
	$.toBack=toBack;
	$.fn.parentU=function(className){
		var p=$(this).parent();
		if(p.hasClass(className))
			return p;
		else
			return p.parentU(className);
	}
//	function parentU(_this,className){
//		var p=_this.parent();
//		if(p.hasClass(className))
//			return p;
//		else
//			return parentU(p,className);
//	}
	function changePage(str,isRe,indexView,fn){
		var divBody=document.createElement("div");
		divBody.innerHTML=str;
		divBody.className="indexBody";
		divBody=$(divBody);
		var oldBody=indexView.children(".indexBody");
		
//		divBody.css({
//			"webkitTransform":"translateX("+(-100*isRe)+"%)",
//			"transform":"translateX("+(-100*isRe)+"%)"
//		});

		divBody.css({
			"transition":"-webkit-transform "+0+"s",
			"webkitTransition":"-webkit-transform "+0+"s",
			"webkitTransform":"translate("+(-100*isRe)+"%,-100%)",
			"transform":"translate("+(-100*isRe)+"%,-100%)"
		});
		oldBody.after(divBody);
		window.setTimeout(function(){
			oldBody.css({
				"transition":"-webkit-transform "+sudu+"s",
				"webkitTransition":"-webkit-transform "+sudu+"s",
				"webkitTransform":"translateX("+(100*isRe)+"%)",
				"transform":"translateX("+(100*isRe)+"%)"
			});
			divBody.css({
				"transition":"-webkit-transform "+sudu+"s",
				"webkitTransition":"-webkit-transform "+sudu+"s",
				"webkitTransform":"translate("+(0)+"%,-100%)",
				"transform":"translate("+(0)+"%,-100%)"
			});
			oldBody.off("transitionend").on("transitionend",function(){
				oldBody.remove();
				divBody.removeAttr("style");
				indexView.attr("hrefArr",JSON.stringify(hrefArr));
				if(!!fn)
					fn();
			});
		},50);


//		window.setTimeout(function(){
//			oldBody.css({
//				"transition":"-webkit-transform "+sudu+"s",
//				"webkitTransition":"-webkit-transform "+sudu+"s",
//				"webkitTransform":"translateX("+(100*isRe)+"%)",
//				"transform":"translateX("+(100*isRe)+"%)"
//			});
//			divBody.css({
//				"transition":"-webkit-transform "+sudu+"s",
//				"webkitTransition":"-webkit-transform "+sudu+"s",
//				"webkitTransform":"translateX("+(0)+"%)",
//				"transform":"translateX("+(0)+"%)"
//			});
//			oldBody.off("transitionend").on("transitionend",function(){
//				oldBody.remove();
//				divBody.removeAttr("style");
//			});
//		},50);


		
	}
	function loadHTML(href,fn){
		$.ajax({
			type: 'get',
			url: href+"?_="+(new Date()).getTime(),
			dataType: 'html',
			success: function (str) {
				var div = document.createElement("div");
				div.innerHTML = handleHTML(str);
				str = $(div).html();
				
				
				$.getHTML(href,function(data){
					if(!data||data==null||data=="null")
						$.addHTML(href, str);	
				});
				
				
				if(!!fn)
					fn(str);
			},
			error: function (msg) {
				
			}
		});
	}
	function handleHTML(str){
		str=str.substring(str.indexOf("<body"),str.indexOf("</body>")+7);
		return str;
	}
})($);
