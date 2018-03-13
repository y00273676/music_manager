(function($){
	$(document).on("keyup",function(){
		if (event.keyCode == "13") {
			if($(".confirmBox").hasClass("show")){
				$(".confirmBox>div>div>span:eq(0)").click();
			}else if($(".confirmBoxInput").hasClass("show")){
				$(".confirmBoxInput>div>div>span:eq(0)").click();
			}else if($(".confirmBoxInputNumber").hasClass("show")){
				$(".confirmBoxInputNumber>div>div>span:eq(0)").click();
			}else if($(".confirmBoxOK").hasClass("show")){
				$(".confirmBoxOK>div>div>span").click();
			}else if($(".confirmBoxIP").hasClass("show")){
				$(".confirmBoxIP>div>div>span:eq(0)").click();
			}
		}
	});
	function createConfirmBox(option){
		$(".confirmBox>div>span:eq(0)").html(option.title);
		$(".confirmBox>div>span:eq(1)").html(option.content);
		$.tap(".confirmBox>div>div>span:eq(0)",function(){
			$(this).parent().parent().parent().removeClass("show");
			if(!!option.click)
				option.click.call(this);
		});
		$.tap(".confirmBox>div>div>span:eq(1)",function(){
			$(this).parent().parent().parent().removeClass("show");
			if(!!option.cancel)
				option.cancel.call(this);
		});
		$(".confirmBox").addClass("show");
	}
	function createConfirmBoxInput(option){
		$(".confirmBoxInput>div>span:eq(0)").html(option.title);
		$(".confirmBoxInput>div>span:eq(1)").html(option.content);
		if(!option.inputVal)
			option.inputVal="";
		if(!option.placeholder)
			option.placeholder="";
		$(".confirmBoxInput>div>input").val(option.inputVal);
		$(".confirmBoxInput>div>input").attr("placeholder",option.placeholder);
		$.tap(".confirmBoxInput>div>div>span:eq(0)",function(){
			$(this).parent().parent().parent().removeClass("show");
			if(!!option.click)
				option.click.call(this);
		});
		$.tap(".confirmBoxInput>div>div>span:eq(1)",function(){
			$(this).parent().parent().parent().removeClass("show");
		});
		$(".confirmBoxInput").addClass("show");
	}
	function createConfirmBoxInputNumber(option){
		$(".confirmBoxInputNumber>div>span:eq(0)").html(option.title);
		$(".confirmBoxInputNumber>div>span:eq(1)").html(option.content);
		if(!option.inputVal)
			option.inputVal="";
		if(!option.placeholder)
			option.placeholder="";
		$(".confirmBoxInputNumber>div>input").val(option.inputVal);
		$(".confirmBoxInputNumber>div>input").attr("placeholder",option.placeholder);
		$.tap(".confirmBoxInputNumber>div>div>span:eq(0)",function(){
			$(this).parent().parent().parent().removeClass("show");
			if(!!option.click)
				option.click.call(this);
		});
		$.tap(".confirmBoxInputNumber>div>div>span:eq(1)",function(){
			$(this).parent().parent().parent().removeClass("show");
		});
		$(".confirmBoxInputNumber").addClass("show");
	}
	function createConfirmBoxOK(option){
		$(".confirmBoxOK>div>span:eq(0)").html(option.title);
		$(".confirmBoxOK>div>span:eq(1)").html(option.content);
		$.tap(".confirmBoxOK>div>div>span",function(){
			$(this).parent().parent().parent().removeClass("show");
			if(!!option.click)
				option.click.call(this);
		});
		$(".confirmBoxOK").addClass("show");
	}
	function createConfirmBoxIP(option){
		$(".confirmBoxIP>div>span:eq(0)").html(option.title);
		$(".confirmBoxIP>div>span:eq(1)").html(option.content);
		if(!option.inputVal)
			$(".confirmBoxIP>div>div>input").val("");
		else{
			var arr=option.inputVal.split(".");
			if(arr.length==4){
				$(".confirmBoxIP>div>div>input").each(function(index){
					$(this).val(arr[index]);
				});
			}
		}
		$.tap(".confirmBoxIP>div>div>span:eq(0)",function(){
			$(this).parent().parent().parent().removeClass("show");
			if(!!option.click)
				option.click.call(this);
		});
		$.tap(".confirmBoxIP>div>div>span:eq(1)",function(){
			$(this).parent().parent().parent().removeClass("show");
		});
		$(".confirmBoxIP").addClass("show");
	}
	$.createConfirmBox=createConfirmBox;
	$.createConfirmBoxInput=createConfirmBoxInput;
	$.createConfirmBoxInputNumber=createConfirmBoxInputNumber;
	$.createConfirmBoxOK=createConfirmBoxOK;
	$.createConfirmBoxIP=createConfirmBoxIP;
})(jQuery)
