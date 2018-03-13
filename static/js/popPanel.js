if(!window._)
	window._={};
(function(_){
	_.popPanel=function(title,html,w,h,isNotClose,fn){
		var pop = document.querySelector(".popPanel");
		var panel = document.querySelector(".popPanel>div");
		var content = document.querySelector(".popPanel>div>div");
		var header = document.querySelector(".popPanel>div>header");
		var span = document.querySelector(".popPanel>div>header>span");
		var close = document.querySelector(".popPanel>div>header>b");
		with(panel.style){
			width=w;
			height=h;
			transform="scale(1,1)";
			webkitTransform="scale(1,1)";
			opacity="1";
		}
		pop.style.pointerEvents="initial";
		header.style.display="block";
		if (!title) {
			header.style.display="none";
			content.style.height="100%";
		}else{
			span.innerHTML=title;
		}
		pop.style.backgroundColor="rgba(0,0,0,0.2)";
		if(isNotClose==undefined||isNotClose==true){
			pop.onclick=function(){
				with(panel.style){
					transform="scale(0.8,0.8)";
					webkitTransform="scale(0.8,0.8)";
					opacity="0";
				}
				pop.style.pointerEvents="none";
				pop.style.backgroundColor="rgba(0,0,0,0)";
			}
			panel.onclick=function(e){
				e.stopPropagation();
			}
		}
		
		content.innerHTML=html;
		close.onclick=function(){
			with(panel.style){
				transform="scale(0.8,0.8)";
				webkitTransform="scale(0.8,0.8)";
				opacity="0";
			}
			pop.style.pointerEvents="none";
			pop.style.backgroundColor="rgba(0,0,0,0)";
			if(!!fn)
				fn();
		}
		_.popPanelClose=function(){
			with(panel.style){
				transform="scale(0.8,0.8)";
				webkitTransform="scale(0.8,0.8)";
				opacity="0";
			}
			pop.style.pointerEvents="none";
			pop.style.backgroundColor="rgba(0,0,0,0)";
		}
	}
})(_)
