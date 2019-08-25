$(document).ready(function() {
    $("#btn-enviar").on("click", function(){
      var prod =  $('#Producto').val();
      var ubi =  $('#Ubicación').val();
      var fecha =  $('#Fecha').val();
      var temp =  $('#TemperaturaPromedio').val();
      var temp_max =  $('#TemperaturaMáxima').val();
      var temp_min =  $('#TemperaturaMínima').val();
      var solar = $('#Solar').val();
      var ev =  $('#Evento').val();
      var pre =  $('#Precio').val();
	     $.ajax({

			 url : "http://10.22.155.51:5000/?location=" + ubi + "&date=" + fecha + "&product=" + prod +
       "&temp_mean=" + temp + "&temp_max=" + temp_max + "&temp_min=" + temp_min + "&sun=" + solar + "&price=1.48&is_special_event=" + ev,
       crossDomain: true,
    dataType: 'json',
       type : "GET",

			 success : function(dataReceived) {
         var hue = dataReceived["prediction"];
         $("#prediction").html("<h3>" + hue + "</h3>" );
				 //  var hue = dataReceived["prediction"];
       //$("#prediction").append("<h3>" + hue "</h3>" )
			 //},
			 //error : function(errorMessage) {
				 //  alert(errorMessage.statusText);
			   }
		  //});
	 });
});
});
