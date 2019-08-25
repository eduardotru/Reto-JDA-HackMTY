$(document).ready(function() {
    $("#btn-enviar").on("click", function(){
      var hue = 15;
      $("#prediction").append("<h3>" + hue + "</h3>" );
	     //$.ajax({
			 //url : "../data/applicationLayer.php",
			 //type : "GET",
			 //dataType : "json",
        //    data : { "action" : "DELETE_SESSION" },
			 //success : function(dataReceived) {
				 //  var hue = dataReceived["prediction"];
       //$("#prediction").append("<h3>" + hue "</h3>" )
			 //},
			 //error : function(errorMessage) {
				 //  alert(errorMessage.statusText);
			   //}
		  //});
	 });
});
