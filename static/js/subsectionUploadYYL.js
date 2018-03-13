(function($){
	$.fn.uploadBtnYYL=function(url,successFn,beforeFn){
		
		var input=null;
		var div=null;
		var ul=null;
		if($(".uploadRollDiv").length>0){
			div=$(".uploadRollDiv");
			ul=$(".uploadRollDiv").children("ul");
		}else{
			div=$("<div></div>").addClass("uploadRollDiv");
			ul=$("<ul></ul>");
		}
		div.append(ul);
		div.css("display","none");
		$("body").append(div);
		
		$("body").on("click",function(){
			div.css("display","none");
		});
		div.off("click").on("click",function(e){
			e.stopPropagation();
		});
		
		$(this).off("click").on("click",function(){
			$("#subsectionUploadFile").remove();
			input = document.createElement("input");
			input.id="subsectionUploadFile";
			input.type="file";
			if(!!$(this).attr("accept"))
				input.accept=$(this).attr("accept");
			if(!!$(this).attr("multiple")&&$(this).attr("multiple")=="multiple")
				input.multiple="multiple";
			input.style.display="none";
			$("body").append($(input));
			input.onchange=function(){
				eachFile(0);
				$(".uploadBox").click();
			}
			input.click();
		});
		
		function eachFile(i){
			if (input.files.hasOwnProperty(i)&&!isNaN(i)&&!!input.files[i]){
				var file=input.files[i];
				if(!!beforeFn){
					if (!beforeFn(file)){
						return;
					}
				}
				var name=file.name;
				var initName=name;
				var nameEnd=name.lastIndexOf(".")==-1?"":name.substring(name.lastIndexOf(".")+1,name.length);
				var size=file.size;
				var postSize=2*1024*1024;
				var smallDataSize=Math.min(size,64*1024);
				var smallData=file.slice(0, smallDataSize);
				
				var li=$("<li></li>");
				var liDiv=$("<div></div>");
				var liDivDiv=$("<div></div>");
				var span=$("<span></span>");
				var b=$("<b></b>");
				ul.append(li.append(liDiv.append(liDivDiv.append(span.html("0%")).append(b.html(name)).css("width","0%"))));
				
				var start = 0;
				var end=Math.min(size,start+postSize);
				sendAjax(url, file, name, start, end, initName, "", liDivDiv, span);
				i++;
				eachFile(i);
			}
		}
		function sendAjax( url, file, name, start, end, initName, path, liDivDiv, span){
			var size=file.size;
			var postSize=2*1024*1024;
			var data=file.slice(start, end);
			var formData=new FormData();
			formData.append("file",data);
			formData.append("fileName",name);
			formData.append("start",start);
			formData.append("end",end);
			formData.append("size",size);
			$.ajax({
				type:"post",
				url:url,
				dataType:"json",
				data:formData,
				processData: false,
	    		contentType: false,  
				success:function(str){
					if(!!str.path)
						path=str.path;
					start += postSize;
					if(end<size){
						showSuccess( end, size, initName, path, liDivDiv, span);
						end = Math.min(size, start+postSize);
						if(!!str.data&&str.data!="0"&&parseInt(str.data)>end){
							start=parseInt(str.data);
							end = Math.min(size, start+postSize);
						}
						sendAjax(url, file, name, start, end, initName, path, liDivDiv, span);
					}else{
						showSuccess( end, size, initName, path, liDivDiv, span);
					}
				},
				error:function(){
					
				}
			});
		}
		function showSuccess( end, size, initName, path, liDivDiv, span){
			var num=parseInt(end/size*100);
			liDivDiv.css("width",num+"%");
			span.html(num+"%");
			if(num==100){
				if(!!successFn)
					successFn(initName,path,size);
				span.html("上传完成!");
			}
		}
	}
	
})($);
