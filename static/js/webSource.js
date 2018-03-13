(function($){
	var sourceArr=[];
	var source=null;
	function initWebSource(url,fn){
		source=new EventSource(url);
		sourceArr.push(source);
		if(!source){
			$.altAuto("浏览器不支持");
			return;
		}
		source.onmessage = function(event) { 
			if(!!fn)
				fn(event.data);
	  };
	}
	$.initWebSource=initWebSource;
	$.closeWebSource=function(){
		for(var i in sourceArr){
			var obj=sourceArr[i];
			if(!!obj){
				// obj.close();
				sourceArr[i]=null;
				obj=null;
			}
		}
	}
})($);
