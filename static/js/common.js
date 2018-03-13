(function($){
	/**
	 * 获取url根目录带端口
	 **/
	function getRootPathAndPort(){
	    var curWwwPath=window.document.location.href;
	    var pathName=window.document.location.pathname;
	    var pos=curWwwPath.indexOf(pathName);
	    var localhostPaht=curWwwPath.substring(0,pos);
	    var projectName=pathName.substring(0,pathName.substr(1).indexOf('/')+1);
	    return (localhostPaht);
	}
	$.getRootPathAndPort=getRootPathAndPort;
	/**
	 * 获取IP
	 **/
	function getRootPath(){
	    var curWwwPath=window.document.location.href;
	    var pathName=window.document.location.pathname;
	    var pos=curWwwPath.indexOf(pathName);
	    var localhostPaht=curWwwPath.substring(0,pos);
	    var projectName=pathName.substring(0,pathName.substr(1).indexOf('/')+1);
	    localhostPaht=localhostPaht.substring(0,localhostPaht.lastIndexOf(':'));
	    return localhostPaht;
	}
	$.getRootPath=getRootPath;
	
	function setDataTemplate(dataTemplate,key,val){
		return dataTemplate.replace(new RegExp("\\{\\["+key+"\\]\\}","ig"),val);
	}
	$.listSetVal=setDataTemplate;
	$.fillData=function(dataTemplate,arrList,filterFn){
		var html="";
		var arr = [].concat(arrList);
		for(var i in arr){
			if(arr.hasOwnProperty(i)){
				var obj=arr[i];
				var tp=dataTemplate;
				for(var key in obj){
					if(obj.hasOwnProperty(key)){
						if(!!filterFn)
							obj[key]=filterFn(key,obj[key])||obj[key];
						tp=setDataTemplate(tp,key,obj[key]);
					}
				}
				html+=tp;
			}
		}
		html=html.replace(new RegExp("\\{\\[.*\\]\\}","ig"),"");
		return html;
	}
//	$.fn.fillDataES6=function(arr,fn){
//		var html="";
//		for(var i of arr)
//			html+=fn(i);
//		$(this).html(html);
//	}
	$.tap=function(selector,fn){
		$(document).off("click",selector).on("click",selector,fn);
	}
	$.createObjDataOnlyKey=function(obj){
		var data="_T="+new Date().getTime();
		for(var key in obj){
			if(obj.hasOwnProperty(key)){
				data+="&"+key+"="+obj[key];
			}
		}
		return data;
	}
	
})($);