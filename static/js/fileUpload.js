	/*
	 图片上传
	 */
	$.fn.upload=function(url,successFn,o,beforFn,formDataFn,content){
		var input=null;
		var fileUpload_Div=document.createElement("div");
		var fileUpload_DivContent=document.createElement("div");
		var fileUpload_DivValue=document.createElement("div");
		var fileUpload_DivSpan=document.createElement("span");
		fileUpload_Div.id="supplement_fileUpload";
		$("#supplement_fileUpload").remove();
		fileUpload_DivSpan.innerHTML="0%";
		fileUpload_DivContent.appendChild(fileUpload_DivValue);
		fileUpload_DivContent.appendChild(fileUpload_DivSpan);
		fileUpload_Div.appendChild(fileUpload_DivContent);
		if(!!content)
			content.before($(fileUpload_Div));
		else
			document.body.appendChild(fileUpload_Div);
		$(this).off("click").on("click",function(){
			input=document.createElement("input");
			input.type="file";
			input.multiple=$(this).attr("multiple");
			input.accept=$(this).attr("accept");
			var fileNM=$(this).attr("fileName");
			input.onchange=function(){
				if(input.files.length==0){
					return;
				}
				if(beforFn){
					var bl=beforFn(input);
					if(bl===false)
						return;
				}
				var formData = new FormData();
				var totalSize=0;
				for(var i in input.files){
					if (input.files.hasOwnProperty(i)&&!isNaN(i)){
						var file = input.files[i];
						if(!!fileNM)
							formData.append("fileName",fileNM);
						else
							formData.append("fileName",file.name);
						formData.append("fileSize",file.size);
						totalSize+=parseInt(file.size);
						formData.append("file",file);
						if(!!formDataFn)
							formDataFn(formData,i,input.files);
					}
				}
				var xhr = new XMLHttpRequest();
				xhr.open('POST', url, true);
				xhr.onload = function (e){
					if (xhr.readyState==4 && xhr.status==200){
						fileUpload_Div.style.transform="scale(0,0)";
						fileUpload_Div.style.webkitTransform="scale(0,0)";
						fileUpload_Div.style.opacity="0";
						if(successFn)
							successFn(xhr,input,fileUpload_Div);
					}
					if(xhr.status==500||xhr.status==404){
						if(!!errorFn)
							errorFn(xhr,fileUpload_Div);
					}
				};
				xhr.upload.onprogress = function(e){
					var num=e.loaded/e.totalSize;
					if(!e.totalSize)
						num=e.loaded/totalSize;
					var numval=parseInt(num*100);
					if(numval>=100)
						numval=100;
					fileUpload_DivSpan.innerHTML=numval+"%";
					fileUpload_DivValue.style.width=numval+"%";
					if(numval==100)
						fileUpload_DivSpan.innerHTML="服务器正在处理中...";
				};
				fileUpload_Div.style.transform="scale(1,1)";
				fileUpload_Div.style.webkitTransform="scale(1,1)";
				fileUpload_Div.style.opacity="1";
				try{
					xhr.send(formData);
				}catch(e){
					if(!!errorFn)
						errorFn(xhr,fileUpload_Div);
				}
			}
			input.click();
		});
	};
	


/**
 * 表单图片上传
 */

$.fn.formImgSubmit=function(option){
	var _this=$(this);
	var url=option.url || _this.attr("action");
	_this.off("submit").on("submit",function(e){
		if (e && e.preventDefault) 
			e.preventDefault(); 
		if(event)
			event.preventDefault();
		if(! - [1,]){
			event.returnValue = false;
		}
		var formdata = new FormData(_this[0]);
		if(!!option.befor)
			if(!option.befor(formdata))
				return;
		var xhr = new XMLHttpRequest();
		xhr.open('POST', url , true);
		xhr.onload = function (e){
			if (xhr.readyState==4 && xhr.status==200){
				if(!!option.success)
					option.success(xhr.responseText);
			}
			if(xhr.status==500){
				console.error("表单提交错误");
			}
		};
		xhr.upload.onprogress = function(e){
			var num=e.loaded/e.totalSize;
			var numval=parseInt(num*100);
			if(!!option.progress)
				option.progress(numval);
		};
		xhr.send(formdata);
	});
}
