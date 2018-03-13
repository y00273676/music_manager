function startTime(date){
	setTimeout(function(){
		i++;
		date.setSeconds(date.getSeconds()+1);
		postMessage(date.getFullYear()+"-"+(date.getMonth()+1)+"-"+date.getDate()+" "+date.getHours()+":"+date.getMinutes()+":"+date.getSeconds());
		startTime(date);
	},1000);
}
var isOne=true;
var i=0;
onmessage = function (event) {
	if(isOne){
		isOne=false;
		var date=new Date(parseFloat(event.data)*1000);
		startTime(date);
	}
		
};