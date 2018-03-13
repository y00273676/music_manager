(function($){
	$.fn.loadPage=function(seletor,fn){
		var div = $(seletor);
		$(this).off("click").on("click",function(){
			var _this=$(this);
			var url = _this.attr("href");
			loadHtml(url,function(str){
				div.html(str);
				if(!!fn)
					fn.call(_this[0]);
			})
		});
	}
	function loadHtml(url,fn){
		$.ajax({
			type: 'get',
			url: url+"?_="+(new Date()).getTime(),
			dataType: 'html',
			success: function (str) {
				var div = document.createElement("div");
				if(url.indexOf("http")>-1)
					div.innerHTML = str;
				else
					div.innerHTML = handleHTML(str);
				str = $(div).html();
				if(fn)
					fn(str);
			},
			error: function (msg) {
				console.log("页面加载失败");
			}
		});
	}
	function handleHTML(str){
		str=str.substring(str.indexOf("<body"),str.indexOf("</body>")+7);
		return str;
	}
})($);
