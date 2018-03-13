(function($){
	var isOpenSaveHTML=true;
	function createView(name,iconName,url,fn){
		$(".indexView").remove();
		if($(".indexView[mark='"+url+"']").length>0){
			$(".indexView.active").removeClass("active");
			
			$(".indexView[mark='"+url+"']").removeClass("animation-scale1-08").addClass("animation-scale08-1").addClass("active");
			return;
		}
		$(".indexView.active").removeClass("active");
		
		var index=document.createElement("div");
		var head=document.createElement("div");
		var body=document.createElement("div");
		var right=document.createElement("div");
		var bottomRight=document.createElement("div");
		var bottom=document.createElement("div");
		var icon=document.createElement("i");
		var h4=document.createElement("h4");
		var option=document.createElement("div");
		var optionA1=document.createElement("a");
		var optionA2=document.createElement("a");
		var optionA3=document.createElement("a");
		var optionA1i=document.createElement("i");
		var optionA2i=document.createElement("i");
		var optionA3i=document.createElement("i");
		
		$(index).attr("mark",url).attr("hrefArr","[\""+url+"\"]");
		
		index.className="indexView animation-scale08-1 active";
		head.className="indexHead";
		body.className="indexBody";
		right.className="indexBoxRight";
		bottomRight.className="indexBoxBottomRight";
		bottom.className="indexBoxBottom";
		icon.className=iconName;
		
		index.appendChild(head);
		index.appendChild(body);
		index.appendChild(right);
		index.appendChild(bottomRight);
		index.appendChild(bottom);
		
		head.appendChild(icon);
		head.appendChild(h4);
		
		optionA1.appendChild(optionA1i);
		optionA2.appendChild(optionA2i);
		optionA3.appendChild(optionA3i);
		
		h4.innerHTML=name;
//		index.ondragstart="return false";
//		head.ondragstart="return false";
//		h4.ondragstart="return false";
//		body.ondragstart="return false";
//		right.ondragstart="return false";
//		bottomRight.ondragstart="return false";
//		bottom.ondragstart="return false";
		
		index.style.top=($(".indexView.animation-scale08-1").length*15)+"px";
		index.style.left=($(".indexView.animation-scale08-1").length*15)+"px";
		
		var content=$(".index_centerContent");
		content.append(index);
		
		$(index).on("mousedown",function(){
			$(".indexView.active").removeClass("active");
			$(this).addClass("active");
		});
		
		var hx=0;
		var hy=0;
		var hLeft=0;
		var hTop=0;
		$(head).on("mousedown",function(e){
			hx=e.pageX;
			hy=e.pageY;
			hLeft=parseInt($(index).css("left"));
			hTop=parseInt($(index).css("top"));
			var maxLeft=content.width()-$(index).width();
			var maxTop=content.height()-$(index).height();
			$(document).on("mousemove",function(e){
				var left=hLeft+(e.pageX-hx);
				var top=hTop+(e.pageY-hy);
				if(left<0) left=0;
				if(top<0) top=0;
				if(left>maxLeft) left=maxLeft;
				if(top>maxTop) top=maxTop;
				$(index).css({"left":left+"px","top":top+"px"});
			}).on("mouseup",function(e){
				$(document).off("mousemove").off("mouseup");
			});
		});
		
		$(head).on("dblclick",function(){
			if(!$(optionA2i).hasClass("icon-resize-small")){
				$(index).attr("w",$(index).width()).attr("h",$(index).height());
				$(index).css({"width":"100%","height":"100%","left":"0px","top":"0px"});
				optionA2i.className="icon-resize-small";
			}else{
				$(index).css({"width":$(index).attr("w")+"px","height":$(index).attr("h")+"px"});
				optionA2i.className="icon-check-empty";
			}
		});
		
		var w=0;
		var h=0;
		var x=0;
		var y=0;
		
		$(right).on("mousedown",function(e){
			x=e.pageX;
			w=$(index).width();
			$(document).on("mousemove",function(e){
				$(index).css("width",(w+(e.pageX-x))+"px");
			}).on("mouseup",function(e){
				$(document).off("mousemove").off("mouseup");
			});
		});
		
		$(bottom).on("mousedown",function(e){
			y=e.pageY;
			h=$(index).height();
			$(document).on("mousemove",function(e){
				$(index).css("height",(h+(e.pageY-y))+"px");
			}).on("mouseup",function(e){
				$(document).off("mousemove").off("mouseup");
			});
		});
		
		$(bottomRight).on("mousedown",function(e){
			x=e.pageX;
			y=e.pageY;
			w=$(index).width();
			h=$(index).height();
			$(document).on("mousemove",function(e){
				$(index).css({"width":(w+(e.pageX-x))+"px","height":(h+(e.pageY-y))+"px"});
			}).on("mouseup",function(e){
				$(document).off("mousemove").off("mouseup");
			});
		});
		
		
		$.getHTML(url,function(html){
			if((!html||html==null||html=="null"||html=="undefined")||!isOpenSaveHTML) {
				loadHtml(url,function(str){
					html=str;
					$(body).append($(html));
					if(!!fn)
						fn();
					if(!!$.timer){
						clearInterval($.timer);
					}
				});
			}else{
				$(body).append($(html));
				if(!!fn)
					fn();
				if(!!$.timer){
					clearInterval($.timer);
				}
			}
		});	
//		loadHtml(url,function(str){
//			$(body).append($(str));
//			if(!!fn)
//				fn();
//			if(!!$.timer){
//				clearInterval($.timer);
//			}
//		});
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
				
				
				$.getHTML(url,function(data){
					if(!data||data==null||data=="null")
						$.addHTML(url, str);	
				});
				
				
				if(fn)
					fn(str);
			},
			error: function (msg) {
				$(".loading").css("display","none");
				$.createConfirmBox({"title":"网络中断","content":"网络已断开,是否重连？","click":function(){
					loadHtml(url,fn);
				}});
			}
		});
	}
	function handleHTML(str){
		str=str.substring(str.indexOf("<body"),str.indexOf("</body>")+7);
		return str;
	}
	$(document).on("click",".hrefTo",function(){
		if(!$.user){
			$("body").removeClass("closeLogin");
			return;
		}
		var name=$.trim($(this).text())||$(this).attr("text");
		var iconName=$(this).children("i").attr("class");
		var url=$(this).attr("href");
		if(!!$.user){
			localStorage.setItem("currentUrl",url);
		}
		createView(name,iconName,url);
	});
	$.createView=createView;
})($);
