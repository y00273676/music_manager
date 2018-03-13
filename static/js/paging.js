(function($){
	$.fn.paging=function(dataCount,pageNum,pageSize,fn){
		var liCount=5;
		if(isNaN(dataCount)||isNaN(pageNum)||isNaN(pageSize)){
			alert("分页参数不可为非数字");
			return;
		}
		var _this=$(this);
		_this.empty();
		var ul=document.createElement("ul");
		var firstPage=document.createElement("li");
		var prevPage=document.createElement("li");
		var nextPage=document.createElement("li");
		var lastPage=document.createElement("li");
		var firstPagei=document.createElement("i");
		var prevPagei=document.createElement("i");
		var nextPagei=document.createElement("i");
		var lastPagei=document.createElement("i");
		var div=document.createElement("div");
		var bPageNum=document.createElement("b");
		var bFG=document.createTextNode("/");
		var bPageSize=document.createElement("b");
		ul.className="paging";
		firstPagei.className="icon-double-angle-left";
		prevPagei.className="icon-angle-left";
		nextPagei.className="icon-angle-right";
		lastPagei.className="icon-double-angle-right";
		div.className="paging_pageInfo";
		var maxPage=0;
		maxPage=Math.ceil(dataCount/pageSize);
		if(maxPage<liCount){
			liCount=maxPage;
		}
//		if(dataCount%pageSize==0){
//			maxPage=dataCount/pageSize;
//		}else{
//			maxPage=parseInt(dataCount/pageSize)+1;
//		}
		var liArr=[];
		var setStartNum=0;
		if(pageNum>2&&pageNum<maxPage-2){
			setStartNum=pageNum-2;
		}else{
			if(pageNum<2+1){
				setStartNum=1;
			}else if(pageNum>maxPage-2-1){
				setStartNum=maxPage-liCount+1;
			}
		}
		for(var i=0;i<liCount;i++){
			var li=document.createElement("li");
			li.innerHTML=setStartNum+i;
			if(li.innerHTML==pageNum)
				li.className="active";
			li.onclick=function(){
				pageNum=this.innerHTML;
				refreshNum();
				if(!!fn)
					fn(pageNum);
			}
			liArr.push(li);
		}
		ul.appendChild(firstPage);
		ul.appendChild(prevPage);
		for(var i in liArr){
			if(liArr.hasOwnProperty(i))
				ul.appendChild(liArr[i]);
		}
		ul.appendChild(nextPage);
		ul.appendChild(lastPage);
		firstPage.appendChild(firstPagei);
		prevPage.appendChild(prevPagei);
		nextPage.appendChild(nextPagei);
		lastPage.appendChild(lastPagei);
		div.appendChild(bPageNum);
		div.appendChild(bFG);
		div.appendChild(bPageSize);
		firstPage.onclick=function(){
			pageNum=1;
			refreshNum();
			if(!!fn)
				fn(pageNum);
		}
		prevPage.onclick=function(){
			if(pageNum>1){
				pageNum--;
				refreshNum();
				if(!!fn)
					fn(pageNum);
			}	
		}
		nextPage.onclick=function(){
			if(pageNum<maxPage){
				pageNum++;
				refreshNum();
				if(!!fn)
					fn(pageNum);
			}	
		}
		lastPage.onclick=function(){
			pageNum=maxPage;
			refreshNum();
			if(!!fn)
				fn(pageNum);
		}
		bPageNum.innerHTML=pageNum;
		bPageSize.innerHTML=maxPage;
		_this.append(ul);
		_this.append(div);
		function refreshNum(){
			if(pageNum>2&&pageNum<maxPage-2){
				setStartNum=pageNum-2;
			}else{
				if(pageNum<2+1){
					setStartNum=1;
				}else if(pageNum>maxPage-2-1){
					setStartNum=parseInt(maxPage-liCount+1);
				}
			}
			bPageNum.innerHTML=pageNum;
			for(var i in liArr){
				var li=liArr[i];
				li.innerHTML=parseInt(setStartNum)+parseInt(i);
				if(li.innerHTML==pageNum){
					$(li).parent().children(".active").removeClass("active");
					li.className="active";
				}
			}
		}
		
	}
	function sliceArrListData(arr,count){
		var pageDataList={};
		var pageIdx=1;
		var start=0;
		for(var i=0;i<arr.length;i++){
			if(i%count==0&&i!=0){
				pageDataList[pageIdx]=arr.slice(start,i);
				start=i;
				pageIdx++;
			}
			if(arr.length-1==i){
				pageDataList[pageIdx]=arr.slice(start,arr.length);
				start=i;
				pageIdx++;
			}
		}
		return pageDataList;
	}
	$.sliceArrListData=sliceArrListData;
	
	function searchArrListData(arr,text,colList){
		var newList=[];
		if(typeof colList == "object"){
			for(var i in arr){
				var obj = arr[i];
				for(var k in colList){
					var key = colList[k];
					if(obj.hasOwnProperty(key)&&colList.hasOwnProperty(k)){
						if(obj[key]==text){
							newList.push(obj);
						}
					}
				}
			}
		}
		if(typeof colList == "string"){
			for(var i in arr){
				var obj = arr[i];
				if(obj.hasOwnProperty(colList)){
					if(obj[colList]==text){
						newList.push(obj);
					}
				}
			}
		}
		return newList;
	}
	$.searchArrListData=searchArrListData;
	function searchArrListDataLike(arr,text,colList){
		var newList=[];
		if(typeof colList == "object"){
			for(var i in arr){
				var obj = arr[i];
				for(var k in colList){
					var key = colList[k];
					if(obj.hasOwnProperty(key)&&colList.hasOwnProperty(k)){
						if(obj[key].toUpperCase().indexOf(text.toUpperCase())>-1){
							newList.push(obj);
						}
					}
				}
			}
		}
		if(typeof colList == "string"){
			for(var i in arr){
				var obj = arr[i];
				if(obj.hasOwnProperty(colList)){
					if(obj[colList].toUpperCase().indexOf(text.toUpperCase())>-1){
						newList.push(obj);
					}
				}
			}
		}
		return newList;
	}
	$.searchArrListDataLike=searchArrListDataLike;
	function jsonSort(arr,attr,order){
		return [].concat(arr).sort(function(a,b){
			if(isNaN(a[attr])){
				if(!!order&&order=="desc")
					return a[attr].localeCompare(b[attr])*-1;
				else
					return a[attr].localeCompare(b[attr]);
			}else{
				if(!!order&&order=="desc")
					return a[attr] + b[attr];
				else
					return a[attr] - b[attr];
			}
		});
	}
	$.jsonSort=jsonSort;
	$.fn.scrollLoad=function(arrList,fn,num){
		if(!num)
			num=0;
		var _this=$(this);
		var list=arrList;
		var size=$.JSONLength(list);
		var i=1;
		_this.html("");
		if(size>0){
			loadData();
			_this.off("scroll").on("scroll",function(e){
				if(parseInt(_this[0].scrollTop)+parseInt(_this.height())==parseInt(_this[0].scrollHeight)+num){
					if(i<=size){
						i++;
						loadData();
					}
				}
			});
		}
		function loadData(){
			var html="";
			if(!!fn)
				html=fn(list[i]);
			_this.append(html);
		}
		function scrollLoadQZ(){
			if(i<=size){
				i++;
				loadData();
			}
		}
		return scrollLoadQZ;
	}
})($);
