(function($){
	$.fn.scrollTable=function(num){
		with($(this)[0].style){
			position="relative";
			transform="scale(1,1)";
			webkitTransform="scale(1,1)";
		}
		var trList=[];
		var trHeight=$(this).children("tr").first().height();
		$(this).children("tr").each(function(){
			trList.push($(this).css("display","none"));
		});
		var len=trList.length;
		var div=$("<div></div>");
		var cDiv=$("<div></div>");
		var divHeight=trHeight*num;
		with(div[0].style){
			width="10px";
			height=divHeight+"px";
			backgroundColor="rgb(199, 199, 199)";
			position="absolute";
			top="0px";
			right="0px";
			borderRadius="10px";
		}
		var cDivHeight=divHeight*(parseFloat(num/len));
		if(len<num){
			cDivHeight=divHeight;
		}
		with(cDiv[0].style){
			width="10px";
			height=cDivHeight+"px";
			backgroundColor="rgb(241, 241, 241)";
			border="1px rgb(199, 199, 199) solid";
			boxSizing="border-box";
			position="absolute";
			top="0px";
			right="0px";
			borderRadius="10px";
			cursor="pointer";
		}
		var movePx=divHeight-cDivHeight;
		div.append(cDiv);
		$(this).append(div);
		var st=0;
		var en=num;
		filterNode();
		var lm=0;
		window.onmousewheel=document.onmousewheel=function(e){
			lm++;
			if(lm%2==0)
				return;
			if(event.wheelDelta<0){
				var prevN=prevNode();
				var nextN=nextNode();
				if(!!prevN&&!!nextN){
					prevN.css("display","none");
					nextN.css("display","inline-flex");
				}
				if(st+num<len){
					st++;
					en=st+num;
				}
			}else{
				var prevN=prevNode();
				var nextN=nextNode();
				if(!!prevN&&!!nextN){
					prevN.css("display","inline-flex");
					nextN.css("display","none");
				}
				if(st>0){
					st--;
					en=st+num;
				}
			}
			var t=movePx/((len-num)/st);
			with(cDiv[0].style){
				top=t+"px";
			}
		}
//		var changeY=0;
//		cDiv.off("mousedown").on("mousedown",function(e){
//			var top = $(cDiv).offset().top;
//			var sy = e.pageY;
//			var inity=sy-top;
//			var orderY=0;
//			$(document).on("mousemove",function(e){
//				var cy = e.pageY;
//				if(orderY!=0){
//					var y=cy-orderY;
//					changeY+=y;
//					if(changeY>0&&changeY<movePx){
//						with(cDiv[0].style){
//							top=changeY+"px";
//						}
//					}
//				}
//				orderY=cy;
//			}).on("mouseup",function(){
//				$(document).off("mousemove").off("mouseup");
//			});
//		});
		function prevNode(){
			if(trList.hasOwnProperty(st))
				return trList[st];
			else
				return null;
		}
		function nextNode(){
			if(trList.hasOwnProperty(en))
				return trList[en];
			else
				return null;
		}
		function filterNode(){
			for(var i=0;i<num;i++){
				if(trList.hasOwnProperty(i)){
					trList[i].css("display","inline-flex");
				}	
			}
		}
	}
})($);
