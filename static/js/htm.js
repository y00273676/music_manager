$.fn.htm=function(text){
	var _this=$(this);
	var newList=$(text);
	var list=_this.children();
	list=list.filter(function(){
		return !!$(this)[0].outerHTML;
	});
	newList=newList.filter(function(){
		return !!$(this)[0].outerHTML;
	});
	if(newList.length==0||(list.length>0&&newList[0].tagName!=list[0].tagName)){
		_this.html(text);
		return;
	}
	try{
		if(newList.length>list.length){
			var count = newList.length-list.length;
			for(var i=0;i<count;i++){
				_this.append(newList.eq(0).clone());
			}
		}
		if(list.length>newList.length){
			var count = list.length-newList.length;
			for(var i=0;i<count;i++){
				list.eq(i).remove();
			}
		}
		list=_this.children();
		list.each(function(){
			var dom=$(this);
			var domHtml=dom[0].outerHTML;
			var attrList=domHtml.match(/ \w+/ig);
			for(var i in attrList){
				if(attrList.hasOwnProperty(i)){
					var name=$.trim(attrList[i]);
					dom.removeAttr(name);
				}
			}
		});
		newList.each(function(i){
			var dom=list.eq(i);
			var newDom=$(this);
			var newDomHtml=newDom[0].outerHTML;
			if(!!newDomHtml){
				var attrList=newDomHtml.match(/ \w+="(\w+|)".*"/ig);
				attrList=attrList[0].split(" ");
				for(var i in attrList){
					if(attrList.hasOwnProperty(i)){
						var t=$.trim(attrList[i]);
						if(!!t){
							var arr=t.split("=");
							var name=arr[0];
							var value=arr[1].substring(1,arr[1].length-1);
							if(!value)
								value="";
							dom.attr(name,value);
						}
					}
				}
				dom.html(newDom.html())
			}
		});
	}catch(e){
		_this.html(text);
		return;
	}
}