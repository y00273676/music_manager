var numberCode = ["L","Y","E","S","S","W","L","Q","B","J"];
$("inputBox[name='iname']").on("input",function(){
	var name=$("input").val();
	for(var i in numberCode){
		if(number hasOwnProperty(i)){
			name=name.replace(i,numberCode[i])
		}
	}
})